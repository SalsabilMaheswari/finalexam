from django.shortcuts import render
import numpy as np
import json
from .models import PredictionLog
from .ml_models import (
    train_beasiswa_model,
    train_non_akademik_model,
    train_konsistensi_model,
    train_magang_model,
    decode_konsistensi_label,
    decode_konsistensi_proba
)

# Load models at server start
beasiswa_model = train_beasiswa_model()
non_akademik_model = train_non_akademik_model()
konsistensi_model = train_konsistensi_model()
magang_model = train_magang_model()

konsistensi_translation = {
    "Naik": "Improving",
    "Turun": "Declining",
    "Konsisten": "Consistent"
}

# Insight generators
def get_insight_beasiswa(midterm, final, project, attendance, eligible):
    if eligible:
        return "✅ Eligible for scholarship due to strong academic scores and consistent attendance."
    
    reasons = []
    if midterm < 85:
        reasons.append("midterm score below 85")
    if final < 85:
        reasons.append("final exam score below 85")
    if project < 85:
        reasons.append("project score below 85")
    if attendance < 90:
        reasons.append("attendance below 90%")

    if not reasons:
        return "❌ Not eligible for scholarship based on overall combination of scores and attendance."

    return "❌ Not eligible for scholarship due to " + ", ".join(reasons) + "."

def get_insight_non_akademik(project, attendance, exam, non_akademik):
    if non_akademik:
        return "📌 High project score and low attendance, probably active non-academic involvement."
    return "📌 No significant signs of strong non-academic activity detected."

def get_insight_konsistensi(midterm, final):
    diff = final - midterm
    if diff > 5:
        return "📈 Student shows improvement in grades (Final > Midterm)."
    elif diff < -5:
        return "📉 Student performance declined (Midterm > Final)."
    else:
        return "⚖️ Student shows consistent academic performance."

def get_insight_magang(project, attendance, final, magang):
    if magang:
        return "🚀 Ready for internship based on solid academic performance and attendance."
    
    reasons = []
    if project < 80:
        reasons.append("project score below 80")
    if final < 80:
        reasons.append("final exam score below 80")
    if attendance < 85:
        reasons.append("attendance below 85%")

    if not reasons:
        return "⏳ Not ready for internship based on overall academic profile."

    return "⏳ Not ready for internship due to " + ", ".join(reasons) + "."

def altara_predict(request):
    return render(request, 'altara/predict.html')

def altara_result(request):
    if request.method == 'POST':
        mid = float(request.POST['midterm'])
        final = float(request.POST['final'])
        proj = float(request.POST['project'])
        att = float(request.POST['attendance'])
        user_name = request.POST.get('name', 'Anonymous')

        features = np.array([[mid, final, proj, att]])
        input_dict = {'midterm': mid, 'final': final, 'project': proj, 'attendance': att}

        # Predictions
        bea = beasiswa_model.predict(features)[0]
        bea_proba = beasiswa_model.predict_proba(features)[0]

        non = non_akademik_model.predict(features)[0]
        non_proba = non_akademik_model.predict_proba(features)[0]

        kons_encoded = konsistensi_model.predict(features)[0]
        kons_proba_dict = decode_konsistensi_proba(konsistensi_model.predict_proba(features)[0])

        magang = magang_model.predict(features)[0]
        magang_proba = magang_model.predict_proba(features)[0]

        # Labels
        bea_label = 'Eligible' if bea == 1 else 'Not Eligible'
        non_label = 'Yes' if non == 1 else 'No'
        kons_label = decode_konsistensi_label(kons_encoded)
        kons_label_eng = konsistensi_translation.get(kons_label, kons_label)
        magang_label = 'Ready' if magang == 1 else 'Not Yet'

        # Save to DB
        for model_name, label in [('beasiswa', bea_label), ('non_akademik', non_label), ('konsistensi', kons_label), ('magang', magang_label)]:
            PredictionLog.objects.create(
                user_name=user_name,
                model_used=model_name,
                input_data=json.dumps(input_dict),
                prediction_result=label
            )

        chart_probs = {
            'beasiswa': float(bea_proba[1]),
            'non_akademik': float(non_proba[1]),
            'konsistensi': float(kons_proba_dict.get(kons_label, 0)),
            'magang': float(magang_proba[1])
        }

        context = {
            'name': user_name,
            'midterm': mid,
            'final': final,
            'project': proj,
            'attendance': att,
            'beasiswa': bea_label,
            'non_akademik': non_label,
            'konsistensi': kons_label_eng,
            'magang': magang_label,
            'probabilities_json': json.dumps(chart_probs),

            # Insights
            'insight_beasiswa': get_insight_beasiswa(mid, final, proj, att, bea),
            'insight_non_akademik': get_insight_non_akademik(proj, att, mid, non),
            'insight_konsistensi': get_insight_konsistensi(mid, final),
            'insight_magang': get_insight_magang(proj, att, final, magang),
        }

        return render(request, 'altara/result.html', context)

import os
import joblib
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View
import pandas as pd
import pickle
from django.views.decorators.http import require_GET



def member1(request):
    return render(request, 'member1/member1.html')

@require_GET
def predict_top_3_instructors(request):
    course_name = request.GET.get('course_name')
    semester = request.GET.get('semester')
    department_name = request.GET.get('department_name')

    if not course_name or not semester or not department_name:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    model_path = os.path.join(settings.BASE_DIR, 'top3_instructor_model.pkl')
    if not os.path.exists(model_path):
        return JsonResponse({'error': 'Model not found'}, status=500)

    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)

    model = model_data['model']
    label_encoders = model_data['label_encoders']

    try:
        course_enc = label_encoders['course_name'].transform([course_name])[0]
        dept_enc = label_encoders['department_name'].transform([department_name])[0]
        sem_enc = label_encoders['semester'].transform([semester])[0]
    except ValueError:
        return JsonResponse({'error': 'Input values not recognized by model encoders'}, status=400)

    X_input = [[course_enc, dept_enc, sem_enc]]
    proba = model.predict_proba(X_input)[0]
    top3_indices = proba.argsort()[-3:][::-1]
    top3_names = label_encoders['instructor_name'].inverse_transform(top3_indices)
    top3_probs = [float(proba[i]) for i in top3_indices]

    # Load CSV instructor info
    csv_path = os.path.join(settings.BASE_DIR, 'course_instructor_train_top3.csv')
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return JsonResponse({'error': 'Instructor info CSV not found'}, status=500)

    top3_descriptions = []
    for name in top3_names:
        row = df[df['instructor_name'] == name]
        if not row.empty:
            teachings = int(row.iloc[0]['total_teachings'])
            description = f"{name} has taught {teachings} times."
        else:
            description = f"No data found for {name}."
        top3_descriptions.append(description)

    return JsonResponse({
        "top_3_instructors": top3_descriptions,
        "probabilities": top3_probs
    })
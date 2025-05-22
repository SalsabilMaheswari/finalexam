from django.http import HttpResponse
from django.shortcuts import render
from .models import ModelInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import joblib
import os
from django.conf import settings
from .forms import StudentPerformanceForm

# Create your views here.
def home(request):
    return render(request,"finalexampredict/home.html")

def about(request):
    return render(request,"finalexampredict/about.html")

def member2(request):
    return render(request, 'finalexampredict/member2.html')

def maheswari(request):  
    model_infos = ModelInfo.objects.all()
    return render(request, 'finalexampredict/maheswari.html', {'model_infos': model_infos})

def member3(request):
    return render(request,"finalexampredict/member3.html")

def student_performance_view(request):
    form = StudentPerformanceForm()
    return render(request, 'finalexampredict/dashboard.html', {'form': form})

@csrf_exempt
def predict_student(request):
    if request.method == "POST":
        try:
        # Parse incoming JSON data
            data = json.loads(request.body)

            # Prepare feature array (ensure correct feature order)
            features = np.array([
                data["avg_grade"],
                data["avg_score"],
                data["avg_attendance"],
                data["total_assessment"],
                data["gpa"]
            ]).reshape(1, -1)

            # Load the model
            model_path = os.path.join(settings.BASE_DIR, 'final_studentgpa_model.pkl')
            model = joblib.load(model_path)

            # Make prediction and calculate probability
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0].tolist()

            # Return prediction and probability as JSON response
            return JsonResponse({
                "prediction": int(prediction),
                "probability": probability
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
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
from .forms import StudentPerformanceForm, GPASearchForm
import pandas as pd


# Create your views here.
def home(request):
    return render(request,"finalexampredict/home.html")

def about(request):
    return render(request,"finalexampredict/about.html")

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
    
def gpa_search_view(request):
    form = GPASearchForm(request.GET or None)
    chart_data = None
    
    if form.is_valid():
        df = pd.read_csv('student_gpa_per_student.csv')
        
        # Apply filters
        min_gpa = form.cleaned_data.get('min_gpa')
        max_gpa = form.cleaned_data.get('max_gpa')
        
        if min_gpa is not None:
            df = df[df['gpa'] >= min_gpa]
        if max_gpa is not None:
            df = df[df['gpa'] <= max_gpa]
        
        # Prepare chart data
        above_3 = len(df[df['gpa'] > 3.0])
        below_3 = len(df[df['gpa'] <= 3.0])
        
        chart_data = {
            'labels': ['GPA > 3.0', 'GPA ≤ 3.0'],
            'data': [above_3, below_3],
            'colors': ['#36a2eb', '#ff6384'],
            'total_students': len(df)
        }
    
    return render(request, 'finalexampredict/gpa_search.html', {
        'form': form,
        'chart_data': chart_data
    })


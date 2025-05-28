from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import joblib
import os
from django.conf import settings
from .forms import StudentPerformanceForm, CourseTestForm
import pandas as pd
import json 

# Create your views here.
def home(request):
    return render(request,"finalexampredict/home.html")

def about(request):
    return render(request,"finalexampredict/about.html")

def member2(request):
    return render(request, 'finalexampredict/member2.html')

def maheswari(request):  
    form = CourseTestForm()
    return render(request, 'finalexampredict/dashboard.html', {'form': form})

def member3(request):
    return render(request,"finalexampredict/member3.html")

@csrf_exempt
def predict_course_cluster(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Load model & scaler
            model_path = os.path.join(settings.BASE_DIR, 'course_clustering_model.pkl')
            scaler_path = os.path.join(settings.BASE_DIR, 'course_scaler.pkl')
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)

            # Map difficulty
            difficulty_map = {
                "Easy": 1,
                "Medium": 2,
                "Hard": 3
            }
            difficulty = difficulty_map.get(data['difficulty'], 0)

            # Prepare input
            X = np.array([
                data['avg_grade'],
                difficulty,
                data['total_student']
            ]).reshape(1, -1)

            X_scaled = scaler.transform(X)
            cluster = model.predict(X_scaled)[0]

            return JsonResponse({
                'cluster': int(cluster),
                'input': X.tolist(),
                'scaled_input': X_scaled.tolist()
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def course_cluster_chart(request):
    df = pd.read_csv('course_performance_clustered.csv')
    data = df.to_dict(orient='records')
    data_json = json.dumps(data)
    return render(request, 'finalexampredict/course_cluster_chart.html', {'data_json': data_json})
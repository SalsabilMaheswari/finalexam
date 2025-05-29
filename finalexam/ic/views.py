from django.shortcuts import render
import json
import pandas as pd
import joblib
from .forms import InstructorPerformanceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import numpy as np
from django.conf import settings
# Create your views here.



# def member3(request):
#     form = InstructorClusterForm(request.POST or None)
#     result = None

#     if request.method == 'POST' and form.is_valid():
#         instructor_id = form.cleaned_data['instructor_id']
#         semester_id = form.cleaned_data['semester_id']
        
#         # Optional: You can do server-side validation or result calculation here
#         # but no need to pass chart data JSON anymore

#         result = f'Submitted Instructor ID: {instructor_id}, Semester ID: {semester_id}'

#     return render(request, "ic/member3.html", {
#         'form': form,
#         'result': result
#     })



# def predict_instructor_view(request):
#     form = ClusterPredictForm()
#     return render(request, "ic/member3.html", {'form': form})

# model_path = os.path.join(settings.BASE_DIR, 'ic/rfc_instructor.pkl')
# model = joblib.load(model_path)

# @csrf_exempt
# def predict_instructor(request):
#     print(f"request method: {request.method}")
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(f"data: {data}")

#         features = np.array([
#             data['avg_grade'],
#             data['avg_score'],
#             data['avg_attendance']
#         ]).reshape(1, -1)

#     prediction = model.predict(features)[0]
#     probability = model.predict_proba(features)[0].tolist()

#     return JsonResponse({
#         'prediction': int(prediction),
#         'probability': probability
#     })

# def customer_prediction_view(request):
#     form = ClusterPredictForm()
#     return render(request, 'ic/member3.html',{'form':form})

# model_path = os.path.join(os.path.dirname(__file__), 'rfc_instructor.pkl')
# model = joblib.load(model_path)

# @csrf_exempt
# def predict_customer(request):
#     print(f"Request method: {request.method}")
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(f"Data received: {data}")

#         features = np.array([
#             data['avg_grade'],
#             data['avg_score'],
#             data['avg_attendance']
#         ]).reshape(1,-1)
        
#         prediction = model.predict(features)[0]
#         probability = model.predict_proba(features)[0].tolist()

#         return JsonResponse({
#             'prediction': int(prediction),
#             'probability': probability
#         })

def customer_prediction_view(request):
    form = InstructorPerformanceForm()
    return render(request, 'ic/member3.html',{'form':form})

model_path = os.path.join(os.path.dirname(__file__), 'rfc_lecture.pkl')
model = joblib.load(model_path)

@csrf_exempt
def predict_customer(request):
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"Data received: {data}")

        features = np.array([
            data['num_students'],
            data['avg_attendance'],
            data['num_A'],
            data['num_B'],
            data['num_C'],
            data['num_D']
        ]).reshape(1,-1)
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()

        return JsonResponse({
            'prediction': int(prediction),
            'probability': probability
        })

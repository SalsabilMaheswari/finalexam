from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import joblib
import os
from django.conf import settings
from .forms import StudentPerformanceForm, GPASearchForm, StudentActivitySearchForm
import pandas as pd


# Create your views here.
def home(request):
    return render(request,"finalexampredict/home.html")

def about(request):
    return render(request,"finalexampredict/about.html")

def member2(request):
    return render(request, 'finalexampredict/member2.html')

def maheswari(request):  
    form = StudentPerformanceForm()
    return render(request, 'finalexampredict/dashboard.html', {'form': form})

def member3(request):
    return render(request,"finalexampredict/member3.html")

def student_activity_search_view(request):
    form = StudentActivitySearchForm()
    results = None

    if request.method == 'POST':
        form = StudentActivitySearchForm(request.POST)
        if form.is_valid():
            # Get form values
            attendance_filter = form.cleaned_data['attendance_filter']
            attendance_value = form.cleaned_data['attendance_value']
            assessment_filter = form.cleaned_data['assessment_filter']
            assessment_value = form.cleaned_data['assessment_value']

            # Load CSV (hasil ETL-mu tadi)
            df = pd.read_csv('student_activity_dataset.csv')

            # Filtering logic
            if attendance_filter == 'above':
                df = df[df['attendance_pct'] > attendance_value]
            else:
                df = df[df['attendance_pct'] < attendance_value]

            if assessment_filter == 'above':
                df = df[df['total_assessment'] > assessment_value]
            else:
                df = df[df['total_assessment'] < assessment_value]

            results = df.to_dict(orient='records')

    return render(request, 'finalexampredict/search.html', {
        'form': form,
        'results': results
    })
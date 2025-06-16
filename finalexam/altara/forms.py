# === forms.py ===
from django import forms

class NewPredictionForm(forms.Form):
    avg_grade = forms.FloatField(label="Average Grade")
    avg_attendance = forms.FloatField(label="Average Attendance")
    avg_assessment_score = forms.FloatField(label="Average Assessment Score")
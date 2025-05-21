from django import forms

class StudentPerformanceForm(forms.Form):
    avg_grade = forms.FloatField(label='Average Grade', min_value=0, max_value=100)
    avg_score = forms.FloatField(label='Average Score', min_value=0, max_value=100)
    avg_attendance = forms.FloatField(label='Average Attendance (%)', min_value=0, max_value=100)
    total_assessment = forms.IntegerField(label='Total Assessments', min_value=0)
    gpa = forms.FloatField(label='GPA', min_value=0.0, max_value=4.0)
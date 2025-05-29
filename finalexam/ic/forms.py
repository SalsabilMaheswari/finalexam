from django import forms

# class InstructorClusterForm(forms.Form):
#     instructor_id = forms.IntegerField(label="Instructor ID")
#     semester_id = forms.IntegerField(label="Semester ID")

# class ClusterPredictForm(forms.Form):
#     avg_grade = forms.IntegerField(label="Average Grade", max_value=100)
#     avg_score = forms.IntegerField(label="Average Score", max_value=100)
#     avg_attendance = forms.IntegerField(label="Average Attendance (%)", max_value=100)

class InstructorPerformanceForm(forms.Form):
    num_students = forms.IntegerField(label="Number of Students", min_value=1)
    avg_attendance = forms.FloatField(label="Average Attendance (%)", min_value=0, max_value=100)
    num_A = forms.IntegerField(label="Number of A Grades", min_value=0)
    num_B = forms.IntegerField(label="Number of B Grades", min_value=0)
    num_C = forms.IntegerField(label="Number of C Grades", min_value=0)
    num_D = forms.IntegerField(label="Number of D Grades", min_value=0)

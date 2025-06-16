from django.db import models

class StudentRecord(models.Model):
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    semester_name = models.CharField(max_length=20)
    attendance_percentage = models.FloatField()
    midterm = models.FloatField()
    final = models.FloatField()
    project = models.FloatField()
    average_score = models.FloatField()

    class Meta:
        unique_together = ('student_id', 'semester_name')

    def __str__(self):
        return f"{self.name} - {self.semester_name}"

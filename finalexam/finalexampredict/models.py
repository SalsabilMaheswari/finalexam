from django.db import models
from django.utils import timezone


# Create your models here.
class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'course'
        managed = False

class Enrollment(models.Model):
    enroll_id = models.IntegerField(primary_key=True)
    stu_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id')
    grade = models.FloatField()

    class Meta:
        db_table = 'enrollment'
        managed = False

class CourseDifficulty(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, db_column='course_id', primary_key=True)
    difficulty_level = models.IntegerField()

    class Meta:

        db_table = 'course_difficulty'
        managed = False
    
    
    
    
class Attendance(models.Model):
    attendance_id = models.IntegerField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, db_column='enroll_id')
    attendance_percentage = models.FloatField()

    class Meta:
        db_table = 'attendance'
        managed = False

    def __str__(self):
        return f'{self.attendance_percentage}%'
    
    
class ModelInfo(models.Model):
    model_name = models.CharField(max_length=100)
    model_file = models.CharField(max_length=255)
    training_data = models.CharField(max_length=255)
    model_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=100, default='maheswari')
    use_case = models.CharField(max_length=100, default='courses performance prediction')
    model_type = models.CharField(max_length=50, choices=[
        ('classification', 'Classification'),
        ('clustering', 'Clustering'),
        ('regression', 'Regression')
    ], default='clustering')

    class Meta:
        db_table = 'model_info'


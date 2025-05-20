from django.db import models

# Create your models here.
class Student(models.Model):
    stu_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    dept_id = models.IntegerField()

    class Meta:
        db_table = 'student'
        managed = False
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    enroll_id = models.IntegerField(primary_key=True)
    stu = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='stu_id')
    course_id = models.IntegerField()
    grade = models.FloatField()
    semester_id = models.IntegerField()

    class Meta:
        db_table = 'enrollment'
        managed = False
    
    def __str__(self):
        return self.grade

class Assessment(models.Model):
    assessment_id = models.IntegerField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, db_column='enroll_id')
    assessment_type = models.CharField(max_length=50)
    score = models.FloatField()

    class Meta:
        db_table = 'assessment'
        managed = False
    
    def __str__(self):
        return f'{self.assessment_type} - {self.score}'
    
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

    class Meta:
        db_table = 'model_info'

from django.db import models
from django.utils import timezone
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
    
class Department(models.Model):
    dept_id = models.IntegerField(primary_key=True)  # gunakan AutoField untuk primary key
    dept_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'department'
        managed = False  # set True jika kamu ingin Django atur tabelnya (biasanya False untuk legacy DB)

    def __str__(self):
        return self.dept_name

class Instructor(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    instructor_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')

    class Meta:
        db_table = 'instructor'
        managed = False

    def __str__(self):
        return self.instructor_name
    
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')

    class Meta:
        db_table = 'course'
        managed = False

    def __str__(self):
        return self.course_name

class Semester(models.Model):
    semester_id = models.IntegerField(primary_key=True)
    semester_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'semester'
        managed = False

    def __str__(self):
        return self.semester_name

class CourseInstructor(models.Model):
    course_instructor_id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='instructor_id')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, db_column='semester_id')

    class Meta:
        db_table = 'course_instructor'
        managed = False
        unique_together = ('course', 'instructor', 'semester')

    def __str__(self):
        return f"{self.course} - {self.instructor} - {self.semester}"

class CourseDifficulty(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True, db_column='course_id')
    difficulty_level = models.CharField(max_length=50)

    class Meta:
        db_table = 'course_difficulty'
        managed = False

    def __str__(self):
        return f"{self.course.course_name} - {self.difficulty_level}"
    
class ModelInfo(models.Model):
    model_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, default='v1.0')
    trained_date = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(null=True, blank=True)
    file_path = models.CharField(max_length=255)
    training_data = models.CharField(max_length=255, null=True, blank=True)
    model_summary = models.TextField(null=True, blank=True)
    
        
    def __str__(self):
        return f"{self.model_name} - {self.version}"

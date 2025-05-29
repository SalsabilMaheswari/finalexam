from django.db import models

# class Department(models.Model):
#     dept_id = models.IntegerField(primary_key=True)
#     dept_name = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'department'
#         managed = False

#     def __str__(self):
#         return self.dept_name

# class Instructor(models.Model):
#     instructor_id = models.IntegerField(primary_key=True)
#     instructor_name = models.CharField(max_length=100)
#     dept = models.ForeignKey(Department, on_delete=models.DO_NOTHING, db_column='dept_id')

#     class Meta:
#         db_table = 'instructor'
#         managed = False

#     def __str__(self):
#         return self.instructor_name

# class Semester(models.Model):
#     semester_id = models.IntegerField(primary_key=True)
#     semester_name = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'semester'
#         managed = False

#     def __str__(self):
#         return self.semester_name

# class Course(models.Model):
#     course_id = models.IntegerField(primary_key=True)
#     course_name = models.CharField(max_length=100)
#     dept = models.ForeignKey(Department, on_delete=models.DO_NOTHING, db_column='dept_id')

#     class Meta:
#         db_table = 'course'
#         managed = False

#     def __str__(self):
#         return self.course_name

# class CourseInstructor(models.Model):
#     course_instructor_id = models.AutoField(primary_key=True)
#     course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, db_column='course_id')
#     instructor = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, db_column='instructor_id')
#     semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING, db_column='semester_id')

#     class Meta:
#         db_table = 'course_instructor'
#         managed = False

#     def __str__(self):
#         return f"{self.instructor} - {self.course} - {self.semester}"

# class Student(models.Model):
#     stu_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10)
#     dob = models.DateField()
#     dept = models.ForeignKey(Department, on_delete=models.DO_NOTHING, db_column='dept_id')

#     class Meta:
#         db_table = 'student'
#         managed = False

#     def __str__(self):
#         return self.name

# class Enrollment(models.Model):
#     enroll_id = models.IntegerField(primary_key=True)
#     stu = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='stu_id')
#     course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, db_column='course_id')
#     semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING, db_column='semester_id')
#     grade = models.FloatField()

#     class Meta:
#         db_table = 'enrollment'
#         managed = False

#     def __str__(self):
#         return f"Enrollment {self.enroll_id}"

# class Assessment(models.Model):
#     assessment_id = models.IntegerField(primary_key=True)
#     enrollment = models.ForeignKey(Enrollment, on_delete=models.DO_NOTHING, db_column='enroll_id')
#     assessment_type = models.CharField(max_length=50)
#     score = models.FloatField()

#     class Meta:
#         db_table = 'assessment'
#         managed = False

#     def __str__(self):
#         return f"{self.assessment_type} - {self.score}"

# class Attendance(models.Model):
#     attendance_id = models.IntegerField(primary_key=True)
#     enrollment = models.ForeignKey(Enrollment, on_delete=models.DO_NOTHING, db_column='enroll_id')
#     attendance_percentage = models.FloatField()

#     class Meta:
#         db_table = 'attendance'
#         managed = False

#     def __str__(self):
#         return f"{self.attendance_percentage}%"

class Instructor(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    instructor_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'instructor'
        managed = False

class CourseInstructor(models.Model):
    course_instructor_id = models.IntegerField(primary_key=True)
    course_id = models.IntegerField()
    instructor = models.ForeignKey(Instructor, db_column='instructor_id', on_delete=models.DO_NOTHING)
    semester_id = models.IntegerField()

    class Meta:
        db_table = 'course_instructor'
        managed = False

class Enrollment(models.Model):
    enroll_id = models.IntegerField(primary_key=True)
    course_id = models.IntegerField()
    semester_id = models.IntegerField()
    grade = models.FloatField()

    class Meta:
        db_table = 'enrollment'
        managed = False

class Assessment(models.Model):
    assessment_id = models.IntegerField(primary_key=True)
    enroll_id = models.IntegerField()
    score = models.FloatField()

    class Meta:
        db_table = 'assessment'
        managed = False

class Attendance(models.Model):
    attendance_id = models.IntegerField(primary_key=True)
    enroll_id = models.IntegerField()
    attendance_percentage = models.FloatField()

    class Meta:
        db_table = 'attendance'
        managed = False

class ModelInfo(models.Model):
    model_name = models.CharField(max_length=100)
    model_file = models.CharField(max_length=255)
    training_data = models.CharField(max_length=255)
    training_date = models.DateTimeField()
    model_summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.model_name} - {self.training_date.strftime('%Y-%M-%d')}"
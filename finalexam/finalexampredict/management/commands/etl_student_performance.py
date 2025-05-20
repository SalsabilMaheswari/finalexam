from django.core.management.base import BaseCommand
from finalexampredict.models import Student, Enrollment, Assessment, Attendance
import pandas as pd


class Command(BaseCommand):
    help = 'ETL process to extract gpa per student data for ML'

    def handle(self, *args, **kwargs):
        data = []

        for student in Student.objects.all():
            enrollments = Enrollment.objects.filter(stu=student)

            if enrollments.count() == 0:
                continue

            total_grade = 0
            total_avg_score = 0
            total_attendance = 0
            total_assessment = 0
            enrollment_count = enrollments.count()

            for enrollment in enrollments:
                assessments = Assessment.objects.filter(enrollment=enrollment)
                attendance = Attendance.objects.filter(enrollment=enrollment).first()

                total_score = sum([a.score for a in assessments])
                count_score = assessments.count()
                avg_score = total_score / count_score if count_score > 0 else 0
                attendance_pct = attendance.attendance_percentage if attendance else 0

                total_grade += enrollment.grade
                total_avg_score += avg_score
                total_attendance += attendance_pct
                total_assessment += count_score

            # Rata-rata per student
            avg_grade = total_grade / enrollment_count #rata-rata semua grade mahasiswa dari semua mata kuliah yang dia ambil di tabel enrollment
            avg_avg_score = total_avg_score / enrollment_count #rata-rata nilai assessment per enrollment, yang kemudian dirata-ratakan lagi per student 
            avg_attendance = total_attendance / enrollment_count
            total_assessment_count = total_assessment

            # Hitung gpa skala 4.0
            gpa = ((avg_grade / 100) * 0.5 + (avg_avg_score / 100) * 0.3 + (avg_attendance / 100) * 0.2) * 4

            # Label Good kalau gpa > 3.5
            performance_label = 1 if gpa > 3.0 else 0

            data.append({
                'stu_id': student.stu_id,
                'name': student.name,
                'dept_id': student.dept_id,
                'avg_grade': round(avg_grade, 2),
                'avg_score': round(avg_avg_score, 2),
                'avg_attendance': round(avg_attendance, 2),
                'total_assessment': total_assessment_count,
                'gpa': round(gpa, 2),
                'performance_label': performance_label
            })

        df = pd.DataFrame(data)
        df.to_csv('student_gpa_per_student.csv', index=False)
        self.stdout.write(self.style.SUCCESS('file student_gpa_per_student.csv created successfully!'))

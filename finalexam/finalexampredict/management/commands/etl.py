from django.core.management.base import BaseCommand
from finalexampredict.models import Enrollment, Course, CourseDifficulty
import pandas as pd
from django.db.models import Avg

class Command(BaseCommand):
    help = 'ETL: Extract average grade, difficulty, number of students per course'

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()
        data = []

        for course in courses:
            enrollments = Enrollment.objects.filter(course_id=course.course_id)
            if enrollments.count() == 0:
                continue

            avg_grade = enrollments.aggregate(avg=Avg('grade'))['avg']
            total_student = enrollments.count()

            try:
                difficulty = CourseDifficulty.objects.get(course_id=course).difficulty_level
            except CourseDifficulty.DoesNotExist:
                difficulty = None

            data.append({
                'course_id': course.course_id,
                'name': course.course_name,
                'avg_grade': round(avg_grade, 2),
                'difficulty': difficulty,
                'total_student': total_student
            })

        df = pd.DataFrame(data)
        df.to_csv('course_performance.csv', index=False)
        self.stdout.write(self.style.SUCCESS('course_performance.csv generated!'))

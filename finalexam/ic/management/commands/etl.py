from django.core.management.base import BaseCommand
from ic.models import CourseInstructor, Instructor, Enrollment, Assessment, Attendance
import pandas as pd
from collections import defaultdict

class Command(BaseCommand):
    help = 'Extract instructor features and save to CSV'

    def handle(self, *args, **kwargs):
        # Container for grouped data
        grouped_data = defaultdict(lambda: {
            'instructor_name': '',
            'grades': [],
            'scores': [],
            'attendances': []
        })

        # Join CourseInstructor with Instructor
        for ci in CourseInstructor.objects.all():
            instructor = ci.instructor
            instructor_name = instructor.instructor_name
            course_id = ci.course_id
            semester_id = ci.semester_id

            enrollments = Enrollment.objects.filter(course_id=course_id, semester_id=semester_id)

            for enrollment in enrollments:
                assessments = Assessment.objects.filter(enroll_id=enrollment.enroll_id)
                attendance = Attendance.objects.filter(enroll_id=enrollment.enroll_id).first()

                grouped_key = (ci.instructor_id, semester_id)
                grouped_data[grouped_key]['instructor_name'] = instructor_name
                grouped_data[grouped_key]['grades'].append(enrollment.grade)

                for a in assessments:
                    grouped_data[grouped_key]['scores'].append(a.score)

                if attendance:
                    grouped_data[grouped_key]['attendances'].append(attendance.attendance_percentage)

        # Build DataFrame
        records = []
        for (instructor_id, semester_id), values in grouped_data.items():
            if not values['grades'] or not values['scores'] or not values['attendances']:
                continue  # Skip if missing data

            avg_grade = round(sum(values['grades']) / len(values['grades']), 2)
            avg_score = round(sum(values['scores']) / len(values['scores']), 2)
            avg_attendance = round(sum(values['attendances']) / len(values['attendances']), 2)

            records.append({
                'instructor_id': instructor_id,
                'semester_id': semester_id,
                'avg_grade': avg_grade,
                'avg_score': avg_score,
                'avg_attendance': avg_attendance,
            })

        df = pd.DataFrame(records)
        df.to_csv('instructorperf2.csv', index=False)

        self.stdout.write(self.style.SUCCESS('instructorperf2.csv has been created!'))

import csv
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Export lecturer performance data to CSV using raw SQL'

    def handle(self, *args, **kwargs):
        query = """
            SELECT
                ci.instructor_id,
                ci.course_id,
                ci.semester_id,
                COUNT(e.enroll_id) AS num_students,
                ROUND(AVG(a.attendance_percentage), 2) AS avg_attendance,

                SUM(CASE WHEN e.grade BETWEEN 85 AND 100 THEN 1 ELSE 0 END) AS num_A,
                SUM(CASE WHEN e.grade BETWEEN 70 AND 84 THEN 1 ELSE 0 END) AS num_B,
                SUM(CASE WHEN e.grade BETWEEN 55 AND 69 THEN 1 ELSE 0 END) AS num_C,
                SUM(CASE WHEN e.grade < 55 THEN 1 ELSE 0 END) AS num_D

            FROM course_instructor ci
            JOIN enrollment e
                ON ci.course_id = e.course_id AND ci.semester_id = e.semester_id
            LEFT JOIN attendance a
                ON e.enroll_id = a.enroll_id

            GROUP BY
                ci.instructor_id,
                ci.course_id,
                ci.semester_id

            ORDER BY
                ci.instructor_id, ci.course_id, ci.semester_id;
        """

        output_file = 'lecturer_data.csv'
        headers = [
            'instructor_id', 'course_id', 'semester_id',
            'num_students', 'avg_attendance',
            'num_A', 'num_B', 'num_C', 'num_D'
        ]

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        self.stdout.write(self.style.SUCCESS(f'Data exported to {output_file} successfully.'))

from django.core.management.base import BaseCommand
from member1.models import (
    Department, Course, Instructor, Semester,
    CourseDifficulty, CourseInstructor, Enrollment, Assessment
)
import pandas as pd

class Command(BaseCommand):
    help = "ETL: Extract training data for predicting Top 3 instructor per course-semester-department."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting ETL for Top 3 Instructor Prediction...")

        # Preload necessary data
        courses = {c.course_id: c for c in Course.objects.select_related('department')}
        instructors = {i.instructor_id: i for i in Instructor.objects.select_related('department')}
        difficulties = {
            d.course.course_id: d.difficulty_level
            for d in CourseDifficulty.objects.select_related('course')
        }

        course_instructor_entries = CourseInstructor.objects.select_related(
            'course__department', 'instructor__department', 'semester'
        )

        seen = set()
        aggregated_data = []

        for entry in course_instructor_entries:
            key = (entry.course.course_id, entry.instructor.instructor_id, entry.semester.semester_id)
            if key in seen:
                continue
            seen.add(key)

            course = entry.course
            instructor = entry.instructor
            semester = entry.semester
            difficulty = difficulties.get(course.course_id, "Unknown")

            enrollments = Enrollment.objects.filter(
                course_id=course.course_id,
                semester_id=semester.semester_id
            )

            total_students = enrollments.count()
            if total_students == 0:
                continue

            total_score = 0
            total_grade = 0
            pass_count = 0
            valid_scores_count = 0

            enrollment_ids = [e.enroll_id for e in enrollments]
            assessment_map = {}

            assessments = Assessment.objects.filter(enrollment_id__in=enrollment_ids)
            for a in assessments:
                assessment_map.setdefault(a.enrollment_id, []).append(a)

            for e in enrollments:
                assessment_list = assessment_map.get(e.enroll_id, [])
                score_sum = sum(a.score for a in assessment_list if a.score is not None)

                if score_sum > 0:
                    total_score += score_sum
                    valid_scores_count += len(assessment_list)
                    if e.grade is not None:
                        total_grade += e.grade
                        if e.grade >= 60:
                            pass_count += 1

            avg_score = total_score / valid_scores_count if valid_scores_count else 0
            avg_grade = total_grade / total_students if total_students else 0
            pass_rate = (pass_count / total_students) * 100 if total_students else 0

            total_teachings = CourseInstructor.objects.filter(
                course_id=course.course_id,
                instructor_id=instructor.instructor_id
            ).values('semester_id').distinct().count()

            aggregated_data.append({
                # Input features for model
                'course_name': course.course_name,
                'department_name': course.department.dept_name,
                'semester': semester.semester_name,
                'difficulty_level': difficulty,

                # Target values for prediction
                'instructor_id': instructor.instructor_id,
                'instructor_name': instructor.instructor_name,

                # Supporting metrics
                'average_score': round(avg_score, 2),
                'average_grade': round(avg_grade, 2),
                'pass_rate': round(pass_rate, 2),
                'total_teachings': total_teachings
            })

        df = pd.DataFrame(aggregated_data)

        df.drop_duplicates(subset=["course_name", "department_name", "semester", "instructor_id"], inplace=True)

        df.to_csv("course_instructor_train_top3.csv", index=False)

        self.stdout.write(self.style.SUCCESS("✅ course_instructor_train_top3.csv created successfully!"))



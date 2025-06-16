import os
import json
import pandas as pd
from django.shortcuts import render
from .ml_models import predict_student_performance
from .models import StudentRecord
from django.conf import settings

# Load dataset
DATASET_PATH = os.path.join(settings.BASE_DIR, 'altara_dataset.csv')
df = pd.read_csv(DATASET_PATH) if os.path.exists(DATASET_PATH) else pd.DataFrame()

def predict_view(request):
    query = request.GET.get('q')
    student_data = None
    prediction = {
        'scholarship': '',
        'internship': '',
        'scholarship_details': [],
        'internship_detail': {}
    }
    semesters = []
    scores = []
    average_total_score = None
    average_total_attendance = None
    top_scholarship = []
    top_internship = []

    student_names = sorted(df['name'].dropna().unique()) if not df.empty else []

    if query and not df.empty:
        student_data_df = df[df['name'] == query]

        if not student_data_df.empty:
            try:
                # Run prediction
                raw_prediction = predict_student_performance(student_data_df)

                # Process predictions into table-ready format
                prediction['scholarship'] = raw_prediction.get('scholarship', '')
                prediction['internship'] = raw_prediction.get('internship', '')
                
                # Scholarship details list of dicts
                prediction['scholarship_details'] = raw_prediction.get('scholarship_details', [])
                
                # Internship single model result as dict
                prediction['internship_detail'] = raw_prediction.get('internship_detail', {})

                # Grouped data for graph
                grouped = student_data_df.groupby('semester_name')['average_score'].mean().sort_index()
                semesters = list(grouped.index)
                scores = list(grouped.values)
                student_data = student_data_df.to_dict(orient='records')

                average_total_score = round(student_data_df['average_score'].mean(), 2)
                average_total_attendance = round(student_data_df['attendance_percentage'].mean(), 2)

                # Save to DB if not already exists
                for _, row in student_data_df.iterrows():
                    StudentRecord.objects.get_or_create(
                        student_id=row['student_id'],
                        semester_name=row['semester_name'],
                        defaults={
                            'name': row['name'],
                            'course_name': row['course_name'],
                            'attendance_percentage': row['attendance_percentage'],
                            'midterm': row['midterm'],
                            'final': row['final'],
                            'project': row['project'],
                            'average_score': row['average_score'],
                        }
                    )

                # Top 10 for scholarship
                top_scholarship_df = (
                    df.groupby('name')['average_score']
                    .mean()
                    .reset_index()
                )
                top_scholarship_df = top_scholarship_df[top_scholarship_df['average_score'] >= 75]
                top_scholarship = (
                    top_scholarship_df
                    .sort_values(by='average_score', ascending=False)
                    .head(10)
                    .to_dict(orient='records')
                )

                # Top 15 for internship
                top_internship_df = (
                    df.groupby('name')['average_score']
                    .mean()
                    .reset_index()
                )
                top_internship_df = top_internship_df[top_internship_df['average_score'] >= 70]
                top_internship = (
                    top_internship_df
                    .sort_values(by='average_score', ascending=False)
                    .head(15)
                    .to_dict(orient='records')
                )

            except Exception as e:
                prediction = {'error': f"Prediction failed: {str(e)}"}

    context = {
        'query': query or '',
        'student_data': student_data,
        'prediction': prediction,
        'semesters': json.dumps(semesters),
        'scores': json.dumps(scores),
        'average_total_score': average_total_score,
        'average_total_attendance': average_total_attendance,
        'top_scholarship': top_scholarship,
        'top_internship': top_internship,
        'student_names': student_names,
    }

    return render(request, 'altara/predict.html', context)

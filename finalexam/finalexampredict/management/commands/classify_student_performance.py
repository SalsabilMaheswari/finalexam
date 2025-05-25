import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from finalexampredict.models import ModelInfo

class Command(BaseCommand):
    help = 'Train a model to classify student performance per student'

    def handle(self, *args, **kwargs):
        # 1. Load CSV
        df = pd.read_csv('student_gpa_per_student.csv')

        # 2. Create target label from GPA (binary classification)
        df['performance_label'] = df['gpa'].apply(lambda gpa: 1 if gpa > 3.0 else 0)

        # 3. Define features & label
        features = ['avg_grade', 'avg_score', 'avg_attendance', 'total_assessment', 'gpa']
        X = df[features]
        y = df['performance_label']

        # 4. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42 #20% of the total dataset is used for test data (test size)
        ) 

        # 5. Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # 6. Predict & evaluate
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions)

        self.stdout.write(self.style.SUCCESS("Classification Report:\n" + report))

        # 7. save model to file
        model_filename = 'final_studentgpa_model.pkl'
        joblib.dump(model, model_filename)
        self.stdout.write(self.style.SUCCESS(f'model saved as {model_filename}'))

        # 8. Save model info to DB
        model_info = ModelInfo.objects.create(
            model_name='Random Forest',
            model_file=model_filename,
            training_data='student_gpa_per_student.csv',
            model_summary=report  # Optional: Store report text if model_summary field exists
        )

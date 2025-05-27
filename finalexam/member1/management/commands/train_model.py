from django.core.management.base import BaseCommand
from member1.models import ModelInfo
from django.utils.timezone import now
from django.conf import settings

import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

class Command(BaseCommand):
    help = "Train top 3 instructor prediction model and save with metadata."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting training for top 3 instructor prediction...")

        # Path ke file training data
        data_path = os.path.join(settings.BASE_DIR, 'course_instructor_train_top3.csv')
        if not os.path.exists(data_path):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {data_path}"))
            return

        # Load data
        df = pd.read_csv(data_path)

        # Encoding label categorical features
        le_course = LabelEncoder()
        le_dept = LabelEncoder()
        le_sem = LabelEncoder()
        le_instr = LabelEncoder()

        df['course_encoded'] = le_course.fit_transform(df['course_name'])
        df['department_encoded'] = le_dept.fit_transform(df['department_name'])
        df['semester_encoded'] = le_sem.fit_transform(df['semester'])
        df['instructor_encoded'] = le_instr.fit_transform(df['instructor_name'])

        # Features and target
        X = df[['course_encoded', 'department_encoded', 'semester_encoded']]
        y = df['instructor_encoded']

        # Split data train-test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model RandomForest
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict test set
        y_pred = model.predict(X_test)

        # Accuracy
        accuracy = model.score(X_test, y_test)

        
        unique_labels = np.unique(y_test)

        # Classification report 
        report = classification_report(
            y_test,
            y_pred,
            labels=unique_labels,
            target_names=[le_instr.classes_[i] for i in unique_labels],
            zero_division=0
        )

        # Confusion matrix
        conf_matrix = confusion_matrix(y_test, y_pred, labels=unique_labels)

        self.stdout.write(self.style.SUCCESS(f"📈 Accuracy: {accuracy:.2%}"))
        self.stdout.write(self.style.SUCCESS("📊 Classification Report:\n" + report))
        self.stdout.write(self.style.SUCCESS("🧮 Confusion Matrix:\n" + str(conf_matrix)))

        model_filename = 'top3_instructor_model.pkl'
        model_path = os.path.join(settings.BASE_DIR, model_filename)

        with open(model_path, 'wb') as f:
            pickle.dump({
                'model': model,
                'label_encoders': {
                    'course_name': le_course,
                    'department_name': le_dept,
                    'semester': le_sem,
                    'instructor_name': le_instr,
                },
                'feature_names': ['course_encoded', 'department_encoded', 'semester_encoded']
            }, f)

        ModelInfo.objects.create(
            model_name='Top 3 Instructor Prediction',
            version='v1.0',
            description='Predict top 3 instructors based on course name, department, and semester.',
            accuracy=accuracy,
            file_path=model_path,
            training_data=os.path.basename(data_path),
            model_summary='RandomForestClassifier with Label Encoded categorical features.'
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Model trained and saved to: {model_path}"))

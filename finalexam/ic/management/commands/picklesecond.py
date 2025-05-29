import pandas as pd
import joblib
from ic.models import ModelInfo
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class Command(BaseCommand):
    help = 'Train RandomForestClassifier for lecturer performance clustering'

    def handle(self, *args, **kwargs):
        # === Step 1: Load CSV ===
        df = pd.read_csv('ic/labeled_lecturer_data.csv')

        # === Step 2: Select Features and Target ===
        X = df[['num_students', 'avg_attendance', 'num_A', 'num_B', 'num_C', 'num_D']]
        y = df['performance_cluster']

        # === Step 3: Train-Test Split ===
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # === Step 4: Train Model ===
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # === Step 5: Evaluate ===
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        self.stdout.write(self.style.SUCCESS("Classification Report:\n" + report))

        # === Step 6: Save Model ===
        model_filename ='rfc_lecture.pkl'
        joblib.dump(model, f'ic/{model_filename}')
        self.stdout.write(self.style.SUCCESS(f'Model saved as ic/{model_filename}'))

        # === Step 7: Save Metadata ===
        model_info = ModelInfo.objects.create(
            model_name='RandomForestInstructorModel',
            model_file=model_filename,
            training_data='labeled_lecturer_data.csv',
            training_date=pd.Timestamp.now(),
            model_summary=report
        )
        self.stdout.write(self.style.SUCCESS(f'Model info saved to DB: ID {model_info.id}'))

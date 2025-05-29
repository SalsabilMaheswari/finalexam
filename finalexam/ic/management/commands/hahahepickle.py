import pandas as pd
import joblib
from ic.models import ModelInfo
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class Command(BaseCommand):
    help = 'Train a model to classify customer value and save it'


    def handle(self, *args, **kwargs):
        df = pd.read_csv('ic/instructorperf_cluster.csv')

        x = df[['avg_grade', 'avg_score', 'avg_attendance']]
        y = df.loc[x.index, 'cluster']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(x_train, y_train)

        predictions = model.predict(x_test)
        report = classification_report(y_test, predictions)
        self.stdout.write(self.style.SUCCESS("Classification Report:\n" + report))

        model_filename = 'rfc_instructor.pkl'
        joblib.dump(model, model_filename) 
        self.stdout.write(self.style.SUCCESS(f'Model saved as {model_filename}'))

        model_info = ModelInfo.objects.create(
            model_name ='RandomForestCustomerModel',
            model_file = model_filename,
            training_data = 'customer_payment_data.csv',
            training_date = pd.Timestamp.now(),
            model_summary = report
        )
        self.stdout.write(self.style.SUCCESS(f'Model info saved to DB: ID {model_info.id}'))
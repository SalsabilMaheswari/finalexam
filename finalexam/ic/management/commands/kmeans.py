# ic/management/commands/kmeans.py

from django.core.management.base import BaseCommand
from sklearn.cluster import KMeans
import pandas as pd

class Command(BaseCommand):
    help = 'Run KMeans clustering on lecturer performance data'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('ic/lecturer_data.csv')

        features = df[['num_students', 'avg_attendance', 'num_A', 'num_B', 'num_C', 'num_D']]
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['performance_cluster'] = kmeans.fit_predict(features)

        df.to_csv('labeled_lecturer_data.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Clustering complete and saved.'))

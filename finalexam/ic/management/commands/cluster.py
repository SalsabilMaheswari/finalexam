import pandas as pd
from sklearn.cluster import KMeans
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run KMeans clustering on instructor performance data'

    def handle(self, *args, **options):
        # Load CSV data
        df = pd.read_csv('ic/instructorperf2.csv')

        # Select features and drop rows with missing data
        X = df[['avg_grade', 'avg_score', 'avg_attendance']].dropna()

        # Fit KMeans with k=3 (you can adjust k)
        k = 4
        kmeans = KMeans(n_clusters=k, random_state=42)
        df.loc[X.index, 'cluster'] = kmeans.fit_predict(X)

        # Save new CSV with cluster labels
        df.to_csv('ic/instructorperf_cluster.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Clustering complete and saved.'))

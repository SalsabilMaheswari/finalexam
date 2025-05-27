from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib
from finalexampredict.models import ModelInfo
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Perform clustering analysis on course performance data'

    def handle(self, *args, **kwargs):
       # Step 1: Load and preprocess data
        df = pd.read_csv('course_performance.csv')
        
        # Convert categorical 'difficulty' to numerical
        difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        df['difficulty'] = df['difficulty'].map(difficulty_map).fillna(0)  # Handle missing value

        # Step 2: Prepare features
        features = ['avg_grade', 'difficulty', 'total_student']
        X = df[features]

        # Step 3: Feature scaling
        self.stdout.write("Standardizing features...")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Step 4: Train clustering model
        self.stdout.write("Training KMeans model with 3 clusters...")
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(X_scaled)

        # Step 5: Assign clusters and evaluate
        df['cluster'] = kmeans.labels_
        score = silhouette_score(X_scaled, kmeans.labels_)
        self.stdout.write(self.style.SUCCESS(f"Model trained. Silhouette Score: {score:.3f}"))

        # Step 6: Save clustered data
        df.to_csv('course_performance_clustered.csv', index=False)
        self.stdout.write(self.style.SUCCESS("Clustered data saved to CSV"))

        # Step 7: Save model artifacts
        model_filename = 'course_clustering_model.pkl'
        scaler_filename = 'course_scaler.pkl'
        joblib.dump(kmeans, model_filename)
        joblib.dump(scaler, scaler_filename)
        self.stdout.write(self.style.SUCCESS(f"Model saved as {model_filename}"))
        self.stdout.write(self.style.SUCCESS(f"Scaler saved as {scaler_filename}"))

        # Step 8: Save model info to database
        model_info = ModelInfo.objects.create(
            model_name='CoursePerformanceClusterModel',
            model_file=model_filename,
            training_data='course_performance.csv',
            created_at=now(),
            model_summary=f"Silhouette Score: {score:.3f}\nFeatures: {', '.join(features)}"
        )
        self.stdout.write(self.style.SUCCESS(f"Model info saved to DB: ID {model_info.id}"))

        self.stdout.write(self.style.SUCCESS("Clustering analysis completed successfully!"))
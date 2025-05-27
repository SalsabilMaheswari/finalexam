from django.db import models

class PredictionLog(models.Model):
    MODEL_CHOICES = [
        ('beasiswa', 'Beasiswa'),
        ('konsistensi', 'Konsistensi'),
        ('magang', 'Magang'),
        ('non_akademik', 'Non Akademik'),
    ]

    user_name = models.CharField(max_length=100)
    model_used = models.CharField(max_length=20, choices=MODEL_CHOICES)
    input_data = models.TextField()  # Bisa JSON string
    prediction_result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.get_model_used_display()} - {self.prediction_result}"

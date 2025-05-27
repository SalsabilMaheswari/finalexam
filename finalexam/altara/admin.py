from django.contrib import admin
from .models import PredictionLog

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'model_used', 'prediction_result', 'created_at')
    list_filter = ('model_used', 'created_at')
    search_fields = ('user_name', 'input_data', 'prediction_result')

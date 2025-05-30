from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import ModelInfo

@admin.register(ModelInfo)
class ModelInfoAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'training_date', 'training_data', 'short_summary', 'retrain_button')
    search_fields = ('model_name', 'training_data')
    
    def short_summary(self, obj):
        return (obj.model_summary[:75] + '...') if obj.model_summary else "-"
    short_summary.short_description = 'Summary'

    def retrain_button(self, obj):
        url = reverse('retrain_model', args=[obj.id])
        return format_html('<a class="button" href="{}">Retrain</a>', url)
    retrain_button.short_description = 'Retrain'

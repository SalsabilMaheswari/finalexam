from django.contrib import admin
from .models import ModelInfo
from django.utils.html import format_html
from django.utils.timezone import now

# Register your models here.
@admin.register(ModelInfo)
class ModelInfoAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'created_at', 'creator', 'use_case', 'model_type', 'training_data', 'model_file', 'short_summary', 'retrain_button')
    search_fields = ('model_name', 'training_data', 'creator', 'use_case')

    def short_summary(self, obj):
        return (obj.model_summary[:75]+ '...') if obj.model_summary else "-"
    short_summary.short_description = "Summary"

    def retrain_button(self, obj):
        return format_html('<a class="button" href="/admin/retrain-model/{}/">Retrain</a>', obj.id)
    retrain_button.short_description = 'Retrain'



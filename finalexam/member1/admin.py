

# from django.contrib import admin
# from .models import ModelInfo
# from django.utils.html import format_html
# from django.urls import path
# from django.http import HttpResponseRedirect
# from django.template.response import TemplateResponse
# from django.db.models import Avg, Max, Min, Count

# @admin.register(ModelInfo)
# class ModelInfoAdmin(admin.ModelAdmin):
#     list_display = ('model_name', 'version', 'trained_date', 'accuracy', 'file_path')
#     search_fields = ('model_name', 'version', 'description')
#     list_filter = ('trained_date',)
#     readonly_fields = ('trained_date',)

#     def has_add_permission(self, request):
#         return request.user.is_superuser

#     def changelist_view(self, request, extra_context=None):
#         # Statistik untuk ditampilkan dalam template
#         stats = {
#             'total_models': ModelInfo.objects.count(),
#             'average_accuracy': ModelInfo.objects.aggregate(Avg('accuracy'))['accuracy__avg'],
#             'max_accuracy': ModelInfo.objects.aggregate(Max('accuracy'))['accuracy__max'],
#             'min_accuracy': ModelInfo.objects.aggregate(Min('accuracy'))['accuracy__min'],
#         }
#         extra_context = extra_context or {}
#         extra_context['stats'] = stats
#         return super().changelist_view(request, extra_context=extra_context)








# from django.contrib import admin
# from django.core.management import call_command
# from django.contrib import messages
# from django.utils.html import format_html
# from member1.models import ModelInfo

# @admin.register(ModelInfo)
# class ModelInfoAdmin(admin.ModelAdmin):
#     list_display = ('model_name', 'version', 'accuracy', 'trained_date')
#     readonly_fields = ('accuracy', 'trained_date', 'model_summary', 'view_model_path', 'view_training_data')
#     actions = ['retrain_model']

#     def retrain_model(self, request, queryset):
#         try:
#             call_command('train_top3_instructor')  # nama file: train_top3_instructor.py
#             self.message_user(request, "✅ Model retrained successfully!", messages.SUCCESS)
#         except Exception as e:
#             self.message_user(request, f"❌ Error during retrain: {str(e)}", messages.ERROR)
    
#     retrain_model.short_description = "🚀 Retrain Top 3 Instructor Model"

#     def view_model_path(self, obj):
#         return format_html('<code>{}</code>', obj.file_path)
    
#     def view_training_data(self, obj):
#         return format_html('<code>{}</code>', obj.training_data)

#     view_model_path.short_description = "📁 Model File Path"
#     view_training_data.short_description = "🗂️ Training Data"











from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from django.utils.html import format_html
from member1.models import ModelInfo

@admin.register(ModelInfo)
class ModelInfoAdmin(admin.ModelAdmin):
    # Tampilkan kolom di daftar admin
    list_display = ('model_name', 'version', 'trained_date', 'accuracy', 'training_data', 'preview_model_path')

    # Kolom yang hanya bisa dibaca (tidak bisa diedit di admin)
    readonly_fields = ('trained_date', 'accuracy', 'file_path', 'training_data', 'model_summary', 'preview_model_path', 'preview_training_data')

    # Tambahkan tombol actions retrain
    actions = ['retrain_model']

    # Fungsi tombol retrain model
    def retrain_model(self, request, queryset):
        try:
            call_command('train_top3_instructor')  # Sesuai dengan nama file command
            self.message_user(request, "✅ Model retrained successfully and saved to database!", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Retraining failed: {e}", messages.ERROR)

    retrain_model.short_description = "🚀 Retrain Top 3 Instructor Prediction Model"

    # Preview file path
    def preview_model_path(self, obj):
        return format_html('<code>{}</code>', obj.file_path)

    def preview_training_data(self, obj):
        return format_html('<code>{}</code>', obj.training_data)

    preview_model_path.short_description = "📁 Model File Path"
    preview_training_data.short_description = "🗂️ Training Data"

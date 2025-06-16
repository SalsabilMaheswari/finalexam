from django.contrib import admin
from .models import StudentRecord

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'semester_name', 'average_score')
    search_fields = ('name', 'student_id', 'semester_name')
    list_filter = ('semester_name',)

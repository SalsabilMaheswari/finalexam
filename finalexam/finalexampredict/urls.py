from django.urls import path
from . import views
from . import admin_view
from .views import student_performance_view, predict_student, gpa_search_view

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('maheswari/', views.maheswari, name='maheswari'),
    path('admin/retrain-model/<int:model_id>/', admin_view.retrain_model_view, name='retrain_model'),
    path('member3/', views.member3, name='member3'),
    path('performance-view/', student_performance_view, name='student_performance_view'),
    path('input-user', student_performance_view, name='student_performance_view'),
    path('predict-student/', predict_student, name='predict_student'),
     path('gpa-search/', gpa_search_view, name='gpa_search'),
]
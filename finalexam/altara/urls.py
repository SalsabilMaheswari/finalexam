from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.altara_predict, name='altara_predict'),
    path('result/', views.altara_result, name='altara_result'),
]
from django.urls import path
from . import views
from .admin_view import retrain_model_view



urlpatterns = [
    # path('', views.home, name='home'),
    # path('predict_instructor/', views.predict_instructor, name='predict_instructor'),
    # path('', views.predict_instructor_view, name='member3'),
    path('admin/retrain-model/<int:model_id>/', retrain_model_view, name='retrain_model'),
    path('predict-view/', views.customer_prediction_view, name='customer_prediction_view'),
    path('predict-customer/', views.predict_customer, name='predict_customer'),
    path('', views.customer_prediction_view, name='member3'),
]
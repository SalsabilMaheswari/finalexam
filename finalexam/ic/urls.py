from django.urls import path
from . import views



urlpatterns = [
    # path('', views.home, name='home'),
    # path('predict_instructor/', views.predict_instructor, name='predict_instructor'),
    # path('', views.predict_instructor_view, name='member3'),
    path('predict-view/', views.customer_prediction_view, name='customer_prediction_view'),
    path('predict-customer/', views.predict_customer, name='predict_customer'),
    path('', views.customer_prediction_view, name='member3'),
]
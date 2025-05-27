
from django.urls import path
from . import views
from .views import predict_top_3_instructors

app_name = 'member1'

urlpatterns = [
    path('', views.member1, name='member1'), 
    path('predict_top_3_instructors/', views.predict_top_3_instructors, name='predict_top_3_instructors'),
]




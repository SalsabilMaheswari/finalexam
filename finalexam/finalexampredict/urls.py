from django.urls import path
from . import views
from . import admin_view

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('member2/', views.member2, name='member2'),
    path('maheswari/', views.maheswari, name='maheswari'),
    path('admin/retrain-model/<int:model_id>/', admin_view.retrain_model_view, name='retrain_model'),
    path('member3/', views.member3, name='member3'),
    path('activity-search/', views.student_activity_search_view, name='student_activity_search'),
]
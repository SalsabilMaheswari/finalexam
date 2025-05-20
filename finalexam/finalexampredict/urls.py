from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('maheswari/', views.maheswari, name='maheswari'),
    path('member3/', views.member3, name='member3'),
]
from django.urls import path
from . import views
from . import admin_view
from ic import views as ic_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('member2/', views.member2, name='member2'),
    path('maheswari/', views.maheswari, name='maheswari'),
    path('admin/retrain-model/<int:model_id>/', admin_view.retrain_model_view, name='retrain_model'),
    # path('predictcluster/', views.course_dashboard, name='course_dashboard'),
    path('predict-course-cluster/', views.predict_course_cluster, name='predict_course_cluster'),
    path('member3/', ic_views.customer_prediction_view, name='member3'),
    path('predict_customer/', ic_views.predict_customer, name='predict_customer'),
    path('predict-course-cluster/', views.predict_course_cluster, name='predict_course_cluster'),
    path('clusterchart/', views.course_cluster_chart, name='cluster_chart'),
]
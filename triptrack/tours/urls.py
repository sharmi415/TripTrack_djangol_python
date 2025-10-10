from django.urls import path
from . import views

urlpatterns = [
    path("", views.tour_list, name="tour_list"),
    path('create/', views.create_tour, name='create_tour'),
    path('hire-form/', views.hire_form, name='hire_form'),
    path('approve/', views.approve_tours, name='approve_tours'),
    path('developer-dashboard/', views.developer_dashboard, name='developer_dashboard'),
    path('user-admin-dashboard/', views.user_admin_dashboard, name='user_admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
]
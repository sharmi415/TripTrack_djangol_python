from django.urls import path
from . import views

urlpatterns = [
    # --- General Tour List ---
    path("", views.tour_list, name="tour_list"),

    # --- Creator ---
    path('creator/dashboard/', views.creator_dashboard, name='creator_dashboard'),
    path('creator/create/', views.create_tour, name='create_tour'),

    # --- Enjoyer ---
    path('enjoyer/dashboard/', views.enjoyer_dashboard, name='enjoyer_dashboard'),
    path('enjoyer/join/<int:tour_id>/', views.join_tour, name='join_tour'),

    # --- User Admin ---
    path('user-admin/dashboard/', views.user_admin_dashboard, name='user_admin_dashboard'),
    path('user-admin/hire/', views.hire_website, name='hire_website'),

    # --- Developer Admin ---
    path('developer/dashboard/', views.developer_dashboard, name='developer_dashboard'),

    # --- Default User Dashboards ---
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
]

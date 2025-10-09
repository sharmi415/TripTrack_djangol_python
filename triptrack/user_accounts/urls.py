from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Auth Routes ---
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # --- Dashboards ---
    path("developer-dashboard/", views.developer_dashboard, name="developer_dashboard"),
    path("user-admin-dashboard/", views.user_admin_dashboard, name="user_admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),

    # --- User Admin Hire Website ---
    path("hire-website/", views.hire_website, name="hire_website"),

    # --- Password Reset ---
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="user_accounts/password_reset.html"
        ),
        name="password_reset",
    ),
]

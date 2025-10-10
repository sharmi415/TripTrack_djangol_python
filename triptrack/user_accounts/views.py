
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import date

from .forms import SignUpForm, HireForm
from .models import Hire
from tours.models import Tour

User = get_user_model()

# ---------------- Signup ----------------
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")

            # Redirect based on role
            if user.role == "developer_admin" or user.is_superuser:
                return redirect("developer_dashboard")
            elif user.role == "user_admin" or user.is_staff:
                return redirect("user_admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, "user_accounts/signup.html", {"form": form})


# ---------------- Login ----------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            # Redirect based on role
            if user.role == "developer_admin" or user.is_superuser:
                return redirect("developer_dashboard")
            elif user.role == "user_admin" or user.is_staff:
                return redirect("user_admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "user_accounts/login.html", {"form": form})


# ---------------- Logout ----------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# ---------------- Developer Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "developer_admin")
def developer_dashboard(request):
    user_admins = User.objects.filter(role="user_admin")
    user_admins_data = []

    for ua in user_admins:
        hire_info = Hire.objects.filter(user_admin=ua).order_by("-start_date").first()
        user_admins_data.append({
            "username": ua.username,
            "email": ua.email,
            "hire_start": getattr(hire_info, "start_date", None),
            "hire_end": getattr(hire_info, "end_date", None),
            "duration_days": (hire_info.end_date - hire_info.start_date).days if hire_info else 0,
            "paid": getattr(hire_info, "paid", False),
        })

    context = {"user_admins_data": user_admins_data}
    return render(request, "user_accounts/dashboards/developer_dashboard.html", context)


# ---------------- Hire Form (User Admin Only) ----------------
@login_required
@user_passes_test(lambda u: u.role == "user_admin")
def hire_website(request):
    if request.method == "POST":
        form = HireForm(request.POST)
        if form.is_valid():
            hire = form.save(commit=False)
            hire.user_admin = request.user
            hire.paid = True  # simulate payment confirmation
            hire.save()
            messages.success(request, "Website hire successful!")
            return redirect("user_admin_dashboard")
    else:
        form = HireForm()

    return render(request, "user_accounts/hire_website.html", {"form": form})


# ---------------- User Admin Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == 'user_admin')
def user_admin_dashboard(request):
    # Check if user admin hire period is active
    hire = Hire.objects.filter(user_admin=request.user, paid=True).order_by('-start_date').first()
    today = date.today()
    can_manage_tours = hire and hire.start_date <= today <= hire.end_date

    tours = Tour.objects.filter(created_by=request.user) if can_manage_tours else []

    context = {
        "can_manage_tours": can_manage_tours,
        "tours": tours
    }
    return render(request, "user_accounts/dashboards/user_admin_dashboard.html", context)


# ---------------- Normal User Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "user")
def user_dashboard(request):
    tours = Tour.objects.filter(status="active").order_by("start_date")
    dashboard_features = [
        "Secure Sign-Up and Login",
        "View Upcoming Tours and Updates",
        "Join Tours and Track Participation",
        "Receive Reminders and Notifications"
    ]

    context = {"tours": tours, "dashboard_features": dashboard_features}
    return render(request, "user_accounts/dashboards/user_dashboard.html", context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date

from .forms import SignUpForm
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
            if user.role == "developer":
                return redirect("developer_dashboard")
            elif user.role == "creator":
                return redirect("creator_dashboard")
            else:  # enjoyer
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
            if user.role == "developer":
                return redirect("developer_dashboard")
            elif user.role == "creator":
                return redirect("creator_dashboard")
            else:  # enjoyer
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
@user_passes_test(lambda u: u.role == "developer")
def developer_dashboard(request):
    creators = User.objects.filter(role="creator")
    context = {"creators": creators}
    return render(request, "user_accounts/dashboards/developer_dashboard.html", context)


# ---------------- Creator Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "creator")
def creator_dashboard(request):
    tours = Tour.objects.filter(created_by=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        cost = request.POST.get("cost")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        location = request.POST.get("location")
        seats_available = request.POST.get("seats_available")

        if title and description and cost and start_date and end_date and location and seats_available:
            Tour.objects.create(
                created_by=request.user,
                name=title,
                description=description,
                cost=cost,
                start_date=start_date,
                end_date=end_date,
                location=location,
                seats_available=seats_available,
                status="active"
            )
            messages.success(request, "Tour created successfully!")
            return redirect("creator_dashboard")
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, "user_accounts/dashboards/creator_dashboard.html", {"tours": tours})


# ---------------- Enjoyer Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "user")
def user_dashboard(request):
    tours = Tour.objects.filter(status="active").order_by("start_date")
    return render(request, "user_accounts/dashboards/user_dashboard.html", {"tours": tours})


# ---------------- Book Tour (Enjoyer) ----------------
@login_required
@user_passes_test(lambda u: u.role == "user")
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    # simulate payment
    messages.success(request, f"You successfully booked '{tour.name}'!")
    return redirect("user_dashboard")

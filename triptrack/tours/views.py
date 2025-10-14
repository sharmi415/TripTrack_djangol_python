from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date

from .models import Tour, Hire, Booking
from .forms import TourForm, HireForm, BookingForm


# ---------------- Creator Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "creator")
def creator_dashboard(request):
    tours = Tour.objects.filter(created_by=request.user)
    return render(request, "tours/creator_dashboard.html", {"tours": tours})


# ---------------- Create Tour ----------------
@login_required
@user_passes_test(lambda u: u.role == "creator")
def create_tour(request):
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.created_by = request.user
            tour.save()
            messages.success(request, "Tour created successfully!")
            return redirect("creator_dashboard")
    else:
        form = TourForm()
    return render(request, "tours/create_tour.html", {"form": form})


# ---------------- Enjoyer Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "enjoyer")
def enjoyer_dashboard(request):
    tours = Tour.objects.filter(status="active").order_by("start_date")
    return render(request, "tours/enjoyer_dashboard.html", {"tours": tours})


# ---------------- Join Tour (Enjoyer) ----------------
@login_required
@user_passes_test(lambda u: u.role == "enjoyer")
def join_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.payment_done = True  # Simulate payment
            booking.save()
            messages.success(request, f"You have joined the tour '{tour.name}'!")
            return redirect("enjoyer_dashboard")
    else:
        form = BookingForm(initial={"tour": tour})

    return render(request, "tours/join_tour.html", {"form": form, "tour": tour})


# ---------------- User Admin Dashboard ----------------
@login_required
@user_passes_test(lambda u: u.role == "user_admin")
def user_admin_dashboard(request):
    # Check if hire is active
    hire = Hire.objects.filter(user_admin=request.user, paid=True).order_by('-start_date').first()
    today = date.today()
    can_manage_tours = hire and hire.start_date <= today <= hire.end_date

    tours = Tour.objects.filter(created_by=request.user) if can_manage_tours else []

    context = {
        "can_manage_tours": can_manage_tours,
        "tours": tours
    }
    return render(request, "tours/user_admin_dashboard.html", context)


# ---------------- Hire Website (User Admin) ----------------
@login_required
@user_passes_test(lambda u: u.role == "user_admin")
def hire_website(request):
    if request.method == "POST":
        form = HireForm(request.POST)
        if form.is_valid():
            hire = form.save(commit=False)
            hire.user_admin = request.user
            hire.paid = True
            hire.save()
            messages.success(request, "Website hire successful!")
            return redirect("user_admin_dashboard")
    else:
        form = HireForm()

    return render(request, "tours/hire_website.html", {"form": form})

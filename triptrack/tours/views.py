from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tour, Hire
from .forms import TourForm, HireForm
from datetime import date

# Check if User Admin hire period is valid
def is_hired(user):
    hire = Hire.objects.filter(user_admin=user, paid=True).order_by('-start_date').first()
    today = date.today()
    return hire and hire.start_date <= today <= hire.end_date

# --- User Admin: Hire Form ---
@login_required
@user_passes_test(lambda u: u.role == 'user_admin')
def hire_form(request):
    if request.method == 'POST':
        form = HireForm(request.POST)
        if form.is_valid():
            hire = form.save(commit=False)
            hire.user_admin = request.user
            hire.paid = True
            hire.save()
            return redirect('user_admin_dashboard')
    else:
        form = HireForm()
    return render(request, 'tours/hire_form.html', {'form': form})

# --- User Admin: Create Tour ---
@login_required
@user_passes_test(lambda u: u.role == 'user_admin')
def create_tour(request):
    if not is_hired(request.user):
        return redirect('hire_form')

    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.created_by = request.user
            tour.save()
            return redirect('user_admin_dashboard')
    else:
        form = TourForm()
    return render(request, 'tours/tour_form.html', {'form': form})

# --- Developer Admin: Approve Tours ---
@login_required
@user_passes_test(lambda u: u.role == 'developer_admin')
def approve_tours(request):
    tours = Tour.objects.filter(status='inactive')
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        tour = get_object_or_404(Tour, id=tour_id)
        tour.status = 'active'
        tour.save()
    return render(request, 'tours/approve_tours.html', {'tours': tours})

# --- User: View Active Tours ---
@login_required
def tour_list(request):
    tours = Tour.objects.filter(status='active').order_by('start_date')
    return render(request, 'tours/tour_list.html', {'tours': tours})

# --- Dashboards ---
@login_required
def developer_dashboard(request):
    return render(request, 'dashboards/developer_dashboard.html')

@login_required
def user_admin_dashboard(request):
    return render(request, 'dashboards/user_admin_dashboard.html')

@login_required
def user_dashboard(request):
    return render(request, 'dashboards/user_dashboard.html')
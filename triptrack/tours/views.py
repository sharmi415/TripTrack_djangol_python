from django.shortcuts import render
from .models import Tour
from .modules import tour_duration, is_tour_active

def tour_list(request):
    tours = Tour.objects.all()  # Database theke sob tours fetch
    context = {
        'tours': tours,
        'tour_duration': tour_duration,
        'is_tour_active': is_tour_active,
    }
    return render(request, "tours/tour_list.html", context)

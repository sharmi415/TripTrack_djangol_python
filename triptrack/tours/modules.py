# tours/modules.py
from datetime import date

def tour_duration(start_date, end_date):
    """Calculate number of days of a tour"""
    return (end_date - start_date).days

def is_tour_active(tour):
    """Check if a tour is active today"""
    today = date.today()
    return tour.status == 'active' and tour.start_date >= today

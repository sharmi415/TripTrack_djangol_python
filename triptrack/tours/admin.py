from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost', 'seats_available', 'status', 'created_at']
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    ordering = ('start_date',)


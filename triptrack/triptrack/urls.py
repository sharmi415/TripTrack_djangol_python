from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Home Page View
def home(request):
    return render(request, "user_accounts/home.html")

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Home Page
    path("", home, name="home"),

    # Apps URLs
    path("accounts/", include("user_accounts.urls")),   # All user_accounts related routes
    path("tours/", include("tours.urls")),              # All tours related routes
]

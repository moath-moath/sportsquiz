"""
URL configuration for sportsquiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from quiz import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="home"),
    path('beginner/', views.beginner, name="beginner"),
    path('amateur/', views.amateur, name="amateur"),
    path('medium/', views.medium, name="medium"),
    path('hard/', views.hard, name="hard"),
    path('legendary/', views.legendary, name="legendary"),

    path(
        'google088b0de6aac36d11.html',
        lambda request: HttpResponse(
            "google-site-verification: google088b0de6aac36d11.html"
        ),
        name="google_verification"
    ),
]
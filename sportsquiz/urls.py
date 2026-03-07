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
from quiz.views import home, beginner, amateur, medium, hard, legendary

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),
    path('beginner/', beginner),
    path('amateur/', amateur),
    path('medium/', medium),
    path('hard/', hard),
    path('legendary/', legendary),

    path('google088b0de6aac36d11.html',
         lambda request: HttpResponse("google-site-verification: google088b0de6aac36d11.html")),
]
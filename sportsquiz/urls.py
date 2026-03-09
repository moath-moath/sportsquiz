"""
URL configuration for sportsquiz project.
"""

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from quiz import views


# تحقق Google Search Console
def google_verification(request):
    return HttpResponse(
        "google-site-verification: google088b0de6aac36d11.html"
    )


urlpatterns = [

    # لوحة الإدارة
    path('admin/', admin.site.urls),

    # الصفحة الرئيسية
    path('', views.home, name="home"),

    # مستويات الكويز
    path('beginner/', views.beginner, name="beginner"),
    path('amateur/', views.amateur, name="amateur"),
    path('medium/', views.medium, name="medium"),
    path('hard/', views.hard, name="hard"),
    path('legendary/', views.legendary, name="legendary"),

    # تحقق Google
    path(
        'google088b0de6aac36d11.html',
        google_verification,
        name="google_verification"
    ),
]

# تشغيل ملفات static أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
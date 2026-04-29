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
    
    path('admin/', admin.site.urls),

    # الصفحة الرئيسية
    path('', views.home, name="home"),
    path('index.html', views.home), # إضافة هذا المسار لمنع خطأ 404 عند استدعاء index.html

    # صفحات المستويات
    path('beginner/', views.beginner, name="beginner"),
    path('beginner.html', views.beginner),
    
    path('amateur/', views.amateur, name="amateur"),
    path('amateur.html', views.amateur),

    path('medium/', views.medium, name="medium"),
    path('medium.html', views.medium),

    path('hard/', views.hard, name="hard"),
    path('hard.html', views.hard),

    path('legendary/', views.legendary, name="legendary"),
    path('legendary.html', views.legendary),

    # حفظ اسم اللاعب (لـ AJAX)
    path('save_player_name/', views.save_player_name, name="save_player_name"),

    # تحقق Google
    path(
        'google088b0de6aac36d11.html',
        google_verification,
        name="google_verification"
    ),
]

# إضافة مسارات الملفات الثابتة (Static & Media) بشكل أفضل
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # إذا كنت تستخدم ملفات ميديا (صور مرفوعة)، يفضل إضافة السطر التالي أيضاً:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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

    # صفحة الترحيب
    path('', views.welcome, name="welcome"),

    # الصفحة الرئيسية
    path('home/', views.home, name="home"),
    path('index.html', views.home),

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

    # لوحة المتصدرين
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('leaderboard.html', views.leaderboard),

    # حفظ اسم اللاعب
    path('save_player_name/', views.save_player_name, name="save_player_name"),

    # مزامنة بيانات اللاعب مع Firebase
    path('api/sync-player/', views.sync_player, name="sync_player"),

    # جلب إحصائيات اللاعب
    path('api/player-stats/', views.player_stats, name="player_stats"),
    path('api/award-quiz-point/', views.award_quiz_point, name="award_quiz_point"),
    path('api/award-player-guess/', views.award_player_guess, name="award_player_guess"),

    # جلب لوحات المتصدرين
    path('api/leaderboard/', views.leaderboard_data, name="leaderboard_data"),

    # توثيق قوقل
    path(
        'google088b0de6aac36d11.html',
        google_verification,
        name="google_verification"
    ),
]

# ملفات static
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

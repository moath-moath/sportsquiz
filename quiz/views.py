
from django.shortcuts import render
from django.conf import settings
from .models import Visitor
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# صفحة الترحيب
def welcome(request):
    return render(request, "welcome.html")


# الحصول على IP الزائر
def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


# الصفحة الرئيسية
def home(request):

    # قاعدة SQLite تعمل محلياً فقط
    if settings.DEBUG:
        ip = get_ip(request)

        visitor, created = Visitor.objects.get_or_create(
            ip_address=ip
        )

        visitor.last_seen = timezone.now()
        visitor.save(update_fields=["last_seen"])

        # حساب المتواجدين آخر 5 دقائق
        online_limit = timezone.now() - timedelta(minutes=5)

        online_users = Visitor.objects.filter(
            last_seen__gte=online_limit
        ).count()

        visitors = Visitor.objects.count()

    else:
        # على Vercel لا نستخدم SQLite للكتابة
        online_users = 0
        visitors = 0

    context = {
        "visitors": visitors,
        "online_users": online_users
    }

    return render(request, "index.html", context)


# صفحات المستويات
def beginner(request):
    return render(request, "beginner.html")


def amateur(request):
    return render(request, "amateur.html")


def medium(request):
    return render(request, "medium.html")


def hard(request):
    return render(request, "hard.html")


def legendary(request):
    return render(request, "legendary.html")


# لوحة المتصدرين
def leaderboard(request):
    return render(request, "quiz/leaderboard.html")


# حفظ اسم اللاعب
@csrf_exempt
def save_player_name(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            name = data.get("name", "").strip()

        except Exception:
            name = request.POST.get("name", "").strip()

        # قائمة الكلمات الممنوعة
        forbidden_words = [
            "قحب", "شرموط", "منيك", "زاني", "زانية",
            "قحبة", "شرموطة", "منيوكة", "منيوك",
            "الله", "رب", "اله", "الملك", "يلعن",
            "ملعون", "العذراء"
        ]

        name_lower = name.lower()

        for word in forbidden_words:
            if word in name_lower:
                return JsonResponse({
                    "status": "error",
                    "message": "عذراً، هذا الاسم غير مسموح به."
                }, status=400)

        if not name:
            return JsonResponse({
                "status": "error",
                "message": "الرجاء إدخال اسم صحيح."
            }, status=400)

        return JsonResponse({
            "status": "success",
            "message": "Name received successfully"
        })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    }, status=400)

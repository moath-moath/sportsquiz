from django.shortcuts import render
from .models import Visitor
from django.utils import timezone
from datetime import timedelta


# الحصول على IP الزائر
def get_ip(request):

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


# الصفحة الرئيسية
def home(request):

    ip = get_ip(request)

    visitor, created = Visitor.objects.get_or_create(ip_address=ip)

    visitor.last_seen = timezone.now()
    visitor.save(update_fields=["last_seen"])

    online_limit = timezone.now() - timedelta(minutes=5)

    online_users = Visitor.objects.filter(
        last_seen__gte=online_limit
    ).count()

    visitors = Visitor.objects.count()

    context = {
        "visitors": visitors,
        "online_users": online_users
    }

    return render(request, "home.html", context)


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
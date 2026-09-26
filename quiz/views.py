from django.shortcuts import render
from .models import Visitor
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# --- دالة صفحة الترحيب الجديدة ---
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
    ip = get_ip(request)
    
    # تحديث أو إنشاء سجل الزائر
    visitor, created = Visitor.objects.get_or_create(ip_address=ip)
    visitor.last_seen = timezone.now()
    visitor.save(update_fields=["last_seen"])

    # حساب المتواجدين حالياً (آخر 5 دقائق) والعدد الكلي
    online_limit = timezone.now() - timedelta(minutes=5)
    online_users = Visitor.objects.filter(last_seen__gte=online_limit).count()
    visitors = Visitor.objects.count()

    context = {
        "visitors": visitors,
        "online_users": online_users
    }
    # تعديل اسم الصفحة إلى index.html ليتوافق مع القالب الخاص بك
    return render(request, "index.html", context)

# --- صفحات المستويات ---

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

# --- دالة حفظ اسم اللاعب ---
@csrf_exempt
def save_player_name(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name", "").strip()
        except Exception:
            name = request.POST.get("name", "").strip()

        # قائمة الكلمات الممنوعة (يمكنك إضافة أو تعديل الكلمات هنا)
        forbidden_words = ["قحب", "شتم", "مسبة"]  # أضف أي كلمات أخرى ممنوعة
        
        # التحقق مما إذا كان الاسم يحتوي على كلمات ممنوعة
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
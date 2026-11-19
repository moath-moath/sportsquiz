from .question_banks import BEGINNER_ANSWERS, PLAYER_GUESS_ANSWERS
from django.shortcuts import render
from django.conf import settings
from .models import Visitor
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .firebase_service import get_firestore_client, get_firebase_app
from firebase_admin import auth as firebase_auth
from firebase_admin import firestore as firebase_firestore


def welcome(request):
    return render(request, "welcome.html")


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def home(request):
    if settings.DEBUG:
        ip = get_ip(request)

        visitor, created = Visitor.objects.get_or_create(
            ip_address=ip
        )

        visitor.last_seen = timezone.now()
        visitor.save(update_fields=["last_seen"])

        online_limit = timezone.now() - timedelta(minutes=5)

        online_users = Visitor.objects.filter(
            last_seen__gte=online_limit
        ).count()

        visitors = Visitor.objects.count()
    else:
        online_users = 0
        visitors = 0

    context = {
        "visitors": visitors,
        "online_users": online_users
    }

    return render(request, "index.html", context)


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


def leaderboard(request):
    return render(request, "quiz/leaderboard.html")


@csrf_exempt
def save_player_name(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name", "").strip()
        except Exception:
            name = request.POST.get("name", "").strip()

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


def verify_firebase_token(request):
    get_firebase_app()

    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        raise ValueError("رمز تسجيل الدخول غير موجود")

    id_token = auth_header.split(" ", 1)[1].strip()

    if not id_token:
        raise ValueError("رمز تسجيل الدخول فارغ")

    return firebase_auth.verify_id_token(id_token)


@csrf_exempt
def sync_player(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Method not allowed"
        }, status=405)

    try:
        decoded_token = verify_firebase_token(request)
        uid = decoded_token["uid"]

        db = get_firestore_client()
        user_ref = db.collection("users").document(uid)

        user_data = {
            "uid": uid,
            "displayName": decoded_token.get("name", "لاعب أسطوري"),
            "email": decoded_token.get("email", ""),
            "photoURL": decoded_token.get("picture", ""),
        }

        snapshot = user_ref.get()

        if not snapshot.exists:
            user_data.update({
                "totalPoints": 0,
                "totalCups": 0,
                "guessCorrectCount": 0,
            })
        else:
            existing_data = snapshot.to_dict() or {}

            for field in [
                "totalPoints",
                "totalCups",
                "guessCorrectCount"
            ]:
                if field not in existing_data:
                    user_data[field] = 0

        user_ref.set(user_data, merge=True)

        return JsonResponse({
            "status": "success",
            "message": "تم التحقق من اللاعب وحفظ بياناته"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=401)


@csrf_exempt
def player_stats(request):
    if request.method != "GET":
        return JsonResponse({
            "status": "error",
            "message": "Method not allowed"
        }, status=405)

    try:
        decoded_token = verify_firebase_token(request)
        uid = decoded_token["uid"]

        db = get_firestore_client()
        user_ref = db.collection("users").document(uid)
        snapshot = user_ref.get()

        if not snapshot.exists:
            return JsonResponse({
                "status": "error",
                "message": "Player not found"
            }, status=404)

        data = snapshot.to_dict() or {}

        return JsonResponse({
            "status": "success",
            "displayName": data.get("displayName", "لاعب"),
            "totalPoints": data.get("totalPoints", 0)
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=401)


@csrf_exempt
def leaderboard_data(request):
    if request.method != "GET":
        return JsonResponse({
            "status": "error",
            "message": "Method not allowed"
        }, status=405)

    try:
        db = get_firestore_client()
        players = db.collection("users").stream()

        points_board = []
        cups_board = []

        for player in players:
            data = player.to_dict() or {}
            name = data.get("displayName", "لاعب")

            points_board.append({
                "uid": player.id,
                "displayName": name,
                "totalPoints": int(data.get("totalPoints", 0) or 0)
            })

            cups_board.append({
                "uid": player.id,
                "displayName": name,
                "totalCups": int(data.get("totalCups", 0) or 0)
            })

        points_board.sort(
            key=lambda x: x["totalPoints"],
            reverse=True
        )

        cups_board.sort(
            key=lambda x: x["totalCups"],
            reverse=True
        )

        return JsonResponse({
            "status": "success",
            "pointsLeaderboard": points_board[:50],
            "cupsLeaderboard": cups_board[:50]
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
     
@csrf_exempt
def award_quiz_point(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Method not allowed"
        }, status=405)

    try:
        decoded_token = verify_firebase_token(request)
        uid = decoded_token["uid"]

        data = json.loads(request.body)

        question_id = str(data.get("question_id", "")).strip()
        level = str(data.get("level", "")).strip()
        selected_answer = str(data.get("selected_answer", "")).strip()

        if level != "beginner" or question_id not in BEGINNER_ANSWERS:
            return JsonResponse({
                "status": "error",
                "message": "بيانات السؤال غير صحيحة"
            }, status=400)

        correct_answer = BEGINNER_ANSWERS[question_id]

        db = get_firestore_client()
        user_ref = db.collection("users").document(uid)

        answered_ref = (
            user_ref.collection("answered_questions")
            .document(f"{level}_{question_id}")
        )

        if selected_answer != correct_answer:
            snapshot = user_ref.get()
            user_data = snapshot.to_dict() or {} if snapshot.exists else {}

            return JsonResponse({
                "status": "success",
                "correct": False,
                "alreadyAnswered": False,
                "correctAnswer": correct_answer,
                "totalPoints": user_data.get("totalPoints", 0)
            })

        transaction = db.transaction()

        @firebase_firestore.transactional
        def award_point(transaction):
            answer_snapshot = answered_ref.get(transaction=transaction)
            user_snapshot = user_ref.get(transaction=transaction)

            user_data = user_snapshot.to_dict() or {}
            current_points = int(user_data.get("totalPoints", 0) or 0)

            if answer_snapshot.exists:
                return {
                    "awarded": False,
                    "totalPoints": current_points
                }

            transaction.set(answered_ref, {
                "question_id": question_id,
                "level": level,
                "answeredAt": firebase_firestore.SERVER_TIMESTAMP
            })

            new_points = current_points + 1

            transaction.set(user_ref, {
                "totalPoints": new_points
            }, merge=True)

            return {
                "awarded": True,
                "totalPoints": new_points
            }

        result = award_point(transaction)

        return JsonResponse({
            "status": "success",
            "correct": True,
            "alreadyAnswered": not result["awarded"],
            "correctAnswer": correct_answer,
            "totalPoints": result["totalPoints"]
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

@csrf_exempt
def award_player_guess(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Method not allowed"
        }, status=405)

    try:
        decoded_token = verify_firebase_token(request)
        uid = decoded_token["uid"]

        data = json.loads(request.body)

        question_id = str(data.get("question_id", "")).strip()
        selected_answer = str(data.get("selected_answer", "")).strip()

        if question_id not in PLAYER_GUESS_ANSWERS:
            return JsonResponse({
                "status": "error",
                "message": "السؤال غير صالح"
            }, status=400)

        correct_answer = PLAYER_GUESS_ANSWERS[question_id]

        db = get_firestore_client()
        user_ref = db.collection("users").document(uid)

        answered_ref = (
            user_ref.collection("answered_players")
            .document(question_id)
        )

        if selected_answer != correct_answer:
            snapshot = user_ref.get()
            user_data = snapshot.to_dict() or {} if snapshot.exists else {}

            return JsonResponse({
                "status": "success",
                "correct": False,
                "alreadyAnswered": False,
                "guessCorrectCount": int(
                    user_data.get("guessCorrectCount", 0) or 0
                ),
                "totalCups": int(
                    user_data.get("totalCups", 0) or 0
                )
            })

        transaction = db.transaction()

        @firebase_firestore.transactional
        def award_guess(transaction):
            answer_snapshot = answered_ref.get(transaction=transaction)
            user_snapshot = user_ref.get(transaction=transaction)

            user_data = user_snapshot.to_dict() or {}

            current_count = int(
                user_data.get("guessCorrectCount", 0) or 0
            )
            current_cups = int(
                user_data.get("totalCups", 0) or 0
            )

            if answer_snapshot.exists:
                return {
                    "awarded": False,
                    "guessCorrectCount": current_count,
                    "totalCups": current_cups,
                    "cupEarned": False
                }

            new_count = current_count + 1
            cup_earned = new_count % 10 == 0
            new_cups = current_cups + (1 if cup_earned else 0)

            transaction.set(answered_ref, {
                "question_id": question_id,
                "answeredAt": firebase_firestore.SERVER_TIMESTAMP
            })

            transaction.set(user_ref, {
                "guessCorrectCount": new_count,
                "totalCups": new_cups
            }, merge=True)

            return {
                "awarded": True,
                "guessCorrectCount": new_count,
                "totalCups": new_cups,
                "cupEarned": cup_earned
            }

        result = award_guess(transaction)

        return JsonResponse({
            "status": "success",
            "correct": True,
            "alreadyAnswered": not result["awarded"],
            "guessCorrectCount": result["guessCorrectCount"],
            "totalCups": result["totalCups"],
            "cupEarned": result["cupEarned"]
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)



import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


def get_firebase_app():
    # إذا كان الاتصال مهيأ مسبقًا، نستخدمه
    try:
        return firebase_admin.get_app()
    except ValueError:
        pass

    # قراءة بيانات الحساب السري من Vercel
    service_account_json = os.environ.get(
        "FIREBASE_SERVICE_ACCOUNT_JSON"
    )

    if not service_account_json:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_JSON is not configured"
        )

    # تحويل النص إلى بيانات JSON
    service_account_info = json.loads(service_account_json)

    # إنشاء الاتصال
    credential = credentials.Certificate(service_account_info)

    return firebase_admin.initialize_app(credential)


def get_firestore_client():
    app = get_firebase_app()
    return firestore.client(app)

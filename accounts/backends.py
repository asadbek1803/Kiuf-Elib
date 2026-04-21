# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from datetime import date, datetime


def parse_date_string(date_str):
    """
    Ko'p formatli sana parsing funksiyasi
    Turli qurilmalardan kelgan sanalarni tushunish uchun
    """
    if not date_str:
        return None

    # Agar allaqachon date tipida bo'lsa
    if isinstance(date_str, date):
        return date_str

    if isinstance(date_str, datetime):
        return date_str.date()

    # String bo'lsa, ko'p formatlarni sinash
    date_formats = [
        "%Y-%m-%d",  # ISO format (2024-04-21)
        "%d.%m.%Y",  # European format (21.04.2024)
        "%d/%m/%Y",  # Slash format (21/04/2024)
        "%m/%d/%Y",  # US format (04/21/2024)
        "%Y/%m/%d",  # ISO with slashes (2024/04/21)
        "%d-%m-%Y",  # Dash format (21-04-2024)
        "%m-%d-%Y",  # US dash format (04-21-2024)
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None


class HemisAuthBackend(BaseBackend):

    def authenticate(self, request, hemis_id=None, birth_date=None, **kwargs):
        # Ikkalasi ham bo'lishi shart
        if not hemis_id or not birth_date:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(hemis_id=hemis_id)
        except UserModel.DoesNotExist:
            return None

        if not user.is_active:
            return None

        if not user.birth_date:
            return None

        # birth_date ni date tipiga o'tkazish (ko'p formatlarni qo'llab-quvvatlaydi)
        parsed_date = parse_date_string(birth_date)
        if not parsed_date:
            return None

        # Tug'ilgan kun to'g'ri bo'lsagina qaytarish
        if parsed_date != user.birth_date:
            return None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
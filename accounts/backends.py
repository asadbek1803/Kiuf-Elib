# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from datetime import date, datetime


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

        # birth_date ni date tipiga o'tkazish
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                return None

        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        # Tug'ilgan kun to'g'ri bo'lsagina qaytarish
        if birth_date != user.birth_date:
            return None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
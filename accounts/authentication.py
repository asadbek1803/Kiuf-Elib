from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class HemisIDBackend(ModelBackend):
    """HEMIS ID orqali autentifikatsiya backend"""
    
    def authenticate(self, request, hemis_id=None, **kwargs):
        try:
            user = User.objects.get(hemis_id=hemis_id)
            return user
        except User.DoesNotExist:
            return None

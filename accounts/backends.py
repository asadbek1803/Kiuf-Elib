from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class HemisAuthBackend(BaseBackend):
    """
    Custom authentication backend for HEMIS ID login (no password required)
    """
    
    def authenticate(self, request, hemis_id=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(hemis_id=hemis_id)
            if user.is_active:
                return user
        except UserModel.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

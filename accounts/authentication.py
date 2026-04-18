from datetime import date, datetime

class HemisIDBackend(ModelBackend):
    """HEMIS ID va tug'ilgan kun orqali autentifikatsiya backend"""

    def authenticate(self, request, hemis_id=None, birth_date=None, **kwargs):
        if not hemis_id or not birth_date:
            return None

        try:
            user = User.objects.get(hemis_id=hemis_id)
        except User.DoesNotExist:
            return None

        if not user.birth_date:
            return None

        # birth_date ni date obyektiga o'tkazish
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                return None

        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        # date vs date taqqoslash
        if birth_date != user.birth_date:
            return None

        return user
from django.contrib.auth.backends import ModelBackend
from TicketingApp.models import CustomUser


class CustomAuth(ModelBackend):
    def authenticate(self, request, email=None, company=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.custom_authenticate(email, company):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None

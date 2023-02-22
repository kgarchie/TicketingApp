from django.db import models
from TicketingApp.models import Ticket
from django.contrib.auth.models import User


# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)

    @property
    def get_recent_messages(self):
        return self.objects.all().order_by('-created_at')[:10]

    @property
    def latest_message(self):
        return self.objects.all().order_by('-created_at')[:1]

    def __str__(self):
        return self.chat.user.username + ' - ' + self.created_at.strftime('%d-%m-%Y %H:%M:%S') + ' - ' + self.message

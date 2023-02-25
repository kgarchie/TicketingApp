from django.db import models
from TicketingApp.models import Ticket, CustomUser


# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_user_id = models.CharField(max_length=255, blank=True, null=True)

    @property
    def get_messages(self):
        return self.message_set.all().order_by('-created_at')

    @property
    def get_chat_with_user(self, user_id=None):
        return self.message_set.filter(to_user=user_id).order_by('-created_at')

    @property
    def latest_unread_messages(self):
        return self.message_set.filter(opened=False).order_by('-created_at')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    to_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='to_user', null=True, blank=False,
                                default=None)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.chat.user.username + ' - ' + self.created_at.strftime('%d-%m-%Y %H:%M:%S') + ' - ' + self.message

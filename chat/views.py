from django.shortcuts import render
from .models import Message, Chat
from TicketingApp.models import Ticket


# Create your views here.

# Tests
def index(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(from_user=request.user)
        context = {
            "chats": chats,
        }
        return render(request, "chat/index.html", context)


def room(request, room_name):
    return render(request, "chat/tests/rooms.html", {"room_name": room_name})


def get_recent_chat_messages(chat_id):
    messages = Message.objects.filter(chat_id=chat_id).order_by('-created_at')[:10]
    context = {
        "messages": messages
    }
    return context

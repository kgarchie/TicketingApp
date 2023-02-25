from django.shortcuts import render
from .models import Chat


# Create your views here.

# Tests
def index(request):
    if not request.user.is_authenticated:
        if request.session.get('session_user_id'):
            chats = Chat.objects.filter(session_user_id=request.session['session_user_id'])
            context = {
                "chats": chats
            }
            return render(request, "chat/index.html", context)

    else:
        chats = Chat.objects.filter(user=request.user)
        context = {
            "chats": chats
        }
        return render(request, "chat/index.html", context)


def room(request, room_name):
    return render(request, "chat/tests/rooms.html", {"room_name": room_name})

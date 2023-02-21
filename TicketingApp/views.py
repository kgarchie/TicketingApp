from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Ticket


# Create your views here.

def index(request):
    return render(request, 'TicketingApp/index.html')


def create(request):
    return render(request, 'TicketingApp/create.html')


def view(request, ticket_id=None):
    if ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        return render(request, 'TicketingApp/view.html', {'ticket': ticket})
    else:
        tickets = Ticket.objects.all()
        return render(request, 'TicketingApp/view.html', {'tickets': tickets})


def edit(request, ticket_id):
    pass


def delete(request, ticket_id):
    pass


def resolve(request, ticket_id):
    pass


def close(request, ticket_id):
    pass


def reopen(request, ticket_id):
    pass


def comment(request, ticket_id):
    pass


def delete_comment(request, ticket_id, comment_id):
    pass


def edit_comment(request, ticket_id, comment_id):
    pass

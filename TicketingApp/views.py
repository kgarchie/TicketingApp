from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def get_pending():
    return Ticket.objects.filter(status='P').order_by('-created_at')


def get_resolved():
    return Ticket.objects.filter(status='R').order_by('-created_at')


def get_exceptions():
    return Ticket.objects.filter(status='E').order_by('-created_at')


def index(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    context = {
        'tickets': tickets,
        'pending': get_pending(),
        'resolved': get_resolved(),
        'exceptions': get_exceptions()
    }

    return render(request, 'TicketingApp/index.html', context)


def create(request):
    if request.method == 'POST':
        transaction_date = request.POST['transaction_date']
        reference = request.POST['reference']
        safaricom_no = request.POST['safaricom_no']
        name = request.POST['name']
        paybill_no = request.POST['paybill_no']
        airtel_no = request.POST['airtel_no']
        issues = request.POST['issue']
        amount = request.POST['amount']
        a_info = request.POST['a_info']
        company = request.POST['company']

        if request.user:
            user = request.user
        else:
            user = None

        if reference is None:
            return HttpResponse('Reference is required')

        ticket = Ticket(transaction_date=transaction_date, reference=reference, safaricom_no=safaricom_no, name=name,
                        paybill_no=paybill_no, airtel_no=airtel_no, issues=issues, amount=amount, a_info=a_info,
                        company=company, user=user)

        ticket.save()

        return redirect('TicketingApp:view')
    return render(request, 'TicketingApp/create.html')


def view(request, *ticket_id):
    if ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        return render(request, 'TicketingApp/view.html', {'ticket': ticket})
    else:
        tickets = Ticket.objects.all()
        paginator = Paginator(tickets, 10)
        try:
            page = paginator.get_page(request.GET.get('page'))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return render(request, 'TicketingApp/view.html', {'tickets': page})


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

import uuid
from datetime import datetime

from django.db.models import Q
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from chat.consumers import NotificationsWorker
from .models import Ticket, EphemeralUser, Notification, CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save

# Get the company paybills from LeizamPaybills.txt
with open('LeizamPaybills.txt', 'r') as f:
    paybills = f.read().splitlines()
    paybills.sort()


# Create your views here.
def check_if_is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def get_pending(tickets):
    return tickets.filter(status='P', deleted=False).order_by('-created_at')


def get_resolved(tickets):
    return tickets.filter(status='R', deleted=False).order_by('-created_at')


def get_exceptions(tickets):
    return (tickets.filter(status='E') | Ticket.objects.filter(deleted=True)).order_by('-created_at').distinct()


def get_new_tickets(tickets):
    return tickets.filter(status='P', deleted=False).order_by('-created_at')


def get_new_notifications(user):
    return Notification.objects.filter(user=user, opened=False).order_by('-created_at')


def index(request):
    user = request.user
    if not user.is_authenticated:
        if not request.session.get('user_id'):
            request.session['user_id'] = str(uuid.uuid4())
            request.session.set_expiry(0)
            ephemeral_user = EphemeralUser(user_id=request.session['user_id'])
            ephemeral_user.save()

        user = EphemeralUser.objects.get_or_create(user_id=request.session['user_id'])
        tickets = Ticket.objects.filter(creator=request.session['user_id'])
    else:
        tickets = Ticket.objects.filter(creator=user.email)
        user = CustomUser.objects.get(email=user.email)

    context = {
        'tickets': get_new_tickets(tickets),
        'pending': get_pending(tickets),
        'resolved': get_resolved(tickets),
        'exceptions': get_exceptions(tickets),
        'notifications': get_new_notifications(user),
    }

    return render(request, 'TicketingApp/index.html', context)


def create(request):
    context = {
        'paybills': paybills
    }
    if request.method == 'POST':
        transaction_date = request.POST['transaction_date']
        reference = request.POST['reference']
        safaricom_no = request.POST['safaricom_no']
        name = request.POST['name']
        paybill_no = request.POST['paybill_no']
        airtel_no = request.POST['airtel_no']
        issue = request.POST['issue']
        amount = request.POST['amount']
        a_info = request.POST['a_info']
        company = request.POST['company']
        try:
            elevation = request.POST['urgency']
        except KeyError:
            elevation = 'D'

        transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()

        if reference is None:
            return HttpResponse('Reference is required')

        ticket = Ticket(transaction_date=transaction_date, reference=reference, safaricom_no=safaricom_no, name=name,
                        paybill_no=paybill_no, airtel_no=airtel_no, issue=issue, amount=amount, a_info=a_info,
                        company=company, urgency=elevation)

        try:
            ticket.creator = request.session['user_id']
        except ValueError:
            return HttpResponse('Adverse Error Encountered, try clearing your cookies and cache')

        if not Ticket.objects.filter(reference=reference).exists():
            ticket.save()
            return redirect('TicketingApp:view')
        else:
            return HttpResponse('Ticket already exists')

    return render(request, 'TicketingApp/create.html', context)


def view(request, ticket_id=None, string=None):
    # TODO: Create personal view and all site view of tickets
    if ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = 'O'
        ticket.save()
    elif string:
        if not request.user.is_authenticated:
            if request.session.get('user_id'):
                tickets = Ticket.objects.filter(creator=request.session['user_id'],
                                                deleted=False).order_by('-created_at')
                if string == 'new':
                    tickets = get_new_tickets(tickets)
                elif string == 'pending':
                    tickets = get_pending(tickets)
                elif string == 'resolved':
                    tickets = get_resolved(tickets)
                elif string == 'exceptions':
                    tickets = get_exceptions(tickets)
        else:
            user = request.user
            if user is None:
                user = request.session['user_id']
                tickets = Ticket.objects.filter(user_id=user, deleted=False).order_by('-created_at')
            else:
                tickets = Ticket.objects.filter(user=request.user, deleted=False).order_by('-created_at')
    else:
        tickets = Ticket.objects.all()

    paginator = Paginator(tickets, 10)
    try:
        page = paginator.get_page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'TicketingApp/view.html', {'tickets': page, 'ticket': ticket if ticket_id else None})


def edit(request, ticket_id):
    pass


def delete(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.deleted = True
        ticket.save()
    except Ticket.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse('TicketingApp:view'))


def resolve(request, ticket_id):
    try:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        ticket.status = 'R'
        ticket.save()
    except Ticket.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse('TicketingApp:view'))


def close(request, ticket_id):
    try:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        ticket.status = 'C'
        ticket.save()
    except Ticket.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse('TicketingApp:view'))


def reopen(request, ticket_id):
    try:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        ticket.status = 'O'
        ticket.save()
        ticket.created_at = datetime.now()
        ticket.save()
    except Ticket.DoesNotExist:
        pass


def comment(request, ticket_id):
    pass


def delete_comment(request, ticket_id, comment_id):
    pass


def edit_comment(request, ticket_id, comment_id):
    pass


def search_by_date(request):
    if request.method == 'POST':
        from_date = request.POST['date_search_from']
        to_date = request.POST['date_search_to']

        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

        tickets = Ticket.objects.filter(transaction_date__range=(from_date, to_date))

        return render(request, 'TicketingApp/view.html', {'tickets': tickets})


def search_by_reference(request):
    if request.method == 'POST':
        reference = request.POST['search_transaction_code_or_reference']
        tickets = Ticket.objects.filter(reference=reference)
    else:
        tickets = None
    return render(request, 'TicketingApp/view.html', {'tickets': tickets})


def search_by_general_info(request):
    if request.method == 'POST':
        search_term = request.POST['general_search_tag']

        tickets = Ticket.objects.filter(Q(name__icontains=search_term) | Q(
            a_info__icontains=search_term) | Ticket.objects.filter(
            Q(safaricom_no__icontains=search_term) | Q(airtel_no__icontains=search_term)))

        tickets = tickets.distinct()
        return render(request, 'TicketingApp/view.html', {'tickets': tickets})
    return render(request, 'TicketingApp/view.html')


@receiver(post_save, sender=Ticket)
def new_ticket_notification(sender, instance, created, **kwargs):
    if created:
        # create notification, user should be in id
        instance = Ticket.objects.get(id=instance.id)
        notification = Notification(message='New ticket created', user=instance.creator)
        notification.save()

        # send notification
        send_notification(notification)


def send_notification(notification):
    print('Sending notification...')
    NotificationsWorker().send_new_notifications(notification)
    print('Notification sent')


@receiver(post_save, sender=Notification)
def new_notification_listener(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.get(id=instance.id)
        send_notification(notification)

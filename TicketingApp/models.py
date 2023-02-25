from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
CHOICES = (
    ('EA', 'Excess Airtime'),
    ('BWN', 'Buying To Wrong Number'),
    ('NC', 'Not Credited'),
    ('O', 'Others')
)

STATUS = (
    ('P', 'Pending'),
    ('R', 'Resolved'),
    ('C', 'Closed'),
    ('O', 'Opened')
)

URGENCY = (
    ('D', 'Default'),
    ('U', 'Urgent'),
    ('M', 'Emergency')
)

NOTIFICATION_TYPE = (
    ('T', 'New Ticket'),
    ('N', 'New Notification'),
)


class Ticket(models.Model):
    transaction_date = models.DateField()
    reference = models.CharField(max_length=20, unique=True)
    safaricom_no = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    paybill_no = models.CharField(max_length=15)
    airtel_no = models.CharField(max_length=15)
    issue = models.CharField(max_length=3, choices=CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    a_info = models.CharField(max_length=100, null=True, blank=True)
    urgency = models.CharField(max_length=1, choices=URGENCY, default='D')

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=1, choices=STATUS, default='P')
    company = models.CharField(max_length=30, null=True, blank=True)

    creator = models.CharField(null=True, blank=True, max_length=255)

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.reference

    class Meta:
        ordering = ['-created_at']


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Paybill(models.Model):
    number = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Notification(models.Model):
    type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    user = models.CharField(null=True, blank=True,
                            max_length=255)  # used to identify the user who created the notification

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)

        admin = CustomUser.objects.filter(
            is_admin=True)  # TODO: Add filter for company so that only admins of the company get the notification
        for user in admin:
            user.notifications.add(self)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']


class EphemeralUser(models.Model):
    user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        ordering = ['-created_at']


class CustomUser(EphemeralUser, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    tickets = models.ManyToManyField(Ticket, blank=True)
    is_admin = models.BooleanField(default=False)

    def custom_authenticate(self, email, company, password=None):
        try:
            user = self.objects.get(email=email, company=company) | self.objects.get(email=email, password=password)
            if user:
                return user
            return None
        except self.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        # get all current data and replace the id with email
        Ticket.objects.filter(creator=self.id).update(creator=self.email)
        Notification.objects.filter(user=self.id).update(user=self.email)

        # delete the old user
        EphemeralUser.objects.filter(user_id=self.id).delete()
        super().user_id = self.email
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['company']

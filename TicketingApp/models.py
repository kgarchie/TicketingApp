from django.db import models

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

    status = models.CharField(max_length=1, choices=STATUS, default='O')
    company = models.CharField(max_length=30, null=True, blank=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.reference

    class Meta:
        ordering = ['-created_at']

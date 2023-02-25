from django.contrib import admin
from .models import Ticket, Company, Paybill

# Register your models here.

admin.site.register(Ticket)
admin.site.register(Company)
admin.site.register(Paybill)

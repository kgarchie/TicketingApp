# Generated by Django 4.1.7 on 2023-02-22 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketingApp', '0002_alter_ticket_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='a_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='urgency',
            field=models.CharField(choices=[('D', 'Default'), ('U', 'Urgent'), ('M', 'Emergency')], default='D', max_length=1),
        ),
    ]

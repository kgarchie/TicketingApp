# Generated by Django 4.1.7 on 2023-02-22 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TicketingApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created_at']},
        ),
    ]
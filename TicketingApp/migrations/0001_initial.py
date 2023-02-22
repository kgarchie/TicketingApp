# Generated by Django 4.1.7 on 2023-02-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField()),
                ('reference', models.CharField(max_length=20, unique=True)),
                ('safaricom_no', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=30)),
                ('paybill_no', models.CharField(max_length=15)),
                ('airtel_no', models.CharField(max_length=15)),
                ('issue', models.CharField(choices=[('EA', 'Excess Airtime'), ('BWN', 'Buying To Wrong Number'), ('NC', 'Not Credited'), ('O', 'Others')], max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('R', 'Resolved'), ('C', 'Closed'), ('O', 'Opened')], default='O', max_length=1)),
                ('company', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]

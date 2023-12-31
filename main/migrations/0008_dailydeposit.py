# Generated by Django 2.2.12 on 2023-10-30 10:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_activatedstock'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_date', models.DateField(default=datetime.date.today, unique=True)),
                ('amount', models.FloatField(default=0.0)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
                #('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ежедневное пополнение',
                'verbose_name_plural': 'Ежедневные пополнения',
            },
        ),
    ]

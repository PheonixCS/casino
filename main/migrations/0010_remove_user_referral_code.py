# Generated by Django 4.2.4 on 2023-09-13 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_user_referral_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='referral_code',
        ),
    ]

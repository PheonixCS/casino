# Generated by Django 2.2.12 on 2023-10-29 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_globalsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsettings',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
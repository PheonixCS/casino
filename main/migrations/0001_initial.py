# Generated by Django 4.2.4 on 2023-09-17 14:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True
    dependencies = [(),]
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', imagekit.models.fields.ProcessedImageField(default='avatars/1s.png', upload_to='avatars/')),
                ('status', models.IntegerField(choices=[(1, 'Статус 1'), (2, 'Статус 2'), (3, 'Статус 3'), (4, 'Статус 4'), (5, 'Статус 5')], default=1)),
                ('referral_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('points', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('balance', models.FloatField(max_length=10, default=0.0)),
                ('groups', models.ManyToManyField(related_name='main_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='main_users_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GameName', models.CharField(max_length=255)),
                ('lastRun', models.DateTimeField(blank=True, null=True)),
                ('countRun', models.IntegerField(blank=True, null=True)),
                ('gamePath', models.CharField(blank=True, max_length=255, null=True)),
                ('gamePathDemo', models.CharField(blank=True, max_length=255, null=True)),
                ('icoPath', models.ImageField(upload_to='media/gameImg_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('time', models.DateTimeField()),
                ('path_to_img', models.ImageField(upload_to='media/stock_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referred_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

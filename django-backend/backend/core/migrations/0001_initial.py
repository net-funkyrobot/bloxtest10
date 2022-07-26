# Generated by Django 3.2.13 on 2022-07-23 14:21

import backend.core.fields
import backend.core.models
import backend.core.utils
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileAppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', backend.core.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', backend.core.fields.AutoUpdatedField(default=django.utils.timezone.now, editable=False)),
                ('uid', models.CharField(help_text='Firebase Auth User ID', max_length=128, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('subscribed', models.BooleanField(default=False, help_text='Marks if the user has been subscribed to the mailing list')),
                ('has_unsubscribed', models.BooleanField(default=False, help_text="Marks if the user has unsubscribed themselves to the mailing list (we shouldn't subsequently re-add them).")),
                ('mailing_list_id', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GaeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', backend.core.fields.CharOrNoneField(blank=True, default=None, max_length=21, null=True, unique=True, validators=[backend.core.utils.validate_google_user_id], verbose_name='User ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('email_lower', backend.core.fields.ComputedCharField(backend.core.models._get_email_lower, max_length=254, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', backend.core.models.GaeUserManager()),
            ],
        ),
    ]

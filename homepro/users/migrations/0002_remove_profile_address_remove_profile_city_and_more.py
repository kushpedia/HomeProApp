# Generated by Django 5.1.6 on 2025-02-20 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='zip_code',
        ),
    ]

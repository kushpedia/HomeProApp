# Generated by Django 5.1.6 on 2025-02-21 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]

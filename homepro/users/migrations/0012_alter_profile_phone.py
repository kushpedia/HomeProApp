# Generated by Django 5.1.6 on 2025-03-24 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=255),
        ),
    ]

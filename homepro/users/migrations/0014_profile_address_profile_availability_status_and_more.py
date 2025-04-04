# Generated by Django 5.1.6 on 2025-03-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_profile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='availability_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='background_check_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='badges_earned',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='booking_history',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='certifications',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='location_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='location_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='preferred_payment_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='preferred_services',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='reviews',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('provider', 'Service Provider'), ('both', 'Both')], default='customer', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='specialization',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_plan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_completed_tasks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='years_of_experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

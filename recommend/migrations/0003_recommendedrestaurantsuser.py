# Generated by Django 4.1.2 on 2023-05-03 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0023_reservation_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommend', '0002_rename_preferences_userpreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedRestaurantsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rated_restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_restaurants', to='restaurant.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

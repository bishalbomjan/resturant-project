# Generated by Django 4.1.2 on 2023-03-19 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_cuisine_image_reservation_restaurant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]

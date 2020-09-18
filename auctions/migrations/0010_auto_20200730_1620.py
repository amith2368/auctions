# Generated by Django 3.0.8 on 2020-07-30 16:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200730_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='wl',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='passengers', to='auctions.Listing'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-30 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200730_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(blank=True, to='auctions.Listing'),
        ),
    ]

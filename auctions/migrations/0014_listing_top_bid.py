# Generated by Django 3.0.8 on 2020-07-31 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200731_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='top_bid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-30 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200730_0825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentsection',
            old_name='commenter',
            new_name='name',
        ),
    ]

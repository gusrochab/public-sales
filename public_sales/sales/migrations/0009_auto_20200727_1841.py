# Generated by Django 2.2 on 2020-07-27 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20200727_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like_immobile',
            old_name='auction',
            new_name='immobile',
        ),
    ]

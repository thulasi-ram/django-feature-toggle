# Generated by Django 2.0.2 on 2018-02-17 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feature_toggle', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featuretoggle',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='featuretoggleattribute',
            options={'managed': False},
        ),
    ]

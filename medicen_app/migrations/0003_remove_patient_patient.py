# Generated by Django 3.2.5 on 2022-04-10 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicen_app', '0002_auto_20220410_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='patient',
        ),
    ]

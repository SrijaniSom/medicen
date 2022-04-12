# Generated by Django 3.2.5 on 2022-04-10 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicen_app', '0004_auto_20220410_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveBigIntegerField()),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('prescribe', models.TextField()),
                ('tests', models.TextField()),
                ('report', models.FileField(upload_to='')),
                ('longterm', models.BooleanField()),
                ('shortterm', models.BooleanField()),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medicen_app.appointments')),
            ],
        ),
    ]

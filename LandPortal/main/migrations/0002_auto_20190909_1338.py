# Generated by Django 2.2.5 on 2019-09-09 13:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landholder',
            name='LandHolder_date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-09 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190909_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landholder',
            name='LandHolder_aadhaar',
            field=models.CharField(max_length=12, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12}$')], verbose_name='Aadhaar Number'),
        ),
    ]

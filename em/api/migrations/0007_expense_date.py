# Generated by Django 3.1.7 on 2021-03-28 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210328_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]

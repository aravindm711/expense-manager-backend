# Generated by Django 3.1.7 on 2021-03-29 05:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

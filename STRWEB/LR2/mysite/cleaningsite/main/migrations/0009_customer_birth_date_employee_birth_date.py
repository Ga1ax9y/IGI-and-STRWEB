# Generated by Django 5.0.4 on 2024-05-20 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_order_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='employee',
            name='birth_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата рождения'),
        ),
    ]

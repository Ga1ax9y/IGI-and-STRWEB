# Generated by Django 5.0.4 on 2024-11-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_partner_alter_company_certificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_slide_delay', models.IntegerField(default=5000, help_text='Время автопрокрутки слайдера в миллисекундах')),
            ],
        ),
    ]

# Generated by Django 5.0.4 on 2024-09-11 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название партнера')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('logo', models.ImageField(upload_to='partner_logos/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
        migrations.AlterField(
            model_name='company',
            name='certificate',
            field=models.TextField(default='Нет сертификатов', verbose_name='Сертификат'),
        ),
    ]

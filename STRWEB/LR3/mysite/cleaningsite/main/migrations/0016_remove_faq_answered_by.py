# Generated by Django 5.0.4 on 2024-05-21 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_faq_answered_by_alter_faq_asked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='answered_by',
        ),
    ]
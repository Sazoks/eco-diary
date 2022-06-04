# Generated by Django 4.0.5 on 2022-06-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_staticpage_in_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpage',
            name='in_menu',
            field=models.BooleanField(default=False, help_text='Заголовки страниц будут отображаться в главном меню.', verbose_name='В меню'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpage',
            name='url',
            field=models.SlugField(help_text='Если Вы хотите получить URL-адрес вида https://domain/page, тогда просто введите page.', max_length=128, unique=True, verbose_name='URL-адрес'),
        ),
    ]
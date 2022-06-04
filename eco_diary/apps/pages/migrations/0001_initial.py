# Generated by Django 4.0.5 on 2022-06-04 15:49

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.SlugField(help_text='Если Вы хотите получить URL-адрес вида https://domain/page, тогда просто введите page.', max_length=128, verbose_name='URL-адрес')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='static_pages', verbose_name='Превью-изображение')),
                ('description', models.TextField(blank=True, help_text='Описание будет использоваться для meta-тега description.', null=True, verbose_name='Описание страницы')),
                ('title', models.CharField(max_length=128, verbose_name='Заголовок страницы')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Контент страницы')),
                ('in_menu', models.BooleanField(default=False, help_text='Заголовок страницы будет отображаться в главном меню.', verbose_name='В меню')),
                ('date_last_change', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Статичная страница',
                'verbose_name_plural': 'Статичные страницы',
            },
        ),
    ]
# Generated by Django 4.0.5 on 2022-06-15 03:51

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_alter_unit_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='practical_task',
            field=ckeditor.fields.RichTextField(blank=True, max_length=4096, null=True, verbose_name='Задание'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='required_materials',
            field=models.TextField(blank=True, max_length=4096, null=True, verbose_name='Необходимые материалы'),
        ),
    ]

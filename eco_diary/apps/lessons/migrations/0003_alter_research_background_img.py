# Generated by Django 4.0.5 on 2022-06-10 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_research_background_img_alter_lesson_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='research',
            name='background_img',
            field=models.ImageField(upload_to='researches/background', verbose_name='Задний фон'),
        ),
    ]
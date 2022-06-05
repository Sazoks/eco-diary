from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):
    """Модель блока уроков"""

    title = models.CharField(
        max_length=128,
        verbose_name=_('Название раздела'),
    )
    image = models.ImageField(
        upload_to='units',
        verbose_name=_('Изображение'),
        help_text=_('Это изображение будет находиться правее от исследования.'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Раздел')
        verbose_name_plural = _('Разделы')

    def __str__(self):
        return self.title


class Research(models.Model):
    """Модель исследования"""

    unit = models.OneToOneField(
        to=Unit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='research',
        related_query_name='research',
        verbose_name=_('Раздел'),
    )
    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('Контент'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Исследование')
        verbose_name_plural = _('Исследования')

    def __str__(self):
        return f'{_("Исследование")}#{self.pk}'


class Lesson(models.Model):
    """Модель урока"""

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Описание страницы'),
        help_text=_('Описание будет использоваться для meta-тега description.'),
    )
    title = models.CharField(
        max_length=128,
        verbose_name=_('Название урока'),
    )
    serial_number = models.CharField(
        max_length=32,
        verbose_name=_('Порядковый номер'),
        help_text=_('Порядковый номер вида "Урок 1-2".'),
    )
    background_image = models.ImageField(
        upload_to='lessons/background',
        verbose_name=_('Задний фон урока'),
    )
    interesting_img = models.ImageField(
        upload_to='lessons/interesting',
        verbose_name=_('Изображение блока "Это интересно"'),
    )
    interesting_text = models.TextField(
        max_length=4096,
        verbose_name=_('Текст блока "Это интересно"'),
    )
    unit = models.ForeignKey(
        to=Unit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='lessons',
        related_query_name='lesson',
        verbose_name=_('Раздел'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Урок')
        verbose_name_plural = _('Уроки')

    def __str__(self):
        return self.title


class Slide(models.Model):
    """Модель слайда для слайдера"""

    image = models.ImageField(
        upload_to='slides',
        verbose_name=_('Изображение слайда'),
    )
    delay = models.PositiveIntegerField(
        verbose_name=_('Время показа'),
        help_text=_('В секундах.'),
    )
    lesson = models.ForeignKey(
        to=Lesson,
        null=True,
        on_delete=models.SET_NULL,
        related_name='slides',
        related_query_name='slide',
        verbose_name=_('Урок'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Слайд')
        verbose_name_plural = _('Слайды')
        order_with_respect_to = 'lesson'

    def __str__(self):
        return f'{_("Слайд")}#{self.pk}'


class Question(models.Model):
    """Абстрактная модель вопроса"""

    text = models.TextField(
        max_length=1024,
        verbose_name=_('Текст вопроса'),
    )

    class Meta:
        """Настройки модели"""

        abstract = True

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Абстрактная модель ответа"""

    text = models.TextField(
        max_length=1024,
        verbose_name=_('Текст ответа'),
    )
    is_true = models.BooleanField(
        default=False,
        verbose_name=_('Правильный ответ'),
    )

    class Meta:
        """Настройки модели"""

        abstract = True

    def __str__(self):
        return self.text


class Trainer(Question):
    """Модель тренажера"""

    explanation = RichTextField(
        max_length=4096,
        verbose_name=_('Объяснение к тренажеру'),
    )
    lesson = models.OneToOneField(
        to=Lesson,
        null=True,
        on_delete=models.SET_NULL,
        related_name='trainer',
        related_query_name='trainer',
        verbose_name=_('Урок'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Тренажер')
        verbose_name_plural = _('Тренажеры')


class TrainerAnswer(Answer):
    """Модель ответа для тренажера"""

    trainer = models.ForeignKey(
        to=Trainer,
        on_delete=models.CASCADE,
        related_name='answers',
        related_query_name='answer',
        verbose_name=_('Тренажер'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Ответ для тренажера')
        verbose_name_plural = _('Ответы для тренажеров')


class Game(Question):
    """Модель игры урока"""

    first_image = models.ImageField(
        upload_to='lessons/game',
        verbose_name=_('Первое изображение для игры'),
    )
    second_image = models.ImageField(
        upload_to='lessons/game',
        verbose_name=_('Второе изображение для игры'),
    )
    lesson = models.OneToOneField(
        to=Lesson,
        null=True,
        on_delete=models.SET_NULL,
        related_name='game',
        related_query_name='game',
        verbose_name=_('Урок'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Игра')
        verbose_name_plural = _('Игры')


class GameAnswer(Answer):
    """Модель ответа для игры"""

    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE,
        related_name='answers',
        related_query_name='answer',
        verbose_name=_('Игра'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Ответ для игры')
        verbose_name_plural = _('Ответы для игр')


class PracticalTaskStep(models.Model):
    """Модель шага практического задания"""

    image = models.ImageField(
        upload_to='lessons/practical_tasks',
        verbose_name=_('Изоражение'),
    )
    text = models.TextField(
        max_length=4096,
        verbose_name=_('Текст'),
    )
    lesson = models.ForeignKey(
        to=Lesson,
        null=True,
        on_delete=models.SET_NULL,
        related_name='practical_steps',
        related_query_name='practical_step',
        verbose_name=_('Урок'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Шаг практического задания')
        verbose_name_plural = _('Практическое задание')
        order_with_respect_to = 'lesson'

    def __str__(self):
        return self.text


class AddMaterial(models.Model):
    """Модель дополнительного материала для урока"""

    image = models.ImageField(
        upload_to='lessons/add_material',
        verbose_name=_('Изображение доп. материала'),
    )
    url = models.URLField(
        verbose_name=_('URL-адрес'),
        help_text=_('Введите полный URL-адрес ресурса.')
    )
    name = RichTextField(
        config_name='minimal',
        max_length=128,
        verbose_name=_('Название доп. материала'),
    )
    lesson = models.ForeignKey(
        to=Lesson,
        null=True,
        on_delete=models.SET_NULL,
        related_name='add_materials',
        related_query_name='add_material',
        verbose_name=_('Урок'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Дополнительный материал')
        verbose_name_plural = _('Дополнительные материалы')

    def __str__(self):
        return self.name

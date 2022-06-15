from typing import (
    Optional,
    Union,
)
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags


class Unit(models.Model):
    """Модель блока уроков"""

    title = RichTextField(
        config_name='minimal',
        max_length=128,
        verbose_name=_('Название раздела'),
    )
    img_1 = models.ImageField(
        upload_to='units',
        verbose_name=_('Изображение 1'),
    )
    img_2 = models.ImageField(
        upload_to='units',
        verbose_name=_('Изображение 2'),
    )
    img_3 = models.ImageField(
        upload_to='units',
        verbose_name=_('Изображение 3'),
    )
    serial_number = models.PositiveIntegerField(
        unique=True,
        verbose_name=_('Порядковый номер'),
        help_text=_('Этот параметр определяет позицию раздела '
                    'среди всех разделов.')
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Раздел')
        verbose_name_plural = _('Разделы')
        ordering = ('serial_number', )

    def get_next_in_order(self) -> Optional['Unit']:
        """Получение следующего раздела"""

        next_unit = Unit.objects.filter(
            serial_number__gt=self.serial_number
        ).first()

        return next_unit

    def get_prev_in_order(self) -> Optional['Unit']:
        """Получение предыдущего раздела"""

        prev_unit = Unit.objects.filter(
            serial_number__lt=self.serial_number
        ).last()

        return prev_unit

    def has_research(self) -> bool:
        return hasattr(self, 'research')

    def __str__(self):
        return strip_tags(self.title)


class Research(models.Model):
    """Модель исследования"""

    url_pattern = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_('Название страницы в URL'),
        help_text=_('Если Вы хотите получить URL-адрес вида https://domain/p'
                    'age, тогда просто введите page.'),
    )
    background_img = models.ImageField(
        upload_to='researches/background',
        verbose_name=_('Задний фон'),
    )
    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('Контент'),
    )
    unit = models.OneToOneField(
        to=Unit,
        on_delete=models.CASCADE,
        related_name='research',
        related_query_name='research',
        verbose_name=_('Раздел'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Исследование')
        verbose_name_plural = _('Исследования')

    def get_next_unit_element(self) -> Optional[Union['Lesson', 'Research']]:
        """Поиск следующего элемента в разделах"""

        next_unit = self.unit.get_next_in_order()
        if next_unit is not None:
            next_unit_first_lesson = next_unit.lessons.first()
            if next_unit_first_lesson is not None:
                return next_unit_first_lesson
            if next_unit.has_research():
                return next_unit.research

    def get_prev_unit_element(self) -> Optional[Union['Lesson', 'Research']]:
        """Поиск предыдущего элемента в разделе"""

        # Если есть последний урок, берем его.
        last_lesson = self.unit.lessons.last()
        if last_lesson is not None:
            return last_lesson

        # Иначе смотрим, есть ли что брать в предыдущем разделе.
        prev_unit = self.unit.get_prev_in_order()
        if prev_unit is not None:
            # Если есть исследование, возвращаем его.
            if prev_unit.has_research():
                return prev_unit.research
            # Иначе возвращаем последний урок. Если его нет, будет None.
            return prev_unit.lessons.last()

    def __str__(self):
        return f'{_("Исследование")}#{self.pk}'


class Lesson(models.Model):
    """Модель урока"""

    url_pattern = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_('Название страницы в URL'),
        help_text=_('Если Вы хотите получить URL-адрес вида https://domain/p'
                    'age, тогда просто введите page.'),
    )
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
    preview = models.ImageField(
        upload_to='lessons/preview',
        verbose_name=_('Превью-изображение'),
    )
    serial_number = models.CharField(
        max_length=32,
        verbose_name=_('Порядковый номер'),
        help_text=_('Порядковый номер вида "1-2".'),
    )
    background_image = models.ImageField(
        upload_to='lessons/background',
        verbose_name=_('Задний фон урока'),
    )
    interesting_img = models.ImageField(
        upload_to='lessons/interesting',
        verbose_name=_('Изображение'),
    )
    interesting_text = models.TextField(
        max_length=4096,
        verbose_name=_('Текст'),
    )
    fact_img = models.ImageField(
        upload_to='lessons/fact',
        verbose_name=_('Изображение'),
    )
    fact_text = models.TextField(
        max_length=4096,
        verbose_name=_('Текст'),
    )
    practical_title = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Название практического задания'),
    )
    required_materials = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name=_('Необходимые материалы'),
    )
    practical_task = RichTextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name=_('Задание'),
    )
    unit = models.ForeignKey(
        to=Unit,
        on_delete=models.CASCADE,
        related_name='lessons',
        related_query_name='lesson',
        verbose_name=_('Раздел'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Урок')
        verbose_name_plural = _('Уроки')
        order_with_respect_to = 'unit'

    def get_next_unit_element(self) -> Optional[Union['Lesson', 'Research']]:
        """
        Поиск следующего элемента в разделах.

        Если в текущем разделе урок - последний, то следующим элементом будет
        исследование, либо первый урок в следующем разделе, либо ничего.
        """

        # Получение списка id уроков в порядке их следования.
        lesson_id_list = list(self.unit.get_lesson_order())

        # Если урок не последний в разделе, берем следующий урок.
        if self.pk != lesson_id_list[-1]:
            return self.get_next_in_order()

        # Иначе если последний, тогда проверяем, есть ли в разделе
        # исследование. Если есть - берем его.
        elif self.unit.has_research():
            return self.unit.research

        # Если раздела нет, тогда смотрим, есть ли следующий раздел.
        else:
            next_unit = self.unit.get_next_in_order()
            if next_unit is not None:
                next_unit_first_lesson = next_unit.lessons.first()
                if next_unit_first_lesson is not None:
                    return next_unit_first_lesson
                if next_unit.has_research():
                    return next_unit.research

    def get_prev_unit_element(self) -> Optional[Union['Lesson', 'Research']]:
        """
        Поиск предыдущего элемента в разделе.

        Если текущий урок - первый, то предыдущим элементом будет исследование
        в предудыщем разделе, либо последний урок в предыдущем разделе, либо
        ничего.
        """

        # Получение списка id уроков в порядке их следования.
        lesson_id_list = list(self.unit.get_lesson_order())

        # Если урок не первый в разделе, берем предыдущий урок.
        if self.pk != lesson_id_list[0]:
            return self.get_previous_in_order()

        # Иначе если урок первый, смотрим, есть ли предыдущий раздел.
        else:
            prev_unit = self.unit.get_prev_in_order()
            if prev_unit is not None:
                # Если есть исследование, возвращаем его.
                if prev_unit.has_research():
                    return prev_unit.research
                # Иначе возвращаем последний урок. Если его нет, будет None.
                return prev_unit.lessons.last()

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
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
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
        null=True,
        blank=True,
        verbose_name=_('Первое изображение для игры'),
    )
    second_image = models.ImageField(
        upload_to='lessons/game',
        null=True,
        blank=True,
        verbose_name=_('Второе изображение для игры'),
    )
    lesson = models.OneToOneField(
        to=Lesson,
        on_delete=models.CASCADE,
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
        verbose_name_plural = _('Ответы для игры')


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
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
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

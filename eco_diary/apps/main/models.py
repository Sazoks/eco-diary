from pathlib import Path
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField


class StaticPage(models.Model):
    """
    Модель статичной страницы.

    Служит для добавления контента на сайт в виде страниц, чей контент
    определяется с помощью CKE-редактора.
    """

    url = models.SlugField(
        max_length=128,
        verbose_name=_('URL-адрес'),
        help_text=_('Если Вы хотите получить URL-адрес вида https://domain/p'
                    'age, тогда просто введите page.'),
    )
    preview = models.ImageField(
        upload_to='static_pages',
        verbose_name=_('Превью-изображение'),
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_('Описание страницы'),
        help_text=_('Описание будет использоваться для meta-тега description.'),
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=128,
        verbose_name=_('Заголовок страницы'),
    )
    content = RichTextUploadingField(
        verbose_name=_('Контент страницы'),
        null=True,
        blank=True,
    )
    in_menu = models.BooleanField(
        default=False,
        verbose_name=_('В меню'),
        help_text=_('Заголовок страницы будет отображаться в главном меню.'),
    )
    date_last_change = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата последнего обновления'),
    )
    date_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата добавления'),
    )

    class Meta:
        """Настройки модели"""

        verbose_name = _('Статичная страница')
        verbose_name_plural = _('Статичные страницы')

    def delete(self, *args, **kwargs):
        """Переопределенный метод удаления записи из БД"""

        # Удаляем изображение из файловой системы, если оно есть.
        removed_img = Path(settings.MEDIA_ROOT + str(self.preview))
        print(removed_img)
        if removed_img.exists():
            removed_img.unlink()

        return super(StaticPage, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

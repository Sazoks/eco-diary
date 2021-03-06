from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class StaticPage(models.Model):
    """
    Модель статичной страницы.

    Служит для добавления контента на сайт в виде страниц, чей контент
    определяется с помощью CKE-редактора.
    """

    url_pattern = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_('Название страницы в URl'),
        help_text=_('Если Вы хотите получить URL-адрес вида https://domain/p'
                    'age, тогда просто введите page.'),
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
    subtitle = RichTextField(
        null=True,
        blank=True,
        verbose_name=_('Подзаголовок страницы'),
        help_text=_('Отображается под заголовком и над главным изображением.')
    )
    preview = models.ImageField(
        upload_to='static_pages',
        verbose_name=_('Главное изображение'),
        null=True,
        blank=True,
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
    in_footer = models.BooleanField(
        default=False,
        verbose_name=_('В футер'),
        help_text=_('Заголовок страницы будет отображаться в футере сайта.'),
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

    def __str__(self):
        return self.title

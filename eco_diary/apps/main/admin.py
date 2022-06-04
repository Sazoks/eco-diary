from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    """
    Класс отображения модели статичных страниц в админке.
    """

    list_display = ('title', 'date_last_change', 'date_add')
    list_display_links = ('title', )
    list_filter = ('in_menu', )
    fieldsets = (
        (_('Служебная информация'), {
            'fields': ('url', 'preview', 'description'),
        }),
        (_('Основная информация'), {
            'fields': ('title', 'content'),
        }),
    )

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StaticPagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pages'
    verbose_name = _('Статичные страницы')

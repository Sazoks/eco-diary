from typing import (
    Dict,
    Any,
)
from django.http import HttpRequest

from .models import StaticPage


def add_menu(request: HttpRequest) -> Dict[str, Any]:
    """Добавление в контекст шаблона меню из статичных страниц"""

    return {'menu': StaticPage.objects.filter(in_menu=True)}

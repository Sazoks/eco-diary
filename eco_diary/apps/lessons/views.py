from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import models


class UnitsView(ListView):
    """Класс-контроллер для получения списка разделов"""

    http_method_names = ('get', )
    template_name = 'lessons/units_list.html'
    model = models.Unit
    context_object_name = 'units'


class LessonView(DetailView):
    """Класс-контроллер для страницы урока"""

    http_method_names = ('get', )
    template_name = 'lessons/lesson.html'
    model = models.Lesson
    context_object_name = 'lesson'
    slug_field = 'url_pattern'
    slug_url_kwarg = 'url_pattern'


class ResearchView(DetailView):
    """Класс-контроллер для страницы исследования"""

    http_method_names = ('get', )
    template_name = 'lessons/research.html'
    model = models.Research
    context_object_name = 'research'
    slug_field = 'url_pattern'
    slug_url_kwarg = 'url_pattern'

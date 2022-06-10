from typing import Optional
from django.http import Http404
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

    def get_object(self, queryset=None):
        """Получение данных об уроке"""

        # Ищем по запись в БД по слагу.
        slug_field = self.get_slug_field()
        slug = self.kwargs.get(self.slug_url_kwarg)

        # Оптимизируем запрос, выполнив JOIN'ы.
        result = models.Lesson.objects \
            .filter(**{slug_field: slug}) \
            .select_related('game', 'trainer', 'unit')

        # Если данные были найдены, возвращаем их.
        if len(result) > 0:
            return result[0]

        raise Http404()

    def get_context_data(self, **kwargs):
        """Формирование контекста шаблона"""

        context = super(LessonView, self).get_context_data(**kwargs)

        # Добавляем в контекст данные о соседних элементах.
        neighbors_elements = {
            'prev_lesson': None,
            'next_lesson': None,
            'prev_research': None,
            'next_research': None,
        }

        # Получаем соседние элементы и сохраняем их в словарь.
        prev_element = self.object.get_prev_unit_element()
        next_element = self.object.get_next_unit_element()

        if type(prev_element) is models.Lesson:
            neighbors_elements['prev_lesson'] = prev_element
        elif type(prev_element) is models.Research:
            neighbors_elements['prev_research'] = prev_element
        if type(next_element) is models.Lesson:
            neighbors_elements['next_lesson'] = next_element
        elif type(next_element) is models.Research:
            neighbors_elements['next_research'] = next_element

        context.update(**neighbors_elements)

        return context


class ResearchView(DetailView):
    """Класс-контроллер для страницы исследования"""

    http_method_names = ('get', )
    template_name = 'lessons/research.html'
    model = models.Research
    context_object_name = 'research'
    slug_field = 'url_pattern'
    slug_url_kwarg = 'url_pattern'

    def get_object(self, queryset=None):
        """Получение данных об исследовании"""

        # Ищем по запись в БД по слагу.
        slug_field = self.get_slug_field()
        slug = self.kwargs.get(self.slug_url_kwarg)

        # Оптимизируем запрос, выполнив JOIN'ы.
        result = models.Research.objects \
            .filter(**{slug_field: slug}).select_related('unit')

        # Если данные были найдены, возвращаем их.
        if len(result) > 0:
            return result[0]

        raise Http404()

    def get_context_data(self, **kwargs):
        """Получение контекста для шаблона"""

        context = super(ResearchView, self).get_context_data(**kwargs)

        # Добавляем в контекст данные о соседних элементах.
        neighbors_elements = {
            'prev_lesson': None,
            'next_lesson': None,
            'prev_research': None,
            'next_research': None,
        }

        # Получаем соседние элементы и сохраняем их в словарь.
        prev_element = self.object.get_prev_unit_element()
        next_element = self.object.get_next_unit_element()

        if type(prev_element) is models.Lesson:
            neighbors_elements['prev_lesson'] = prev_element
        elif type(prev_element) is models.Research:
            neighbors_elements['prev_research'] = prev_element
        if type(next_element) is models.Lesson:
            neighbors_elements['next_lesson'] = next_element
        elif type(next_element) is models.Research:
            neighbors_elements['next_research'] = next_element

        context.update(**neighbors_elements)

        return context

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
        # Добавляем в контекст данны о следующем и предыдущем элементах.
        context.update(**self._get_prev_next_elements())

        return context

    def _get_prev_next_elements(self):
        """
        Получение предыдущего и следующего элементов.

        Предыдущий и следующий элемент могут быть либо уроками, либо
        исследованиями, если такие имеются.

        :return: Словарь с предыдущим и следющим элементами.
        """

        # Предыдущий и следующий уроки.
        prev_lesson: Optional[models.Lesson] = None
        next_lesson: Optional[models.Lesson] = None

        # Предыдущее и следующее исследования.
        prev_research: Optional[models.Research] = None
        next_research: Optional[models.Research] = None

        # Список не может быть пустым, т.к. формирование контекст шаблона
        # урока не запустилось бы, если бы не было хотя бы одного урока.
        lesson_id_list = list(self.object.unit.get_lesson_order())
        first_lesson_id = lesson_id_list[0]
        last_lesson_id = lesson_id_list[-1]

        # Если урок находится посередине раздела, просто берем соседние уроки.
        if self.object.pk != first_lesson_id and self.object.pk != last_lesson_id:
            prev_lesson = self.object.get_previous_in_order()
            next_lesson = self.object.get_next_in_order()
        # Иначе урок либо первый, либо последний.
        else:
            # Получаем все разделы и позицию текущего раздела среди всех.
            units = models.Unit.objects.all()
            current_unit_index = -1
            for i, unit in enumerate(units):
                if unit.pk == self.object.unit.pk:
                    current_unit_index = i
                    break

            # Если урок в разделе всего один.
            if len(lesson_id_list) == 1:
                next_research = self.object.unit.research
                if current_unit_index > 0:
                    prev_research = units[current_unit_index - 1].research
            # Если урок первый, но есть и другие уроки.
            elif self.object.pk == first_lesson_id:
                # Если раздел не первый, тогда указываем на исследование в
                # предыдущем разделе.
                if current_unit_index > 0:
                    prev_research = units[current_unit_index - 1].research
                next_lesson = self.object.get_next_in_order()
            # Если урок последний, но есть и другие уроки.
            elif self.object.pk == last_lesson_id:
                next_research = self.object.unit.research
                prev_lesson = self.object.get_previous_in_order()

        return {
            'prev_lesson': prev_lesson,
            'next_lesson': next_lesson,
            'prev_research': prev_research,
            'next_research': next_research,
        }


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
        # Добавляем следующий и предыдущий уроки.
        context.update(**self._get_prev_next_element())

        return context

    def _get_prev_next_element(self):
        """
        Получение предыдущего и следующего элементов.

        Предыдущим элементом может быть только последний урок в текущем
        разделе, а следующим - первый урок в следующем разделе, если такие
        существуют.

        :return: Словарь с предыдущим и следующим элементами.
        """

        prev_lesson: Optional[models.Lesson] = self.object.unit.lessons.last()
        next_lesson: Optional[models.Lesson] = None

        # Определение позиции текущего раздела.
        units = models.Unit.objects.all()
        current_unit_index = -1
        for i, unit in enumerate(units):
            if unit.pk == self.object.unit.pk:
                current_unit_index = i
                break

        # Если текущий раздел не последний, то берем первый урок в
        # следующем разделе.
        if current_unit_index < units.count() - 1:
            next_unit = units[current_unit_index + 1]
            if next_unit.lessons.exists():
                next_lesson = units[current_unit_index + 1].lessons.first()

        return {
            'prev_lesson': prev_lesson,
            'next_lesson': next_lesson,
        }

from django.views.generic.base import TemplateView


class MainView(TemplateView):
    """Класс-контроллер главной страницы"""

    http_method_names = ('get', )
    template_name = 'main/index.html'


class AboutProjectView(TemplateView):
    """Класс-контроллер страницы 'О проекте'"""

    http_method_names = ('get', )
    template_name = 'main/about.html'

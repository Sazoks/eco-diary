from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import StaticPage


class MainView(TemplateView):
    """Класс-контроллер главной страницы"""

    http_method_names = ('get', )
    template_name = 'main/index.html'


class AboutProjectView(TemplateView):
    """Класс-контроллер страницы 'О проекте'"""

    http_method_names = ('get', )
    template_name = 'main/about_project.html'


class StaticPageView(DetailView):
    """Класс-контроллер статичных страниц"""

    http_method_names = ('get', )
    template_name = 'main/static_page.html'
    model = StaticPage
    context_object_name = 'page'
    slug_field = 'url'
    slug_url_kwarg = 'page_path'

from django.views.generic.detail import DetailView

from .models import StaticPage


class StaticPageView(DetailView):
    """Класс-контроллер статичных страниц"""

    http_method_names = ('get', )
    template_name = 'pages/static_page.html'
    model = StaticPage
    context_object_name = 'page'
    slug_field = 'url_pattern'
    slug_url_kwarg = 'url_pattern'

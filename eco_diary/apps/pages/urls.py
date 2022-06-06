from django.urls import path

from . import views


app_name = 'pages'
urlpatterns = [
    path('<slug:url_pattern>/', views.StaticPageView.as_view(), name='static_page'),
]

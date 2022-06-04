from django.urls import path

from . import views


app_name = 'pages'
urlpatterns = [
    path('<slug:page_path>/', views.StaticPageView.as_view(), name='static_page'),
]

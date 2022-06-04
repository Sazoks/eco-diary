from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('<slug:page_path>/', views.StaticPageView.as_view(), name='static_page'),
    path('about-project/', views.AboutProjectView.as_view(), name='about_project'),
]

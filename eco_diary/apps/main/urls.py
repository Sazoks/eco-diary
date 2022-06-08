from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about/', views.AboutProjectView.as_view(), name='about_project'),
]

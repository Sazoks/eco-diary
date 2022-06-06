from django.urls import path

from . import views


app_name = 'lessons'
urlpatterns = [
    path('', views.UnitsView.as_view(), name='units'),
    # path('')
]

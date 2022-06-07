from django.urls import path

from . import views


app_name = 'lessons'
urlpatterns = [
    path('', views.UnitsView.as_view(), name='units'),
    path(
        'researches/<slug:url_pattern>/',
        views.ResearchView.as_view(),
        name='research',
    ),
    path('<slug:url_pattern>/', views.LessonView.as_view(), name='lesson'),
]

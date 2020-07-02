from django.contrib import admin
from django.urls import path
from app.controllers import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', HomePageView.as_view(), name="home"),
    path('coding/', ProjectPageView.as_view(), name="project"),
    path('alive-program/<pk>', AlwaysProgramPageView.as_view(), name="alwaysRunningProgram"),
    path('program/<pk>', ProgramPageView.as_view(), name="program"),
    path('not-found', NotFoundPageView.as_view(), name="notFound"),
]

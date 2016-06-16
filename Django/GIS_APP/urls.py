# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin

# GIS_APP.views.home - перенаправляет на вьювc, а там есть функция home
import GIS_APP.views

urlpatterns = [
    url(r'^$', GIS_APP.views.home, name = 'home'),
    url(r'^about/$', GIS_APP.views.about, name = 'about'),
    url(r'^map/$', GIS_APP.views.map, name = 'map'),
    url(r'articles/(?P<article_id>[0-9]+)/$', GIS_APP.views.show_articles, name = 'article'),
]

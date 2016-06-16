# coding=utf-8

from django.shortcuts import render, get_object_or_404
from GIS_APP.models import Articles

# Create your views here.


def home(request):
    articles = Articles.objects.all()
    # Перенаправление на templates, где есть файл home.html
    context = {
        "articles": articles
    }
    return render(request, 'GIS_APP/home.html', context)

def about(request):
    return render(request, 'GIS_APP/about.html')


def map(request):
    return render(request, 'GIS_APP/map.html')

def show_articles(request, article_id):
    article = get_object_or_404(Articles, id = article_id)
    return render(request, 'GIS_APP/article.html', {'article': article})
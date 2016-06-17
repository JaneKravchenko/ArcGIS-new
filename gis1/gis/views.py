from django.shortcuts import render, get_object_or_404

'''
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("Hello world!")
'''

from gis.models import Articles

def home(request):
    articles = Articles.objects.all()
    context = {
        'articles' : articles
    }
    return render(request, "mygis/home.html", context)

def about(request):
    return render(request, "mygis/about.html")

def map(request):
    return render(request, "mygis/map.html")

def show_articles(request,article_id):
    article = get_object_or_404(Articles,id=article_id)
    return render(request, "mygis/article.html",{'article':article})



from django.shortcuts import render
from .models import Movie

# Create your views here.


def home( request):

    movies = Movie.objects.all()

    return render(request,'video/home.html',{'movies': movies })

def list( request):

    return render(request,'video/list.html',{})


def test( request):

    return render(request,'video/test.html',{})

def single( request, movie_id ):

    item = Movie.objects.get( pk = movie_id )

    return render(request,'video/single.html',{'item': item })

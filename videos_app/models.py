import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator

from django.core.files import File
from urllib import request
import os


import tmdbsimple as tmdb
tmdb.API_KEY = '5cdc25ad718688d4bcb67f1be2276284'

# Create your models here.

class Movie(models.Model):

    FILMS = 'Films'
    ANIMES = 'Animes'
    DOCS = 'Docs'
    NEWS = 'News'
    NA = 'NA'
    CAT_CHOICES = (
        (FILMS, 'Films'),
        (ANIMES, 'Animes'),
        (DOCS, 'Docs'),
        (NA, 'NA'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    #addtime = l'heure d'ajout enregistre par la machine
    dateheure = models.DateTimeField( auto_now=True )
    tmdb = models.CharField( max_length=100, null=True, blank=True , unique=True)
    imdb = models.CharField( max_length=100, default='N.A' , unique=True )
    titre = models.CharField( max_length=100, null=True, blank=True )
    video = models.CharField( max_length=100, null=True, blank=True )
    annee = models.CharField( max_length=100, null=True, blank=True )
    tagline = models.CharField( max_length=100, null=True, blank=True )
    categories = models.CharField( max_length=10, choices=CAT_CHOICES, default=NA, )
    genres = models.CharField( max_length=100, null=True, blank=True )
    casting = models.CharField( max_length=100, null=True, blank=True )
    note = models.DecimalField( max_digits=5, decimal_places=2 , null=True , blank=True )
    poster = models.FileField( upload_to="posters", null=True, blank=True )
    poster_url = models.URLField( null=True , blank=True)
    thumbnail = models.FileField( upload_to="thumnails", null=True, blank=True )
    thumbnail_url = models.URLField( null=True, blank=True)
    resume = models.TextField( null=True, blank=True)
    

    def __str__(self):
        return 'tmbd ID : {} '.format(self.tmdb)

    class Meta:
        ordering = ['-dateheure',]

    def save(self, *args, **kwargs):

        movie = tmdb.Movies(self.tmdb)
        m = movie.info(language='fr', append_to_response = 'credits' )
        self.titre = m['title']
        self.annee = m['release_date'][0:4]
        self.genres = m['genres'][0]['name']
        self.tagline = m['tagline']
        self.resume = m['overview']
        self.note = m['vote_average']
        self.imdb = m['imdb_id']
        #La ligne en dessous renvoie une erreur list index out of range
        self.casting = '{} ,{} ,{} '.format(m['credits']['cast'][0]['name'], m['credits']['cast'][1]['name'] , m['credits']['cast'][2]['name'] )
        self.poster_url = 'https://image.tmdb.org/t/p/w185{}'.format(m['poster_path'] )
        self.thumbnail_url = 'https://image.tmdb.org/t/p/w780{}'.format(m['backdrop_path'] )

        if self.poster_url and not self.poster :
            result = request.urlretrieve(self.poster_url)
            self.poster.save( os.path.basename(self.poster_url), File(open(result[0], 'rb') ) )

        if self.thumbnail_url and not self.thumbnail :
            result = request.urlretrieve(self.thumbnail_url)
            self.thumbnail.save( os.path.basename(self.thumbnail_url), File(open(result[0], 'rb') ) )
        
        super(Movie, self).save(*args, **kwargs)

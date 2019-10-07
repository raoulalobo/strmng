from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Movie

# Register your models here.



@admin.register(Movie)
class PlainteAdmin(admin.ModelAdmin):
    list_display = ['imdb', 'titre', 'tagline']
    list_filter = ['titre']
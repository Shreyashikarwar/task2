from django.contrib import admin
from main_app.models import Movie, Casting, Dialogue
# Register your models here.

# admin.site.register(Movie)
# admin.site.register(Casting)
# admin.site.register(Dialogue)


class CastingAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'cast_name', 'gender', 'movie_name')  # Add 'movie_name' to the list_display

    def movie_name(self, obj):
        return obj.movie.name

class DialogueAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'dialogue', 'movie_name')  # Add 'movie_name' to the list_display

    def movie_name(self, obj):
        return obj.movie.name

admin.site.register(Movie)
admin.site.register(Casting, CastingAdmin)  # Register CastingAdmin
admin.site.register(Dialogue, DialogueAdmin)
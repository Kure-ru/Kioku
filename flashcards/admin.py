from django.contrib import admin

# Register your models here.
from .models import Flashcard, UserProgress, Deck

admin.site.register(Deck)
admin.site.register(Flashcard)
admin.site.register(UserProgress)
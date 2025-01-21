from django.contrib import admin
from .models import Card, Game, Room, PlayerRoom, Deck
# Register your models here.

admin.site.register(Card)
admin.site.register(Game)
admin.site.register(Room)
admin.site.register(PlayerRoom)
admin.site.register(Deck)
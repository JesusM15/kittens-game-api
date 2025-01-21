from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from social.models import Player
from django.contrib.auth.hashers import make_password, check_password

class Card(models.Model):
    ACTION_TYPE = [
        ('SKIP', 'Saltar turno'),
        ('SUPER_SKIP', 'Saltar turnos'),
        ('DEFUSE', 'Desactivar bomba'),
        ('EXPLODING_KITTEN', 'Exploding Kitten'),
        ('SEE_THE_FUTURE_3', 'Ver el futuro'),
        ('SEE_THE_FUTURE_5', 'Ver el futuro'),
        ('ALTER_THE_FUTURE_3', 'Ver el futuro'),
        ('ALTER_THE_FUTURE_5', 'Ver el futuro por 5'),
        ('ATTACK', 'Atacar'),
        ('NOPE', 'Nope'),
        ('CATOMIC_BOMB', 'Bomba atomica'),
        ("BLIND", 'Cegar'),
        ("DRAW_FROM_THE_BOTTOM", 'Agarrar desde abajo'),
        ('REVEAL_THE_FUTURE', 'Revela el futuro'),
        ('SHUFFLE', 'Mezclar cartas'),
        ('TACOCAT', 'Carta para robar')
    ]
     
    description = models.TextField()
    image = models.ImageField(upload_to='cartas/')
    type = models.CharField(max_length=60, choices=ACTION_TYPE)

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    players = models.ManyToManyField(Player, through='PlayerRoom')
    max_players = models.IntegerField(default=2, validators=[
        MaxValueValidator(4), 
        MinValueValidator(2)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def add_player(self, player):
        if self.players.count() >= self.max_players:
            raise ValueError("La sala está llena.")
        if Room.objects.filter(players=player).exists():
            raise ValueError("El usuario ya está en otra sala.")
        self.players.add(player)
        
    def remove_player(self, player):
        self.players.remove(player)
        
    def dissolve_room(self):
        self.is_active = False
        self.save()

class Game(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # players = models.ManyToManyField(User, through='Player')
    is_over = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="games_won")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partida {self.id} en la Sala {self.room.id}"
    
    def start_game(self):
        pass
    
class Deck(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    cards = models.JSONField(default=list)  # [{'id': 1, 'flipped': False}, ...]
    discarded = models.JSONField(default=list)
    
class PlayerRoom(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_ready = models.BooleanField(default=False)

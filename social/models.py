from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Setting(models.Model):
    LANG_OPTIONS = [    
        ('ES', 'Español'),
        ('EN', 'English')
    ]
    
    lang = models.CharField(max_length=3, default="ES", choices=LANG_OPTIONS)
    volume = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Valor decimal entre 0 y 1"
    )
    
    
    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hand = models.JSONField(default=list, blank=True, null=True)  # [{id: 1, flipped: False}, ...]
    settings = models.OneToOneField(Setting, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d', null=True, blank=True, default="images/default/avatar_default.png")  # Cambié %M a %m para el mes

    def draw_card(self, card_id, flipped=False):
        self.hand.append({"id": card_id, "flipped": flipped})
        self.save()

    def remove_card(self, card_id):
        self.hand = [card for card in self.hand if card["id"] != card_id]
        self.save()
        
    def get_profile_picture_url(self, request=None):
        """
        Retorna la URL completa de la foto de perfil, incluyendo el dominio,
        si se proporciona un objeto request. De lo contrario, usa MEDIA_URL.
        """
        if self.profile_picture:
            if request:
                return request.build_absolute_uri(self.profile_picture.url)
            return f"{settings.MEDIA_URL}{self.profile_picture}"
        return None
        
# Crear automáticamente un `Player` para cada usuario
def create_player(sender, instance, created, **kwargs):
    if created:
        settings = Setting.objects.create()
        Player.objects.create(user=instance, settings=settings)

post_save.connect(create_player, sender=User)

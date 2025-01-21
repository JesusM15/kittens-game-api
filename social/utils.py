from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from social.models import Player  # Ajusta según tu estructura de proyecto

def create_guest_user():
    # Crear el usuario invitado
    username = f"guest_{get_random_string(8)}"
    guest_user = User.objects.create_user(
        username=username,
        password=None  # Sin contraseña, solo para uso temporal
    )
    guest_user.is_active = False  # Opcional: limitar funciones
    guest_user.save()

    # Crear el Player asociado
    player = Player.objects.create(user=guest_user)
    player.save()

    return player

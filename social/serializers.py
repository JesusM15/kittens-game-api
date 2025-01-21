from .models import Player, Setting
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

# serializadores

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    
    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url) if request else obj.profile_picture.url
        return None
    
    class Meta:
        model = Player
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Player.objects.create(user=user)
        return user
    
    
from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Player, Setting
from django.db.models import Q
import json
from django.forms.models import model_to_dict
from .serializers import UserSerializer, ProfileSerializer, SettingsSerializer

class ObtainUserFromToken(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = get_object_or_404(Player, user=user)
        
        profile_picture = profile.get_profile_picture_url(request)
        
        return Response({
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_login': user.last_login,
            'id': user.id,
            'Player': {
                'hand': profile.hand,
                'profile_picture': profile_picture,
                'Settings': {   
                    'volume': profile.settings.volume,
                    'lang': profile.settings.lang
                }
                
            },
            'profile_picture': profile_picture
        }, status=status.HTTP_200_OK)
        
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Player, user=user)
        user_settings = get_object_or_404(Setting, player=profile)
        
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else: 
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
        else: 
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        settings_serializer = SettingsSerializer(user_settings, data=request.data, partial=True)
        if settings_serializer.is_valid():
            settings_serializer.save()
        else:
            return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        profile_picture = profile.profile_picture_url(request)
        
        return Response({
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_login': user.last_login,
            'id': user.id,
            'Player': {
                'hand': profile.hand,
                'profile_picture': profile_picture,
                'Settings': {   
                    'volume': profile.settings.volume,
                    'lang': profile.settings.lang
                }
                
            },
            'profile_picture': profile_picture
        }, status=status.HTTP_200_OK)
        
class SettingsUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Player, user=user)
        user_settings = get_object_or_404(Setting, player=profile)
        
        user_settings_serializer = SettingsSerializer(user_settings, data=request.data, partial=True)
        if user_settings_serializer.is_valid():
            user_settings_serializer.save()
        else:
            return Response(user_settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'volume': user_settings.volume,
            'lang': user_settings.lang
        })

        
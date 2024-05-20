from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment, Favourite, Like

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Comment
        fields = '__all__'
        

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Like
        fields = '__all__'
        

class FavouriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Favourite
        fields = '__all__'


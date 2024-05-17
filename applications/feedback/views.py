from django.shortcuts import render

from applications.feedback.serializers import FavouriteSerializer
from .models import Comment, Favourite, Like
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class FeedbackMixin:
    def add_comment(self, request, pk=None):
        try:
            event = self.get_object()
            comment = request.data['comment']
            user= request.user
            comment_obj = Comment.objects.create(owner=user, event=event, comment=comment)
            comment_obj.save()
            return Response('Комментарий добавлен', status=status.HTTP_201_CREATED)
        except:
            return Response('Нужно написать комментарий', status=status.HTTP_400_BAD_REQUEST)
        
    def delete_comment(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response('Комментарий удален', status=status.HTTP_404_NOT_FOUND)
    
    def like(self, request, pk=None, *args, **kwargs):
        try:
            like_obj, _ = Like.objects.get_or_create(owner=request.user, event_id=pk)
            like_obj.like = not like_obj.like
            like_obj.save()
            msg = 'Вы поставили лайк'
            if not like_obj.like:
                msg = 'Вы убрали лайк'
            return Response(msg)
        except:
            return Response('Что то пошло не так', status=status.HTTP_400_BAD_REQUEST)
        
    def favourite(self, request, pk=None, *args, **kwargs):
        try:
            fav_obj, _ = Favourite.objects.get_or_create(owner=request.user, event_id=pk)
            fav_obj.favourite = not fav_obj.favourite
            fav_obj.save()
            msg = 'Сохранены в любимые'
            if not fav_obj.favourite:
                fav_obj.delete()
                msg = 'Удалены из любимых'
            return Response(msg)
        except:
            return Response('Что то пошло не так', status=status.HTTP_400_BAD_REQUEST)
        
    def get_favourites(self, request, *args, **kwargs):
        try:
            list_of_fav = Favourite.objects.filter(owner=request.user, favourite=True)
            serializer = FavouriteSerializer(list_of_fav, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong')
        
        
    
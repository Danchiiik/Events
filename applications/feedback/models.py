from django.db import models
from django.contrib.auth import get_user_model

from applications.events.models import Events

User = get_user_model()


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.owner} - {self.comment[:5]}'
    

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.owner} - {str(self.like)}'
    

class Favourite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.owner} - {str(self.favourite)}'
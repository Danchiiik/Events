from rest_framework.permissions import BasePermission, SAFE_METHODS
from applications.feedback.models import Comment
from rest_framework.response import Response

class IsEventOwner_or_ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return request.user.is_authenticated
     
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated or request.user.is_staff
        return request.user.is_authenticated and (request.user == obj.owner or request.user.is_staff)
    
    
class IsFeedbackOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        try:
            return request.user.is_authenticated and request.user == Comment.object.get(id=view.kwargs['pk']).owner
        except:
            return Response('Что-то пошло не так')
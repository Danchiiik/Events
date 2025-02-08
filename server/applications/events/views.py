from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from applications.events.models import Events
from applications.events.permissions import IsFeedbackOwner, IsEventOwner_or_ReadOnly
from applications.events.serializers import EventsSerializer
from applications.feedback.views import FeedbackMixin


class PaginationApiView(PageNumberPagination):
    page_size = 6
    max_page_size = 100
    page_size_query_param = 'events_page'


class EventsViewSet(ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsEventOwner_or_ReadOnly]
    
    pagination_class = PaginationApiView
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region', 'type', 'type_of_event']
    search_fields = ['name', 'owner']
    ordering_fields = ['date']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'delete_comment':
            return [IsFeedbackOwner()]
        return super().get_permissions()        
        
        
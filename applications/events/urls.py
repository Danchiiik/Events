from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.events.views import EventsViewSet

router = DefaultRouter()
router.register('', EventsViewSet)

urlpatterns = [
    path('<int:pk>/like/', EventsViewSet.as_view({'post': 'like'})),
    path('<int:pk>/comment/', EventsViewSet.as_view({'post': 'add_comment'})),
    path('comment/<int:pk>/', EventsViewSet.as_view({'delete': 'delete_comment'})),
    path('favourites/', EventsViewSet.as_view({'get': 'get_favourites'})),
    path('<int:pk>/favourite/', EventsViewSet.as_view({'post':'favourite'})),
]

urlpatterns += router.urls

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from applications.accounts.views import ActivationApiView, ChangePasswordApiView, ForgotPasswordApiView, ForgotPasswordFinishApiView, ProfileViewSet, RegisterApiView
from . import views

router = DefaultRouter()
router.register('', ProfileViewSet)


urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('confirm/<uuid:activation_code>/', ActivationApiView.as_view()),
    path('change_password/', ChangePasswordApiView.as_view()),
    path('forgot_password/', ForgotPasswordApiView.as_view()),
    path('forgot_password_finish/', ForgotPasswordFinishApiView.as_view()),    
    path('profile/', include(router.urls)),

    path('', views.home),
    path('logout/', views.logout_view)
       
]



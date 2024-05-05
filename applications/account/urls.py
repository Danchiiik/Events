from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from applications.account.views import ActivationApiView, ChangePasswordApiView, ForgotPasswordApiView, ForgotPasswordFinishApiView, RegisterApiView


urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('confirm/<uuid:activation_code>/', ActivationApiView.as_view()),
    path('change_password/', ChangePasswordApiView.as_view()),
    path('forgot_password/', ForgotPasswordApiView.as_view()),
    path('forgot_password_finish/', ForgotPasswordFinishApiView.as_view()),    
]



from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from applications.accounts.models import Profile
from applications.accounts.permissions import IsProfileOwner
from applications.accounts.serializers import ChangePasswordSerializer, ForgotPasswordFinishSerializer, ForgotPasswordSerializer, ProfileSerializer, RegisterSerializer

User = get_user_model()

class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегестрировались. На вашу почту отправлена ссылка для активации аккаунта', status=status.HTTP_201_CREATED)
        
    
class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'message' : 'Успешно'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message' : 'Не правильная почта'}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordApiView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль изменен успешно', status=status.HTTP_200_OK)
    

class ForgotPasswordApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('На вашу почту был отправлен код', status=status.HTTP_200_OK)
    

class ForgotPasswordFinishApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль обновлен успешно', status=status.HTTP_200_OK)
    
    
class ProfileViewSet(mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin, 
                     GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner]
    


def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('http://localhost:8080')

@login_required
def generate_jwt_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    request.session['access'] = token['access']
    request.session['refresh'] = token['refresh']


    redirect_url = f"http://localhost:8080/google-callback?access={token['access']}&refresh={token['refresh']}"
    
    return redirect(redirect_url)
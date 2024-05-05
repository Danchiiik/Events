from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from applications.account.serializers import ChangePasswordSerializer, ForgotPasswordFinishSerializer, ForgotPasswordSerializer, RegisterSerializer

User = get_user_model()

class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('You have successfully registered. We have sent you an activation code', status=status.HTTP_201_CREATED)
        
    
class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'message' : 'Successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message' : 'Wrong email'}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordApiView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password changed successfully', status=status.HTTP_200_OK)
    

class ForgotPasswordApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('We have sent you code', status=status.HTTP_200_OK)
    

class ForgotPasswordFinishApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password updated successfully', status=status.HTTP_200_OK)
    
    
        
        

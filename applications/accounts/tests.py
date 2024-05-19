import uuid
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class AccountTests(APITestCase):
    @property
    def example_bearer_token(self):
        user = CustomUser.objects.create_user(email="example@mail.com",
                                              password="12345678", 
                                              is_active=True)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    @property
    def trial_bearer_token(self):
        user = CustomUser.objects.create_user(email="dcabatar@gmail.com",
                                              password="12345678",
                                              is_active=True)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    # @property
    # def bearer_token(self):
    #     print("\nPlease enter working email address again")
    #     user = CustomUser.objects.create_user(email=input("Enter email address:\t"),
    #                                           password=input("Set password:\t"),
    #                                           is_active=True)
    #     refresh = RefreshToken.for_user(user)
    #     return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    
    
    def test_create_account(self):
        print("-"*60,"\nTesting creaete account\n","-"*60)
        url = 'http://127.0.0.1:8000/api/v1/account/register/'
        
        response = self.client.post(url, data={"email": 'dcabatar@gmail.com', 
                                               "password": '12345678', 
                                               "password2": '12345678'})
        print("\nCase with correct passwords\n", "="*60)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Wrong email or password")
        
    def test_login_account(self):
        print("-"*60,"\nTesting login account\n","-"*60)
        url = 'http://127.0.0.1:8000/api/v1/account/login/'
        user = CustomUser.objects.create_user(email="dcabatar@gmail.com", 
                                              password="12345678", 
                                              is_active=False)

        print("\nCase with inactive account\n", "="*70)        
        response = self.client.post(url, data={"email": "dcabatar@gmail.com", 
                                               "password": "12345789"}, 
                                                format='json',
                                                is_valid=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
        print("\nCase with active account\n", "="*70)
        user.is_active = True
        user.save()
        response = self.client.post(url, data={"email": "dcabatar@gmail.com", 
                                               "password": "12345678"}, 
                                                format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_change_password(self):
        # print("-"*60,"\nTesting change password account\n","-"*60)
        url = 'http://127.0.0.1:8000/api/v1/account/change_password/'
        
        response = self.client.post(url, data={"old_password": "123456789", 
                                               "new_password": '87654321', 
                                               "new_password2": "87654321"}, 
                                                **self.example_bearer_token)
        print("\nCase with wrong password\n", "="*70)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        print("\nOld password:\t12345678")
        response = self.client.post(url, data={"old_password": "12345678", 
                                               "new_password": '87654321', 
                                               "new_password2": '87654321'}, 
                                                **self.trial_bearer_token)
        print("\nCase with correct password\n", "="*70)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Wrong password")

    def test_forgot_password(self):
        print("-"*60,"\nTesting change password code\n","-"*60)
        url = 'http://127.0.0.1:8000/api/v1/account/forgot_password/'
        response = self.client.post(url, data={"email": 'dcabatar@gmail.com'}, **self.trial_bearer_token)
        print("\nCase with email recovery\n", "="*70)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Please enter working email address")
        
        
    def test_forgot_password_finish(self):
        user = CustomUser.objects.create_user(email="dsabatar@gmail.com", 
                                              password="12345678", 
                                              is_active=True,
                                              activation_code='')
        
        url = 'http://127.0.0.1:8000/api/v1/account/forgot_password/'
        response = self.client.post(url, data={"email": user.email}, **self.example_bearer_token)

        

        url = 'http://127.0.0.1:8000/api/v1/account/forgot_password_finish/'
        response = self.client.post(url, data={"email": user.email,
                                                "code": user.activation_code,
                                                "password": '11223344',
                                                "password2": '11223344'},
                                                **self.trial_bearer_token)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
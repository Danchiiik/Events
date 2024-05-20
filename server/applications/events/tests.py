from io import BytesIO
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()

class EventsTestCase(TestCase):
    
    def setUp(self) -> None:
        User.objects.create(email='dcabatar@gmail.com', password='12345678', is_active = True)
        
        
        self.image = SimpleUploadedFile(
            name='hello.jpg',
            content=b'file_content',  # Simulate the content of the image file
            content_type='image/jpeg'
        )
        
        self.data = dict(name='test_event', image=self.image, region='Бишкек', address='dfd', date='2024-05-23', time='10:10', type_of_event='Открытие', type='Открытый', owner=User.objects.get(email='dcabatar@gmail.com'))
        
    @property
    def jwt_token(self):
        user1 = User.objects.get(email='dcabatar@gmail.com')
        refresh = RefreshToken.for_user(user1)
        return {'HTTP_AUTHORIZATION':f'Bearer {refresh.access_token}'}
    

    def test_event_post(self):  
        url = 'http://127.0.0.1:8000/api/v1/events/'
        response = self.client.post(url, data=self.data, **self.jwt_token)
        print(response.data)
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        
    def test_events_get(self):
        url = 'http://127.0.0.1:8000/api/v1/events/'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(response.data)
        
        
    
    def test_events_get_detail(self):
        url = 'http://127.0.0.1:8000/api/v1/events/'
        response = self.client.post(url, data=self.data, **self.jwt_token)
        
        print(response.data)
        url = f'http://127.0.0.1:8000/api/v1/events/{response.data["id"]}/'
        response = self.client.get(url)
        
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        
    file_path = "/home/daniel/Documents/diploma/media/images/hello.jpg"
    def get_upload_photo(self) -> SimpleUploadedFile:
        with open(file=self.file_path, mode="rb") as file:
            return SimpleUploadedFile(
                name="hello.jpg",
                content=file.read(),
                content_type="image/jpg"
            )
            
    
    # def test_events_put(self):    
    #     url = 'http://127.0.0.1:8000/api/v1/events/'
    #     response = self.client.post(url, data=self.data, **self.jwt_token)
    #     image = self.get_upload_photo()
        
    #     data1 = {
    #         'name': 'put',
    #         'image': image,
    #         'region': 'Бишкек',
    #         'address': 'dfd',
    #         'date': '2024-05-23',
    #         'time': '10:10',
    #         'type_of_event': 'Открытие',
    #         'type': 'Открытый'
    #     }
        
    #     url = f'http://127.0.0.1:8000/api/v1/events/{response.data["id"]}/'
    #     response = self.client.put(url, data=data1, **self.jwt_token, format='multipart')
        
    #     self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
      
            
    def test_events_patch(self):      
        url = 'http://127.0.0.1:8000/api/v1/events/'
        response = self.client.post(url, data=self.data, **self.jwt_token)
        
        print(response.data)
        data1 = {'name':'patch', 'date': '2024-05-24'}
        url = f'http://127.0.0.1:8000/api/v1/events/{response.data["id"]}/'
        response = self.client.patch(url, data=data1, **self.jwt_token, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        
    def test_events_delete(self):
        url = 'http://127.0.0.1:8000/api/v1/events/'
        response = self.client.post(url, data=self.data, **self.jwt_token)
        
        print(response.data)
        url = f'http://127.0.0.1:8000/api/v1/events/{response.data["id"]}/'
        response = self.client.delete(url, **self.jwt_token, content_type='application/json')
        
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.utils import json
from post.models import Post



class PostTestCase(APITestCase):
   url_list = reverse('post:list')
   url_create = reverse('post:create')
   url_token = reverse('token_obtain_pair')

   def setUp(self):
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      # self.post = Post.objects.create(user=self.user, content='icerik', title='baslik')      
      self.test_jwt_auth()

   def test_jwt_auth(self):
      response = self.client.post(self.url_token, {"username": self.username, "password": self.password})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue("access" in json.loads(response.content))
      self.token = response.data["access"]

      # The credentials method can be used to set headers that will then be included on all subsequent requests by the test client.
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

   def test_create(self):
      data = {
         "title": "creating new post",
         "content": "post content",
      }
      response = self.client.post(self.url_create, data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_create_un_auth(self):
      self.client.credentials()
      data = {
         "title": "creating new post",
         "content": "post content",
      }
      response = self.client.post(self.url_create, data)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_list(self):
      self.test_create()
      response = self.client.get(self.url_list)
      self.assertEqual(response.status_code, status.HTTP_200_OK)




class PostUpdateDelete(APITestCase):
   url_token = reverse('token_obtain_pair')

   def setUp(self):
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      self.user2 = User.objects.create_user(username='chinaskitest', password='chinaskitest')
      self.post = Post.objects.create(user=self.user, content='icerik', title='baslik')
      self.url_update = reverse('post:update', kwargs={"slug": self.post.slug})
      self.url_delete = reverse('post:delete', kwargs={"slug": self.post.slug})
      self.test_jwt_auth()

   def test_jwt_auth(self, username='mustafatest', password='mustafatest'):
      response = self.client.post(self.url_token, {"username": username, "password": password})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue("access" in json.loads(response.content))
      self.token = response.data["access"]
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

   def test_delete(self):
      response = self.client.delete(self.url_delete)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_another_user(self):
      """baska bir kullanici baska bir kullanicinin postlarini silememeli"""

      self.test_jwt_auth(username='chinaskitest', password='chinaskitest') # baska bir kullanici ile giris yapilir
      response = self.client.delete(self.url_delete)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_update(self):
      data = {
         "title": "update title",
         "content": "update content",
      }
      response = self.client.put(self.url_update, data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue(Post.objects.get(id=self.post.id).content == data['content']) # content dogru kayit edilmis mi
   
   
   def test_update_another_user(self):
      """baska bir kullanici baska bir kullanicinin postlarini guncelleyememeli"""

      self.test_jwt_auth(username='chinaskitest', password='chinaskitest') # baska bir kullanici ile giris yapilir

      data = {
         "title": "update title",
         "content": "update content",
      }
      response = self.client.put(self.url_update, data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      self.assertFalse(Post.objects.get(id=self.post.id).content == data['content'])

   def test_update_unauth(self):
      """kullanici giris yapmamissa"""
      
      self.client.credentials()
      response = self.client.get(self.url_update)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_delete_unauth(self):
      """kullanici giris yapmamissa"""
      
      self.client.credentials()
      response = self.client.get(self.url_delete)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



      

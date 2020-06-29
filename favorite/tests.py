from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.utils import json
from post.models import Post
from favorite.models import Favorite


class FavoriteTestCase(APITestCase):
   url = reverse('favorite:list-create')
   url_token = reverse('token_obtain_pair')

   def setUp(self):
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      self.post = Post.objects.create(user=self.user, content='icerik', title='baslik')      
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
         "content": "conten is king",
         "user": self.user.id,
         "post": self.post.id
      }

      response = self.client.post(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_list(self):
      self.test_create()
      response = self.client.get(self.url)
      print(response.content)
      print(Favorite.objects.filter(user=self.user))
      # self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue(
         len(json.loads(response.content)["results"]) == Favorite.objects.filter(user=self.user).count()
      )





class FavoriteUpdateDelete(APITestCase):
   url_token = reverse('token_obtain_pair')

   def setUp(self):
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      self.user2 = User.objects.create_user(username='chinaskitest', password='chinaskitest')
      self.post = Post.objects.create(user=self.user, content='icerik', title='baslik')
      self.favorite = Favorite.objects.create(user=self.user, post=self.post, content='deneme')
      self.url = reverse('favorite:update-delete', kwargs={"pk": self.favorite.pk})
      self.test_jwt_auth()

   def test_jwt_auth(self, username='mustafatest', password='mustafatest'):
      response = self.client.post(self.url_token, {"username": username, "password": password})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue("access" in json.loads(response.content))
      self.token = response.data["access"]
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

   def test_delete(self):
      response = self.client.delete(self.url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # eger get ile bir deger dondurmezseniz 204 no content alirsiniz

   def test_delete_another_user_fav(self):
      """baska biri baska birinin favorilerini silememeli"""

      self.test_jwt_auth(username='chinaskitest', password='chinaskitest')
      response = self.client.delete(self.url)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
     

   def test_update(self):
      """update your favorite"""

      data = {
         "content": "new icerik"
      }
      response = self.client.put(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue(Favorite.objects.get(id=self.favorite.id).content == data['content'])


   def test_update_another_user(self):
      """baska bir kullanici baska bir kullanicinin favorilerinin guncelleyememeli"""

      self.test_jwt_auth(username='chinaskitest', password='chinaskitest')
      data = {
         "content": "new icerik asdf",
         "user": self.user2.id,
      }
      response = self.client.put(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_user_un_auth(self):
      self.client.credentials() # overwrites any existing credentials by calling the method with no arguments.
      response = self.client.get(self.url)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
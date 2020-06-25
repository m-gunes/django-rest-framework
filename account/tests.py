from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


"""
 1 Dogru veriler ile kayit islemi yap
 2 Sifre invalid olabilir
 3 kullanici adi zaten kullanilmis olabilir
 4 uye girisi yaptiysak register sayfasi gozukmemeli - session
 5 Token ile giris islemi yapildiginda 403 hatasi alinacak
"""

class UserTestCase(APITestCase):
   url = reverse('account:register')

   def test_create(self):
      """1 Dogru veriler ile kayit islemi"""

      data = {
         'username': 'testmustafa',
         'password': 'testmustafa'
      }
      response = self.client.post(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   
   def test_password(self):
      """2 invalid password"""

      data = {
         'username': 'testmustafa',
         'password': '1'
      }
      response = self.client.post(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      
      
   def test_username(self):
      """3 unique username"""

      self.test_create()

      data = {
         'username': 'testmustafa',
         'password': 'testmustafaaaaa'
      }
      response = self.client.post(self.url, data)
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


   def test_auth_session(self):
      """4 session ile giris yapmis kullanici registration sayfasini gorememeli. 403"""
      
      self.test_create() # uyeyi olusturduk
      self.client.login(username='testmustafa', password='testmustafa') # uye giris islemini yaptik
      response = self.client.get(self.url) # giris yaptiktan sonra get istegi yaptik
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # get isteginden sonra 403 forbidden alinmali


   def test_auth_token(self):
      """5 token ile giris yapmis kullanici registration sayfasini gorememeli. 403"""
      
      url_login = reverse('token_obtain_pair')
      self.test_create() # uyeyi olusturduk
      data = {
         'username': 'testmustafa',
         'password': 'testmustafa'
      }

      response = self.client.post(url_login, data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

      response_2 = self.client.get(self.url)
      self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)

      


      
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.utils import json


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

      


# token ile giris
class UserLogin(APITestCase):
   url = reverse('token_obtain_pair')

   # testler calismadan once calisan. constructor gibi
   def setUp(self): 
      # Setup run before every test method.
      # Every test needs access to the request factory.
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      # boylece test methodlarimiz calismadan kullanicimizi o metodlarda kullanmak uzere olusturmus oluyoruz

   def test_login(self):
      """Kullanici dogru bilgilerle giris yapiyor"""
      response = self.client.post(self.url, {'username': 'mustafatest', 'password': 'mustafatest'})
      # response = self.client.post(self.url, {'username': self.username, 'password': self.password}) # bu da oluyor. self ile yukarida tanimladigimiz degerlere(setUp()) erisebiliyoruz
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertTrue('access' in json.loads(response.content))
   
   def test_login_invalid(self):
      """Kullanici gecersiz bilgilerle login olmaya calisirsa"""
      response = self.client.post(self.url, {'username': 'salllamasyon', 'password': 'salllamasyon'})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_login_blank(self):
      """kullanici adinin ve sifrenin bos gonderilmesi durumu"""
      response = self.client.post(self.url, {'username': '', 'password': ''} )
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPasswordChange(APITestCase):
   url = reverse('account:update-password')
   url_token = reverse('token_obtain_pair')

   def setUp(self): 
      # Setup run before every test method.
      # Every test needs access to the request factory.
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      # boylece test methodlarimiz calismadan kullanicimizi o metodlarda kullanmak uzere olusturmus oluyoruz

   def login_with_token(self):
      """Kullanici dogru bilgilerle giris yapiyor"""
      response = self.client.post(self.url_token, {'username': 'mustafatest', 'password': 'mustafatest'})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

   def test_user_not_auth(self):
      """login olunmadan parola degistirilmek istendiginde http 401 alinmali"""
      response = self.client.get(self.url)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_change_pass(self):
      """sifre degistirme islemi"""
      self.login_with_token() # giris islemini yaptik
      response = self.client.put(self.url, {'old_password': 'mustafatest', 'new_password': 'mustafatest1'})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   
   def test_change_pass_invalid(self):
      """old_password yanlis girildiginde"""
      self.login_with_token() # giris islemini yaptik
      response = self.client.put(self.url, {'old_password': 'wrongpass', 'new_password': 'mustafatest1'})
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   def test_change_pass_blank(self):
      """bos gonderim yapildiginda"""
      self.login_with_token() # giris islemini yaptik
      response = self.client.put(self.url, {'old_password': '', 'new_password': ''})
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
      

class UserProfile(APITestCase):
   url = reverse('account:me')
   url_token = reverse('token_obtain_pair')
      
   def setUp(self): 
      # Setup run before every test method.
      # Every test needs access to the request factory.
      self.username = 'mustafatest'
      self.password = 'mustafatest'
      self.user = User.objects.create_user(username=self.username, password=self.password)
      # boylece test methodlarimiz calismadan kullanicimizi o metodlarda kullanmak uzere olusturmus oluyoruz

   def login_with_token(self):
      """Kullanici dogru bilgilerle giris yapiyor"""
      response = self.client.post(self.url_token, {'username': 'mustafatest', 'password': 'mustafatest'})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      token = response.data['access']
      self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
   
   def test_user_not_auth(self):
      """login olunmadan islem yapilmak istendiginde http 401 alinmali"""
      response = self.client.get(self.url)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_empty_info(self):
      self.login_with_token()
      data = {
            "first_name": "",
            "last_name": "",
            "profile": {
               "about": "",
               "twitter": ""
            }
         }
      response = self.client.put(self.url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


   def test_valid_info(self):
      self.login_with_token()
      data = {
            "id": "1",
            "first_name": "mustafa",
            "last_name": "gunes",
            "profile": {
                "id": "1",
               "about": "about me",
               "twitter": "asdf"
            }
         }
      response = self.client.put(self.url, data, format='json')
      print(response.data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

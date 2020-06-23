from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChangePasswordSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .permissions import NotAuthenticated

class ProfileAPIView(RetrieveUpdateAPIView):
   permission_classes = [IsAuthenticated]
   serializer_class = UserSerializer
   # queryset = User.objects.all()
   
   # sadece get_queryset ile filtreleme yapildiginda lookup_field eklenecek ve url ona gore duzenlenecek
   # Expected view ProfileAPIView to be called with a URL keyword argument named "pk". Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.
   def get_queryset(self):
      queryset = User.objects.filter(id=self.request.user.id)
      return queryset
   
   def get_object(self):
      queryset = self.get_queryset() # self.queryset diye direct'te yazilabilir
      obj = get_object_or_404(queryset)
      return obj
      
   # version 1 ---- get_object_or_404(queryset, id=self.request.user.id)
   # queryset = User.objects.all() 
   # def get_object(self):
   #    queryset = self.get_queryset() # self.queryset diye direct'te yazilabilir
   #    obj = get_object_or_404(queryset, id=self.request.user.id)
   #    return obj

   # version 2  ------ get_object_or_404(queryset)
   # burada queryset olarak tum user lar gelsin istemiyorum ve bir filterleme yapiyorum
   # def get_queryset(self):
   #    queryset = User.objects.filter(id=self.request.user.id)
   #    return queryset
   # get_object_or_404 icerisinde bir filtelemeye ihtiyac duymuyorum ve sadece queryset'i donduruyorum. 
   # eger bu alan olmazsa lookup_field olmali ve urlde pk olmali. 
   # def get_object(self):
   #    queryset = self.get_queryset() # self.queryset diye direct'te yazilabilir
   #    obj = get_object_or_404(queryset)
   #    return obj
   
      

# https://stackoverflow.com/a/38846554/7961551
class UpdatePassword(APIView):
   permission_classes = [IsAuthenticated]

   def get_object(self):
      return self.request.user

   def put(self, request):
      self.userInfos = self.get_object()
      serializer = ChangePasswordSerializer(data=request.data)

      if serializer.is_valid():
         old_pass = serializer.data.get('old_password')
         new_pass = serializer.data.get('new_password')
         if not self.userInfos.check_password(old_pass):
            return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
         self.userInfos.set_password(new_pass)
         self.userInfos.save()
         update_session_auth_hash(request, self.userInfos) # password guncellendikten sonra oturumun kapanmamasi icin
         response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
         }
         return Response(response)
      
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create user - Registration
class CreateUserView(CreateAPIView):
   serializer_class = RegisterSerializer
   permission_classes = [NotAuthenticated]
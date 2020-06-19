from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer

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
   
      


   # def perform_update(self, serializer):
   #    serializer.save(user=self.request.user)
      
   
      
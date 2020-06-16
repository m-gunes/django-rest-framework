from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from favorite.models import Favorite
from .serializers import FavoriteListCreateSerializer
from .permissions import isOwner
from .paginations import FavoritePagination


class FavoriteListCreateAPIView(ListCreateAPIView):
   queryset = Favorite.objects.all()
   serializer_class = FavoriteListCreateSerializer
   permission_classes = [IsAuthenticated, isOwner]
   pagination_class = FavoritePagination

   # istegi gonderen kisinin kendi favorilerini gosterir.
   def get_queryset(self):
      return Favorite.objects.filter(user=self.request.user)

   # istegi gonderen kisi kendi adina kaydetme islemi yapar. user'i baskasi secse bile durum degismez
   def perform_create(self, serializer):
      serializer.save(user=self.request.user)
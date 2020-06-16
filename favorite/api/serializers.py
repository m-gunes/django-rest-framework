from rest_framework import serializers
from favorite.models import Favorite


class FavoriteListCreateSerializer(serializers.ModelSerializer):
   class Meta:
      model = Favorite
      fields = '__all__'

   # Eger daha once favorilerine eklemissen tekrar ekleyememelisin
   def validate(self, attrs):
      queryset = Favorite.objects.filter(post=attrs['post'], user=attrs['user'])
      if queryset.exists():
         raise serializers.ValidationError('Already exist in your favorites')
      return attrs



class FavoriteAPISerializer(serializers.ModelSerializer):
   class Meta:
      model = Favorite
      fields = ('content',)
      
   
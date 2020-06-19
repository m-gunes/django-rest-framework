from rest_framework.serializers import ModelSerializer
from account.models import Profile
from django.contrib.auth.models import User



class ProfileSerializer(ModelSerializer):
   class Meta:
      model = Profile
      fields = ('id', 'about', 'twitter')


class UserSerializer(ModelSerializer):
   profile = ProfileSerializer()
   
   class Meta:
      model = User
      fields = ('id', 'first_name', 'last_name', 'profile')

   # ic ice (nested) serializer update yada save islemini serializer otamatik yapmaz
   # onun icin def update()
   # update() tam olarak anlasilmadi
   # https://www.django-rest-framework.org/api-guide/serializers/#handling-saving-related-instances-in-model-manager-classes
   def update(self, instance, validated_data):
      profile = validated_data.pop('profile') # dict olarak geliyor validated_data ve profile icinden cikarip profile degiskenine asign ediyoruz
      profile_serializer = ProfileSerializer(instance=instance.profile, data=profile)
      profile_serializer.is_valid(raise_exception=True)
      profile_serializer.save()
      return super(UserSerializer, self).update(instance, validated_data)
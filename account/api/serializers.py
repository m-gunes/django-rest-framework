from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from account.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password



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



class ChangePasswordSerializer(Serializer):
   old_password = serializers.CharField(required=True)
   new_password = serializers.CharField(required=True)

   class Meta:
      model = User

   def validate_new_password(self, value):
      validate_password(value) # girilen sifrenin guclu olup olmadigina bakiyoruz
      return value
      
   

class RegisterSerializer(ModelSerializer):
   password = serializers.CharField(write_only=True) # required=True

   class Meta:
      model = User
      fields = ('id', 'username', 'password')

   def validate(self, attrs):
      validate_password(attrs['password']) # girilen password guclu mu
      return attrs
   
   def create(self, validated_data):
      user = User.objects.create(
         username = validated_data['username']
      )
      user.set_password(validated_data['password'])
      user.save()
      return user

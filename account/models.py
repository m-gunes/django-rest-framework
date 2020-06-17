from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE) # Her kullanicinin bir profili olabilir => OneToOneField
   about = models.CharField(max_length=200)
   twitter = models.CharField(max_length=200)

   def __str__(self):
      return self.user.username
      


@receiver(post_save, sender=User) # User'a kayit islemi oldugunda
def create_user_profile(sender, instance, created, **kwargs):
   if created:
      Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
   instance.profile.save()
   
    
# her kullanici kaydi olusturuldugunda otamatik Profile kaydi olusturulmali.
# Bunun icin signals kullaniyoruz
# kayit isleminin yapilmasi icin post_save
# dispatch bu isin tetikleme kismi




# Another usage
# @receiver(post_save, sender=User) 
# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#       Profile.objects.create(user=instance)
#    instance.profile.save()
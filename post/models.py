from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


# Create your models here.
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True) # Automatically set the field to now every time the object is saved.
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created.
    modified_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user', blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_unique_slug(self):
        new_slug = slugify(self.title.replace('ı', 'i'))
        count = 1
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(new_slug, count)
            count += 1
        return new_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)
        # if not self.id:
        #     self.created_at = timezone.now()
        # self.updated_at = timezone.now()

    def __str__(self):
        return self.title


# auto_now=True
# auto_now_add=True
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#datefield

# slugify(' Joel is a slug ')
# 'joel-is-a-slug'

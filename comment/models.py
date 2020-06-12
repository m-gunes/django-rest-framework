from django.db import models
from django.contrib.auth.models import User
from post.models import Post


# Create your models here.
class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
   content = models.TextField(max_length=5000)
   parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering = ['-created_at']

   def __str__(self):
      return self.post.title + " " + self.user.username


   # bir yorumun altindaki yorumlari bulmayi saglayacak. Yani comment'e ait yorumlar
   def children(self):
      return Comment.objects.filter(parent=self)

   # asagidaki alani hic anlamadim
   @property
   def any_children(self):
      return Comment.objects.filter(parent=self).exists()
      
   
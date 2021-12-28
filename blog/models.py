from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.TextField()
    author=models.TextField()
    slug=models.TextField(max_length=500) 
    #image = models.ImageField(upload_to = 'thumbnail',default='thumbnail.jpg')
    timeStamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    likes = models.ManyToManyField(User,related_name='post_liked')

    def __str__(self):
        return str(self.sno)

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    
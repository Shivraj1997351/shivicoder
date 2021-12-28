from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email


class userdetail(models.Model):
     user_id = models.TextField()
     user = models.TextField()
     def __str__(self):
          return str(self.user_id)
  
class Privacy(models.Model):
     priv_id = models.AutoField(primary_key=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     status = models.CharField(max_length=30)
     def __str__(self):
          return str(self.user)

class requestuser(models.Model):
     req_id = models.AutoField(primary_key=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     req = models.CharField(max_length=100)
     status = models.CharField(max_length=30)
     def __str__(self):
          return str(self.req)
     
class View(models.Model):
     view_id = models.AutoField(primary_key=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     count = models.IntegerField()
     def __str__(self):
          return str(self.user)
     
class FollowersCount(models.Model):
     follower = models.CharField(max_length=100)
     user = models.CharField(max_length=100)
     def __str__(self):
          return self.user 

class Image(models.Model):
 user = models.CharField(max_length=200)
 photo = models.ImageField(upload_to='myimage',blank=True)
 def __str__(self):
         return self.user
    
class Bio(models.Model):
 user = models.CharField(max_length=100)
 bio = models.CharField(max_length=500,default='Hey I am using mini blog')
 def __str__(self):
        return self.user
 
 
class Trendingblogger(models.Model):
    trend_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=14)
    count = models.BigIntegerField()
    def __str__(self):
        return str(self.author)
   
class Review(models.Model):
     review_id = models.AutoField(primary_key=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     comment = models.CharField(max_length=500)
     rate = models.IntegerField(default=0)
     created_at = models.DateTimeField(auto_now_add=True)
     def __str__(self):
          return str(self.user)
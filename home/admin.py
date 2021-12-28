from django.contrib import admin
from .models import Contact, FollowersCount,Image,Trendingblogger,Bio,Review,View,Privacy,requestuser,userdetail

# Register your models here.
admin.site.register((Contact,FollowersCount,Image,Trendingblogger,Bio,Review,View,Privacy,requestuser,userdetail))

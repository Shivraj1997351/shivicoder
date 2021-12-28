from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('postCommentblog', views.postCommentblog, name="postCommentblog"),
    path('', views.blogHome, name="bloghome"),
    path('like',views.like),
    path('view/<int:id>',views.showblog, name="showblog"),
    path('view/edit/<int:id>', views.editblog, name="update"),
    path('view/delete',views.deleteblog),
]

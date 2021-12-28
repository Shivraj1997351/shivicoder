from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('search', views.search, name="search"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('loginpage', views.loginpage, name="loginpage"),
    path('signuppage',views.signup,name="signuppage"),
    path('messages',views.messages,name="messages"),
    path('favourites',views.favourites,name="favourites"),
    path('rateus',views.rateus,name="rateus"),
    path('editrateus',views.editrateus,name="editrateus"),
    path('profile', views.profile, name="profile"),
    path('profile/edit/<str:username>',views.editprofile,name="editprofile"),
    path('profile/editbio',views.updatebio,name="editbio"),
    path('profile/followers/<str:username>',views.showfollowers,name="showfollowers"),
    path('profile/followings/<str:username>',views.showfollowings,name="showfollowings"),
    path('profile/profilepic/<str:username>',views.uploadpic,name="profilepic"),
    path('profile/profilepic/edit/<str:username>',views.editpic,name="editprofilepic"),
    path('profile/profilepic/delete/<str:username>',views.deletepic,name="deleteprofilepic"),
    path('searchpeople/<str:username>', views.viewpeople, name="viewpeople"),
    path('searchpeople/followers/<str:username>',views.showfollowersuser,name="showfollowersuser"),
    path('searchpeople/followings/<str:username>',views.showfollowingsuser,name="showfollowingsuser"),
    path('followers_count',views.followers_count),
    path('privacy',views.privacy)
    #path('requestuser',views.Requestuser)
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

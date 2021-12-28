from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from home.models import Bio, Contact,FollowersCount,Image, Privacy, Review, Trendingblogger, View,requestuser, userdetail
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
from django.contrib.auth.hashers import make_password
from home.forms import ImageForm
from django.http import JsonResponse
from django.db.models import Q
import sweetify
from django.db.models import Avg


def home(request): 
    if request.user.username:
     view = View.objects.filter(user=request.user).first()
     if not view:
         sweetify.info(request, request.user.first_name,button='close', imageUrl="static/home/img/welcome.jpg", timer=5000)
         view = View(user=request.user,count=1)
         view.save()
         
    posts = Post.objects.filter(likes__gt=4).order_by('-timeStamp').distinct()
    allPosts = Post.objects.all().order_by('-timeStamp')[:24]
    ids1 = []
    for i in posts:
        ids1.append(i.author)
        
    Trendingbloger = Trendingblogger.objects.filter(count__gt=5)
    ids2 = []
    for i in Trendingbloger:
        ids2.append(i.author)
    users = User.objects.filter(username__in=ids2).exclude(username='admin')
    imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    suggestedbloggers = User.objects.filter(username__in=ids1).exclude(username='admin')
    
    
    rate = Review.objects.all().order_by('-created_at')[:5]
    if rate:
        total_review = len(Review.objects.all())
        avg_rate = Review.objects.all().aggregate(avg=Avg('rate'))
        context = {'posts':posts,'allPosts':allPosts,'users':users,'imgs':imgs,'suggestedbloggers':suggestedbloggers,'rates':rate,'avg_rate':avg_rate,'total_review':total_review}   
        return render(request,'home/home.html',context)
    
    
    context = {'posts':posts,'allPosts':allPosts,'users':users,'suggestedbloggers':suggestedbloggers,'imgs':imgs}
    return render(request, 'home/home.html',context)

@login_required(login_url='loginpage')
def messages(request):
    feedback =  Contact.objects.filter(name=request.user.username).order_by('-timeStamp')
    return render(request,'home/messages.html',{'feedback':feedback})

@login_required(login_url='loginpage')    
def rateus(request):
    if request.method=="POST":
        user = request.user
        comment = request.POST['comment']
        rate = request.POST['rate']
        review = Review(user=user,comment=comment,rate=rate)
        review.save()
        sweetify.info(request, 'Thanks for rating us :)',imageUrl='static/home/img/thankyou.gif', button='close', timer=4000)
    rate = Review.objects.filter(user=request.user)
    if rate:
      context = {'rate':str(rate[0].rate),'comment':rate[0].comment,'user':rate[0].user,'time':rate[0].created_at}   
      return render(request,'home/rateus.html',context)
    return render(request,'home/rateus.html')

@login_required(login_url='loginpage')        
def editrateus(request):
    if request.method=='POST':
        user = request.user
        comment = request.POST['comment']
        rate = request.POST['rate']
        review = Review.objects.get(user=user)
        review.comment = comment 
        review.rate = rate
        review.save()
        sweetify.info(request, 'Rating updated', icon='success',button='close', timer=2000)
        
    rate = Review.objects.filter(user=request.user)
    context = {'rate':str(rate[0].rate),'comment':rate[0].comment}
    return render(request,'home/editrateus.html',context)
    
@login_required(login_url='loginpage')
def contact(request):
    if request.method=="POST":
        name=request.user.username
        email=request.user.email
        phone=request.POST['phone']
        content=request.POST['content']   
        if len(phone) < 10 or len(phone) > 10:
           sweetify.warning(request, 'Invalid phone number :(', icon='warning', button='close', timer=2000) 
        else:
           contact=Contact(name=name, email=email, phone=phone, content=content)
           contact.save()  
           sweetify.info(request, 'Thanks for your suggestion:)', imageUrl="static/home/img/thankyou.gif", button='close', timer=4000)
            
    totalmails = len(Contact.objects.filter(name=request.user.username))        
    return render(request, "home/contact.html",{'totalmails':totalmails})        

@login_required(login_url='loginpage')
def profile(request):
    loginus = userdetail.objects.filter(user_id=request.user).first()
    if loginus is not None:
        user = request.user
        posts = Post.objects.filter(author=user).order_by('-timeStamp')
        user_followers = len(FollowersCount.objects.filter(user=user))
        user_following = len(FollowersCount.objects.filter(follower=user))
        bio = Bio.objects.filter(user=request.user.username)
        private_value = Privacy.objects.filter(user=user).first()
        imgcnt = len(Image.objects.filter(user=user))
        if imgcnt != 0:
         img = Image.objects.get(user=user)   
         if bio:
             biodata = bio[0].bio
             if private_value:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'img':img,'bio':biodata,'private_value':private_value.status}
             else:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'img':img,'bio':biodata}
         else:
             if private_value:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'img':img,'bio':'Hey I am using mini blog','private_value':private_value.status}
             else:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'img':img,'bio':'Hey I am using mini blog'}
        else:
         if bio:
             biodata = bio[0].bio
             if private_value:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'bio':biodata,'private_value':private_value.status}
             else:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'bio':biodata} 
         
         else:
             if private_value:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'bio':'Hey I am using mini blog','private_value':private_value.status}
             else:
              context = {'posts':posts,'user_followers':user_followers,'user_following':user_following,'bio':'Hey I am using mini blog'}
        return render(request, 'home/profile.html',context)    
    else:
        return redirect('/loginpage')
    
@login_required(login_url='loginpage')
def favourites(request):
    posts = Post.objects.all()
    return render(request,'home/favourites.html',{'posts':posts})
    
@login_required(login_url='loginpage')
def showfollowers(request,username):
    user_followerslist = FollowersCount.objects.filter(user=username)
    ids2 = []
    for i in user_followerslist:
        ids2.append(i.follower)
    imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    context = {'user_followerslist':user_followerslist,'imgs':imgs}
    return render(request,'home/showfollowers.html',context)

@login_required(login_url='loginpage')
def showfollowings(request,username):
    user_followinglist = FollowersCount.objects.filter(follower=username)
    ids2 = []
    for i in user_followinglist:
        ids2.append(i.user)
    imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    context = {'user_followinglist':user_followinglist,'imgs':imgs}
    return render(request,'home/showfollowings.html',context)

@login_required(login_url='loginpage')
def showfollowersuser(request,username):
    user_followerslist = FollowersCount.objects.filter(user=username)
    ids2 = []
    for i in user_followerslist:
        ids2.append(i.follower)
    imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    context = {'user_followerslist':user_followerslist,'imgs':imgs}
    return render(request,'home/showfollowers.html',context)

@login_required(login_url='loginpage')
def showfollowingsuser(request,username):
    user_followinglist = FollowersCount.objects.filter(follower=username)
    ids2 = []
    for i in user_followinglist:
        ids2.append(i.user)
    imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    context = {'user_followinglist':user_followinglist,'imgs':imgs}
    return render(request,'home/showfollowings.html',context)

@login_required(login_url='loginpage')
def editprofile(request,username):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        user = User.objects.get(username=username)
        user.first_name = fname
        user.last_name = lname
        user.save()
        sweetify.info(request, 'Profile updated', icon='success',button='close', timer=2000)
        return redirect('/profile')
    else:
        user = User.objects.get(username=username)  
        uname = user.username
        fname = user.first_name
        lname = user.last_name
        email = user.email
        context = {'fname':fname,'lname':lname,'uname':uname,'email':email}  
        return render(request,'home/editprofile.html',context)

@login_required(login_url='loginpage')
def updatebio(request):
    if request.method == "POST":
        bio = request.POST.get('bio')
        user = request.user.username 
        oldbio = Bio.objects.filter(user=user)
        oldbio.delete()
        biodata = Bio(bio=bio,user=user)
        biodata.save()
        sweetify.info(request, 'Bio updated', icon='success',button='close', timer=2000)
        return redirect('/profile/editbio')
        
    else:
        biodata = Bio.objects.filter(user=request.user.username)
        if biodata:
            context = {'bio':biodata[0].bio}
        else:
            context = {'bio':'Hey I am using mini blog'}
    return render(request,'home/editbio.html',context)   
    
            

@login_required(login_url='loginpage')    
def uploadpic(request,username):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.POST['user']
            img = form.cleaned_data.get("profilepic")
            obj = Image.objects.create(user=user,photo=img)
            obj.save()
            sweetify.info(request, 'Profile pic uploaded', icon='success',button='close', timer=3000)
           
    else:
        form = ImageForm()
    context = {'form':form}
    return render(request,'home/profilepic.html',context)

@login_required(login_url='loginpage')    
def editpic(request,username):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.POST['user']
            img = form.cleaned_data.get("profilepic")
            img1 = Image.objects.get(user=user)
            img1.photo.delete()
            img1.delete()
            obj = Image.objects.create(user=user,photo=img)
            obj.save()
            sweetify.info(request, 'Profile pic updated', icon='success',button='close', timer=3000)
            
    else:
        form = ImageForm()
    context = {'form':form}
    return render(request,'home/profilepic.html',context)


@login_required(login_url='loginpage')   
def deletepic(request,username):
    user =  username 
    img = Image.objects.get(user=user)
    img.photo.delete()
    img.delete()
    return redirect('/profile')


@login_required(login_url='loginpage')
def viewpeople(request,username):
        if username != request.user.username:
            trend = Trendingblogger.objects.filter(author=username).first()
            if trend:
                trend.count+=1
                trend.save()
            else:
                trends = Trendingblogger.objects.create(author=username,count=1)
                trends.save()
            person = User.objects.get(username=username)
            private_value = Privacy.objects.filter(user=person).first()
            posts = Post.objects.filter(author=username)
            user_followers = len(FollowersCount.objects.filter(user=username))
            user_following = len(FollowersCount.objects.filter(follower=username))
            user_followers0 = FollowersCount.objects.filter(user=username)
            imgcnt = len(Image.objects.filter(user=username))   
            user_followers1 = []
            for i in user_followers0:
                j = i.follower
                user_followers1.append(j)
            if request.user.username in user_followers1:
                follow_button_value = 'unfollow'
                access_profile_value = 'true'
            else:
                follow_button_value = 'follow'
                access_profile_value = 'false'
            if imgcnt != 0:
             img = Image.objects.get(user=username)   
             bio = Bio.objects.filter(user=username) 
             if bio:    
               if private_value:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'img':img,
                            'bio':bio[0].bio,
                            'private_value':private_value.status,
                            'access_profile_value':access_profile_value
                            }
               else:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'img':img,
                            'bio':bio[0].bio
                            }   
             else:
              if private_value:   
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'img':img,
                            'bio':'Hey I am using mini blog',
                            'private_value':private_value.status,
                            'access_profile_value':access_profile_value
                }
              
              else:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'img':img,
                            'bio':'Hey I am using mini blog'
                }    
            else:
             bio = Bio.objects.filter(user=username) 
             if bio:    
               if private_value:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'bio':bio[0].bio,
                            'private_value':private_value.status,
                            'access_profile_value':access_profile_value
                            }
               else:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'bio':bio[0].bio
                            }   
             else:
              if private_value:   
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'bio':'Hey I am using mini blog',
                            'private_value':private_value.status,
                            'access_profile_value':access_profile_value
                }
              else:
                context = {
                            'person':person,
                            'posts':posts,
                            'user_followers':user_followers,
                            'user_following':user_following,
                            'follow_button_value':follow_button_value,
                            'bio':'Hey I am using mini blog'
                }
                 
            return render(request, 'home/viewprofile.html',context)
        else:
            return redirect('profile')
    
@login_required(login_url='loginpage')
def followers_count(request):
    if request.method == 'GET':
        value = request.GET['value']
        user = request.GET['user']
        follower = request.GET['follower']
        if value == 'Follow':
            followers_cnt = FollowersCount.objects.create(follower=follower,user=user)
            followers_cnt.save()
            fmsg = 'UnFollow'
            followcount = FollowersCount.objects.filter(user=user).count()
            followingcount = FollowersCount.objects.filter(follower=user).count()
            data = {
                'fmsg':fmsg,
                'fcount':followcount,
                'fcount1':followingcount
            }
        else:
            followers_cnt = FollowersCount.objects.filter(follower=follower,user=user).first()
            followers_cnt.delete()
            fmsg = 'Follow'
            followcount = FollowersCount.objects.filter(user=user).count()
            followingcount = FollowersCount.objects.filter(follower=user).count()
            data = {
                'fmsg':fmsg,
                'fcount':followcount,
                'fcount1':followingcount
            }
        return JsonResponse(data)
    
@login_required(login_url='loginpage')
def privacy(request):
    if request.method == 'GET':
        value = request.GET['value']
        user = request.user
        if value == 'make private':
            followers_cnt = Privacy.objects.create(user=user,status='make public')
            followers_cnt.save()
            fmsg = 'make public'
            data = {
                'fmsg':fmsg
            }
        else:
            followers_cnt = Privacy.objects.filter(user=user).first()
            followers_cnt.delete()
            fmsg = 'make private'
            data = {
                'fmsg':fmsg
            }
        return JsonResponse(data)
'''   
@login_required(login_url='loginpage')
def Requestuser(request):
    if request.method == 'GET':
        value = request.GET['value']
        user = request.GET['user']
        uservalue = User.objects.get(username=user)
        if value == 'Follow request':
            followers_cnt = requestuser.objects.create(user=uservalue,req=request.user.username,status='pending')
            followers_cnt.save()
            fmsg = 'Cancel Follow request'
            data = {
                'fmsg':fmsg
            }
        else:
            followers_cnt = requestuser.objects.filter(user=uservalue,req=request.user.username).first()
            followers_cnt.delete()
            fmsg = 'Follow request'
            data = {
                'fmsg':fmsg
            }
        return JsonResponse(data)
'''
def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsdesc = Post.objects.filter(slug__icontains=query)
        allPosts=  allPostsTitle.union(allPostsAuthor,allPostsdesc)
        users = User.objects.filter(username__icontains=query).exclude(username='admin')
        ids2 = []
        for i in users:
            ids2.append(i.username)
        imgs = Image.objects.filter(user__in=ids2).exclude(user='admin')
    params={'allPosts': allPosts, 'users':users, 'query': query,'imgs':imgs}
    return render(request, 'home/search.html', params)

    
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        uname = User.objects.filter(username=username)
        em = User.objects.filter(email=email)
        # check for errorneous input
        if uname:
            sweetify.warning(request,'Username should be unique',icon='warning',button='close',timer=2000)
            
        elif em:
            sweetify.warning(request,'email should be unique',icon='warning',button='close',timer=2000)
        
        elif len(pass1)<8:
            sweetify.warning(request,'Password length should be atleast 8',icon='warning',button='close',timer=2000)
                
        elif (pass1!= pass2):
            sweetify.warning(request,'Password do not match',icon='warning',button='close',timer=2000)
        
        else:
         myuser = User.objects.create_user(username, email, pass1)
         myuser.first_name= fname
         myuser.last_name= lname
         myuser.save()
         sweetify.success(request, 'Account created successfully', icon='success',button='close', timer=3000)
        return redirect('home')

    

def signup(request):
 if request.method=="POST":
    username=request.POST['username']
    email=request.POST['email']
    fname=request.POST['fname']
    lname=request.POST['lname']
    pass1=request.POST['pass1']
    pass2=request.POST['pass2']
    uname = User.objects.filter(username=username)
    em = User.objects.filter(email=email)
    
    if uname:
            sweetify.warning(request,'Username should be unique',icon='warning',button='close',timer=2000)
            return redirect('home')
    elif em:
            sweetify.warning(request,'email should be unique',icon='warning',button='close',timer=2000)
            return redirect('home')
    elif len(pass1)<8:
            sweetify.warning(request,'Password length should be atleast 8',icon='warning',button='close',timer=2000)
            return redirect('home')   
    elif (pass1!= pass2):
            sweetify.warning(request,'Password do not match',icon='warning',button='close',timer=2000)
            return redirect('home')
    else:
         myuser = User.objects.create_user(username, email, pass1)
         myuser.first_name= fname
         myuser.last_name= lname
         myuser.save()
         sweetify.success(request, 'Account created successfully', icon='success',button='close', timer=3000)
 
         return redirect('home')

 else:
   return render(request,'home/signup.html')
 
 

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            #hashpassword = make_password(loginpassword)
            hashusername = make_password(loginusername)
            #response.set_cookie('loginusername',hashusername,max_age=365 * 24 * 60 * 60)
            #response.set_cookie('loginpassword',hashpassword,max_age=365 * 24 * 60 * 60)
            userdata = userdetail(user=hashusername,user_id=loginusername) 
            userdata.save()
            return redirect("home")
        else:
            sweetify.warning(request, "Invalid credentials! Please try again",icon='warning',button='close',timer=2000)
            return redirect("home")


def loginpage(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            hashusername = make_password(loginusername)
            if 'next' in request.POST:
                #response.set_cookie('loginusername',hashusername,max_age=365 * 24 * 60 * 60)
                #response.set_cookie('loginpassword',hashpassword,max_age=365 * 24 * 60 * 60)
                userdata = userdetail(user=hashusername,user_id=loginusername) 
                userdata.save()
                return redirect(request.POST.get('next'))
            else:
                #response.set_cookie('loginusername',hashusername,max_age=365 * 24 * 60 * 60)
                #response.set_cookie('loginpassword',hashpassword,max_age=365 * 24 * 60 * 60)
                userdata = userdetail(user=hashusername,user_id=loginusername) 
                userdata.save()
                return  redirect('home')
        else:
            sweetify.warning(request, "Invalid credentials! Please try again",icon='warning',button='close',timer=2000)
            return redirect("home")

    return render(request,'home/loginpage.html')
   

def handelLogout(request):
    view = View.objects.get(user=request.user)
    view.delete()
    userdata = userdetail.objects.filter(user_id=request.user.username).first()
    userdata.delete()
    logout(request)
    response = redirect('/loginpage')
    #response.delete_cookie('loginusername')
    #response.delete_cookie('loginpassword')
    if request.COOKIES.get('postid'):
       response.delete_cookie('postid')
    return response






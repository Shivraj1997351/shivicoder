from django.http.response import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from django.contrib.auth.decorators import login_required
from home.models import FollowersCount
from django.db.models import Q
import sweetify
from django.contrib.auth.models import User 
# Create your views here.
@login_required(login_url='loginpage')
def blogHome(request): 
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.user
        slug = request.POST.get('slug')
        content = request.POST.get('blog')
        post = Post(title=title, author=author, slug=slug, content=content)
        post.save()
        sweetify.success(request,'Blog posted',icon='success',button='close',timer=2000)
        return redirect('/blog/')
    
               
    user  = FollowersCount.objects.filter(follower=request.user)    #users followed by current user
    userlen = len(user)
         
    if userlen == 0:                                               # no followed users
        if request.COOKIES.get('postid'):                          #cookie for browse post
            postid = request.COOKIES.get('postid')                 #postid in cookie of post
            post3 = Post.objects.filter(sno=postid).first()                   #get post using postid
            if post3:
                post4 = Post.objects.filter(author=post3.author).order_by('-timeStamp')  #all post by author of cookie post 
                post7 = list(post4)
                post5 = Post.objects.all()                             #all post
                result = list(post7)
                result.extend(y for y in post5 if y not in result)     #all post excluding common post
                context = {'allPosts': result} 
            post5 = Post.objects.all().order_by('-timeStamp')[:15] # if no cookie then 15 post
            context = {'allPosts': post5}
        else:
            post5 = Post.objects.all().order_by('-timeStamp')[:15] # if no cookie then 15 post
            context = {'allPosts': post5}
              
                
    else:    
        allPost = []
        for i in user:
         j = Post.objects.filter(author=i).order_by('-timeStamp')   #post by followed users
        for k in j:
         allPost.append(k)                                          #all post in a list 
        # if followed users are present
        if request.COOKIES.get('postid'):                          # cookie for browse post
            postid = request.COOKIES.get('postid')                 #postid in cookie of post
            post3 = Post.objects.filter(sno=postid).first()                   #get post using postid
            if post3:
                post4 = Post.objects.filter(author=post3.author).order_by('-timeStamp')  #all post by author of cookie post
                post6 = list(post4)
                result = list(allPost)                                 #all post
                result.extend(y for y in post6 if y not in result)     #all post excluding common post
                context = {'allPosts': result} 
            post5 = Post.objects.all().order_by('-timeStamp')[:15] # if no cookie then 15 post
            context = {'allPosts': post5}
        else:
            post5 = Post.objects.all().order_by('-timeStamp')[:15]
            post8 = list(post5)
            result = list(allPost)
            result.extend(y for y in post8 if y not in result)
            context = {'allPosts': result}
    return render(request, "blog/blogHome.html",context)

@login_required(login_url='loginpage')
def showblog(request, id): 
    post=Post.objects.filter(sno=id).first()
    if post:
        comments = BlogComment.objects.filter(post=post, parent=None).order_by('-timestamp')
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        totalcomments = comments.all().count() + replies.all().count()   
        context={'post':post, 'comments': comments, 'totalcomments':totalcomments, 'user': request.user, 'replyDict': replyDict}
        response = render(request, "blog/showblog.html", context)
        response.set_cookie('postid',id,max_age=3*24*60*60)
        return response
    return render(request,'blog/showblog.html')

@login_required(login_url='loginpage')
def editblog(request, id):
    if request.method == "POST":
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('blog')
        post = Post.objects.get(sno=id)
        post.title = title
        post.slug = slug
        post.content = content
        post.save()
        sweetify.success(request,'Blog updated',icon='success',button='close',timer=2000)
        return redirect('/profile')
        #return redirect('/blog/view/edit/'+str(id))
    else:
        post = Post.objects.get(sno=id)  
        title = post.title
        slug = post.slug
        content = post.content
        context = {'title':title,'slug':slug,'content':content}  
    return render(request,'blog/editblog.html',context)

@login_required(login_url='loginpage')
def deleteblog(request):
    if request.method == 'GET':
        sno = request.GET['post_id']
        post = Post.objects.get(sno=sno)
        if request.COOKIES.get('postid'):
            postid = request.COOKIES.get('postid')
            if str(post.sno) == str(postid):
                data = {'fmsg':'deleted'}
                response = JsonResponse(data)
                response.delete_cookie('postid')
                post.delete()
                return response
            else:    
                post.delete()
                data = {'fmsg':'deleted'}
                return JsonResponse(data)
        else:
            post.delete()
            data = {'fmsg':'deleted'}
            return JsonResponse(data)
    
@login_required(login_url='loginpage')
def postCommentblog(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
                    
    return redirect(f"/blog/view/{post.sno}")

@login_required(login_url='loginpage')    
def like(request):
 user = request.user
 if request.method == 'GET':
  post_id = request.GET['value']
  get_video = get_object_or_404(Post,sno=post_id)
  if user in get_video.likes.all():
   get_video.likes.remove(user)
   fcount = get_video.likes.count()
   data = {
                'fmsg':'far fa-heart',
                'css':'black',
                'message':'Removed from favourites',
                'fcount':fcount
            }
  else:
   get_video.likes.add(user)
   fcount = get_video.likes.count()
   data = {
                'fmsg':'fas fa-heart',
                'css':'red',
                'message':'Added to favourites',
                'fcount':fcount
            }

  return JsonResponse(data)


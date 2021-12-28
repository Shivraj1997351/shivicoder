from django import forms
from blog.models import Post
class ImageForm(forms.Form):
  profilepic = forms.ImageField()

  

  
  
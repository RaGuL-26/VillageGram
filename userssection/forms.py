# forms.py
from django import forms
from .models import AboutOfUsers
from .models import *

class AboutForm(forms.ModelForm):
    class Meta:
        model = AboutOfUsers
        fields = ['about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'parent': forms.HiddenInput()
        }

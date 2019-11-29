from django import forms
from .models import Post, Comment, UserProfileInfo
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

     # email = forms.EmailField(label='Your email',max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))  # inline widget

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())   # vezi si L3/forms, am setat un widget html pt prezentare

    class Meta():
        model = User                                # User model https://docs.djangoproject.com/en/2.2/ref/contrib/auth/  raw pwds are not accepted
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
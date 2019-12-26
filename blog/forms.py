from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

'''
Widgeturile sunt legate de clase CSS/Bootstrap

'''   

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  

    class Meta():
        model = User                                # User model https://docs.djangoproject.com/en/2.2/ref/contrib/auth/  raw pwds are not accepted
        fields = ('username','email','password')
           
'''
# Widgets:

class SignupFormName(forms.ModelForm):   
    first_name = forms.CharField(label='Your name',max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))  
    last_name = forms.CharField(label='Last name',max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your email',max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    verify_email = forms.EmailField (label='Re-enter you email',max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))

 
    def clean(self):  # most used!!!
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        
        
        if email != vmail:
            raise forms.ValidationError("MAKE SURE EMAILS MATCH!")
        

    class Meta:
        model= User
        fields=('first_name','last_name','email')              



Poti seta si valorile default HTML (SimplesocialProject):
e.g <input type="email" name="useremail" value="Email here">


class UserCreateForm(UserCreationForm):
    
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

                                                                                           
'''    









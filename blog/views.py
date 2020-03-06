from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, UserForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User as User


class PostListView(ListView):              # Template default suffix is _list (post_list.html)
    model = Post                            
          
                   
# ListViews will populate the result from get_queryset() to populate the template context. 
# Model Post will have a context object post_list (in HTML)

'''    
Se poate scrie si asa:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return context
        
# Poti face filtrare si in HTML la rezultatele deja intoarse de view
'''

class PostDetailView(DetailView):                # Template default suffix is _detail.
    #template_name='blog/post_detail.html'
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):  # Template default suffix is '_form'
    #template_name='blog/post_form.html'
    form_class = PostForm
    model = Post
    #success_url = reverse_lazy('post_list')
    

# Fara LoginRequiredMixin oricine poate vedea pagina dc are linkul!

class PostUpdateView(LoginRequiredMixin,UpdateView):  # Template default suffix is '_form'
    #template_name='blog/post_form.html' 
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):  # Template default suffix is '_confirm_delete'
    #template_name='blog/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):      # Default suffix is _list.
    template_name='blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

class AboutView(TemplateView):
    template_name = 'blog/about.html'


#######################################
# PK-ul este argument ce vine cu requestul
 
# get_object_or_404()
# Calls get() on a given model manager, but it raises Http404 instead of the model's DoesNotExist exception.
 #######################################


@login_required
def post_publish(request, pk):                    # does not have a render function, just does what is requested
    post = get_object_or_404(Post, pk=pk)   # Post model   
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def comment_approve(request, pk):                  # does not have a render function, just does what is requested
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)  # FK la Post

@login_required
def comment_remove(request, pk):                   # does not have a render function, just does what is requested 
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk   # salveaza post PK  pt a putea returna postul mai jos dupa stergerea commentului
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   # the first save just saves the results of the form to that variable 
            comment.post = post                 # leaga commentul de post prin FK (vezi modelul comment, are coloana post)! Comment.post= titlul luat mai sus (are pk-ul din get_object_or_404)
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid() :
            user = user_form.save()             #the first save just saves the results of the form to that variable user
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            print(user_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    return render(request,'blog/registration.html', {'user_form':user_form,'registered':registered})

def logare(request):  # Formul e in login.html

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function (user gets authenticated at this step/ login is not done yet!!!)
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return redirect('post_list')
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else: # authenticate is false, wrong user and/or password
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'blog/logare.html', {})
    

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect('post_list')













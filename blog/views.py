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
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Extra Imports for the Login and Logout Capabilities


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):              # Template default suffix is _list
    #template_name='blog/post_list.html'   
    model = Post                           # You can avoid context_object_name too. The default behaviour of ListView is to populate the template with context name object_list (vezi get_context_object_name)             
 
 # Obiectele Post sunt intoarse in pagina impreuna cu PK-ul lor
     
    def get_queryset(self):                # Get the list of items for this view. This must be an iterable and may be a queryset (in which queryset-specific behavior will be enabled).
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

'''    
Se poate scrie si asa:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return context
        
# get_context_object_name(object_list) Return the context variable name that will be used to contain the list of data that this view is manipulating. If object_list is a queryset of Django objects 
and context_object_name is not set, the context name will be the model_name of the model that the queryset is composed from, with postfix '_list' appended. 
For example, the model Article would have a context object named article_list. => Cum metoda vezi post_list in HTML
'''
   
# Poti face filtrare si in HTML la rezultatele deja intoarse de view
    
class PostDetailView(DetailView):                # Template default suffix is _detail.
    #template_name='blog/post_detail.html'
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):  # Template default suffix is '_form'
    #template_name='blog/post_form.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post.html'

    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):  # Template default suffix is '_form'
    #template_name='blog/post_form.html' 
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):  # Template default suffix is '_confirm_delete'
    #template_name='blog/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):      # Default suffix is _list.
    template_name='blog/post_draft_list.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')



#######################################
## Functions that require a pk match ##
#######################################

# PK-ul este argument ce vine cu requestul
 
 
# get_object_or_404()
# Calls get() on a given model manager, but it raises Http404 instead of the model's DoesNotExist exception.
 
@login_required
def post_publish(request, pk):                    # does not have a render function, just does what is requested
    post = get_object_or_404(Post, pk=pk)   # POst model   
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
    post_pk = comment.post.pk   # salveaza post PK  pt a putea returna postul mia jos dupa stergerea commentului
    comment.delete()
    return redirect('post_detail', pk=post_pk)

##@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   # commentul nu e salvat
            comment.post = post                 # leaga commentul de post (vezi modelul comment, are fk la post)!!!!!
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})






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
    















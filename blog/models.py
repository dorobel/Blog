from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)  # FK spre modelul auth.User (autentificarea userilor in admin) 
    title = models.CharField(max_length=200)                          # FK-ul este cel ce  umple capul Author cu valori selectabile la crearea unui nou post
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    #comments este "related_name-ul" de mai jos
    # Poti folosi post.comments.all pt a afisa toate commenturile unui post (vezsi post_detail.html)
    # In oracle un astfel de select ar fi :
    #  select d.departments from employees e join departments d where e.name='John'
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):  # afiseaza lista de commentarii aprobate -- filter |  vezi post_list_html 
        return self.comments.filter(approved_comment=True) # poti folosi self.comments deoarece Comment are FK in Post iar comments este "related_name-ul" de mai jos!
                                                           # In oracle un astfel de select ar fi :
                                                           #  select d.departments from employees e join departments d where e.name='John'  
                                                           
    def get_absolute_url(self):                    
        return reverse("post_detail",kwargs={'pk':self.pk})  # Dupa ce creezi un post se intoarce pe post_detail
    # creare post: reverse face redirect dupa ce ai salvat formul (doar dupa salvarea formului un post are pk)
    # list posturi: nu ai neparat nevoie de post_detail pt ca e inclus in href="{% url 'post_detail' pk=post.pk %} doar pk-ul este intors (pk=post.pk)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)  # related_name -- vezi mai sus! Fk catre POst (din ce vad in admin se duce la titlu)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

  #  def get_absolute_url(self):
  #      return reverse("post_list")

    def __str__(self):
        return self.text









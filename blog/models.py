from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)  # FK spre modelul auth.User (autentificarea userilor in admin) # FK-ul este cel ce  umple capul Authod cu valori selectabile
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):  #afiseaza lista de commentarii aprobate
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})  # Dupa ce creezi un post se intoarce pe pagina asta
    # Spre deosebire de expl cu scoala, aici trebuie sa pui linkul de redirect (post_detail); si asta pt ca atunci cand salvezi formul trebuie sa intoarca pk-ul
    # postului care nu e valabil decat dupa SAVE!

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)  #Fk catre POst
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text









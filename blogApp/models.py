from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class blogPost(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
    def __str__(self) -> str:
        return self.title
    
    def like_list(self):
        return self.likes
    
    def like_count(self):
        return self.likes.count()

class postComment(models.Model):
    post = models.ForeignKey(blogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-created_at']
    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk':self.pk})
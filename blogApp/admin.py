from django.contrib import admin
from .models import blogPost, postComment, User
# Register your models here.


admin.site.register(blogPost)
admin.site.register(postComment)

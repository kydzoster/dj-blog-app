from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # post title field
    title = models.CharField(max_length=250)
    # this field is used in URL
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    # when the post was published
    publish = models.DateTimeField(default=timezone.now)
    # when the post was created
    created = models.DateTimeField(auto_now_add=True)
    # last time the post was updated
    updated = models.DateTimeField(auto_now=True)
    # status of the post
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # sort by publish field in descending order, most recent posts will be shown first
        ordering = ('-publish',)

    def __str__(self):
        return self.title

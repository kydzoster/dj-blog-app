from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


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

    # Default manager, if not added it wont be created, this is optional
    objects = models.Manager()
    # custom manager
    published = PublishedManager()

    class Meta:
        # sort by publish field in descending order, most recent posts will be shown first
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
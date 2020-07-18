from django import template
from django.db.models import Count
from ..models import Post


register = template.Library()

# returns total number of posts published so far
@register.simple_tag
def total_posts():
    return Post.published.count()

# displays latest posts as titles
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# displays the most commented post
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

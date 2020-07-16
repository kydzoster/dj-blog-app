from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


def post_share(request, post_id):
    # retrieve post by id and its status must be published
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form was submitted and needs to be processed
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form field passes validation
            cd = form.cleaned_data
            # sends email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_email@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_list(request):
    object_list = Post.published.all()
    # 3 posts in each page
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    # use a specific query set instead of retrieving all objects
    queryset = Post.published.all()
    # use the context variable posts for the query results
    context_object_name = 'posts'
    # paginate the result displaying 3 objects per page
    paginate_by = 3
    # use the custom template to render the page
    template_name = 'blog/post/list.html'
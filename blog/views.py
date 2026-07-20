from django.shortcuts import render
from .models import Post
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

def post_list(request):
   
    #template context processors
    posts = Post.published.all()

    #pagination with 3 posts per page
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page',1)
    posts = paginator.page(page_number)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except: 
    #     Post.DoesNotExist
    #     raise Http404("No Post Found")
    
    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year =year,
                             publish__month =month,
                             publish__day =day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})


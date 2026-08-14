from django.shortcuts import render
from .models import Post
from comments.models import Comment
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm, SearchForm
from comments.forms import CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST

from taggit.models import Tag
from django.db.models import Count

from django.contrib.postgres.search import SearchVector,\
                                            SearchQuery, SearchRank, \
                                           TrigramSimilarity

from django.contrib.auth import login
from .forms import SignUpForm 

from django.contrib.auth.decorators import login_required
from .forms import PostForm

from django.utils.text import slugify

from django.db.models import Q
 

# class PostListView(ListView):

#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


#function based view for post_list

def post_list(request, tag_slug = None):
    query = request.GET.get('query')
    #template context processors
    posts = Post.published.all()
    tag = None

    if query:
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        posts = posts.annotate(
            rank=SearchRank(search_vector, search_query),
            similarity=TrigramSimilarity('title', query),
        ).filter(
            Q(rank__gte=0.1) | Q(similarity__gte=0.1)
        ).order_by('-rank', '-similarity')
    elif tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    #pagination with 3 posts per page
    paginator = Paginator(posts,6)
    page_number = request.GET.get('page',1)
    #empty page error handled
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #if page_number is not an integer then deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag':tag})
    
    
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
    #List of active comments for this post
    comments = post.comments.filter (active = True)
    #Form for users to comment
    form = CommentForm()

    #List of similar posts
    post_tags_id = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_id)\
                        .exclude(id= post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
                        .order_by('-same_tags','-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                   'comments': comments,
                   'form': form,
                   'similar posts': similar_posts})

def post_share(request, post_id):
    #rertieve post by id
    post=get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}'s. comments:{cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            sent = True
            
            # send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form':form, 'sent' : sent})

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,id = post_id, status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #Create a comment object without saving it to the database
        comment = form.save(commit = False)
        #Assign the post to the comment
        comment.post= post
        #Save the comment to the database
        comment.save()
        return render(request, 'blog/post/comment.html', {
            'post':post,
            'form':form,
            'comment': comment
        })

'''
#search filter using postgres
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight = 'A') + \
                            SearchVector('body', weight = 'B')
            search_query = SearchQuery(query,)
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gte = 0.1).order_by('-similarity')

    return render (request,
                   'blog/post/search.html',
                   {'form': form,
                    'query': query,
                    'results': results})
'''

#signup function
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

#for creating posts
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()  # saves the tags
            if post.status == Post.Status.PUBLISHED:
                return redirect(post.get_absolute_url())
            return redirect('blog:my_posts')
    else:
        form = PostForm()
    return render(request, 'blog/post/form.html', {'form': form})

#for editing the posts
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Only the author can edit their own post
    if post.author != request.user:
        raise Http404("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post/form.html', {'form': form, 'post': post})

#deleting the post
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise Http404("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post/delete_confirm.html', {'post': post})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-publish')
    return render(request, 'blog/post/my_posts.html', {'posts': posts})


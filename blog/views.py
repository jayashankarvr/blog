from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Tutorial, Message, Comment
from .forms import MessageForm, CommentForm


def homepage(request):
    '''
    blog home page with the latest 6 posts and categories
    Args:
        object: request
    Returns:
        list: latest posts
        list: blog categories
    '''
    categories = Category.objects.all()
    latest_items = Tutorial.objects.all().order_by('-updated_at')[:6]
    context = {
        'latest_items': latest_items, 
        'categories': categories}
    return render(request, 'home.html',context=context)


def blog_post(request, post_id):
    '''
    get post by id
    Args:
        object: request
        int: post id
    Returns:
        object: post

    TODO: handel unfound post
    '''
    categories = Category.objects.all()
    # TODO: raise an error when there is no post id
    tutorial = Tutorial.objects.get(pk=post_id)
    # comments related to post
    post_comments = Comment.objects.filter(tutorial__pk=tutorial.pk).all() 
    form = CommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('blog:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            print(request.user)
            comment = Comment(
                content=form.cleaned_data["comment"],
                tutorial=tutorial,
                user=request.user
            )
            comment.save()
            tutorial.commented()
            return redirect('blog:post', post_id=tutorial.pk)
    context = {'tutorial': tutorial, 
               'categories': categories,
               'form': form, 
               'comments':post_comments
               }
    return render(request, 'post.html', context=context)


def category_posts(request, slug):
    '''
    get posts related to category
    Args:
        object: request
        string: category slug
    Returns:
        list: posts in the category
        list: all categories
        int: number of posts in that category
    TODO: Handle unfound slug  
    '''
    category = Category.objects.get(category_slug=slug)
    related_tutorials = Tutorial.objects.filter(category=category).all()
    categories = Category.objects.all()
    tut_count = len(related_tutorials)
    context = {'latest_items': related_tutorials,
                'categories': categories,
                'category': category,
                'tut_count': tut_count}
    return render(request, 'category_posts.html', context=context)


def visitor_message(request):
    '''
    visitors messages
    Args:
        object: request
    Returns:
        object: message form
    '''
    form = MessageForm()
    if request.method == 'POST':
        # save message
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                author=form.cleaned_data["author"],
                email=form.cleaned_data["email"],
                body=form.cleaned_data["body"]
            )
            message.save()
            return redirect("blog:homepage")

    return render(request, 'contact_me.html', context={"form": form})


def login(request):
    return render(request, 'login.html')
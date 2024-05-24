from django.shortcuts import render,get_object_or_404,redirect
from users.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.decorators.http import require_POST


@login_required(login_url='login')
def profile_page(request, slug):
    user = get_object_or_404(User, slug=slug)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    is_friend = False
    
    if request.user.is_authenticated and user != request.user:
        is_friend = Friendship.objects.filter(user=request.user, friend=user).exists()

    context = {
        'user': user,
        'posts': posts,
        'is_friend': is_friend,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def edit_image(request, slug):
    user = get_object_or_404(User, slug=slug)
    user_data, created = ImageOfUsers.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        if request.FILES:
            user_data.profile_pic = request.FILES['profile_pic']
            user_data.save()
            return redirect('myprofile', slug=user.slug)
    
    context = {'user': user, 'user_data': user_data}
    return render(request, 'editprofile.html', context)

@login_required(login_url='login')
def remove_pic(request, slug):
    user = get_object_or_404(User, slug=slug)
    user_data, created = ImageOfUsers.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_data.profile_pic = None
        user_data.save()
        return redirect('myprofile', slug=user.slug)
    
    context = {'user': user, 'user_data': user_data}
    return render(request, 'editprofile.html', context)

@login_required(login_url='login')
def update_about(request, slug):
    user = get_object_or_404(User, slug=slug)
    user_about, created = AboutOfUsers.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=user_about)
        if form.is_valid():
            form.save()
            return redirect('myprofile', slug=user.slug)
    else:
        form = AboutForm(instance=user_about)
    
    context = {'form': form, 'user': user}
    return render(request, 'profileabout.html', context)

@login_required(login_url='login')
def create_post(request,slug):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('myprofile', slug=request.user.slug)
    else:
        form = PostForm()
    return render(request, 'addpost.html', {'form': form})



@login_required(login_url='login')
def like_post(request,slug, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('postdetail', slug=slug, post_id=post_id)

@login_required(login_url='login')
def post_detail(request, slug, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent__isnull=True) 
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect('postdetail', slug=slug, post_id=post_id)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'postdetail.html', context)

@login_required(login_url='login')
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    Friendship.objects.filter(user=request.user, friend=friend).delete()
    return redirect('myprofile', slug=request.user.slug)

@login_required(login_url='login')
def friend_list(request, slug):
    user = get_object_or_404(User, slug=slug)
    friends = Friendship.objects.filter(user=user).select_related('friend')
    
    context = {
        'user': user,
        'friends': friends,
    }
    return render(request, 'friendlist.html', context)

@login_required(login_url='login')
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'notification.html', {'notifications': notifications})

@login_required(login_url='login')
def add_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    
    if not Friendship.objects.filter(user=request.user, friend=friend).exists():
        # Create a friendship
        Friendship.objects.create(user=request.user, friend=friend)
        
        # Create a notification for the friend
        Notification.objects.create(sender=request.user, recipient=friend)
        
    return redirect('myprofile', slug=request.user.slug)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
from accounts.models import User
from notifications.utils import create_notification


def feed_view(request):
    sort = request.GET.get('sort', 'latest')
    posts_qs = Post.objects.select_related('author').prefetch_related('collaborators', 'likes')

    if sort == 'trending':
        posts_list = sorted(posts_qs, key=lambda p: p.trending_score, reverse=True)
    else:
        posts_list = list(posts_qs.order_by('-created_at'))

    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Determine user's liked and bookmarked posts
    liked_ids = set()
    bookmarked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        bookmarked_ids = set(Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/feed.html', {
        'page_obj': page_obj,
        'sort': sort,
        'liked_ids': liked_ids,
        'bookmarked_ids': bookmarked_ids,
    })


def post_detail_view(request, pk):
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('collaborators', 'comments__author', 'likes'), pk=pk)

    # Increment views
    Post.objects.filter(pk=pk).update(views_count=post.views_count + 1)

    comment_form = CommentForm()
    is_liked = False
    is_bookmarked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
        is_bookmarked = Bookmark.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # Notify post author
            if post.author != request.user:
                create_notification(
                    user=post.author,
                    notification_type='comment',
                    message=f"{request.user.username} commented on your project '{post.title[:30]}'",
                    link=f"/posts/{post.pk}/"
                )
            messages.success(request, "Comment added!")
            return redirect('posts:detail', pk=pk)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Handle collaborators
            collaborators_input = form.cleaned_data.get('collaborators_input', '')
            if collaborators_input:
                usernames = [u.strip() for u in collaborators_input.split(',') if u.strip()]
                for username in usernames:
                    try:
                        collab_user = User.objects.get(username=username)
                        if collab_user != request.user:
                            post.collaborators.add(collab_user)
                    except User.DoesNotExist:
                        pass
            post.save()
            messages.success(request, "Project posted successfully! 🚀")
            return redirect('posts:detail', pk=post.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            # Update collaborators
            post.collaborators.clear()
            collaborators_input = form.cleaned_data.get('collaborators_input', '')
            if collaborators_input:
                usernames = [u.strip() for u in collaborators_input.split(',') if u.strip()]
                for username in usernames:
                    try:
                        collab_user = User.objects.get(username=username)
                        if collab_user != request.user:
                            post.collaborators.add(collab_user)
                    except User.DoesNotExist:
                        pass
            messages.success(request, "Project updated successfully!")
            return redirect('posts:detail', pk=post.pk)
    else:
        initial_collabs = ', '.join(post.collaborators.values_list('username', flat=True))
        form = PostForm(instance=post, initial={'collaborators_input': initial_collabs})
    return render(request, 'posts/create_post.html', {'form': form, 'editing': True, 'post': post})


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Project deleted.")
        return redirect('posts:feed')
    return render(request, 'posts/confirm_delete.html', {'post': post})


@login_required
def like_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
        if post.author != request.user:
            create_notification(
                user=post.author,
                notification_type='like',
                message=f"{request.user.username} liked your project '{post.title[:30]}'",
                link=f"/posts/{post.pk}/"
            )
    return JsonResponse({'is_liked': is_liked, 'likes_count': post.likes_count})


@login_required
def bookmark_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        bookmark.delete()
        is_bookmarked = False
    else:
        is_bookmarked = True
    return JsonResponse({'is_bookmarked': is_bookmarked})


@login_required
def bookmarks_view(request):
    bookmarked_post_ids = Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
    posts = Post.objects.filter(pk__in=bookmarked_post_ids).select_related('author')
    liked_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    return render(request, 'posts/bookmarks.html', {
        'posts': posts,
        'liked_ids': liked_ids,
        'bookmarked_ids': set(bookmarked_post_ids),
    })


def search_view(request):
    query = request.GET.get('q', '').strip()
    tech_filter = request.GET.get('tech', '').strip()
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tech_stack__icontains=query) |
            Q(author__username__icontains=query)
        ).select_related('author')

    if tech_filter:
        posts = posts.filter(tech_stack__icontains=tech_filter)

    liked_ids = set()
    bookmarked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        bookmarked_ids = set(Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/search.html', {
        'posts': posts,
        'query': query,
        'tech_filter': tech_filter,
        'liked_ids': liked_ids,
        'bookmarked_ids': bookmarked_ids,
    })

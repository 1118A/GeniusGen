from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from accounts.models import User
from posts.models import Post, Like, Comment
from quizzes.models import Quiz, QuizResult


@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()
    total_quizzes = Quiz.objects.count()
    total_quiz_attempts = QuizResult.objects.count()

    # Recent signups (last 5)
    recent_users = User.objects.order_by('-date_joined')[:5]

    # Top posts by likes
    top_posts = Post.objects.annotate(
        num_likes=Count('likes')
    ).order_by('-num_likes')[:5]

    # Quiz participation
    quiz_stats = Quiz.objects.annotate(
        attempts=Count('quizresult')
    ).order_by('-attempts')[:5]

    # Posts per day (last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.now().date()
    posts_per_day = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = Post.objects.filter(created_at__date=day).count()
        posts_per_day.append({'day': day.strftime('%a'), 'count': count})

    # Users per day (last 7 days)
    users_per_day = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = User.objects.filter(date_joined__date=day).count()
        users_per_day.append({'day': day.strftime('%a'), 'count': count})

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_quizzes': total_quizzes,
        'total_quiz_attempts': total_quiz_attempts,
        'recent_users': recent_users,
        'top_posts': top_posts,
        'quiz_stats': quiz_stats,
        'posts_per_day': posts_per_day,
        'users_per_day': users_per_day,
    })

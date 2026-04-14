from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/<int:pk>/', views.post_detail_view, name='detail'),
    path('post/create/', views.create_post_view, name='create'),
    path('post/<int:pk>/edit/', views.edit_post_view, name='edit'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete'),
    path('post/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('post/<int:pk>/bookmark/', views.bookmark_toggle, name='bookmark_toggle'),
    path('bookmarks/', views.bookmarks_view, name='bookmarks'),
    path('search/', views.search_view, name='search'),
]

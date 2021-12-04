from django.urls import path 
from . import views

urlpatterns = [
    path('', views.post_comment_create_and_list_view, name='main_post_view'),
    path('liked/', views.like_unlike_post, name='like_unlike_post'),
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
]
 
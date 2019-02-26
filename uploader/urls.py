from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import permission_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('posts/self', views.UserPostList.as_view(), name='user_post_list'),
    path('post/new/', views.NewPost.as_view(), name='post_new'),
    path('post/download/<int:pk>/', views.download, name='download'),
    path('post/edit/<int:pk>/', views.PostEdit.as_view(), name='post_edit'),
    path('post/delete/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),
    path('tags/', views.TagList.as_view(), name="tag_list"),
    path('tag/new/', permission_required('request.user.is_superuser')(views.NewTag.as_view()),
         name='tag_new'),
    path('tags/<str:tag_name>/', views.TagDetail.as_view(), name="tag_detail"),
    path('about/', views.about, name='about'),
    path('register/', views.RegisterView.as_view(), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

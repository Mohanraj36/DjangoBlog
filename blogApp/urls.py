from django.urls import path
from . import views
urlpatterns = [
    path('', views.postListView.as_view(), name='post-list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView, name='logout'),
    path('register/', views.CustomRegisterPage.as_view(), name='register'),
    path('post-detail/<int:pk>/', views.postDetailView.as_view(), name='post-detail'),
    path('comment-create/<int:pk>', views.postDetailView.as_view(), name='comment-create'),
    path('comment-delete/<int:pk>', views.postCommentDeleteView.as_view(), name='comment-delete'),
    path('post-like/<int:pk>/', views.postLikeView.as_view(), name='post-like'),
    path('post-create/', views.postCreateView.as_view(), name='post-create'),
    path('post-update/<int:pk>/', views.postUpdateView.as_view(), name='post-update'),
    path('post-delete/<int:pk>/', views.postDeleteView.as_view(), name='post-delete'),
]

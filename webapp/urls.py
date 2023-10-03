from django.urls import path
from webapp.views import *
from webapp.views import PostList, PostDetail, PostCreate, ResponseCreate, PostResponseList, ResponseList, PostResponseDetail, PostResponseAccept, PostResponseDelete, CategoryList, \
    subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('posts', PostList.as_view()),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts/create', PostCreate.as_view()),

    path('responses_to_post', PostResponseList.as_view()),
    path('my_responses', ResponseList.as_view()),
    path('responses_posts/<int:pk>', PostResponseDetail.as_view()),


    path('responses_posts/<int:pk>/accept', PostResponseAccept.as_view(success_url='/board/responses_to_post'), name='accept'),
    path('response_create', ResponseCreate.as_view(), name='response_create'),
    path('responses_posts/<int:pk>/delete', PostResponseDelete.as_view(), name='delete'),


    path('categories', CategoryList.as_view()),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
]

from django.urls import path

from .views import *
from facility.views import *
urlpatterns = [
    path('request/', BloggerRequestView.as_view(), name="blogging-request"),
    path('', blog_page, name='blog'),
    path('<str:slug>/', PostListView.as_view(), name='posts'),
    path('post/create', PostCreateView.as_view(), name='create-post'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post'),
    path('post/update/<str:slug>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<str:slug>/', PostDeleteView.as_view(), name='delete-post'),
    path('post/<str:slug>/add_comment/',  ReviewPostCreateView.as_view(), name='add_comment'),
    path('post/<str:slug>/list_comments/', ReviewIndexPage.as_view(), name='comments'),
    path('search', SearchListView.as_view(), name='search'),
    path('like/<str:slug>', like_view, name='like_post'),
]


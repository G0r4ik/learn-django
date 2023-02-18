from django.urls import path
from Main.views.post_views import *
from Main.middleware import CustomAuthenticationMiddleware


urlpatterns = [
    path("getAll", getAllPosts),
    path("", addPost),
    path("delete/<int:postID>", deletePostById),
    path("get/<int:postID>", getPostById),
    path("update/<int:postID>", postUpdateById),
    path("search/<str:searchText>", searchPost),
]

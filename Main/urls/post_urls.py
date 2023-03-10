from django.urls import path
from Main.views.post_views import *


urlpatterns = [
    path("getAll", getAllPosts),
    path("search/<str:searchText>", searchPost),
    path("", addPost),
    path("delete/<int:postID>", deletePostById),
    path("get/<int:postID>", getPostById),
    path("update/<int:postID>", postUpdateById),
]

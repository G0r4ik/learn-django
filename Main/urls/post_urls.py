from django.urls import path
from Main.views.post_views import *
from Main.middleware import CustomAuthenticationMiddleware

post_middleware = [
    CustomAuthenticationMiddleware,
]
# Всем authToken
urlpatterns = [
    path("<int:postID>/", deletePostById),
    path("<int:postID>/", getPostById, ),
    path("getAll", getAllPosts, ),
    path("", addPost),
    path("update/<int:postID>/", postUpdateById),  # checkPostIDAndSetPost
    path("<int:postID>/", deletePostById),  # checkPostIDAndSetPost
    path("<int:postID>/", getPostById),  # checkPostIDAndSetPost getUserOfPosts
    path("search/<str:searchText>/", searchPost),
]

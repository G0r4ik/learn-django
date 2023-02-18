from django.urls import path, include

urlpatterns = [
    path("api/", include("Main.urls.user_urls")),
    path("api/post/", include("Main.urls.post_urls")),
    path("api/post/<int:postID>/comments/", include("Main.urls.comment_urls")),
]

from django.urls import path, include
from Main.views import *

urlpatterns = [
    path("api/", include("Main.urls.user_urls")),
    path("api/post/", include("Main.urls.post_urls")),
    path("api/post/<int:postID>/comments/", include("Main.urls.comment_urls")),
]

# handler404 = pageNotFound

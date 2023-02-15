from django.urls import path
from Main.views.comment_views import *

# Всем authToken
urlpatterns = [
    # везде checkAuthToken checkPostIDAndSetPost
    path("<int:postID>/comments/add", addComment),
    path(
        "<int:postID>/comments/update/<int:commentID>/", updateComment
    ),  # checkComment
    path(
        "<int:postID>/comments/delete/<int:commentID>/", deleteComment
    ),  # checkComment
    path("<int:postID>/comments/showAll", showAllComments),
]

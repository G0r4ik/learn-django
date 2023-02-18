from django.urls import path
from Main.views.comment_views import *

# Всем authToken
urlpatterns = [
    path("add", addComment),
    path("update/<int:commentID>/", updateComment),  # checkComment
    path("delete/<int:commentID>/", deleteComment),  # checkComment
    path("showAll", showAllComments),
]

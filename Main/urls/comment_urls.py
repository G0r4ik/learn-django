from django.urls import path
from Main.views.comment_views import *

urlpatterns = [
    path("add", addComment),
    path("update/<int:commentID>", updateComment),
    path("delete/<int:commentID>", deleteComment),
    path("showAll", showAllComments),
]

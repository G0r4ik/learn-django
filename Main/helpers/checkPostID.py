from django.urls import resolve
from Main.helpers.errorHandler import errorHandler

from Main.models.post import Post


def checkPostID(request, postID):
    kwargs = resolve(request.path_info).kwargs
    if "postID" not in kwargs:
        return False

    postID = kwargs["postID"]
    post = Post.objects.filter(id=postID).first()
    if not post:
        return False

    return post

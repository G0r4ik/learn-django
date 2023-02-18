from datetime import date
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from Main.models.comment import Comment
from django.forms import model_to_dict
from django.http import JsonResponse

from Main.models.user import User
from Main.views.user_views import normalizeUser


def updateComment(request, postID, commentID):
    return JsonResponse("updateComment")


def addComment(request, postID):
    dateOfCreate = date.today()
    text = request.POST.get("text")
    author = request.POST.get("author")
    newComment = Comment(
        author=author,
        text=text,
        id_post_id=request.post.id,
        id_user_id=request.user.id,
        date=dateOfCreate,
    )
    return JsonResponse(newComment)


def deleteComment(request, postID, commentID):
    return JsonResponse("deleteComment")


def showAllComments(request, postID):
    comments = list(Comment.objects.filter(id_post_id=postID))
    for comment in comments:
        user = model_to_dict(User.objects.get(id=comment["id_user_id"]))
        user = normalizeUser(user)
        comment["user"] = user
        del comment["id_user_id"]

    return JsonResponse({"data": comments})

    # return JsonResponse(model_to_dict(list(comments)), safe=False)

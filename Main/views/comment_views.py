from datetime import date
from Main.helpers.checkPostID import checkPostID
from Main.helpers.errorHandler import errorHandler
from Main.models.comment import Comment
from django.forms import model_to_dict
from django.http import JsonResponse
from .user_views import normalizeUser
from Main.models.user import User
from Main.views.user_views import normalizeUser
from datetime import date
import json
from ..helpers.validate import validate_comment_author, validate_comment_text


def updateComment(request, postID, commentID):
    data = json.loads(request.body)
    text = data.get("text")
    author = data.get("author")
    dateOfCreate = date.today()

    if None in (text, author):
        return errorHandler("Не все параметры переданы", 400)

    error = validate_comment_author(author)
    if error:
        return errorHandler(error, 400)
    error = validate_comment_text(text)
    if error:
        return errorHandler(error, 400)

    updatedComment = Comment.objects.filter(id=commentID).first()

    if request.user.id != updatedComment.id_user_id:
        return errorHandler("Вы не можете удалять чужие комментарии")

    print(updatedComment, 10900000000000000000000000000)
    if not updatedComment:
        return errorHandler("Такого комменатрия не существует")

    updatedComment.author = author
    updatedComment.text = text
    updatedComment.date = dateOfCreate
    updatedComment.save()

    return JsonResponse(model_to_dict(updatedComment))


def addComment(request, postID):
    data = json.loads(request.body)
    text = data.get("text")
    author = data.get("author")
    dateOfCreate = date.today()

    if None in (text, author):
        return errorHandler("Не все параметры переданы", 400)

    error = validate_comment_author(author)
    if error:
        return errorHandler(error, 400)
    error = validate_comment_text(text)
    if error:
        return errorHandler(error, 400)

    newComment = Comment(
        author=author,
        text=text,
        id_post_id=postID,
        id_user_id=request.user.id,
        date=dateOfCreate,
    )
    newComment.save()

    return JsonResponse(model_to_dict(newComment))


def deleteComment(request, postID, commentID):
    comment = Comment.objects.filter(id=commentID).first()
    if not comment:
        return errorHandler("Такого комментария не существует")
    if request.user.id != comment.id_user_id:
        return errorHandler("Вы не можете удалять чужие комментарии")

    comment.delete()
    comment = model_to_dict(comment)
    comment["user"] = normalizeUser(model_to_dict(request.user))
    return JsonResponse(comment, safe=False)


def showAllComments(request, postID):
    post = checkPostID(request, postID)
    if not post:
        return errorHandler("Такого поста не сушествует")

    comments = list(Comment.objects.all().values())
    for comment in comments:
        user = normalizeUser(model_to_dict(User.objects.get(id=comment["id_user_id"])))
        comment["user"] = user

    return JsonResponse(comments, safe=False)

import json
from django.forms import model_to_dict
from django.http import JsonResponse
from Main.helpers.checkPostID import checkPostID
from Main.helpers.errorHandler import errorHandler
from Main.helpers.validate import validate_title, validate_text
from Main.models.user import User
from .user_views import normalizeUser
from ..models.post import Post
from datetime import date
from urllib.parse import unquote_plus
from django.db.models import Q


def getAllPosts(request):
    allPost = list(Post.objects.all().values())
    for post in allPost:
        user = model_to_dict(User.objects.get(id=post["id_user_id"]))
        user = normalizeUser(user)
        post["user"] = user
        del post["id_user_id"]

    return JsonResponse(allPost, safe=False)


def getPostById(request, postID):
    post = checkPostID(request, postID)
    if not post:
        return errorHandler("Такого поста не сушествует")

    post = model_to_dict(post)
    user = normalizeUser(model_to_dict(User.objects.get(id=post["id_user"])))
    post["user"] = user

    return JsonResponse(post)


def searchPost(request, searchText):
    try:
        searchText = unquote_plus(searchText)
        print(searchText)
        posts = Post.objects.filter(
            Q(text__contains=searchText) | Q(title__contains=searchText)
        )
        post_list = []
        for post in posts:
            post_dict = model_to_dict(post)
            post_list.append(post_dict)
        return JsonResponse(post_list, safe=False)
    except Exception as e:
        print(e)


def deletePostById(request, postID):
    post = checkPostID(request, postID)
    if not post:
        return errorHandler("Такого поста не сущетсвует", 400)

    if request.user.id != post.id_user_id:
        return errorHandler("Это не ваш пост", 400)

    post.delete()
    return JsonResponse(model_to_dict(post), safe=False)


def addPost(request):
    data = json.loads(request.body)
    user = request.user
    text = data.get("text")
    title = data.get("title")
    dateOfCreate = date.today()

    if None in (text, title):
        return errorHandler("Не все параметры переданы", 400)

    error = validate_text(text)
    if error:
        return errorHandler(error, 400)

    error = validate_title(text)
    if error:
        return errorHandler(error, 400)

    newPost = Post(text=text, title=title, date=dateOfCreate, id_user=user)
    newPost.save()
    newPost = model_to_dict(newPost)
    newPost["user"] = normalizeUser(model_to_dict(user))
    del newPost["id_user"]
    return JsonResponse(newPost, safe=False)


def postUpdateById(request, postID):
    data = json.loads(request.body)
    text = data.get("text")
    title = data.get("title")
    dateOfCreate = date.today()

    if None in (text, title):
        return errorHandler("Не все параметры переданы", 400)

    post = checkPostID(request, postID)
    if not post:
        return errorHandler("Такого поста не сущетсвует")

    if request.user.id != post.id_user_id:
        return errorHandler("Это не ваш пост", 400)

    post.title = title
    post.text = text
    post.date = dateOfCreate
    post.save()
    post = model_to_dict(post)
    post["user"] = normalizeUser(model_to_dict(request.user))
    del post["id_user"]
    return JsonResponse(post, safe=False)

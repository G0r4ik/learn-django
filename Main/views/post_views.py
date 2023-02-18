from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from Main.helpers import errorHandler

from Main.models.user import User


from .user_views import normalizeUser
from ..models.post import Post
from datetime import date


def checkTitle(title):
    if len(title) < 5:
        return errorHandler("Слишком короткий заголовок", 400)


def checkText(text):
    if len(text) < 5:
        return errorHandler("Слишком короткий текст поста", 400)


def normalizePost(user, post):
    normalizePost = {
        "title": post.title,
        "text": post.text,
        "date": post.date,
        "postID": post.post_id or post.id,
        "user": normalizeUser(user),
    }
    return normalizePost


def getAllPosts(request):
    allPost = list(Post.objects.all().values())
    for post in allPost:
        user = model_to_dict(User.objects.get(id=post["id_user_id"]))
        user = normalizeUser(user)
        post["user"] = user
        del post["id_user_id"]

    return JsonResponse({"data": allPost})


def addPost(request):
    user = model_to_dict(request.user)
    text = request.POST.get("text")
    title = request.POST.get("title")
    dateOfCreate = date.today()

    user = User.objects.get(id=user["id"])
    newPost = Post(text=text, title=title, date=dateOfCreate, id_user=user)
    newPost.save()
    newPost = model_to_dict(newPost)
    newPost["user"] = model_to_dict(user)
    del newPost["id_user"]
    return JsonResponse(newPost, safe=False)


def getPostById(request, postID):
    try:
        post = model_to_dict(Post.objects.get(id=postID))
        user = User.objects.get(id=post["id_user"])
        post["user"] = model_to_dict(user)

    except Post.DoesNotExist:
        return errorHandler.errorHandler("Такого поста нет", 400)
    return JsonResponse(post)


def postUpdateById(request, postID):
    try:
        user = model_to_dict(request.user)
        text = request.POST.get("text")
        title = request.POST.get("title")
        idP = request.POST.get("id")
        dateOfCreate = date.today()

        post = request.post
        post = Post.objects.get(id=postID)

        post.title = title
        post.text = text
        post.date = dateOfCreate
        post.save()
        return JsonResponse(model_to_dict(post), safe=False)
    except Post.DoesNotExist:
        return errorHandler.errorHandler("Такого поста не существует 2", 400)


def deletePostById(request, postID):
    post = get_object_or_404(Post, id=postID)

    if request.post:
        post.delete()
        return JsonResponse(model_to_dict(post), safe=False)
    else:
        return None
        # return errorHandler.errorHandler("Такого поста не существует 1", 400)


def searchPost(request, searchText):
    posts = Post.objects.filter(text__contains=searchText)
    post_list = []
    for post in posts:
        post_dict = model_to_dict(post)
        post_list.append(post_dict)
    return JsonResponse(post_list, safe=False)

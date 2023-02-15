from django.forms import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from Main.models.user import User


from .user_views import normalizeUser
from ..models.post import Post
from datetime import date


def normalizePost(user, post):
    # normalizeUser = {
    #     "username": user.username or post.username,
    #     "email": user.email or post.email,
    #     "userID": user.id or post.id_user,
    # }
    normalizePost = {
        "title": post.title,
        "text": post.text,
        "date": post.date,
        "postID": post.post_id or post.id,
        "user": normalizeUser(user),
    }
    return normalizePost


def getAllPosts(request):
    user = model_to_dict(request.user)
    print(user["username"])
    allPost = list(Post.objects.all().values())
    print(allPost)
    return JsonResponse({"data": allPost})


def addPost(request):
    user = model_to_dict(request.user)
    text = request.POST.get("text")
    title = request.POST.get("title")
    dateOfCreate = date.today()

    user = User.objects.get(id=user["id"])
    newPost = Post(text=text, title=title, date=dateOfCreate, id_user=user)
    newPost.save()
    
    return JsonResponse(model_to_dict(newPost), safe=False)


def getPostById(request, postID):
    post = Post.objects.filter(id=postID)
    return JsonResponse(post)


def postUpdateById(request, postID):
    return JsonResponse()


def deletePostById(request, postID):
    return JsonResponse()


def searchPost(request, postID):
    return JsonResponse()

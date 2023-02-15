from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods


def updateComment(request, postID, commentID):
    return HttpResponse("updateComment")


def addComment(request, postID):
    return HttpResponse("addComment")


def deleteComment(request, postID, commentID):
    return HttpResponse("deleteComment")


def showAllComments(request, postID):
    return HttpResponse("showAllComments")

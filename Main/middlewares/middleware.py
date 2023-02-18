from django.forms import ValidationError, model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Main.helpers import errorHandler
from Main.models.post import Post
from mysite.settings import SECRET_KEY
from django.urls import resolve
import jwt

from Main.models.user import User


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/post"):
            return self.get_response(request)

        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        if not token:
            # raise errorHandler.CustomException("Некоректный токен", 400)
            print("YYYY")
            raise ValidationError("Некоректный токен")

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if not decoded_token:
            raise errorHandler.CustomException("Некоректный токен", 400)
        user_id = decoded_token.get("id")
        user = User.objects.get(id=user_id)
        request.user = user

        return self.get_response(request)


class CustomPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        postID = resolve(request.path_info).kwargs.get("postID")
        if not postID:
            return errorHandler.CustomException("postID is not provided", 400)

        post = Post.objects.filter(id=postID).first()
        if not post:
            raise errorHandler.CustomException("Такого поста не существует", 404)
        request.post = post

        return self.get_response(request)


class CheckCommentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        post_id = request.path_info.split("/")[-2]
        # Изменено для работы с URL вида /api/post/<post_id>/comments/

        if not request.path.startswith(f"/api/post/{post_id}/comments"):
            return self.get_response(request)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise errorHandler.CustomException(
                "Такого поста не существует middleware", 400
            )

        if request.user == post.id_user:
            request.post = post
        else:
            request.post = False
            raise errorHandler.CustomException("Это не ваш пост", 400)

        response = self.get_response(request)
        return response


class ErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("1----------------------------------------------------")
        try:
            print("3----------------------------------------------------")
            response = self.get_response(request)
        except ValidationError:
            print("4---------------------------------------------------")
        except Exception as e:
            print("2----------------------------------------------------")
            error_dict = {}
            if hasattr(e, "message"):
                error_dict["message"] = e.message
            else:
                error_dict["message"] = str(e)

            error_dict["code"] = 500

            if hasattr(e, "status"):
                error_dict["code"] = e.status

            if hasattr(e, "errors"):
                error_dict["errors"] = e.errors

            return JsonResponse({"error": error_dict}, status=error_dict["code"])
        return response

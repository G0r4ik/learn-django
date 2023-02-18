from django.forms import model_to_dict
from Main import errorHandler
from Main.models.post import Post
from mysite.settings import SECRET_KEY
from django.urls import resolve
import jwt

from Main.models.user import User


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if not request.path.startswith("/api/post"):
                response = self.get_response(request)
                return response
                # return self.get_response(request)

            token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
            if not token:
                raise errorHandler.CustomException("Некоректный токен", 400)
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if not decoded_token:
                raise errorHandler.CustomException("Некоректный токен", 400)
            user_id = decoded_token.get("id")
            user = User.objects.get(id=user_id)
            request.user = user

            response = self.get_response(request)

            return response
        except errorHandler.CustomException as e:
            return errorHandler.errorHandler(e.message, e.status)


class CustomPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            postID = resolve(request.path_info).kwargs["postID"]
            if not postID:
                return self.get_response(request)
            if (
                not request.path.startswith("/api/post/delete")
                and not request.path.startswith("/api/post/update")
                and not request.path.startswith(f"/api/post/${postID}/comments")
            ):
                return self.get_response(request)
            # postID = resolve(request.path_info).kwargs["postID"]

            # print(request)

            post = Post.objects.get(id=postID)
            request.post = post
            response = self.get_response(request)
            return response
            # return errorHandler.errorHandler("Это не ваш пост", 400)
        except KeyError as e:
            return errorHandler.errorHandler("Ошибка", 400)
        except AttributeError as e:
            "Такого поста не существует middleware", 400
        except errorHandler.CustomException as e:
            return errorHandler.errorHandler(e.message, e.status)
        except Post.DoesNotExist:
            return errorHandler.errorHandler(
                "Такого поста не существует middleware", 400
            )


class checkCommentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            postID = postID = request.path_info.split("/")[-1]
            if not request.path.startswith(f"/api/post/{postID}/comments"):
                return self.get_response(request)

            post = Post.objects.get(id=postID)
            if request.user == post.id_user:
                request.post = post
                response = self.get_response(request)
                return response

            request.post = False
            response = self.get_response(request)
            return errorHandler.errorHandler("Это не ваш пост", 400)

        except errorHandler.CustomException as e:
            return errorHandler.errorHandler(e.message, e.status)
        except Post.DoesNotExist:
            return errorHandler.errorHandler(
                "Такого поста не существует middleware", 400
            )

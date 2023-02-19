from Main.helpers.errorHandler import errorHandler
from Main.models.post import Post
from mysite.settings import SECRET_KEY
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
            return errorHandler("Токен не обнаружен", 400)

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return errorHandler("Токен либо истек, либо некоректен")

        if not decoded_token:
            return errorHandler("Ошибка при проверке токена", 400)

        user_id = decoded_token.get("id")
        user = User.objects.get(id=user_id)
        request.user = user
        return self.get_response(request)

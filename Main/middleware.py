from mysite.settings import SECRET_KEY
from django.http import HttpResponseForbidden
import jwt

from Main.models.user import User


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/post"):
            return self.get_response(request)

        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        print(token)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(decoded_token)
        user_id = decoded_token.get("id")
        user = User.objects.get(id=user_id)
        request.user = user

        response = self.get_response(request)

        return response

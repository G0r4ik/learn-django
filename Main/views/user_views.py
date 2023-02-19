import datetime

# import json
import jwt
from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from Main.helpers.normalize import normalizeUser
from Main.helpers.validate import validate_email, validate_password, validate_username
from mysite.settings import SECRET_KEY
from Main.helpers.errorHandler import errorHandler
from Main.models.user import User
from django.db.models import Q
import simplejson as json


def generateToken(user):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=100)
    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "exp": expires_at,
    }
    token = jwt.encode(payload, SECRET_KEY)
    return token


def registerUser(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if None in (username, email, password):
        return errorHandler("Не все параметры переданы", 400)

    hasUserInDB = User.objects.filter(Q(username=username) | Q(email=email))

    if hasUserInDB:
        return errorHandler("Пользователь уже сущетсвует", 401)

    error = validate_email(email)
    if error:
        return errorHandler(error, 400)

    error = validate_username(username)
    if error:
        return errorHandler(error, 400)

    error = validate_password(password)
    if error:
        return errorHandler(error, 400)

    hashPassword = make_password(password)
    newUser = User.objects.create(username=username, email=email, password=hashPassword)

    newUser = normalizeUser(model_to_dict(newUser))
    token = generateToken(newUser)

    return JsonResponse({"token": token, "user": newUser})


def loginUser(request):
    data = json.loads(request.body)
    login = data.get("username")
    password = data.get("password")

    print(login, password, "heklkkkkkk")
    if None in (login, password):
        return errorHandler("Не все параметры переданы", 405)

    user = User.objects.filter(Q(username=login) | Q(email=login)).values().first()

    if not user:
        return errorHandler("Нет такого пользователя", 401)

    isValidPassword = check_password(password, user["password"])
    if not isValidPassword:
        return errorHandler("Неверный пароль", 402)

    normalizedUser = normalizeUser(user)
    token = generateToken(normalizedUser)

    return JsonResponse({"token": token, "user": normalizeUser(normalizedUser)})


def checkAuthToken(request):
    print("lalal")
    token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
    if not token:
        return JsonResponse({"isValid": False})

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return JsonResponse({"isValid": False})

    if not decoded_token:
        return JsonResponse({"isValid": False})

    return JsonResponse({"isValid": True})


# def logoutUser(request):
#     return HttpResponse("logoutUser")

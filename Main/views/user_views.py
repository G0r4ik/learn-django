import datetime
import jwt
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from mysite.settings import SECRET_KEY
from Main.helpers.errorHandler import errorHandler, CustomException
from Main.models.user import User
from django.db.models import Q


def normalizeUser(user):
    return {"id": user["id"], "email": user["email"], "username": user["username"]}


def checkUsername(username):
    if len(username) < 5:
        raise CustomException("Некоректный лоигн", 400)


def checkEmail(email):
    if len(email) < 5:
        raise CustomException("Некоректная почта", 400)


def checkPassword(password):
    if len(password) < 5:
        raise CustomException("Некоректный пароль", 400)


def generateToken(user):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "exp": expires_at,
    }
    token = jwt.encode(payload, SECRET_KEY)
    return token


def checkAuthToken(request):
    return HttpResponse("checkAuthToken")


def registerUser(request):
    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        hasUserInDB = User.objects.filter(Q(username=username) | Q(email=email))

        if hasUserInDB:
            raise CustomException("Пользователь уже сущетсвует", 401)

        if None in (username, email, password):
            raise CustomException("Не все параметры переданы", 400)

        checkEmail(email)
        checkUsername(username)
        checkPassword(password)

        hashPassword = make_password(password)
        newUser = User(username=username, email=email, password=hashPassword)
        newUser.save()
        newUser = model_to_dict(newUser)
        token = generateToken(newUser)

        return JsonResponse({"token": token, "user": normalizeUser(newUser)})

    except CustomException as e:
        return errorHandler(e.message, e.status)


def loginUser(request):
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username).values().first()

        if not user:
            raise CustomException("Нет такого пользователя", 400)
        isValidPassword = check_password(password, user["password"])
        if not isValidPassword:
            raise CustomException("Неверный пароль", 400)
        token = generateToken(user)

        return JsonResponse({"token": token, "user": normalizeUser(user)})

    except CustomException as e:
        return errorHandler(e.message, e.status)


def logoutUser(request):
    return HttpResponse("logoutUser")

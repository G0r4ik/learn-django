from django.urls import path
from Main.views.user_views import *

urlpatterns = [
    # checkUsername, checkEmail, checkPassword,
    path("checkAuthToken", checkAuthToken),
    path("register", registerUser),
    path("login", loginUser),
    path("logout", logoutUser),
]

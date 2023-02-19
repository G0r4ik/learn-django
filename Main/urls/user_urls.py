from django.urls import path
from Main.views.user_views import *

urlpatterns = [
    path("register", registerUser),
    path("login", loginUser),
    # path("logout", logoutUser),
    path("checkAuthToken", checkAuthToken),
]

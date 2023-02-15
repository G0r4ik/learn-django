from django.urls import path, include
from Main.views import *

urlpatterns = [
    path('api/post/', include('Main.urls.post_urls')),
    path('api/comment/', include('Main.urls.comment_urls')),
    path('api/', include('Main.urls.user_urls')),
]

# handler404 = pageNotFound

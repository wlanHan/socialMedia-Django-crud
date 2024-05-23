"""
URL configuration for django_tweet_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tweetApp.views import *
from tweetAPI.views import *


# django config ayarları
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Anasayfa, name="index-view"),
    path("edit/user", AnaSayfa_POST, name="edit-view"),
    path("tweet/<tweetId>/guncelle", TweetGuncelle, name="update-tweet-view"),
    path("tweet/<tweetId>/sil", TweetSil, name="delete-tweet-view"),
    path("tweet/<tweetId>", TweetDetay, name="tweet-detail-view"),
    path("tweet/<tweetId>/yorum-yap", TweetYorum, name="tweet-comment-view"),
    path("users/<userId>", ProfilDetay, name="user-view"),
    path("users/<userId>/ban", ProfilYasakla, name="ban-view"),
    path("giris-yap", GirisYap, name="login-view"),
    path("cikis-yap", CikisYap, name="logout-view"),
    path("kayit-ol", KayitOl, name="register-view"),


    # API ENDPOINTS
    path("api/tweet/<tweetId>/begen", Begen, name="tweet-like-view"),
    path("api/user/followers/add/<userId>", Takip, name="follower-add-view"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

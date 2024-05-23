from .models import TweetLikes
from tweetApp.models import TweetUser as User
from tweetApp.models import UserFollowers, TweetModel

# JSON kütüphanesi
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="login-view")
def Begen(request, tweetId):
    
    message = {}

    try:
        # bu user bu postu daha önce beğenmiş mi?
        isLikedTweet = TweetLikes.objects.filter(post_id = int(tweetId), user=request.user).first()
        instance = TweetModel.objects.get(id = int(tweetId))
      
        # kişi bu postu zaten beğenmişse o zaman like kaldır.
        if isLikedTweet:
            
            instance.tweetLikes.remove(isLikedTweet)

            isLikedTweet.delete()

            message["api_message"] = {

                "status": "Unlike Yapıldı",
                "total_likes": TweetLikes.objects.filter(post_id=tweetId).count()
            }

        else:
            
            # like oluştur
         
            liked_tweet = TweetLikes.objects.create(post_id = int(tweetId), user = request.user)
            instance.tweetLikes.add(liked_tweet)
            
            message["api_message"] = {

                "status": "Like Eklendi",
                "total_likes": TweetLikes.objects.filter(post_id=tweetId).count()
            }


    except Exception as e:
        
        print("apı da hata:", e)

        message["api_message"] = {

            "status": "Bir hata meydana geldi lütfen daha sonra tekrar dene",
        }


    # JSON mesaj dön
    return JsonResponse(message)



# takip et / etme
@login_required(login_url="login-view")
def Takip(request, userId):

    message = {}

    try:

        user = User.objects.get(id = int(userId))

        userInstance = UserFollowers.objects.filter(user = user).first()

        # instance oluştur
        if userInstance is None:
             
            userInstance = UserFollowers.objects.create(user = user)
            request.user.followers.add(userInstance)

            message["api_message"] = {

                "status": "eklendi",
                "message": f"{user.username} takipçi listenize eklendi"
            }

        else:
            # zaten takip ediliyor mu?
            request.user.followers.remove(userInstance)
            userInstance.delete()
            
            message["api_message"] = {

                "status": "çıkarıldı",
                "message": f"{user.username} takipçi listenizden çıkarıldı"
            }

    except Exception as error:

            print("FOLLOW API HATA:", error)

            message["api_message"] = {

            "status": "hata",
            "message": "Bir şeyler ters gitti, Lütfen daha sonra tekrar deneyiniz"
        }
            

    return JsonResponse(message)
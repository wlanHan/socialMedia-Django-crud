from .models import TweetUser as User
from .models import TweetModel
from datetime import datetime, timedelta

def get_current_recent_users(request):

    
    now = datetime.now()
    # 24 saat öncesini hesapla
    start_time = now - timedelta(days=1)
    new_users = User.objects.filter(date_joined__gte=start_time, date_joined__lt=now)

    return {"recent_users": new_users }


def get_user_tweet_count(request):
            
            # user login değilse hepsini 0 olarak ayarla
            if request.user.is_authenticated is False:
                    return {"user_tweets_count": 0, "user_total_likes": 0} 
            
            tweets = TweetModel.objects.all()    
            tweetCount = tweets.filter(author = request.user)
            
            total_likes = 0
            for tweet in tweetCount:
                
                print("GELEN TWEEET:", tweet.tweetLikes)
                total_likes += tweet.tweetLikes.count()

            # userin toplam tweet sayısı
            return {"user_tweets_count": tweetCount.count(), "user_total_likes": total_likes} 




def recommend_random_users(request):
    randomUsers = { "random_users": [] }
    
    # Rastgele 3 user öner
    all_users = User.objects.all()

    i = 0
    while i < 3:

        if all_users.count() <= i:
            break
        
        user = all_users.order_by("?").first()

        if request.user.is_authenticated:
            if user.id == request.user.id:
                continue

        if randomUsers["random_users"].__contains__(user):
            continue

        randomUsers["random_users"].append(user)
        i += 1



        return randomUsers

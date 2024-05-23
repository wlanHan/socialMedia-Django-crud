from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Tweet Modelini Çek
from .models import *
from .models import TweetUser as User

# formu çek
from .form import UserProfile

# utils
from datetime import datetime, timedelta
# Create your views here.



def Anasayfa(request):
    context = {}
    tweetInstances = {}

    tweets = TweetModel.objects.all().order_by("-createdAt")

    for tweet in tweets:

        print("tweet:", tweet.tweet, "yorum:", tweet.comments.all())
        tweetInstances[tweet.id] = {
            
            "data": tweet,
        }

        if request.user.is_authenticated:

            tweetInstances[tweet.id].setdefault("isLiked", TweetLikes.objects.filter(post_id = tweet.id, user = request.user).exists())

    else:
        # döngü bittiginde calisan else
        context["tweets"] = tweetInstances
    
        if request.user.is_authenticated:
            context["form"] = UserProfile(instance=request.user)


    if request.method == 'POST':
        
           tweetContent = request.POST.get('tweetContent')
           tweetAttachment = request.FILES.get('tweetAttachment')

           if tweetContent:
               
               if tweetAttachment:
                   
                    TweetModel.objects.create(author=request.user, tweet=tweetContent, attachment=tweetAttachment)
               else:
                    TweetModel.objects.create(author=request.user, tweet=tweetContent)
           else:
               # bir şeyler ters gitmiştir
               context['error'] = "Birşeyler ters gitti lütfen daha sonra tekrar dene."
               return render(request, "index.html", context)
           

           return redirect('index-view')
               
    else:
        return render(request, "index.html", context)

# anasayfaya post isteği gelirse
def AnaSayfa_POST(request):

    if request.method == 'POST':

        # username ve email al
        username = request.POST.get("username")
        email = request.POST.get("email")
        # avatar al
        avatar = request.FILES.get("avatar")
        # şifreleri al
        oldPassword = request.POST.get('old_password')
        newPassword = request.POST.get('new_password')
        avatar = request.FILES.get('avatar')

        if username:

            request.user.username = username

        if email:

            request.user.email = email

        if avatar:

            request.user.avatar = avatar

        if oldPassword and newPassword:

            # şu an ki şifre eski şifre ile uyuşuyor mu?
            match_old_password = request.user.check_password(oldPassword)

            if match_old_password is False:
                print("[USER EDIT ENPOINT]: Şifreler uyuşmuyor")
                return redirect("index-view")

            # yeni şifreyi belirle
            request.user.set_password(newPassword)
            print("[USER EDIT ENPOINT]: Şifre değişti")


        # user modelini kaydet
        request.user.save()

        # anasayfaya yönlendir
        return redirect('index-view')

# tweeet güncelleme
def TweetGuncelle(request, tweetId):

    print("GELEN İD:", tweetId)
    # kullanıcı giriş yapmamışsa engelle
    if request.user.is_authenticated == False:

        return redirect("login-view")
    
    if request.method == 'POST':
        # tweeti bul
        tweet = TweetModel.objects.filter(id = tweetId).first()

        if tweet is None:
            print("Tweet bulunamadı.")
            return redirect('index-view')
        
        
        # yetki kontrol
        if request.user.is_superuser or request.user.id == tweet.author.id:

            newTweet = request.POST.get('newContent')
            tweet.tweet = newTweet
            tweet.save()
            return redirect("index-view")
        
        else:
            print("rütbe yok")
            return redirect("index-view")
        
    else:
        # get istekleri icin hep anasayfaya yonlendşir
        return redirect('index-view')



def TweetSil(request, tweetId):
        
        if request.user.is_authenticated == False:

            return redirect('login-view')
        
    
        tweet = TweetModel.objects.filter(id = tweetId).first()

        if tweet is None:
            return redirect('index-view')
        

        # yetki kontrol
        if request.user.is_superuser == False or request.user.id != tweet.author.id:

            return redirect("index-view")
        
        
        tweet.delete()

        return redirect("index-view")


def TweetDetay(request, tweetId):

    context = {}

    try:

        tweet = TweetModel.objects.filter(id = int(tweetId)).first()
            
        if tweet is None:
            # eğer böyle bi tweet yoksa
            return redirect("index-view")
        
        context["tweet"] = {

            "data": tweet,
           
        }
        # kullanıcı login olmuşsa bu postu begenmis mi diye bak
        if request.user.is_authenticated:

                context.setdefault("isLiked", TweetLikes.objects.filter(post_id = tweet.id, user = request.user).exists())
            
    except:
        return redirect("index-view")
    

    return render(request, "TweetDetail.html", context)


# yorum yapma alanı
def TweetYorum(request, tweetId):


    if request.method == "POST":

        try:
            # böyle bit tweet varmı?
            tweet = TweetModel.objects.filter(id = int(tweetId)).first()

            if tweet is None:
                return redirect("index-view")
            
            comment = request.POST.get("comment-input")

            TweetCommentModel.objects.create(author = request.user, post = tweet, message = comment)

            return redirect("tweet-detail-view", tweet.id)

        except:
             return redirect("index-view")
        
    else:

        return redirect("index-view")
        



# yetkilendirme işlemleri burada başlar
def GirisYap(request):
    context = {}

    if request.user.is_authenticated:

        return redirect('index-view')
    

    if request.method == 'POST':
        
        usernameInput = request.POST.get('username')
        passwordInput = request.POST.get('password')

        # böyle bir user var mi?
        user = authenticate(request, username = usernameInput, password = passwordInput)

        if user is None:
            # böyle bi usee yok
            context["error"] = "Girdiğiniz bilgiler Geçersiz Lütfen Tekrar Deneyin."
            return render(request, "login.html", context)
        else:
            login(request, user)
            return redirect('index-view')

    else:
        return render(request, "login.html")
    

def CikisYap(request):

        logout(request)
        return redirect('index-view')



def KayitOl(request):
     
     context = {}

     if request.method == 'POST':
          
          usernameInput = request.POST.get('username')
          passwordInput = request.POST.get('password')
          password2Input = request.POST.get('password2')

          if usernameInput and passwordInput and password2Input:
              
            # bu ada sahip başka bir user var mı?
            buAdaSahipHesaplar = User.objects.filter(username = usernameInput)

            if buAdaSahipHesaplar.__len__():
                context['hata'] = "Bu hesap adı alınmış lütfen başka bir ad deneyiniz."
                return render(request, 'register.html', context)
            # şifreler aynı mı?
            if passwordInput == password2Input:
                # hesabı oluştur
                User.objects.create_user(username=usernameInput, password=password2Input)
                return redirect('login-view')
            else:
                # şifreler aynı değil
                context['hata'] = "Şifreler Uyuşmuyor"
                return render(request, 'register.html', context)
          else:
               context['hata'] = "Lütfen gerekli olan tüm alanları doldurunuz"
               return render(request, 'register.html', context)


     else:
        return render(request, "register.html")
     


def ProfilDetay(request, userId):
    context = {}
    tweetInstances = {}

    requestedUser = User.objects.filter(id = int(userId)).first()
    totalBans = BanRecord.objects.filter(suspect = requestedUser).count()

    context["user"] = requestedUser
    context["ban_count"] = totalBans

    # ilgili userin göndermiş oldugu tweetler
    usersTweets = TweetModel.objects.filter(author = requestedUser)

    for tweet in usersTweets:
        tweetInstances[tweet.id] = {

           "data": tweet,
        }


    if request.user.is_authenticated:

            tweetInstances[tweet.id].setdefault("isLiked", TweetLikes.objects.filter(post_id = tweet.id, user = request.user).exists())
    
    
    context['tweets'] = tweetInstances
    
    return render(request, "profile.html", context)



# user ban
def ProfilYasakla(request, userId):

    if request.method == "POST":

        ban_reason = request.POST.get("ban_reason")

        user = User.objects.filter(id = int(userId)).first()

        if user.isBanned is False:

            user.isBanned = True
            # user modelini kaydet
            user.save()
            # ban kaydı oluştur
            BanRecord.objects.create(authorized = request.user, suspect = user, reason = ban_reason)

            return redirect("user-view", userId)

    else:

        return redirect("index-view")

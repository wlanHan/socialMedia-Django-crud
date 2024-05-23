from django.db import models
from django.contrib.auth.models import AbstractUser
from tweetAPI.models import TweetLikes


class TweetUser(AbstractUser):

    iliski_durumu_secenekler = (

        ("1", "Evli"),
        ("2", "Bekar"),
        ("3", "Dul"),
        ("4", "İlişkisi Var"),
        ("5","İlişkisi Yok"),
        ("6", "Karışık"),
        ("7", "Belirtmek İstemiyorum")
    )
    
    avatar = models.FileField(("Avatar"), upload_to="Profile_Avatar", default="Profile_Avatar/defaultAvatar.png", max_length=100, blank=True, null=True)
    birthday = models.DateTimeField(("Doğum Tarihi"), auto_now=False, auto_now_add=False, blank=True, null=True)
    location = models.CharField(("Yaşadığı Yer"), max_length=50, blank=True, null=True)
    relation = models.CharField(("İlişki Durumu"), max_length=50, choices=iliski_durumu_secenekler, null=True, blank=True)
    followers = models.ManyToManyField("tweetApp.UserFollowers", verbose_name=("Takipçiler"))
    isBanned = models.BooleanField(("Yasaklı"), default=False)


    def get_user_location(self):
         
         if self.location:
              return self.location
         else: 
              return "Belirtilmedi"
         
    def get_relation_status(self):
         
         if self.relation:
              return self.relation[0][0]
         else: 
              return "Belirtilmedi"
         
    def get_birthdate(self):
         
        if self.birthday:
              return self.birthday
        else: 
              return "Belirtilmedi"

# ban modeli
class BanRecord(models.Model):
     
     authorized = models.ForeignKey(TweetUser, related_name="banned_from", verbose_name=("Banlayan"), on_delete=models.CASCADE)
     suspect = models.ForeignKey(TweetUser, verbose_name=("Banlanan"), on_delete=models.CASCADE)
     reason = models.CharField(("Sebep"), max_length=50)

# takipci
class UserFollowers(models.Model):

        user = models.ForeignKey(TweetUser, verbose_name=("Takipçi"), on_delete=models.CASCADE)

        def __str__(self):
            return self.user.username
        

# tweet model
class TweetModel(models.Model):

    # id
    author = models.ForeignKey(TweetUser, verbose_name=("Tweet Yazarı"), on_delete=models.CASCADE)
    tweet = models.TextField(("Tweet"))
    tweetLikes = models.ManyToManyField("tweetAPI.TweetLikes", verbose_name=("Beğeniler"), blank=True)
    attachment = models.FileField(("Ek"), upload_to="Tweet_Uploads", max_length=100, blank=True)   # """blank = True = Opsiyonel"""
    createdAt = models.DateTimeField(("Tarih"), auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField(("Güncellenme Tarih"), auto_now=False, auto_now_add=True)
    # comments = [yorum 1, yorum 2]


    def __str__(self) -> str:
        return f"Yazar: {self.author.username} Post: {self.tweet}"
    

    def show_likes(self):
        return TweetLikes.objects.filter(post_id = self.id).count()
    
# yorum şeması
class TweetCommentModel(models.Model):
     
     author = models.ForeignKey(TweetUser, verbose_name=("Yorum Yapan"), on_delete=models.CASCADE)
     post = models.ForeignKey(TweetModel, related_name="comments", verbose_name=("Tweet"), on_delete=models.CASCADE)
     message = models.TextField(("Yorum"))
     createdAt = models.DateTimeField(("Tarih"), auto_now=True, auto_now_add=False)
     updatedAt = models.DateTimeField(("Güncellenme Tarih"), auto_now=False, auto_now_add=True)

     def __str__(self) -> str:
        return self.message
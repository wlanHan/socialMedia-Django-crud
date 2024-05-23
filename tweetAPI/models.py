from django.db import models

# Create your models here.
# bu model tweet beğenmesi sağlar
class TweetLikes(models.Model):

    post = models.ForeignKey("tweetApp.TweetModel", verbose_name=("Tweet"), on_delete=models.CASCADE)
    user = models.ForeignKey("tweetApp.TweetUser", verbose_name=("Beğenen Kişi"), on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.user.username
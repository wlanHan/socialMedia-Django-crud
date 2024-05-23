from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TweetUser)
admin.site.register(TweetModel)
admin.site.register(UserFollowers)
admin.site.register(TweetCommentModel)
admin.site.register(BanRecord)
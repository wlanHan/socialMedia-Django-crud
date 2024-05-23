from django import forms
# user model
from .models import TweetUser

# form validation
class UserProfile(forms.ModelForm):

    class Meta:
        model = TweetUser
        fields = ["username", "email", "avatar"]
        help_texts = {

            "username": None
        }
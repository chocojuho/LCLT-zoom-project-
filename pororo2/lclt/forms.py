from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ["first_name","last_name","username", "password1","password2" ,"email"]
        
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name','users','imgfile']
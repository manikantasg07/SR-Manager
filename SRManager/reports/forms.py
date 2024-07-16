from .models import Managers,Tasks,CustomUser,Projectteams,Projects
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Taskform(forms.ModelForm):
    class Meta:
        model=Tasks
        fields="__all__"

class Projectform(forms.ModelForm):
    class Meta:
        model=Projects
        fields="__all__"

class Managerform(forms.ModelForm):
    manager=forms.ModelChoiceField(CustomUser.objects.filter(role="PM"))
    class Meta:
        model=Managers
        fields="__all__"

class Memberform(forms.ModelForm):
    member=forms.ModelChoiceField(CustomUser.objects.filter(role="ME"))
    class Meta:
        model=Projectteams
        fields="__all__"

class Userform(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["first_name","last_name","username",'email',"password1","password2","role"]
from .models import Managers,Tasks,CustomUser,Projectteams
from django import forms

class Taskform(forms.ModelForm):
    class Meta:
        model=Tasks
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

class Userform(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=["username",'email', 'first_name', 'last_name',"role"]
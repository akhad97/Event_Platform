from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *



class OrganizerSignUpForm(UserCreationForm):
  
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_organizer = True
        user.save()
        return user


# class ChatForm(forms.ModelForm):
#     class Meta:
#         model = Chat
#         fields = ('message', )
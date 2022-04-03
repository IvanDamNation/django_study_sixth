from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.forms import ModelForm


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(BaseRegisterForm, self).save()
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class UserFormUpd(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class SubscriptionSendForm(forms.Form):
    subject = forms.CharField(
        label='Topic',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    content = forms.CharField(
        label='Text',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

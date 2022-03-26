from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.forms import ModelForm


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        print('Print login')
        print('self:', self)
        print(type(self))
        user = self.user
        print(user)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return super(CustomLoginForm, self).login(*args, **kwargs)


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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print('Custom group works!')
        return print(user)


class UserFormUpd(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

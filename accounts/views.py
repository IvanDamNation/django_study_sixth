from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from news.models import Category
from .forms import UserFormUpd, BaseRegisterForm
from .models import SubscribersToCategory


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts_user_edit.html'
    form_class = UserFormUpd
    success_url = '/'

    def get_object(self, **kwargs):
        return self.request.user


class SubscribersToCategoryView(SubscribersToCategory):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts_make_subscription.html', {})

    def post(self, request, *args, **kwargs):
        subscribe = SubscribersToCategory(
            date=datetime.strftime(request.POST['date'], '%Y-%m-%d'),
            subscriber=request.POST['user'],
            message=request.POST['message'],
        )
        subscribe.save()

        send_mail(
            subject=f'{subscribe.subscriber} {subscribe.date.strftime("%Y-%m-%d")}',
            message=subscribe.message,
            from_email='fortestapps@yandex.ru',
            recipient_list=['fortestapps@yandex.ru', ]
        )

        return redirect('subscribe:make_subscription')


@login_required
def add_subscribe(request):
    user = request.user
    category = Category.objects.get(pk=request.POST['id'])
    subscribe = SubscribersToCategory(id_user=user, id_category=category)
    subscribe.save()

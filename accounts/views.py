from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from news.models import Category, PostCategory
from .forms import UserFormUpd, BaseRegisterForm, SubscriptionSendForm
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


# Из конспекта куски кода
# class SubscribersToCategoryView(SubscribersToCategory):
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts_make_subscription.html', {})
#
#     def post(self, request, *args, **kwargs):
#         subscribe = SubscribersToCategory(
#             date=datetime.strftime(request.POST['date'], '%Y-%m-%d'),
#             subscriber=request.POST['user'],
#             message=request.POST['message'],
#         )
#         subscribe.save()
#
#         send_mail(
#             subject=f'{subscribe.subscriber} {subscribe.date.strftime("%Y-%m-%d")}',
#             message=subscribe.message,
#             from_email='fortestapps@yandex.ru',
#             recipient_list=['fortestapps@yandex.ru', ]
#         )
#
#         return redirect('subscribe:make_subscription')


@login_required
def add_subscribe(request, pk):
    user = request.user
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    category = Category.objects.get(name=category_object_name)
    subscribe = SubscribersToCategory(subscriber=user, categoryThrough=category)
    subscribe.save()
    return redirect(f'/news/{pk}')


def test_mail(request):
    if request.method == 'POST':
        form = SubscriptionSendForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'fortestapps@yandex.ru',
                ['fortestapps@yandex.ru'],
                fail_silently=False
            )

            if mail:
                messages.success(request, 'Email send successful!')
                return redirect('/')
            else:
                messages.error(request, 'Send error.')

        else:
            messages.error(request, 'Error.')

    else:
        form = SubscriptionSendForm()

    return render(request, 'test.html', {'form': form})

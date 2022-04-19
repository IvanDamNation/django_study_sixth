from datetime import datetime

from allauth.account.views import EmailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

from news.models import Category, PostCategory, Author
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
        author_obj = Author(authorUser=user)
        author_obj.save()
    return redirect('/')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts_user_edit.html'
    form_class = UserFormUpd
    success_url = '/'

    def get_object(self, **kwargs):
        return self.request.user


@login_required
def add_subscribe(request, pk):
    user = request.user
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    category = Category.objects.get(name=category_object_name)
    subscribe = SubscribersToCategory(subscriber=user, categoryThrough=category)
    subscribe.save()
    html_content = render_to_string(
        'accounts_email_make_subscription.html',
        {
            'user': user,
            'category_object_name': category_object_name
        }
    )
    mail = EmailMultiAlternatives(
        subject=f'Hello, {user.username}',
        body='',
        from_email='fortestapps@yandex.ru',
        to=[user.email],
    )
    mail.attach_alternative(html_content, 'text/html')
    mail.send()

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

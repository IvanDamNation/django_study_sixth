from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 5


class PostPermission(PermissionRequiredMixin, PostList):
    permission_required = ('news.add_post', 'news.change_post', )


class PostSearch(PostList):
    template_name = 'news_search.html'

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class PostAdd(PostPermission, PostList):
    template_name = 'news_add.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(authorUser=user)
        form = self.form_class(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = author
            obj.save()

            html_content = render_to_string(
                'accounts_email_new_post.html',
                {
                    'user': user,
                    'title': obj.title,
                    'text': obj.text,
                    'path': obj.pk,
                }
            )
            mail = EmailMultiAlternatives(
                subject=f'Something new for {user.username}',
                body='',
                from_email='fortestapps@yandex.ru',
                to=[user.email],
            )
            mail.attach_alternative(html_content, 'text/html')
            mail.send()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post', )

    def get_object(self, **kwargs):
        editing_news_key = self.kwargs.get('pk')
        return Post.objects.get(pk=editing_news_key)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.add_post', 'news.change_post', )

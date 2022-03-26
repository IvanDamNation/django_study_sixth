from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view(), name='NewsSearch'),
    path('add/', PostAdd.as_view(), name='NewsAdd'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='NewsEdit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='NewsDelete'),

]

from django.db import models
from django.contrib.auth.models import User
from django import forms


class SubscribersToCategory(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey('news.Category', on_delete=models.CASCADE)

    # __reserved
    # def __str__(self):
    #     return '{user}: {category}'.format(user=self.subscriber, category=self.categoryThrough)

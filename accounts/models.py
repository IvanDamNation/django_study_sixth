from django.db import models
from django.contrib.auth.models import User
from django import forms
from news.models import Category


# В news для избежания цикличного импорта?
class SubscribersToCategory(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{user}: {category}'.format(user=self.subscriber, category=self.categoryThrough)

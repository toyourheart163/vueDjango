from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    visited = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

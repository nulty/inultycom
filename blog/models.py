from django.db import models
from django.utils import timezone


# Create your models here.
class BlogArticle(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    body = models.TextField(null=False)
    hero_image = models.CharField(max_length=400, null=True, blank=True)
    slug = models.SlugField()
    featured = models.BooleanField(null=True)
    likes = models.IntegerField("likes", default=0)
    published_at = models.DateTimeField("date published", null=True, blank=True)
    created_at = models.DateTimeField("created at", default=timezone.now)
    updated_at = models.DateTimeField("updated at", default=timezone.now)

from django.db import models
from django.urls import reverse
from django.utils import timezone


class BlogArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_at__isnull=False, published_at__lte=timezone.now())


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

    objects = BlogArticleQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.published_at is not None and self.published_at <= timezone.now()

    def get_absolute_url(self):
        # Gives the admin its "View on site" link, which doubles as draft preview.
        return reverse("show", kwargs={"slug": self.slug})

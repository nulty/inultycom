# Register your models here.
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import BlogArticle


@admin.register(BlogArticle)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "sub_title",
        "body",
        "hero_image",
        "slug",
        "featured",
        "likes",
        "published_at",
        "created_at",
        "updated_at",
    )
    ordering = ["created_at"]
    list_filter = ("featured", "published_at", "created_at", "updated_at")
    list_editable = list_display[1:]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = (
        "slug",
        "title",
        "sub_title",
    )
    date_hierarchy = "created_at"

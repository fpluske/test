from django.contrib import admin
from .models import Category, HomePhoto, NewsPost, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "theme_class", "sort_order")
    list_editable = ("theme_class", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "sort_order")
    list_filter = ("category",)
    list_editable = ("sort_order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("category", "is_published", "published_at")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "content")
    date_hierarchy = "published_at"


@admin.register(HomePhoto)
class HomePhotoAdmin(admin.ModelAdmin):
    list_display = ("image", "title", "sort_order", "is_published", "created_at")
    list_editable = ("sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "alt_text")
    ordering = ("sort_order", "-created_at")

from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True, max_length=50)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=8, default="✦")
    theme_class = models.SlugField(max_length=50, default="elementary")
    chapter = models.CharField(max_length=100)
    lead = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "kategorie"
        verbose_name_plural = "kategorie"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        constraints = [models.UniqueConstraint(fields=["category", "slug"], name="unique_subcategory_slug_per_category")]
        verbose_name = "subkategorie"
        verbose_name_plural = "subkategorie"

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class NewsPost(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news_posts")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        constraints = [models.UniqueConstraint(fields=["category", "slug"], name="unique_news_slug_per_category")]
        verbose_name = "aktualita"
        verbose_name_plural = "aktuality"

    def __str__(self):
        return self.title


class HomePhoto(models.Model):
    image = models.ImageField(upload_to="home_photos/")
    title = models.CharField(max_length=160, blank=True)
    alt_text = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "fotografie na úvodní stránce"
        verbose_name_plural = "fotografie na úvodní stránce"

    def __str__(self):
        return self.title or f"Fotografie {self.pk}"

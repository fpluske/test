from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .models import Category, NewsPost, Subcategory

URL_NAMES = {
    "elementary": "school:elementary",
    "kindergarten": "school:kindergarten",
    "canteen": "school:canteen",
    "club": "school:club",
}
SUB_URL_NAMES = {
    "elementary": "school:elementary_subcategory",
    "kindergarten": "school:kindergarten_subcategory",
    "canteen": "school:canteen_subcategory",
    "club": "school:club_subcategory",
}

def category_data(category):
    return {
        "slug": category.slug,
        "name": category.name,
        "icon": category.icon,
        "class": category.theme_class,
        "chapter": category.chapter,
        "lead": category.lead,
        "url_name": URL_NAMES.get(category.slug, "school:home"),
        "sub_url_name": SUB_URL_NAMES.get(category.slug, "school:home"),
        "links": [(item.slug, item.name) for item in category.subcategories.all()],
    }


def all_categories():
    return [category_data(item) for item in Category.objects.prefetch_related("subcategories")]


def shared_context(active_slug=None):
    return {"categories": all_categories(), "active_slug": active_slug}


def home(request):
    return render(request, "home.html", shared_context())


def error_page(request, exception):
    return render(request, "404.html", shared_context(), status=404)


def category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404("Kategorie nebyla nalezena")
    context = shared_context(slug)
    context["category"] = category_data(category)
    return render(request, "category.html", context)


def subcategory(request, slug, page_slug):
    try:
        category = Category.objects.get(slug=slug)
        page = category.subcategories.get(slug=page_slug)
    except (Category.DoesNotExist, Subcategory.DoesNotExist):
        raise Http404("Podstránka nebyla nalezena")
    context = shared_context(slug)
    context.update({"category": category_data(category), "subcategory": page})
    if page_slug == "aktuality":
        context["news_posts"] = NewsPost.objects.filter(category=category, is_published=True, published_at__lte=timezone.now())
    return render(request, "subcategory.html", context)

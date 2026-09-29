import json
from functools import lru_cache
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.http import Http404, JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Category, HomePhoto, NewsPost, Subcategory

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

LOCAL_HOLIDAYS = {
    (9, 25): "Zlata",
}


@lru_cache(maxsize=7)
def holiday_name(day, month):
    query = urlencode({"date": f"{day}.{month}."})
    for scheme in ("https", "http"):
        request = Request(
            f"{scheme}://svatky.adresa.info/json?{query}",
            headers={"User-Agent": "ZSMSBolatice/1.0"},
        )
        try:
            with urlopen(request, timeout=2) as response:
                holidays = json.load(response)
            if holidays and holidays[0].get("name"):
                return holidays[0]["name"]
        except (OSError, ValueError):
            continue
    return LOCAL_HOLIDAYS.get((month, day), "Svátek dnes není uveden")


def date_context():
    today = timezone.localdate()
    return {
        "today": today,
        "holiday_name": holiday_name(today.day, today.month),
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
    return {"categories": all_categories(), "active_slug": active_slug, **date_context()}


def home(request):
    context = shared_context()
    context["home_photos"] = HomePhoto.objects.filter(is_published=True)
    return render(request, "home.html", context)


def search_page(request):
    query = request.GET.get("q", "").strip()
    is_live_search = request.headers.get("x-requested-with") == "XMLHttpRequest"
    results = []
    if query:
        categories = Category.objects.filter(
            Q(name__icontains=query)
            if is_live_search
            else Q(name__icontains=query) | Q(chapter__icontains=query) | Q(lead__icontains=query)
        )
        for category in categories:
            results.append({
                "title": category.name,
                "type": "Kategorie",
                "excerpt": category.lead,
                "url": reverse(URL_NAMES.get(category.slug, "school:home")),
                "theme": category.theme_class,
            })

        subcategories = Subcategory.objects.filter(
            Q(name__icontains=query)
            if is_live_search
            else Q(name__icontains=query) | Q(content__icontains=query)
        ).select_related("category")
        for subcategory in subcategories:
            results.append({
                "title": subcategory.name,
                "type": subcategory.category.name,
                "excerpt": subcategory.content,
                "url": reverse(
                    SUB_URL_NAMES.get(subcategory.category.slug, "school:home"),
                    kwargs={"page_slug": subcategory.slug},
                ),
                "theme": subcategory.category.theme_class,
            })

        news_posts = NewsPost.objects.filter(
            Q(title__icontains=query)
            if is_live_search
            else Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query),
            is_published=True,
            published_at__lte=timezone.now(),
        ).select_related("category")
        for post in news_posts:
            results.append({
                "title": post.title,
                "type": f"Aktualita · {post.category.name}",
                "excerpt": post.excerpt or post.content,
                "url": reverse(URL_NAMES.get(post.category.slug, "school:home")),
                "theme": post.category.theme_class,
            })

    if is_live_search:
        return JsonResponse({"results": results[:8]})

    context = shared_context()
    context.update({"query": query, "search_results": results})
    return render(request, "search.html", context)


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

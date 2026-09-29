from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path("/", views.home, name="home"),
    path("hledat/", views.search_page, name="search"),
    path("zakladni-skola/", views.category, {"slug": "elementary"}, name="elementary"),
    path("materska-skola/", views.category, {"slug": "kindergarten"}, name="kindergarten"),
    path("skolni-jidelna/", views.category, {"slug": "canteen"}, name="canteen"),
    path("druzina/", views.category, {"slug": "club"}, name="club"),
    path("zakladni-skola/<slug:page_slug>/", views.subcategory, {"slug": "elementary"}, name="elementary_subcategory"),
    path("materska-skola/<slug:page_slug>/", views.subcategory, {"slug": "kindergarten"}, name="kindergarten_subcategory"),
    path("skolni-jidelna/<slug:page_slug>/", views.subcategory, {"slug": "canteen"}, name="canteen_subcategory"),
    path("druzina/<slug:page_slug>/", views.subcategory, {"slug": "club"}, name="club_subcategory"),
]

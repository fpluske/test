from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [path("admin/", admin.site.urls), path("", include("school.urls"))]
urlpatterns += [re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR})]
handler404 = "school.views.error_page"

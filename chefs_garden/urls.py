from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = "Chefs Garden Fiji — Culinary Admin"
admin.site.site_title = "Chefs Garden Fiji Admin"
admin.site.index_title = "Microgreens Catalog, Photos & Wholesale Inquiries"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

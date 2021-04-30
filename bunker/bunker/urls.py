from django.contrib import admin
from django.urls import path
from app.views import api as api_v1
from auth.views import api_auth
from ninja import NinjaAPI
from bunker import settings
from django.conf.urls.static import static

from auth.jwt import AuthBearer

api = NinjaAPI(auth=AuthBearer())
api.add_router("/", api_v1)
api.add_router("/auth/", api_auth)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/", api.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(r'^favicon.ico$', document_root='media/ugolok_logo.png')

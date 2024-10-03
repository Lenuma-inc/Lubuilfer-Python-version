from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main_app import views as main_views

router = routers.DefaultRouter()
router.register(r'packages', main_views.PackageViewSet)
router.register(r'builds', main_views.BuildViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('django_prometheus.urls')),
    path('webhook/', main_views.webhook, name='webhook'),
]

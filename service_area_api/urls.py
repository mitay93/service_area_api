"""
URL configuration for service_area_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework.routers import DefaultRouter
from env import env
from .views import ProviderViewSet, ServiceAreaViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet, basename="providers")
router.register(r'service-areas', ServiceAreaViewSet, basename="service-areas")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls + [path(f"ht/{env('HEALTH_CHECK_TOKEN')}/", include('health_check.urls'))])),
    path('docs/', include([
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/", SpectacularSwaggerView.as_view(), name="swagger")
    ])),
]

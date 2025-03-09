"""
URL configuration for restro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from home.views import (
    RestaurantViewSet, FoodItemViewSet, FoodItemAvailableViewSet,
    NGOViewSet, FoodItemRequirementViewSet, FoodDonationViewSet,
    notify_food_availability, page_view # Add the new view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restro.urls')),
    path('<str:page_name>/', page_view, name='page'),  # Generic pattern for other pages
    path('notify_food_availability/', notify_food_availability, name='notify_food_availability'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register('restaurant', RestaurantViewSet)
router.register('fooditem', FoodItemViewSet)
router.register('item_available', FoodItemAvailableViewSet)
router.register('ngo', NGOViewSet)
router.register('food_requirement', FoodItemRequirementViewSet)
router.register('donation', FoodDonationViewSet)

urlpatterns += router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'foods', views.FoodViewSet)
router.register(r'diet-plan-templates', views.DietPlanTemplateViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'diet-plans', views.DietPlanViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PatientViewSet, 
    FoodViewSet, 
    GenerateDietPlanView, 
    PDFExportView,
    FoodStatisticsView,
    FoodSearchView
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'foods', FoodViewSet, basename='food')

urlpatterns = [
    # Diet Plan Generation
    path('generate-diet-plan/', GenerateDietPlanView.as_view(), name='generate-diet-plan'),
    path('plans/<int:plan_id>/export-pdf/', PDFExportView.as_view(), name='export-pdf'),
    
    # Food Database APIs
    path('foods/statistics/', FoodStatisticsView.as_view(), name='food-statistics'),
    path('foods/search/', FoodSearchView.as_view(), name='food-search'),
    
    # Default router URLs
    path('', include(router.urls)),
]
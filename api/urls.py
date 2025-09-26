from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PatientViewSet, 
    FoodViewSet, 
    GenerateDietPlanView, 
    PDFExportView,
    FoodStatisticsView,
    FoodSearchView,
    PatientDashboardView,
    PatientFeedbackView
)
from .auth_views import register_user, login_user, user_profile, create_demo_users

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'foods', FoodViewSet, basename='food')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/profile/', user_profile, name='profile'),
    path('auth/create-demo-users/', create_demo_users, name='create-demo-users'),
    
    # Patient-specific endpoints
    path('patient/dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('patient/feedback/', PatientFeedbackView.as_view(), name='patient-feedback'),
    
    # Diet Plan Generation (Practitioner)
    path('generate-diet-plan/', GenerateDietPlanView.as_view(), name='generate-diet-plan'),
    path('plans/<int:plan_id>/export-pdf/', PDFExportView.as_view(), name='export-pdf'),
    
    # Food Database APIs
    path('foods/statistics/', FoodStatisticsView.as_view(), name='food-statistics'),
    path('foods/search/', FoodSearchView.as_view(), name='food-search'),
    
    # Default router URLs
    path('', include(router.urls)),
]
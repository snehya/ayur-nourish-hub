from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PatientViewSet, FoodViewSet, GenerateDietPlanView, PDFExportView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'foods', FoodViewSet, basename='food')

urlpatterns = [
    path('generate-diet-plan/', GenerateDietPlanView.as_view(), name='generate-diet-plan'),
    path('plans/<int:plan_id>/export-pdf/', PDFExportView.as_view(), name='export-pdf'),
    path('', include(router.urls)),
]
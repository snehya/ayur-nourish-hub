from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Food, DietPlanTemplate, Patient, DietPlan
from .serializers import FoodSerializer, DietPlanTemplateSerializer, PatientSerializer, DietPlanSerializer


class FoodViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing foods with comprehensive filtering options
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    
    def get_queryset(self):
        queryset = Food.objects.all()
        
        # Filter by food category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(food_category__icontains=category)
        
        # Filter by dosha effects
        vata_effect = self.request.query_params.get('vata_effect', None)
        if vata_effect:
            queryset = queryset.filter(vata_effect__icontains=vata_effect)
            
        pitta_effect = self.request.query_params.get('pitta_effect', None)
        if pitta_effect:
            queryset = queryset.filter(pitta_effect__icontains=pitta_effect)
            
        kapha_effect = self.request.query_params.get('kapha_effect', None)
        if kapha_effect:
            queryset = queryset.filter(kapha_effect__icontains=kapha_effect)
        
        # Filter by virya (heating/cooling)
        virya = self.request.query_params.get('virya', None)
        if virya:
            queryset = queryset.filter(virya__icontains=virya)
        
        # Filter by rasa (taste)
        rasa = self.request.query_params.get('rasa', None)
        if rasa:
            queryset = queryset.filter(rasa__icontains=rasa)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('name')
    
    @action(detail=False, methods=['get'])
    def by_dosha_balance(self, request):
        """
        Get foods that balance a specific dosha
        Usage: /api/foods/by_dosha_balance/?dosha=vata
        """
        dosha = request.query_params.get('dosha', '').lower()
        
        if dosha == 'vata':
            foods = Food.objects.filter(vata_effect__icontains='Balances')
        elif dosha == 'pitta':
            foods = Food.objects.filter(pitta_effect__icontains='Balances')
        elif dosha == 'kapha':
            foods = Food.objects.filter(kapha_effect__icontains='Balances')
        else:
            return Response({'error': 'Please specify dosha parameter (vata, pitta, or kapha)'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(foods, many=True)
        return Response({
            'dosha': dosha.title(),
            'balancing_foods_count': foods.count(),
            'foods': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def food_categories(self, request):
        """
        Get all available food categories
        """
        categories = Food.objects.values_list('food_category', flat=True).distinct()
        categories = [cat for cat in categories if cat]  # Remove None values
        return Response({'categories': sorted(categories)})


class DietPlanTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing diet plan templates
    """
    queryset = DietPlanTemplate.objects.all()
    serializer_class = DietPlanTemplateSerializer
    
    def get_queryset(self):
        queryset = DietPlanTemplate.objects.all()
        
        # Filter by plan type
        plan_type = self.request.query_params.get('plan_type', None)
        if plan_type:
            queryset = queryset.filter(plan_type=plan_type)
        
        # Filter by target dosha
        target_dosha = self.request.query_params.get('target_dosha', None)
        if target_dosha:
            queryset = queryset.filter(target_dosha__icontains=target_dosha)
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Search by name or conditions
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(conditions_treated__icontains=search)
            )
        
        return queryset.order_by('name')
    
    @action(detail=False, methods=['get'])
    def by_condition(self, request):
        """
        Get diet plans for specific health conditions
        Usage: /api/diet-plan-templates/by_condition/?condition=diabetes
        """
        condition = request.query_params.get('condition', '')
        
        if not condition:
            return Response({'error': 'Please specify condition parameter'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        plans = DietPlanTemplate.objects.filter(conditions_treated__icontains=condition)
        serializer = self.get_serializer(plans, many=True)
        
        return Response({
            'condition': condition,
            'matching_plans_count': plans.count(),
            'plans': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def plan_types(self, request):
        """
        Get all available plan types
        """
        plan_types = DietPlanTemplate.objects.values_list('plan_type', flat=True).distinct()
        return Response({'plan_types': list(plan_types)})


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        # Filter by practitioner (assuming authentication)
        return Patient.objects.filter(practitioner=self.request.user).order_by('name')


class DietPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing individual diet plans
    """
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanSerializer
    
    def get_queryset(self):
        queryset = DietPlan.objects.all()
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('-plan_date')
    
    @action(detail=False, methods=['post'])
    def create_from_template(self, request):
        """
        Create a diet plan from a template for a specific patient
        """
        template_id = request.data.get('template_id')
        patient_id = request.data.get('patient_id')
        plan_date = request.data.get('plan_date')
        customizations = request.data.get('customizations', '')
        
        try:
            template = DietPlanTemplate.objects.get(id=template_id)
            patient = Patient.objects.get(id=patient_id)
        except (DietPlanTemplate.DoesNotExist, Patient.DoesNotExist):
            return Response({'error': 'Template or Patient not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Create diet plan from template
        diet_plan = DietPlan.objects.create(
            patient=patient,
            template=template,
            plan_date=plan_date,
            full_plan=template.daily_schedule,
            customizations=customizations,
            practitioner_notes=f"Created from template: {template.name}"
        )
        
        serializer = self.get_serializer(diet_plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

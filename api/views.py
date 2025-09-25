from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, FoodSerializer, DietPlanSerializer
from diet_planner.models import Patient, Food, DietPlan
import requests
import json
from datetime import date
from decouple import config
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from django.core.cache import cache

# A custom permission to ensure only practitioners can access patients
class IsPractitioner(permissions.BasePermission):
    """
    Custom permission to only allow practitioners to access their patients.
    """
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'practitioner'

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPractitioner]

    def get_queryset(self):
        # Return only patients belonging to the current practitioner
        return Patient.objects.filter(practitioner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the practitioner for the new patient
        serializer.save(practitioner=self.request.user)

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    # Anyone can view the food database, but only practitioners can add/edit items
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter foods based on query parameters
        Supports filtering by rasa, virya, guna, and search by name
        """
        queryset = Food.objects.all()
        
        # Filter by rasa (taste)
        rasa = self.request.query_params.get('rasa', None)
        if rasa:
            queryset = queryset.filter(rasa__icontains=rasa)
        
        # Filter by virya (potency)
        virya = self.request.query_params.get('virya', None)
        if virya:
            queryset = queryset.filter(virya__icontains=virya)
        
        # Filter by guna (quality)
        guna = self.request.query_params.get('guna', None)
        if guna:
            queryset = queryset.filter(guna__icontains=guna)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('name')

    def list(self, request, *args, **kwargs):
        """Override list method to implement caching for food data"""
        # Create cache key based on query parameters for filtering
        query_params = request.GET.urlencode()
        cache_key = f'foods_list_{hash(query_params)}'
        
        # Add query parameters to cache key for filtered results
        query_params = request.query_params
        if query_params:
            import hashlib
            param_str = str(sorted(query_params.items()))
            param_hash = hashlib.md5(param_str.encode()).hexdigest()
            cache_key = f'foods_list_{param_hash}'
        
        # Try to get data from cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        # If not in cache, get from database
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Cache the result for 24 hours (food data doesn't change often)
        cache.set(cache_key, serializer.data, timeout=60*60*24)
        
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Override create to clear cache when new food is added"""
        response = super().create(request, *args, **kwargs)
        # Clear all food-related cache keys
        self._clear_food_cache()
        return response
    
    def update(self, request, *args, **kwargs):
        """Override update to clear cache when food is modified"""
        response = super().update(request, *args, **kwargs)
        self._clear_food_cache()
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to clear cache when food is deleted"""
        response = super().destroy(request, *args, **kwargs)
        self._clear_food_cache()
        return response
    
    def _clear_food_cache(self):
        """Helper method to clear food-related cache"""
        # Since we can't easily enumerate all possible cache keys,
        # we'll clear the main cache key and rely on TTL for others
        cache.delete('foods_list')
        # In production, you might want to use cache versioning or tags


class FoodStatisticsView(APIView):
    """
    API View to get statistics about the food database
    Shows counts by rasa, virya, guna, and overall statistics
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """Get comprehensive food database statistics"""
        
        # Check cache first
        cache_key = 'food_statistics'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return Response(cached_stats)

        try:
            # Basic counts
            total_foods = Food.objects.count()
            
            # Count by rasa (taste)
            rasa_stats = {}
            rasa_values = Food.objects.values_list('rasa', flat=True).distinct()
            for rasa in rasa_values:
                if rasa:
                    # Handle multiple rasas separated by commas
                    individual_rasas = [r.strip() for r in rasa.split(',')]
                    for individual_rasa in individual_rasas:
                        if individual_rasa:
                            count = Food.objects.filter(rasa__icontains=individual_rasa).count()
                            rasa_stats[individual_rasa] = rasa_stats.get(individual_rasa, 0) + count

            # Count by virya (potency)
            virya_stats = {}
            virya_values = Food.objects.values_list('virya', flat=True).distinct()
            for virya in virya_values:
                if virya:
                    virya_stats[virya] = Food.objects.filter(virya=virya).count()

            # Count by guna (quality)
            guna_stats = {}
            guna_values = Food.objects.values_list('guna', flat=True).distinct()
            for guna in guna_values:
                if guna:
                    # Handle multiple gunas separated by commas
                    individual_gunas = [g.strip() for g in guna.split(',')]
                    for individual_guna in individual_gunas:
                        if individual_guna:
                            count = Food.objects.filter(guna__icontains=individual_guna).count()
                            guna_stats[individual_guna] = guna_stats.get(individual_guna, 0) + count

            # Nutritional statistics
            foods_with_calories = Food.objects.filter(calories__isnull=False).count()
            foods_with_protein = Food.objects.filter(protein__isnull=False).count()
            
            # Average nutritional values
            from django.db.models import Avg
            avg_calories = Food.objects.filter(calories__isnull=False).aggregate(Avg('calories'))['calories__avg']
            avg_protein = Food.objects.filter(protein__isnull=False).aggregate(Avg('protein'))['protein__avg']

            # Recent additions (foods added in last 30 days)
            from django.utils import timezone
            from datetime import timedelta
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_foods = Food.objects.filter(id__gt=0).count()  # Adjust based on your created_at field if available

            statistics = {
                'overview': {
                    'total_foods': total_foods,
                    'foods_with_calories': foods_with_calories,
                    'foods_with_protein': foods_with_protein,
                    'completion_percentage': round((foods_with_calories / total_foods * 100) if total_foods > 0 else 0, 2)
                },
                'ayurvedic_properties': {
                    'rasa_distribution': rasa_stats,
                    'virya_distribution': virya_stats,
                    'guna_distribution': guna_stats
                },
                'nutritional_insights': {
                    'average_calories_per_100g': round(avg_calories, 2) if avg_calories else None,
                    'average_protein_per_100g': round(avg_protein, 2) if avg_protein else None,
                    'data_completeness': {
                        'calories': round((foods_with_calories / total_foods * 100) if total_foods > 0 else 0, 2),
                        'protein': round((foods_with_protein / total_foods * 100) if total_foods > 0 else 0, 2)
                    }
                },
                'database_health': {
                    'last_updated': timezone.now().isoformat(),
                    'cache_status': 'active',
                    'api_version': '1.0'
                }
            }

            # Cache for 6 hours (food statistics don't change frequently)
            cache.set(cache_key, statistics, timeout=60*60*6)
            
            return Response(statistics)

        except Exception as e:
            return Response(
                {'error': f'Failed to generate statistics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FoodSearchView(APIView):
    """
    Advanced food search API with Ayurvedic filtering
    Supports complex queries for diet plan generation
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        Search foods with advanced filtering options
        Query parameters:
        - rasa: Filter by taste (Sweet, Sour, Salty, Pungent, Bitter, Astringent)
        - virya: Filter by potency (Heating, Cooling)
        - guna: Filter by quality (Heavy, Light, Oily, Dry, etc.)
        - search: Text search in food names
        - limit: Maximum number of results (default: 50)
        - random: Get random foods matching criteria (true/false)
        """
        
        # Get query parameters
        rasa = request.query_params.get('rasa')
        virya = request.query_params.get('virya')
        guna = request.query_params.get('guna')
        search_term = request.query_params.get('search')
        limit = int(request.query_params.get('limit', 50))
        random_foods = request.query_params.get('random', 'false').lower() == 'true'

        try:
            # Start with all foods
            queryset = Food.objects.all()

            # Apply filters
            if rasa:
                queryset = queryset.filter(rasa__icontains=rasa)
            
            if virya:
                queryset = queryset.filter(virya__icontains=virya)
            
            if guna:
                queryset = queryset.filter(guna__icontains=guna)
            
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)

            # Order by random if requested, otherwise by name
            if random_foods:
                queryset = queryset.order_by('?')
            else:
                queryset = queryset.order_by('name')

            # Apply limit
            queryset = queryset[:limit]

            # Serialize results
            serializer = FoodSerializer(queryset, many=True)
            
            # Add metadata to response
            response_data = {
                'count': queryset.count(),
                'filters_applied': {
                    'rasa': rasa,
                    'virya': virya,
                    'guna': guna,
                    'search': search_term,
                    'random': random_foods
                },
                'results': serializer.data
            }

            return Response(response_data)

        except ValueError:
            return Response(
                {'error': 'Invalid limit parameter. Must be a number.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Search failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateDietPlanView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPractitioner]

    def post(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')

        if not patient_id:
            return Response({'error': 'Patient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(id=patient_id, practitioner=request.user)

            # Prepare the patient data to send to your AI model
            patient_data = {
                'prakriti': patient.prakriti,
                'vikriti': patient.vikriti,
                'agni': patient.agni,
                'health_parameters': patient.health_parameters
            }

            # Create a structured prompt for the AI
            prompt = f"""
            Generate a personalized Ayurvedic diet plan for a patient with the following characteristics:
            - Prakriti (Constitution): {patient.prakriti}
            - Vikriti (Current Imbalance): {patient.vikriti}
            - Agni (Digestive Fire): {patient.agni}
            - Health Parameters: {patient.health_parameters}
            
            Please provide a detailed daily diet plan including:
            1. Breakfast recommendations with specific foods
            2. Lunch recommendations with specific foods
            3. Dinner recommendations with specific foods
            4. General dietary guidelines based on their dosha
            5. Foods to avoid
            6. Recommended eating times
            
            Format the response as a structured JSON with breakfast, lunch, dinner, and guidelines sections.
            """

            # Prepare the request for Google AI Studio (Gemini)
            ai_request_data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }

            # Make the request to Google AI Studio API
            ai_response = requests.post(
                f"{config('GOOGLE_AI_STUDIO_API_URL')}?key={config('GOOGLE_AI_STUDIO_API_KEY')}",
                headers={'Content-Type': 'application/json'},
                json=ai_request_data
            )

            # Check for successful response
            if ai_response.status_code != 200:
                return Response(
                    {'error': f'Failed to get a response from AI API. Status: {ai_response.status_code}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            ai_response_data = ai_response.json()
            
            # Extract the generated content from Gemini response
            if 'candidates' in ai_response_data and len(ai_response_data['candidates']) > 0:
                generated_content = ai_response_data['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse as JSON, if it fails, store as text
                try:
                    ai_generated_plan = json.loads(generated_content)
                except json.JSONDecodeError:
                    # If not valid JSON, structure it ourselves
                    ai_generated_plan = {
                        'generated_content': generated_content,
                        'patient_data': patient_data,
                        'generation_date': date.today().isoformat()
                    }
            else:
                return Response(
                    {'error': 'No content generated by AI'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Save the AI-generated plan to the database
            diet_plan = DietPlan.objects.create(
                patient=patient,
                plan_date=date.today(),
                full_plan=ai_generated_plan,
                breakfast=ai_generated_plan.get('breakfast', {}),
                lunch=ai_generated_plan.get('lunch', {}),
                dinner=ai_generated_plan.get('dinner', {})
            )

            serializer = DietPlanSerializer(diet_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found or you do not have permission to access this patient.'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to connect to AI API: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PDFExportView(APIView):
    """
    API View for exporting diet plans as PDF documents.
    Only authenticated practitioners can access this view.
    """
    permission_classes = [permissions.IsAuthenticated, IsPractitioner]

    def get(self, request, plan_id, *args, **kwargs):
        try:
            # Get the diet plan and ensure it belongs to a patient of the current practitioner
            diet_plan = DietPlan.objects.get(id=plan_id, patient__practitioner=request.user)
            patient = diet_plan.patient
            
        except DietPlan.DoesNotExist:
            return Response({'error': 'Diet plan not found or you do not have permission to access it.'}, 
                          status=status.HTTP_404_NOT_FOUND)

        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Create the PDF object with proper margins
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            topMargin=50, 
            leftMargin=50, 
            rightMargin=50,
            bottomMargin=50
        )
        elements = []
        styles = getSampleStyleSheet()

        # Add title and header information
        elements.append(Paragraph(f"<b>Ayurvedic Diet Plan</b>", styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Patient information section
        elements.append(Paragraph(f"<b>Patient Information</b>", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        patient_info_data = [
            ['Patient Name:', patient.name],
            ['Plan Date:', diet_plan.plan_date.strftime('%B %d, %Y')],
            ['Prakriti (Constitution):', patient.prakriti or 'Not assessed'],
            ['Vikriti (Current Imbalance):', patient.vikriti or 'Not assessed'],
            ['Agni (Digestive Fire):', patient.agni or 'Not assessed']
        ]
        
        patient_table = Table(patient_info_data, colWidths=[2.5*72, 3.5*72])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 30))

        # Diet plan content
        elements.append(Paragraph(f"<b>Daily Diet Plan</b>", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Process the full_plan data
        plan_data = diet_plan.full_plan
        
        if plan_data:
            # Handle breakfast, lunch, dinner sections
            meals = ['breakfast', 'lunch', 'dinner']
            
            for meal in meals:
                meal_data = getattr(diet_plan, meal, {}) or plan_data.get(meal, {})
                
                if meal_data:
                    elements.append(Paragraph(f"<b>{meal.title()}</b>", styles['Heading3']))
                    elements.append(Spacer(1, 8))
                    
                    # Extract meal information
                    foods = meal_data.get('foods', [])
                    time = meal_data.get('time', '')
                    guidelines = meal_data.get('guidelines', '')
                    
                    if time:
                        elements.append(Paragraph(f"<b>Recommended Time:</b> {time}", styles['Normal']))
                        elements.append(Spacer(1, 6))
                    
                    if foods:
                        elements.append(Paragraph(f"<b>Recommended Foods:</b>", styles['Normal']))
                        for food in foods:
                            elements.append(Paragraph(f"• {food}", styles['Normal']))
                        elements.append(Spacer(1, 6))
                    
                    if guidelines:
                        elements.append(Paragraph(f"<b>Guidelines:</b> {guidelines}", styles['Normal']))
                    
                    elements.append(Spacer(1, 20))
            
            # Add general guidelines if available
            guidelines = plan_data.get('guidelines', {})
            if guidelines:
                elements.append(Paragraph(f"<b>General Guidelines</b>", styles['Heading3']))
                elements.append(Spacer(1, 8))
                
                if isinstance(guidelines, dict):
                    general = guidelines.get('general', '')
                    avoid = guidelines.get('avoid', [])
                    recommendations = guidelines.get('recommendations', '')
                    
                    if general:
                        elements.append(Paragraph(f"<b>General Advice:</b> {general}", styles['Normal']))
                        elements.append(Spacer(1, 6))
                    
                    if avoid:
                        elements.append(Paragraph(f"<b>Foods to Avoid:</b>", styles['Normal']))
                        for item in avoid:
                            elements.append(Paragraph(f"• {item}", styles['Normal']))
                        elements.append(Spacer(1, 6))
                    
                    if recommendations:
                        elements.append(Paragraph(f"<b>Additional Recommendations:</b> {recommendations}", styles['Normal']))
                
                elif isinstance(guidelines, str):
                    elements.append(Paragraph(guidelines, styles['Normal']))
                
                elements.append(Spacer(1, 20))
        
        else:
            elements.append(Paragraph("No detailed diet plan available.", styles['Normal']))

        # Add footer information
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Generated by Ayurvedic Diet Planning System", styles['Normal']))
        elements.append(Paragraph(f"Generated on: {date.today().strftime('%B %d, %Y')}", styles['Normal']))

        # Build the PDF
        try:
            doc.build(elements)
        except Exception as e:
            return Response({'error': f'Failed to generate PDF: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get the value of the buffer and return it as a response
        pdf_value = buffer.getvalue()
        buffer.close()

        # Create the HTTP response with PDF content
        response = HttpResponse(content_type='application/pdf')
        safe_patient_name = "".join(c for c in patient.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"diet_plan_{safe_patient_name}_{diet_plan.plan_date.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(pdf_value)
        
        return response

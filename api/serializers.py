from rest_framework import serializers
from diet_planner.models import Patient, Food, DietPlan
import re

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'prakriti', 'vikriti', 'agni', 'health_parameters']
    
    def validate_name(self, value):
        """Validate patient name contains only letters, spaces, and basic punctuation"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Name cannot exceed 100 characters.")
        if not re.match(r'^[a-zA-Z\s\.\-\']+$', value):
            raise serializers.ValidationError("Name can only contain letters, spaces, periods, hyphens, and apostrophes.")
        return value.strip()
    
    def validate_prakriti(self, value):
        """Validate prakriti field"""
        valid_prakritis = ['Vata', 'Pitta', 'Kapha']  # Match model choices
        if value and value not in valid_prakritis:
            raise serializers.ValidationError(f"Prakriti must be one of: {', '.join(valid_prakritis)}")
        return value
    
    def validate_vikriti(self, value):
        """Validate vikriti field"""
        valid_vikritis = ['Vata', 'Pitta', 'Kapha']  # Match model choices
        if value and value not in valid_vikritis:
            raise serializers.ValidationError(f"Vikriti must be one of: {', '.join(valid_vikritis)}")
        return value
    
    def validate_agni(self, value):
        """Validate agni field"""
        valid_agni = ['Sama', 'Tikshna', 'Manda', 'Vishama']  # Match model choices
        if value and value not in valid_agni:
            raise serializers.ValidationError(f"Agni must be one of: {', '.join(valid_agni)}")
        return value

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'  # Expose all fields
    
    def validate_name(self, value):
        """Validate food name"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Food name must be at least 2 characters long.")
        if len(value) > 200:
            raise serializers.ValidationError("Food name cannot exceed 200 characters.")
        return value.strip()
    
    def validate_rasa(self, value):
        """Validate rasa (taste)"""
        valid_rasas = ['sweet', 'sour', 'salty', 'pungent', 'bitter', 'astringent']
        if value and value.lower() not in valid_rasas:
            raise serializers.ValidationError(f"Rasa must be one of: {', '.join(valid_rasas)}")
        return value.lower() if value else value
    
    def validate_virya(self, value):
        """Validate virya (energy)"""
        valid_viryas = ['heating', 'cooling']
        if value and value.lower() not in valid_viryas:
            raise serializers.ValidationError(f"Virya must be either 'heating' or 'cooling'")
        return value.lower() if value else value
    
    def validate_vipaka(self, value):
        """Validate vipaka (post-digestive effect)"""
        valid_vipakas = ['sweet', 'sour', 'pungent']
        if value and value.lower() not in valid_vipakas:
            raise serializers.ValidationError(f"Vipaka must be one of: {', '.join(valid_vipakas)}")
        return value.lower() if value else value

class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = '__all__'
    
    def validate_plan_date(self, value):
        """Validate plan date is not in the future beyond reasonable limits"""
        from datetime import date, timedelta
        
        if value < date.today() - timedelta(days=365):
            raise serializers.ValidationError("Plan date cannot be more than 1 year in the past.")
        if value > date.today() + timedelta(days=365):
            raise serializers.ValidationError("Plan date cannot be more than 1 year in the future.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Ensure the practitioner is the owner of the patient
        if 'patient' in data and hasattr(data['patient'], 'practitioner'):
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                if data['patient'].practitioner != request.user:
                    raise serializers.ValidationError("You can only create diet plans for your own patients.")
        
        return data
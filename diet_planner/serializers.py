from rest_framework import serializers
from .models import Food, DietPlanTemplate, Patient, DietPlan


class FoodSerializer(serializers.ModelSerializer):
    """
    Serializer for Food model with all nutritional and Ayurvedic properties
    """
    class Meta:
        model = Food
        fields = [
            'id', 'name', 'food_category', 'calories', 'protein', 'carbs', 'fat',
            'rasa', 'virya', 'vipaka', 'guna', 'vata_effect', 'pitta_effect', 
            'kapha_effect', 'digestibility', 'used_in_plans', 'seasonal_use',
            'therapeutic_use', 'contraindications'
        ]


class DietPlanTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for DietPlanTemplate model
    """
    class Meta:
        model = DietPlanTemplate
        fields = [
            'id', 'name', 'plan_type', 'target_dosha', 'conditions_treated',
            'principle', 'daily_schedule', 'meal_guidelines', 'foods_to_favor',
            'foods_to_avoid', 'key_points', 'seasonal_adjustments',
            'therapeutic_foods', 'difficulty_level'
        ]


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    practitioner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'practitioner', 'name', 'prakriti', 'vikriti', 'agni',
            'health_parameters'
        ]
    
    def create(self, validated_data):
        # Set the practitioner to the current user
        validated_data['practitioner'] = self.context['request'].user
        return super().create(validated_data)


class DietPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for DietPlan model
    """
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    template = DietPlanTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = DietPlan
        fields = [
            'id', 'patient', 'patient_id', 'template', 'template_id',
            'plan_date', 'breakfast', 'lunch', 'dinner', 'snacks',
            'full_plan', 'customizations', 'practitioner_notes',
            'is_active'
        ]


class DietPlanCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating diet plans from templates
    """
    template_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    
    class Meta:
        model = DietPlan
        fields = [
            'template_id', 'patient_id', 'plan_date', 'customizations'
        ]
from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model we will define later
User = get_user_model()

# Constants for Ayurvedic choices
DOSHA_CHOICES = [
    ('Vata', 'Vata'),
    ('Pitta', 'Pitta'),
    ('Kapha', 'Kapha'),
]

AGNI_CHOICES = [
    ('Tikshna', 'Tikshna'),
    ('Manda', 'Manda'),
    ('Vishama', 'Vishama'),
    ('Sama', 'Sama'),
]

# Model for individual food items with comprehensive nutritional and Ayurvedic data
class Food(models.Model):
    # Basic information
    name = models.CharField(max_length=200, unique=True, db_index=True)
    food_category = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    # Nutritional information (per 100g)
    calories = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protein = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    carbs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fat = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Ayurvedic properties
    rasa = models.CharField(max_length=200, null=True, blank=True, db_index=True)  # Taste
    virya = models.CharField(max_length=100, null=True, blank=True, db_index=True)  # Potency (Heating/Cooling)
    vipaka = models.CharField(max_length=100, null=True, blank=True)  # Post-digestive effect
    guna = models.CharField(max_length=200, null=True, blank=True)  # Qualities
    
    # Dosha effects
    vata_effect = models.CharField(max_length=100, null=True, blank=True, db_index=True)  # Increases/Balances/Decreases
    pitta_effect = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    kapha_effect = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    # Digestibility and usage
    digestibility = models.CharField(max_length=200, null=True, blank=True)
    used_in_plans = models.TextField(null=True, blank=True)  # Which diet plans this food is used in
    
    # Additional properties
    seasonal_use = models.CharField(max_length=200, null=True, blank=True)
    therapeutic_use = models.TextField(null=True, blank=True)
    contraindications = models.TextField(null=True, blank=True)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['food_category']),
            models.Index(fields=['rasa', 'virya']),
            models.Index(fields=['vata_effect', 'pitta_effect', 'kapha_effect']),
        ]

    def __str__(self):
        return self.name

# Model for a patient profile
class Patient(models.Model):
    practitioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=200, db_index=True)  # Index for patient name searches
    prakriti = models.CharField(max_length=50, choices=DOSHA_CHOICES, null=True, blank=True, db_index=True)
    vikriti = models.CharField(max_length=50, choices=DOSHA_CHOICES, null=True, blank=True, db_index=True)
    agni = models.CharField(max_length=50, choices=AGNI_CHOICES, null=True, blank=True)
    health_parameters = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=['practitioner', 'name']),  # Composite index for practitioner's patients
            models.Index(fields=['prakriti']),
        ]

    def __str__(self):
        return self.name

# Model for pre-defined Ayurvedic diet plan templates
class DietPlanTemplate(models.Model):
    PLAN_TYPE_CHOICES = [
        ('dosha_balance', 'Dosha Balance'),
        ('dual_constitution', 'Dual Constitution'),
        ('therapeutic', 'Therapeutic'),
        ('seasonal', 'Seasonal'),
        ('detox', 'Detoxification'),
    ]
    
    # Basic information
    name = models.CharField(max_length=200, unique=True, db_index=True)
    plan_type = models.CharField(max_length=50, choices=PLAN_TYPE_CHOICES, db_index=True)
    target_dosha = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    conditions_treated = models.TextField(null=True, blank=True)
    
    # Plan structure
    principle = models.TextField()  # Core Ayurvedic principle behind the plan
    daily_schedule = models.JSONField()  # Complete meal timing and structure
    meal_guidelines = models.JSONField()  # Detailed meal recommendations
    
    # Foods to favor and avoid
    foods_to_favor = models.TextField()
    foods_to_avoid = models.TextField()
    
    # Additional guidance
    key_points = models.TextField(null=True, blank=True)
    seasonal_adjustments = models.TextField(null=True, blank=True)
    therapeutic_foods = models.TextField(null=True, blank=True)
    
    # Metadata
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='intermediate')
    
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['plan_type', 'target_dosha']),
            models.Index(fields=['difficulty_level']),
        ]
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.plan_type})"

# Model for a specific diet plan assigned to a patient
class DietPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diet_plans')
    template = models.ForeignKey(DietPlanTemplate, on_delete=models.CASCADE, null=True, blank=True)
    plan_date = models.DateField(db_index=True)
    
    # Meal structure
    breakfast = models.JSONField(default=dict)
    lunch = models.JSONField(default=dict)
    dinner = models.JSONField(default=dict)
    snacks = models.JSONField(default=dict)
    
    # Complete plan with timing and instructions
    full_plan = models.JSONField(default=dict)
    
    # Customizations for individual patient
    customizations = models.TextField(null=True, blank=True)
    practitioner_notes = models.TextField(null=True, blank=True)
    
    # Status tracking
    is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['patient', 'plan_date']),
            models.Index(fields=['-plan_date']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-plan_date']

    def __str__(self):
        return f"Diet plan for {self.patient.name} on {self.plan_date}"

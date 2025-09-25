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

# Model for individual food items
class Food(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)  # Add index for faster searches
    calories = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protein = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # Ayurvedic properties
    rasa = models.CharField(max_length=50, null=True, blank=True, db_index=True) # Six tastes - indexed for filtering
    guna = models.CharField(max_length=50, null=True, blank=True) # Qualities (e.g., heavy, light)
    virya = models.CharField(max_length=50, null=True, blank=True, db_index=True) # Potency (Hot/Cold) - indexed

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['rasa', 'virya']),  # Composite index for Ayurvedic filtering
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

# Model for a specific diet plan
class DietPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diet_plans')
    plan_date = models.DateField(db_index=True)  # Index for date-based queries
    breakfast = models.JSONField(default=dict)
    lunch = models.JSONField(default=dict)
    dinner = models.JSONField(default=dict)
    # Add a JSONField for the full plan, including snack times, notes, etc.
    full_plan = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=['patient', 'plan_date']),  # Composite index for patient's plans by date
            models.Index(fields=['-plan_date']),  # Index for recent plans (descending order)
        ]
        ordering = ['-plan_date']  # Default ordering by most recent plans

    def __str__(self):
        return f"Diet plan for {self.patient.name} on {self.plan_date}"

# api/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
from users.models import CustomUser
from diet_planner.models import Patient, Food, DietPlan
from datetime import date, timedelta
import json

class GenerateDietPlanTest(APITestCase):
    def setUp(self):
        """Set up test data for diet plan generation tests"""
        # Clear cache before each test
        cache.clear()
        
        # Create a practitioner and log them in
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        self.client.force_authenticate(user=self.practitioner)

        # Create a patient for the test
        self.patient = Patient.objects.create(
            name='Test Patient',
            practitioner=self.practitioner,
            prakriti='Vata',
            vikriti='Pitta',
            agni='Sama'
        )

        # Create some test foods
        self.test_foods = [
            Food.objects.create(name='Brown Rice', rasa='sweet', virya='cooling', calories=216),
            Food.objects.create(name='Quinoa', rasa='sweet', virya='heating', calories=222),
            Food.objects.create(name='Spinach', rasa='astringent', virya='cooling', calories=23),
        ]

        # Get the URL for diet plan generation
        self.generate_url = reverse('generate-diet-plan')

    def test_generate_diet_plan_success(self):
        """Test successful diet plan generation"""
        data = {'patient_id': self.patient.id}
        response = self.client.post(self.generate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('generated_plan', response.data)
        self.assertEqual(int(response.data['generated_plan']['patient_id']), self.patient.id)

    def test_generate_diet_plan_invalid_patient(self):
        """Test diet plan generation with invalid patient ID"""
        data = {'patient_id': 99999}  # Non-existent patient
        response = self.client.post(self.generate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_generate_diet_plan_unauthorized(self):
        """Test diet plan generation without authentication"""
        self.client.force_authenticate(user=None)  # Remove authentication
        data = {'patient_id': self.patient.id}
        response = self.client.post(self.generate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_generate_diet_plan_different_practitioner(self):
        """Test diet plan generation for patient of different practitioner"""
        # Create another practitioner
        other_practitioner = CustomUser.objects.create_user(
            username='other_practitioner',
            email='other@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        
        # Create patient for other practitioner
        other_patient = Patient.objects.create(
            name='Other Patient',
            practitioner=other_practitioner,
            prakriti='Kapha'
        )

        data = {'patient_id': other_patient.id}
        response = self.client.post(self.generate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PatientViewSetTest(APITestCase):
    def setUp(self):
        """Set up test data for patient tests"""
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        self.client.force_authenticate(user=self.practitioner)

        self.patient_data = {
            'name': 'John Doe',
            'prakriti': 'Vata',
            'vikriti': 'Pitta',
            'agni': 'Sama'
        }

    def test_create_patient_success(self):
        """Test successful patient creation"""
        url = reverse('patient-list')
        response = self.client.post(url, self.patient_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['prakriti'], 'Vata')

    def test_create_patient_invalid_data(self):
        """Test patient creation with invalid data"""
        url = reverse('patient-list')
        invalid_data = {
            'name': 'A',  # Too short
            'prakriti': 'InvalidDosha',  # Invalid choice
            'agni': 'InvalidAgni'  # Invalid choice
        }
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('prakriti', response.data)

    def test_list_patients_own_only(self):
        """Test that practitioners only see their own patients"""
        # Create patient for current practitioner
        Patient.objects.create(
            name='My Patient',
            practitioner=self.practitioner,
            prakriti='Vata'
        )

        # Create another practitioner and patient
        other_practitioner = CustomUser.objects.create_user(
            username='other_practitioner',
            email='other@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        Patient.objects.create(
            name='Other Patient',
            practitioner=other_practitioner,
            prakriti='Pitta'
        )

        url = reverse('patient-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'My Patient')


class FoodViewSetTest(APITestCase):
    def setUp(self):
        """Set up test data for food tests"""
        cache.clear()  # Clear cache before each test
        
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )

        # Create test foods
        self.food1 = Food.objects.create(
            name='Brown Rice',
            rasa='sweet',
            virya='cooling',
            calories=216
        )
        self.food2 = Food.objects.create(
            name='Quinoa',
            rasa='sweet',
            virya='heating',
            calories=222
        )

    def test_list_foods_anonymous(self):
        """Test that anonymous users can view foods"""
        url = reverse('food-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_food_authenticated(self):
        """Test food creation by authenticated practitioner"""
        self.client.force_authenticate(user=self.practitioner)
        url = reverse('food-list')
        food_data = {
            'name': 'Organic Spinach',
            'rasa': 'astringent',
            'virya': 'cooling',
            'calories': 23
        }
        response = self.client.post(url, food_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Organic Spinach')

    def test_create_food_invalid_data(self):
        """Test food creation with invalid data"""
        self.client.force_authenticate(user=self.practitioner)
        url = reverse('food-list')
        invalid_food_data = {
            'name': 'A',  # Too short
            'rasa': 'invalid_taste',  # Invalid rasa
            'virya': 'invalid_energy'  # Invalid virya
        }
        response = self.client.post(url, invalid_food_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('rasa', response.data)

    def test_food_caching(self):
        """Test that food list is properly cached"""
        url = reverse('food-list')
        
        # First request should hit database
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second request should hit cache (same data)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data, response2.data)


class PDFExportTest(APITestCase):
    def setUp(self):
        """Set up test data for PDF export tests"""
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        self.client.force_authenticate(user=self.practitioner)

        self.patient = Patient.objects.create(
            name='Test Patient',
            practitioner=self.practitioner,
            prakriti='Vata',
            vikriti='Pitta'
        )

        self.diet_plan = DietPlan.objects.create(
            patient=self.patient,
            plan_date=date.today(),
            breakfast={'foods': ['Oatmeal', 'Almonds']},
            lunch={'foods': ['Rice', 'Dal', 'Vegetables']},
            dinner={'foods': ['Soup', 'Bread']}
        )

    def test_pdf_export_success(self):
        """Test successful PDF export"""
        url = reverse('export-pdf', kwargs={'plan_id': self.diet_plan.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_pdf_export_invalid_plan(self):
        """Test PDF export with invalid plan ID"""
        url = reverse('export-pdf', kwargs={'plan_id': 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pdf_export_unauthorized(self):
        """Test PDF export without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('export-pdf', kwargs={'plan_id': self.diet_plan.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ValidationTest(APITestCase):
    def setUp(self):
        """Set up test data for validation tests"""
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        self.client.force_authenticate(user=self.practitioner)

    def test_patient_name_validation(self):
        """Test patient name validation rules"""
        url = reverse('patient-list')
        
        # Test short name
        response = self.client.post(url, {'name': 'A'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid characters
        response = self.client.post(url, {'name': 'John@123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test valid name
        response = self.client.post(url, {'name': 'John Doe'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ayurvedic_validation(self):
        """Test Ayurvedic field validation"""
        url = reverse('patient-list')
        
        # Test invalid prakriti
        response = self.client.post(url, {
            'name': 'John Doe',
            'prakriti': 'InvalidDosha'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test valid Ayurvedic fields
        response = self.client.post(url, {
            'name': 'John Doe',
            'prakriti': 'Vata',
            'vikriti': 'Pitta',
            'agni': 'Sama'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SecurityTest(APITestCase):
    def setUp(self):
        """Set up test data for security tests"""
        self.practitioner = CustomUser.objects.create_user(
            username='test_practitioner',
            email='prac@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        
        self.regular_user = CustomUser.objects.create_user(
            username='regular_user',
            email='user@test.com',
            password='testpassword',
            user_type='patient'  # Not a practitioner
        )

    def test_practitioner_only_endpoints(self):
        """Test that practitioner-only endpoints reject non-practitioners"""
        # Test with regular user (not practitioner)
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authentication_required(self):
        """Test that protected endpoints require authentication"""
        # No authentication
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_data_isolation(self):
        """Test that practitioners can only access their own data"""
        # Create two practitioners with their own patients
        practitioner1 = self.practitioner
        practitioner2 = CustomUser.objects.create_user(
            username='practitioner2',
            email='prac2@test.com',
            password='testpassword',
            user_type='practitioner'
        )
        
        patient1 = Patient.objects.create(
            name='Patient 1',
            practitioner=practitioner1
        )
        patient2 = Patient.objects.create(
            name='Patient 2',
            practitioner=practitioner2
        )
        
        # Authenticate as practitioner1
        self.client.force_authenticate(user=practitioner1)
        url = reverse('patient-list')
        response = self.client.get(url)
        
        # Should only see own patient
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Patient 1')

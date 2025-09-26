from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user (practitioner or patient)
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return JWT token with user type
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user_type = request.data.get('user_type')  # Optional filter
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        # If user_type is specified, verify it matches
        if user_type and user.user_type != user_type:
            return Response({
                'error': f'Invalid credentials for {user_type} login'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def user_profile(request):
    """
    Get current user profile
    """
    if not request.user.is_authenticated:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_demo_users(request):
    """
    Create demo users for testing (DEMO ONLY - REMOVE IN PRODUCTION)
    """
    demo_users = []
    
    # Create demo practitioner
    practitioner, created = User.objects.get_or_create(
        username='dr_sharma',
        defaults={
            'email': 'dr.sharma@ayurdiet.com',
            'first_name': 'Rajesh',
            'last_name': 'Sharma',
            'user_type': 'practitioner',
        }
    )
    if created:
        practitioner.set_password('demo123')
        practitioner.save()
        demo_users.append('dr_sharma (practitioner)')
    
    # Create demo patient
    patient, created = User.objects.get_or_create(
        username='patient_ravi',
        defaults={
            'email': 'ravi@example.com',
            'first_name': 'Ravi',
            'last_name': 'Kumar',
            'user_type': 'patient',
        }
    )
    if created:
        patient.set_password('demo123')
        patient.save()
        demo_users.append('patient_ravi (patient)')
    
    return Response({
        'message': 'Demo users created successfully',
        'users': demo_users,
        'credentials': {
            'practitioner': {'username': 'dr_sharma', 'password': 'demo123'},
            'patient': {'username': 'patient_ravi', 'password': 'demo123'}
        }
    })
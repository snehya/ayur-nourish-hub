// frontend/src/config/api.js
// API Configuration for AyurDiet Pro Frontend

// Environment-based API configuration
const API_CONFIG = {
  development: {
    BASE_URL: 'http://localhost:8000/api',
    TIMEOUT: 10000, // 10 seconds
  },
  production: {
    BASE_URL: 'https://your-backend-url.com/api', // Update with your production URL
    TIMEOUT: 15000, // 15 seconds for production
  }
};

// Get current environment
const ENV = process.env.NODE_ENV || 'development';
const config = API_CONFIG[ENV];

// API endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/token/',
  REFRESH_TOKEN: '/token/refresh/',
  
  // User Management
  REGISTER: '/users/', // If you add user registration endpoint
  PROFILE: '/users/profile/', // If you add user profile endpoint
  
  // Patient Management
  PATIENTS: '/patients/',
  PATIENT_DETAIL: (id) => `/patients/${id}/`,
  
  // Food Management
  FOODS: '/foods/',
  FOOD_DETAIL: (id) => `/foods/${id}/`,
  
  // Diet Plan Management
  DIET_PLANS: '/plans/',
  DIET_PLAN_DETAIL: (id) => `/plans/${id}/`,
  GENERATE_DIET_PLAN: '/generate-diet-plan/',
  
  // PDF Export
  EXPORT_PDF: (planId) => `/plans/${planId}/export-pdf/`,
  
  // Documentation (for development)
  DOCS_SWAGGER: '/schema/swagger-ui/',
  DOCS_REDOC: '/schema/redoc/',
  DOCS_SCHEMA: '/schema/',
};

// Export configuration
export const API_BASE_URL = config.BASE_URL;
export const API_TIMEOUT = config.TIMEOUT;

// Helper function to build full URLs
export const buildApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

// Export default configuration
export default {
  BASE_URL: API_BASE_URL,
  TIMEOUT: API_TIMEOUT,
  ENDPOINTS: API_ENDPOINTS,
  buildUrl: buildApiUrl,
};
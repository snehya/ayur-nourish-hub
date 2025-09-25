// API Configuration for AyurDiet Pro Frontend

interface ApiConfig {
  BASE_URL: string;
  TIMEOUT: number;
}

// Environment-based API configuration
const API_CONFIG: Record<string, ApiConfig> = {
  development: {
    BASE_URL: 'http://localhost:8000/api',
    TIMEOUT: 10000, // 10 seconds
  },
  production: {
    BASE_URL: 'https://your-backend-url.com/api', // Update with your production URL
    TIMEOUT: 15000, // 15 seconds for production
  }
};

// Get current environment (using Vite's import.meta.env)
const ENV = typeof window !== 'undefined' ? 'development' : 'development';
const config = API_CONFIG[ENV] || API_CONFIG.development;

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
  PATIENT_DETAIL: (id: string | number) => `/patients/${id}/`,
  
  // Food Management
  FOODS: '/foods/',
  FOOD_DETAIL: (id: string | number) => `/foods/${id}/`,
  
  // Diet Plan Management
  DIET_PLANS: '/plans/',
  DIET_PLAN_DETAIL: (id: string | number) => `/plans/${id}/`,
  GENERATE_DIET_PLAN: '/generate-diet-plan/',
  
  // PDF Export
  EXPORT_PDF: (planId: string | number) => `/plans/${planId}/export-pdf/`,
  
  // Documentation (for development)
  DOCS_SWAGGER: '/schema/swagger-ui/',
  DOCS_REDOC: '/schema/redoc/',
  DOCS_SCHEMA: '/schema/',
};

// Export configuration
export const API_BASE_URL = config.BASE_URL;
export const API_TIMEOUT = config.TIMEOUT;

// Helper function to build full URLs
export const buildApiUrl = (endpoint: string): string => {
  return `${config.BASE_URL}${endpoint}`;
};

// Export default configuration
export default {
  baseURL: config.BASE_URL,
  timeout: config.TIMEOUT,
  endpoints: API_ENDPOINTS,
  buildUrl: buildApiUrl,
};
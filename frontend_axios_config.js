// frontend/src/services/axiosConfig.js
// Axios Configuration for AyurDiet Pro

import axios from 'axios';
import { API_BASE_URL, API_TIMEOUT } from '../config/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage (or your preferred storage)
    const token = localStorage.getItem('ayurdiet_access_token');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log API calls in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`🌐 API Call: ${config.method?.toUpperCase()} ${config.url}`);
    }
    
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle common responses and errors
apiClient.interceptors.response.use(
  (response) => {
    // Log successful responses in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ API Success: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    }
    
    return response;
  },
  (error) => {
    // Handle common error cases
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // Unauthorized - token expired or invalid
          console.warn('🔒 Authentication required - redirecting to login');
          localStorage.removeItem('ayurdiet_access_token');
          localStorage.removeItem('ayurdiet_refresh_token');
          
          // Redirect to login (you'll need to implement this based on your routing)
          // window.location.href = '/login';
          break;
          
        case 403:
          // Forbidden - user doesn't have permission
          console.error('🚫 Access forbidden');
          break;
          
        case 404:
          // Not found
          console.error('🔍 Resource not found');
          break;
          
        case 429:
          // Rate limited
          console.error('⏰ Too many requests - please slow down');
          break;
          
        case 500:
          // Server error
          console.error('🔥 Server error - please try again later');
          break;
          
        default:
          console.error(`❌ API Error (${status}):`, data);
      }
    } else if (error.request) {
      // Network error
      console.error('🌐 Network Error:', error.message);
    } else {
      // Something else happened
      console.error('❌ Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
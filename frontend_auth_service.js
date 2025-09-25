// frontend/src/services/authService.js
// Authentication Service for AyurDiet Pro

import apiClient from './axiosConfig';
import { API_ENDPOINTS } from '../config/api';

class AuthService {
  constructor() {
    this.TOKEN_KEY = 'ayurdiet_access_token';
    this.REFRESH_TOKEN_KEY = 'ayurdiet_refresh_token';
    this.USER_KEY = 'ayurdiet_user';
  }

  // Login user
  async login(username, password) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.LOGIN, {
        username,
        password,
      });

      const { access, refresh } = response.data;
      
      // Store tokens
      this.setTokens(access, refresh);
      
      // Decode and store user info (optional)
      const userInfo = this.decodeToken(access);
      localStorage.setItem(this.USER_KEY, JSON.stringify(userInfo));
      
      console.log('✅ Login successful');
      return { success: true, user: userInfo };
      
    } catch (error) {
      console.error('❌ Login failed:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  }

  // Refresh token
  async refreshToken() {
    try {
      const refreshToken = this.getRefreshToken();
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await apiClient.post(API_ENDPOINTS.REFRESH_TOKEN, {
        refresh: refreshToken,
      });

      const { access } = response.data;
      localStorage.setItem(this.TOKEN_KEY, access);
      
      console.log('✅ Token refreshed');
      return access;
      
    } catch (error) {
      console.error('❌ Token refresh failed:', error);
      this.logout();
      throw error;
    }
  }

  // Logout user
  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    console.log('✅ Logged out');
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = this.getAccessToken();
    if (!token) return false;
    
    // Check if token is expired
    try {
      const payload = this.decodeToken(token);
      const currentTime = Date.now() / 1000;
      
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  // Get access token
  getAccessToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  // Get refresh token
  getRefreshToken() {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  // Get current user
  getCurrentUser() {
    const userStr = localStorage.getItem(this.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }

  // Set tokens
  setTokens(accessToken, refreshToken) {
    localStorage.setItem(this.TOKEN_KEY, accessToken);
    if (refreshToken) {
      localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
    }
  }

  // Decode JWT token (simple base64 decode - for display purposes only)
  decodeToken(token) {
    try {
      const payload = token.split('.')[1];
      const decoded = atob(payload);
      return JSON.parse(decoded);
    } catch (error) {
      console.error('❌ Token decode error:', error);
      return null;
    }
  }

  // Get user type (practitioner/patient)
  getUserType() {
    const user = this.getCurrentUser();
    return user?.user_type || null;
  }

  // Check if user is practitioner
  isPractitioner() {
    return this.getUserType() === 'practitioner';
  }

  // Check if user is patient
  isPatient() {
    return this.getUserType() === 'patient';
  }
}

// Export singleton instance
const authService = new AuthService();
export default authService;
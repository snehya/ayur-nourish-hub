// Authentication service for AyurDiet Pro
import apiClient, { tokenManager } from '../api/client';
import { API_ENDPOINTS } from '../api/config';

// Types for authentication
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  user_type: 'practitioner' | 'patient';
  is_staff: boolean;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
}

class AuthService {
  /**
   * Login user with username and password
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await apiClient.post<LoginResponse>(API_ENDPOINTS.LOGIN, credentials);
      const { access, refresh } = response.data;
      
      // Store tokens
      tokenManager.setToken(access);
      tokenManager.setRefreshToken(refresh);
      
      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Login failed. Please check your credentials.');
    }
  }

  /**
   * Logout user and clear tokens
   */
  async logout(): Promise<void> {
    try {
      // Clear tokens from storage
      tokenManager.clearTokens();
      
      // You could also call a logout endpoint if your backend has one
      // await apiClient.post('/logout/');
      
    } catch (error) {
      // Even if logout fails, clear local tokens
      tokenManager.clearTokens();
      console.error('Logout error:', error);
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(): Promise<string> {
    const refreshToken = tokenManager.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await apiClient.post<{ access: string }>(
        API_ENDPOINTS.REFRESH_TOKEN, 
        { refresh: refreshToken }
      );
      
      const newToken = response.data.access;
      tokenManager.setToken(newToken);
      
      return newToken;
    } catch (error) {
      // Refresh failed, clear tokens
      tokenManager.clearTokens();
      throw new Error('Token refresh failed. Please login again.');
    }
  }

  /**
   * Get current authentication state
   */
  getAuthState(): AuthState {
    const token = tokenManager.getToken();
    const isAuthenticated = tokenManager.hasValidToken();
    
    let user: User | null = null;
    
    if (token && isAuthenticated) {
      try {
        // Decode JWT payload to get user info
        const payload = JSON.parse(atob(token.split('.')[1]));
        user = {
          id: payload.user_id,
          username: payload.username || '',
          email: payload.email || '',
          user_type: payload.user_type || 'patient',
          is_staff: payload.is_staff || false,
        };
      } catch (error) {
        console.error('Error decoding token:', error);
      }
    }

    return {
      isAuthenticated,
      user,
      token,
    };
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return tokenManager.hasValidToken();
  }

  /**
   * Get current access token
   */
  getAccessToken(): string | null {
    return tokenManager.getToken();
  }

  /**
   * Get current user information from token
   */
  getCurrentUser(): User | null {
    const authState = this.getAuthState();
    return authState.user;
  }

  /**
   * Check if current user is a practitioner
   */
  isPractitioner(): boolean {
    const user = this.getCurrentUser();
    return user?.user_type === 'practitioner' || false;
  }

  /**
   * Check if current user is a patient
   */
  isPatient(): boolean {
    const user = this.getCurrentUser();
    return user?.user_type === 'patient' || false;
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService;
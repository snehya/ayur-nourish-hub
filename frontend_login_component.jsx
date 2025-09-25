// frontend/src/components/LoginForm.jsx
// Login Form Component for AyurDiet Pro

import React, { useState } from 'react';
import authService from '../services/authService';

const LoginForm = ({ onLoginSuccess }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await authService.login(formData.username, formData.password);
      
      if (result.success) {
        console.log('✅ Login successful:', result.user);
        // Call parent component's success handler
        if (onLoginSuccess) {
          onLoginSuccess(result.user);
        }
        // Or redirect programmatically
        // window.location.href = '/dashboard';
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('Login failed. Please try again.');
      console.error('❌ Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <div className="login-form">
        <h2>Login to AyurDiet Pro</h2>
        
        {error && (
          <div className="error-message" style={{ color: 'red', marginBottom: '1rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Enter your username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Enter your password"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="login-button"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="login-help">
          <p>Demo Credentials:</p>
          <p>Username: <strong>sneha</strong> | Password: <strong>password123</strong></p>
        </div>
      </div>

      <style jsx>{`
        .login-form-container {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
          background-color: #f5f5f5;
        }
        
        .login-form {
          background: white;
          padding: 2rem;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          width: 100%;
          max-width: 400px;
        }
        
        .form-group {
          margin-bottom: 1rem;
        }
        
        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: bold;
        }
        
        input {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
        }
        
        input:disabled {
          background-color: #f5f5f5;
          cursor: not-allowed;
        }
        
        .login-button {
          width: 100%;
          padding: 0.75rem;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 1rem;
          cursor: pointer;
          transition: background-color 0.3s;
        }
        
        .login-button:hover:not(:disabled) {
          background-color: #0056b3;
        }
        
        .login-button:disabled {
          background-color: #6c757d;
          cursor: not-allowed;
        }
        
        .login-help {
          margin-top: 1rem;
          padding-top: 1rem;
          border-top: 1px solid #eee;
          text-align: center;
          font-size: 0.9rem;
          color: #666;
        }
      `}</style>
    </div>
  );
};

export default LoginForm;
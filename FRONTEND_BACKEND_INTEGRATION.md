# 🚀 FRONTEND-BACKEND INTEGRATION GUIDE

## ✅ **BACKEND STATUS: READY!**
- ✅ Django server running on http://localhost:8000
- ✅ Supabase PostgreSQL connected with 117 foods
- ✅ CORS configured for frontend requests
- ✅ All API endpoints working

## 🔗 **API ENDPOINTS FOR FRONTEND**

### **Base URL**
```javascript
const API_BASE_URL = 'http://localhost:8000/api'; // Development
```

### **1. Food Data APIs**
```javascript
// Get all foods
GET /api/foods/
Response: [
  {
    "id": 1,
    "name": "Basmati Rice",
    "calories": 130,
    "protein": 2.7,
    "rasa": "Sweet",
    "virya": "Cooling",
    "guna": "Light, Easy to digest"
  }
]

// Search foods by properties
GET /api/foods/search/?virya=Cooling
GET /api/foods/search/?rasa=Sweet
GET /api/foods/search/?name=rice

// Get food statistics
GET /api/foods/statistics/
Response: {
  "total_foods": 117,
  "virya_distribution": {"Cooling": 49, "Heating": 68},
  "rasa_distribution": {"Sweet": 87, "Pungent": 26, ...}
}
```

### **2. User Authentication APIs**
```javascript
// Register new user
POST /api/users/register/
Body: {
  "username": "practitioner1",
  "email": "doctor@example.com",
  "password": "securepass123",
  "user_type": "practitioner"
}

// Login
POST /api/token/
Body: {
  "username": "practitioner1",
  "password": "securepass123"
}
Response: {
  "access": "jwt_token_here",
  "refresh": "refresh_token_here"
}
```

### **3. Patient Management APIs**
```javascript
// Create patient (requires auth)
POST /api/patients/
Headers: { "Authorization": "Bearer jwt_token" }
Body: {
  "name": "John Doe",
  "prakriti": "Vata",
  "vikriti": "Pitta",
  "agni": "Sama",
  "health_parameters": {
    "age": 30,
    "weight": 70,
    "height": 175
  }
}

// Get all patients for practitioner
GET /api/patients/
Headers: { "Authorization": "Bearer jwt_token" }
```

## 🎯 **FRONTEND INTEGRATION STEPS**

### **Step 1: Update API Configuration**
In your React app, create or update `src/services/api.js`:

```javascript
// src/services/api.js
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.com/api'
  : 'http://localhost:8000/api';

export const apiClient = {
  // Get all foods
  async getFoods() {
    const response = await fetch(`${API_BASE_URL}/foods/`);
    return response.json();
  },

  // Search foods
  async searchFoods(params) {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/foods/search/?${queryString}`);
    return response.json();
  },

  // User authentication
  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    return response.json();
  },

  // Create patient
  async createPatient(patientData, token) {
    const response = await fetch(`${API_BASE_URL}/patients/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(patientData)
    });
    return response.json();
  }
};
```

## 🧪 **TESTING CHECKLIST**

### **Backend Tests (Complete these first)**
- [ ] Visit http://localhost:8000/api/foods/ in browser
- [ ] Test login at http://localhost:8000/admin/ 
- [ ] Check food search: http://localhost:8000/api/foods/search/?virya=Cooling
- [ ] Verify 117 foods in database

### **Frontend Integration Tests**
- [ ] Frontend can fetch food data from backend
- [ ] Login form submits to Django authentication
- [ ] Patient creation saves to Supabase database
- [ ] Diet generation uses real Ayurvedic food data
- [ ] No CORS errors in browser console

---

## 🎯 **CURRENT STATUS**
✅ **Backend**: Fully functional with Supabase  
✅ **Database**: 117 Ayurvedic foods loaded  
✅ **APIs**: All endpoints working  
🔄 **Frontend**: Ready for integration  
🎯 **Next**: Connect your React components to these APIs!
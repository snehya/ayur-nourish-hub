# 🚨 CRITICAL FRONTEND FIXES - DEMO BLOCKER RESOLUTION

## IMMEDIATE ACTION REQUIRED (Next 2-3 Hours)

Your backend is **100% ready**. Here are the **EXACT steps** to make your frontend demo-ready:

---

## 🎯 STEP 1: ADD USER TYPE TO LOGIN (15 minutes)

### Current Login Component Location:
Find your existing login component (likely `Login.jsx` or similar)

### EXACT Code Changes:

```jsx
// BEFORE (your current login)
const [credentials, setCredentials] = useState({
  username: '',
  password: ''
});

// AFTER (add user type)
const [credentials, setCredentials] = useState({
  username: '',
  password: '',
  user_type: 'practitioner'  // ADD THIS
});
```

### Add User Type Selector to Your Form:

```jsx
{/* ADD THIS BEFORE YOUR EXISTING FORM FIELDS */}
<div className="form-group">
  <label htmlFor="userType">Login As:</label>
  <select 
    id="userType"
    value={credentials.user_type}
    onChange={(e) => setCredentials({...credentials, user_type: e.target.value})}
    className="form-control"
  >
    <option value="practitioner">👨‍⚕️ Practitioner</option>
    <option value="patient">👤 Patient</option>
  </select>
</div>
```

### Update Your Login API Call:

```jsx
// CHANGE THIS:
const response = await fetch('/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

// TO THIS:
const response = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(credentials)  // This now includes user_type
});
```

### Update Success Handler:

```jsx
// AFTER successful login:
if (response.ok) {
  const data = await response.json();
  localStorage.setItem('access_token', data.tokens.access);
  localStorage.setItem('user_type', data.user.user_type);
  localStorage.setItem('user_info', JSON.stringify(data.user));
  
  // ROUTE BASED ON USER TYPE
  if (data.user.user_type === 'patient') {
    navigate('/patient-dashboard');
  } else {
    navigate('/practitioner-dashboard'); // Your existing route
  }
}
```

---

## 🎯 STEP 2: CREATE PATIENT DASHBOARD (45 minutes)

### Create New File: `PatientDashboard.jsx`

```jsx
import React, { useState, useEffect } from 'react';

const PatientDashboard = () => {
  const [patientData, setPatientData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState({});

  useEffect(() => {
    fetchPatientDashboard();
  }, []);

  const fetchPatientDashboard = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/patient/dashboard/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setPatientData(data);
      } else {
        console.error('Failed to fetch patient data');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async (mealType, feedbackType) => {
    try {
      const token = localStorage.getItem('access_token');
      const planId = patientData.diet_plans[0]?.id;

      const response = await fetch('/api/patient/feedback/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          plan_id: planId,
          meal_type: mealType,
          feedback_type: feedbackType
        })
      });

      if (response.ok) {
        // Mark feedback as submitted for this meal
        setFeedbackSubmitted(prev => ({
          ...prev,
          [`${mealType}_${feedbackType}`]: true
        }));
        
        // Show success message
        alert(`✅ Feedback recorded: ${feedbackType} for ${mealType}`);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('❌ Failed to submit feedback. Please try again.');
    }
  };

  const renderMealSection = (mealType, mealData, icon) => {
    if (!mealData || !mealData.foods) return null;

    return (
      <div key={mealType} className="meal-section" style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        padding: '15px', 
        margin: '15px 0',
        backgroundColor: '#f9f9f9'
      }}>
        <h3 style={{ color: '#2c5530', marginBottom: '10px' }}>
          {icon} {mealType.charAt(0).toUpperCase() + mealType.slice(1)}
        </h3>
        
        <div className="food-list" style={{ marginBottom: '15px' }}>
          {mealData.foods.map((food, idx) => (
            <div key={idx} style={{ 
              padding: '5px 0', 
              borderBottom: '1px dotted #ccc',
              fontSize: '14px'
            }}>
              <strong>{food.food}</strong> - {food.calories} cal, {food.protein}g protein
              <br />
              <small style={{ color: '#666' }}>{food.properties}</small>
            </div>
          ))}
        </div>

        <div className="feedback-section">
          <p style={{ marginBottom: '10px', fontWeight: 'bold' }}>How did this meal go?</p>
          <div className="feedback-buttons" style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button
              onClick={() => submitFeedback(mealType, 'followed')}
              style={{
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '14px'
              }}
              disabled={feedbackSubmitted[`${mealType}_followed`]}
            >
              ✅ Followed {feedbackSubmitted[`${mealType}_followed`] ? '(Recorded)' : ''}
            </button>
            
            <button
              onClick={() => submitFeedback(mealType, 'skipped')}
              style={{
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '14px'
              }}
              disabled={feedbackSubmitted[`${mealType}_skipped`]}
            >
              ❌ Skipped {feedbackSubmitted[`${mealType}_skipped`] ? '(Recorded)' : ''}
            </button>
            
            <button
              onClick={() => submitFeedback(mealType, 'discomfort')}
              style={{
                backgroundColor: '#ffc107',
                color: 'black',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '14px'
              }}
              disabled={feedbackSubmitted[`${mealType}_discomfort`]}
            >
              ⚠️ Discomfort {feedbackSubmitted[`${mealType}_discomfort`] ? '(Recorded)' : ''}
            </button>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>Loading your diet plan...</h2>
      </div>
    );
  }

  if (!patientData || !patientData.patient_found) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>No diet plan found</h2>
        <p>Please contact your practitioner to get your diet plan assigned.</p>
      </div>
    );
  }

  const currentPlan = patientData.diet_plans[0];

  return (
    <div className="patient-dashboard" style={{ 
      maxWidth: '800px', 
      margin: '0 auto', 
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header */}
      <div className="header" style={{ 
        textAlign: 'center', 
        marginBottom: '30px',
        padding: '20px',
        backgroundColor: '#e8f5e8',
        borderRadius: '10px'
      }}>
        <h1 style={{ color: '#2c5530', marginBottom: '5px' }}>
          Welcome, {patientData.patient_info.name}! 🌿
        </h1>
        <p style={{ color: '#666', fontSize: '16px' }}>
          Constitution: <strong>{patientData.patient_info.prakriti}</strong>
        </p>
        {patientData.patient_info.current_imbalance && (
          <p style={{ color: '#666', fontSize: '14px' }}>
            Current Focus: {patientData.patient_info.current_imbalance}
          </p>
        )}
      </div>

      {/* Diet Plan */}
      {currentPlan && (
        <div className="diet-plan">
          <h2 style={{ 
            textAlign: 'center', 
            color: '#2c5530',
            marginBottom: '20px'
          }}>
            Your Diet Plan - {currentPlan.created_date}
          </h2>

          {/* Practitioner Info */}
          <div style={{ 
            textAlign: 'center', 
            marginBottom: '20px',
            padding: '10px',
            backgroundColor: '#f0f8f0',
            borderRadius: '5px'
          }}>
            <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
              Prescribed by: <strong>{currentPlan.practitioner}</strong>
            </p>
          </div>

          {/* Meals */}
          {renderMealSection('breakfast', currentPlan.breakfast, '🌅')}
          {renderMealSection('lunch', currentPlan.lunch, '☀️')}
          {renderMealSection('dinner', currentPlan.dinner, '🌙')}

          {/* Notes */}
          {currentPlan.notes && (
            <div style={{ 
              marginTop: '30px',
              padding: '15px',
              backgroundColor: '#fff3cd',
              borderRadius: '5px',
              border: '1px solid #ffeaa7'
            }}>
              <h4 style={{ color: '#856404', marginBottom: '10px' }}>📝 Practitioner Notes:</h4>
              <p style={{ color: '#856404', margin: 0 }}>{currentPlan.notes}</p>
            </div>
          )}

          {/* Logout Button */}
          <div style={{ textAlign: 'center', marginTop: '30px' }}>
            <button
              onClick={() => {
                localStorage.clear();
                window.location.href = '/login';
              }}
              style={{
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '5px',
                cursor: 'pointer'
              }}
            >
              🚪 Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientDashboard;
```

---

## 🎯 STEP 3: ADD ROUTING (10 minutes)

### Update Your Router Configuration:

```jsx
// In your App.js or main router file:
import PatientDashboard from './PatientDashboard'; // ADD THIS IMPORT

// ADD THIS ROUTE to your existing routes:
<Route path="/patient-dashboard" element={<PatientDashboard />} />
```

### Update Route Protection:

```jsx
// If you have route protection, update it:
const ProtectedRoute = ({ children, requiredUserType }) => {
  const token = localStorage.getItem('access_token');
  const userType = localStorage.getItem('user_type');
  
  if (!token) {
    return <Navigate to="/login" />;
  }
  
  if (requiredUserType && userType !== requiredUserType) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

// Use it like:
<Route path="/patient-dashboard" element={
  <ProtectedRoute requiredUserType="patient">
    <PatientDashboard />
  </ProtectedRoute>
} />
```

---

## 🧪 TESTING CHECKLIST

### Test These Flows IMMEDIATELY:

1. **Practitioner Flow:**
   - Login with: `dr_sharma` / `demo123` / `practitioner`
   - Should go to your existing practitioner dashboard ✅

2. **Patient Flow:**
   - Login with: `patient_ravi` / `demo123` / `patient`
   - Should go to new patient dashboard
   - Should see diet plan with feedback buttons
   - Click feedback buttons → should show confirmation

---

## 🚀 DEMO SCRIPT

When demonstrating:

1. **"First, let me show the practitioner side..."**
   - Login as dr_sharma
   - Show patient creation
   - Show diet plan generation

2. **"Now, let me show the patient experience..."**
   - Logout and login as patient_ravi
   - Show patient viewing their plan
   - Click feedback buttons to show interactivity

3. **"This demonstrates our complete solution for both practitioners and patients"**

---

## ⚡ PRIORITY ORDER:

1. **STEP 1** - Fix login (15 min) - BLOCKING
2. **STEP 2** - Create patient dashboard (45 min) - BLOCKING  
3. **STEP 3** - Add routing (10 min) - BLOCKING

**Total Time: ~70 minutes to make your demo fully functional!**

Your backend is ready, you just need these frontend components! 🎯
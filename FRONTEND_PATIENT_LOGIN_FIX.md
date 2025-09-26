# 🚨 CRITICAL FRONTEND FIXES FOR PATIENT LOGIN

## IMMEDIATE ACTION REQUIRED

Your backend is 100% ready! Now you need to make these frontend changes to support patient login:

## 1. UPDATE LOGIN FORM (URGENT)

Add user type selection to your login component:

```jsx
// In your Login component
const [userType, setUserType] = useState('practitioner');

// Add this dropdown BEFORE the login button:
<div className="form-group">
  <label>Login As:</label>
  <select 
    value={userType} 
    onChange={(e) => setUserType(e.target.value)}
    className="form-control"
  >
    <option value="practitioner">👨‍⚕️ Practitioner</option>
    <option value="patient">👤 Patient</option>
  </select>
</div>

// Update your login API call:
const loginData = {
  username,
  password,
  user_type: userType  // ADD THIS LINE
};
```

## 2. UPDATE LOGIN API CALL

Change your login endpoint from:
```
POST /api/token/
```

TO:
```
POST /api/auth/login/
```

The response will include user type:
```json
{
  "user": {
    "id": 1,
    "username": "patient_ravi",
    "user_type": "patient",
    "first_name": "Ravi"
  },
  "tokens": {
    "access": "jwt_token_here"
  }
}
```

## 3. ROUTE USERS AFTER LOGIN

```jsx
// After successful login:
if (response.user.user_type === 'patient') {
  navigate('/patient-dashboard');
} else if (response.user.user_type === 'practitioner') {
  navigate('/practitioner-dashboard');
}
```

## 4. CREATE PATIENT DASHBOARD COMPONENT

```jsx
// PatientDashboard.jsx
import React, { useState, useEffect } from 'react';

const PatientDashboard = () => {
  const [patientData, setPatientData] = useState(null);
  const [selectedPlan, setSelectedPlan] = useState(null);

  useEffect(() => {
    fetchPatientData();
  }, []);

  const fetchPatientData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/patient/dashboard/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setPatientData(data);
      if (data.diet_plans.length > 0) {
        setSelectedPlan(data.diet_plans[0]); // Show latest plan
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const submitFeedback = async (mealType, feedbackType) => {
    try {
      const token = localStorage.getItem('access_token');
      await fetch('/api/patient/feedback/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          plan_id: selectedPlan.id,
          meal_type: mealType,
          feedback_type: feedbackType
        })
      });
      alert(`Feedback recorded: ${feedbackType} for ${mealType}`);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!patientData) return <div>Loading...</div>;

  return (
    <div className="patient-dashboard">
      <h1>Welcome, {patientData.patient_info.name}!</h1>
      <p>Constitution: {patientData.patient_info.prakriti}</p>
      
      {selectedPlan && (
        <div className="diet-plan">
          <h2>Your Diet Plan ({selectedPlan.created_date})</h2>
          
          {/* Breakfast */}
          <div className="meal-section">
            <h3>🌅 Breakfast</h3>
            {selectedPlan.breakfast?.foods?.map((food, idx) => (
              <div key={idx}>
                • {food.food} - {food.calories} cal, {food.protein}g protein
              </div>
            ))}
            <div className="feedback-buttons">
              <button onClick={() => submitFeedback('breakfast', 'followed')}>
                ✅ Followed
              </button>
              <button onClick={() => submitFeedback('breakfast', 'skipped')}>
                ❌ Skipped
              </button>
              <button onClick={() => submitFeedback('breakfast', 'discomfort')}>
                ⚠️ Discomfort
              </button>
            </div>
          </div>

          {/* Lunch */}
          <div className="meal-section">
            <h3>☀️ Lunch</h3>
            {selectedPlan.lunch?.foods?.map((food, idx) => (
              <div key={idx}>
                • {food.food} - {food.calories} cal, {food.protein}g protein
              </div>
            ))}
            <div className="feedback-buttons">
              <button onClick={() => submitFeedback('lunch', 'followed')}>
                ✅ Followed
              </button>
              <button onClick={() => submitFeedback('lunch', 'skipped')}>
                ❌ Skipped
              </button>
              <button onClick={() => submitFeedback('lunch', 'discomfort')}>
                ⚠️ Discomfort
              </button>
            </div>
          </div>

          {/* Dinner */}
          <div className="meal-section">
            <h3>🌙 Dinner</h3>
            {selectedPlan.dinner?.foods?.map((food, idx) => (
              <div key={idx}>
                • {food.food} - {food.calories} cal, {food.protein}g protein
              </div>
            ))}
            <div className="feedback-buttons">
              <button onClick={() => submitFeedback('dinner', 'followed')}>
                ✅ Followed
              </button>
              <button onClick={() => submitFeedback('dinner', 'skipped')}>
                ❌ Skipped
              </button>
              <button onClick={() => submitFeedback('dinner', 'discomfort')}>
                ⚠️ Discomfort
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientDashboard;
```

## 5. ADD ROUTING

```jsx
// In your App.js or router:
<Route path="/patient-dashboard" element={<PatientDashboard />} />
```

## 6. DEMO CREDENTIALS

**Practitioner Login:**
- Username: `dr_sharma`
- Password: `demo123`
- User Type: `practitioner`

**Patient Login:**
- Username: `patient_ravi`
- Password: `demo123`
- User Type: `patient`

## 7. TESTING CHECKLIST

- [ ] Login form has user type dropdown
- [ ] Practitioner login works (existing functionality)
- [ ] Patient login works (new functionality)
- [ ] Patient sees their diet plan
- [ ] Feedback buttons work and show confirmation
- [ ] User is routed correctly based on user type

## 8. QUICK VERIFICATION

Test these API endpoints in your browser network tab:
- `POST /api/auth/login/` (should work for both user types)
- `GET /api/patient/dashboard/` (patient only)
- `POST /api/patient/feedback/` (patient only)

## DEMO FLOW

1. **Show Practitioner Flow:** Login as dr_sharma → Create diet plan
2. **Show Patient Flow:** Login as patient_ravi → View diet plan → Give feedback
3. **Explain:** "In production, practitioners would share secure links with patients"

Your backend is 100% ready! The patient can log in and see their diet plan with working feedback buttons. Just need these frontend changes! 🚀
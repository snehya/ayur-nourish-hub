// frontend/src/components/DietPlanGenerator.jsx
// Diet Plan Generator Component for AyurDiet Pro

import React, { useState, useEffect } from 'react';
import dietPlanService from '../services/dietPlanService';
import patientService from '../services/patientService';

const DietPlanGenerator = () => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [generatedPlan, setGeneratedPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [patientsLoading, setPatientsLoading] = useState(true);

  // Load patients on component mount
  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    setPatientsLoading(true);
    try {
      const result = await patientService.getPatients();
      if (result.success) {
        setPatients(result.data);
      } else {
        setError('Failed to load patients: ' + result.error);
      }
    } catch (error) {
      setError('Failed to load patients');
      console.error('❌ Failed to load patients:', error);
    } finally {
      setPatientsLoading(false);
    }
  };

  const handlePatientSelect = (patientId) => {
    const patient = patients.find(p => p.id === parseInt(patientId));
    setSelectedPatient(patient);
    setGeneratedPlan(null); // Clear previous plan
    setError('');
  };

  const handleGeneratePlan = async () => {
    if (!selectedPatient) {
      setError('Please select a patient first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await dietPlanService.generateDietPlan(selectedPatient.id);
      
      if (result.success) {
        setGeneratedPlan(result.data);
        console.log('✅ Diet plan generated:', result.data);
      } else {
        setError('Failed to generate diet plan: ' + result.error);
      }
    } catch (error) {
      setError('Failed to generate diet plan. Please try again.');
      console.error('❌ Diet plan generation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!generatedPlan) return;

    setLoading(true);
    try {
      const result = await dietPlanService.downloadDietPlanPDF(
        generatedPlan.generated_plan.id, 
        selectedPatient.name
      );
      
      if (result.success) {
        console.log('✅ PDF downloaded successfully');
      } else {
        setError('Failed to download PDF: ' + result.error);
      }
    } catch (error) {
      setError('Failed to download PDF');
      console.error('❌ PDF download error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatMealData = (mealData) => {
    if (typeof mealData === 'string') {
      try {
        return JSON.parse(mealData);
      } catch (e) {
        return { foods: [mealData] };
      }
    }
    return mealData || { foods: [] };
  };

  if (patientsLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Loading patients...</div>
      </div>
    );
  }

  return (
    <div className="diet-plan-generator">
      <div className="generator-header">
        <h2>🥗 Generate Ayurvedic Diet Plan</h2>
        <p>Select a patient and generate a personalized diet plan based on their Ayurvedic constitution.</p>
      </div>

      {error && (
        <div className="error-message">
          <span>⚠️ {error}</span>
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      {/* Patient Selection */}
      <div className="form-section">
        <h3>1. Select Patient</h3>
        {patients.length === 0 ? (
          <div className="no-patients">
            <p>No patients found. Please add a patient first.</p>
            <button className="add-patient-btn">Add New Patient</button>
          </div>
        ) : (
          <div className="patient-selection">
            <select 
              value={selectedPatient?.id || ''} 
              onChange={(e) => handlePatientSelect(e.target.value)}
              disabled={loading}
            >
              <option value="">Choose a patient...</option>
              {patients.map(patient => (
                <option key={patient.id} value={patient.id}>
                  {patient.name} - {patient.prakriti || 'Unknown'} Constitution
                </option>
              ))}
            </select>

            {selectedPatient && (
              <div className="selected-patient-info">
                <h4>Patient Details:</h4>
                <div className="patient-details">
                  <div className="detail-item">
                    <strong>Name:</strong> {selectedPatient.name}
                  </div>
                  <div className="detail-item">
                    <strong>Prakriti:</strong> {selectedPatient.prakriti || 'Not specified'}
                  </div>
                  <div className="detail-item">
                    <strong>Vikriti:</strong> {selectedPatient.vikriti || 'Not specified'}
                  </div>
                  <div className="detail-item">
                    <strong>Agni:</strong> {selectedPatient.agni || 'Not specified'}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Generate Button */}
      {selectedPatient && (
        <div className="form-section">
          <h3>2. Generate Diet Plan</h3>
          <button 
            className="generate-button"
            onClick={handleGeneratePlan}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner">⏳</span>
                Generating Plan...
              </>
            ) : (
              <>
                <span>🔮</span>
                Generate Ayurvedic Diet Plan
              </>
            )}
          </button>
        </div>
      )}

      {/* Generated Plan Display */}
      {generatedPlan && (
        <div className="form-section">
          <h3>3. Generated Diet Plan</h3>
          <div className="generated-plan">
            <div className="plan-header">
              <h4>Diet Plan for {selectedPatient.name}</h4>
              <div className="plan-actions">
                <button 
                  className="download-pdf-btn"
                  onClick={handleDownloadPDF}
                  disabled={loading}
                >
                  {loading ? 'Downloading...' : '📄 Download PDF'}
                </button>
              </div>
            </div>

            <div className="meals-container">
              {/* Breakfast */}
              {generatedPlan.generated_plan.breakfast && (
                <div className="meal-section">
                  <h5>🌅 Breakfast</h5>
                  <div className="meal-content">
                    {formatMealData(generatedPlan.generated_plan.breakfast).foods?.map((food, index) => (
                      <span key={index} className="food-item">{food}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* Lunch */}
              {generatedPlan.generated_plan.lunch && (
                <div className="meal-section">
                  <h5>☀️ Lunch</h5>
                  <div className="meal-content">
                    {formatMealData(generatedPlan.generated_plan.lunch).foods?.map((food, index) => (
                      <span key={index} className="food-item">{food}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* Dinner */}
              {generatedPlan.generated_plan.dinner && (
                <div className="meal-section">
                  <h5>🌙 Dinner</h5>
                  <div className="meal-content">
                    {formatMealData(generatedPlan.generated_plan.dinner).foods?.map((food, index) => (
                      <span key={index} className="food-item">{food}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Guidelines */}
            {generatedPlan.ayurvedic_guidelines && (
              <div className="guidelines-section">
                <h5>📋 Ayurvedic Guidelines</h5>
                <div className="guidelines-content">
                  {generatedPlan.ayurvedic_guidelines.map((guideline, index) => (
                    <div key={index} className="guideline-item">
                      • {guideline}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        .diet-plan-generator {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem;
        }
        
        .generator-header {
          text-align: center;
          margin-bottom: 2rem;
        }
        
        .generator-header h2 {
          color: #2c5530;
          margin-bottom: 0.5rem;
        }
        
        .loading-container {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
        }
        
        .loading-spinner {
          font-size: 1.2rem;
          color: #666;
        }
        
        .error-message {
          background-color: #f8d7da;
          color: #721c24;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .error-message button {
          background: none;
          border: none;
          color: #721c24;
          font-size: 1.2rem;
          cursor: pointer;
          padding: 0;
          margin-left: 1rem;
        }
        
        .form-section {
          background: white;
          padding: 1.5rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          margin-bottom: 1.5rem;
        }
        
        .form-section h3 {
          color: #2c5530;
          margin-bottom: 1rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .no-patients {
          text-align: center;
          padding: 2rem;
          color: #666;
        }
        
        .add-patient-btn {
          background-color: #28a745;
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          cursor: pointer;
          margin-top: 1rem;
        }
        
        .patient-selection select {
          width: 100%;
          padding: 0.75rem;
          border: 2px solid #ddd;
          border-radius: 6px;
          font-size: 1rem;
          margin-bottom: 1rem;
        }
        
        .selected-patient-info {
          background-color: #f8f9fa;
          padding: 1rem;
          border-radius: 6px;
          border-left: 4px solid #007bff;
        }
        
        .patient-details {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 0.5rem;
          margin-top: 0.5rem;
        }
        
        .detail-item {
          font-size: 0.9rem;
        }
        
        .generate-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 1rem 2rem;
          border-radius: 8px;
          font-size: 1.1rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: transform 0.2s;
          width: 100%;
          justify-content: center;
        }
        
        .generate-button:hover:not(:disabled) {
          transform: translateY(-2px);
        }
        
        .generate-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
          transform: none;
        }
        
        .generated-plan {
          border: 2px solid #28a745;
          border-radius: 8px;
          overflow: hidden;
        }
        
        .plan-header {
          background-color: #28a745;
          color: white;
          padding: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .plan-header h4 {
          margin: 0;
        }
        
        .download-pdf-btn {
          background-color: #dc3545;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.9rem;
        }
        
        .meals-container {
          padding: 1rem;
        }
        
        .meal-section {
          margin-bottom: 1.5rem;
        }
        
        .meal-section h5 {
          color: #2c5530;
          margin-bottom: 0.5rem;
          font-size: 1.1rem;
        }
        
        .meal-content {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        
        .food-item {
          background-color: #e8f5e8;
          color: #2c5530;
          padding: 0.25rem 0.75rem;
          border-radius: 15px;
          font-size: 0.9rem;
          border: 1px solid #28a745;
        }
        
        .guidelines-section {
          background-color: #fff3cd;
          padding: 1rem;
          border-top: 1px solid #ddd;
        }
        
        .guidelines-section h5 {
          color: #856404;
          margin-bottom: 0.5rem;
        }
        
        .guidelines-content {
          color: #856404;
        }
        
        .guideline-item {
          margin-bottom: 0.25rem;
          font-size: 0.9rem;
        }
        
        .spinner {
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default DietPlanGenerator;
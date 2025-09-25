// frontend/src/components/PatientForm.jsx
// Patient Creation/Edit Form Component for AyurDiet Pro

import React, { useState, useEffect } from 'react';
import patientService from '../services/patientService';

const PatientForm = ({ patient = null, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    prakriti: '',
    vikriti: '',
    agni: '',
    health_parameters: {
      age: '',
      weight: '',
      height: '',
      allergies: [],
      conditions: []
    }
  });
  
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [newAllergy, setNewAllergy] = useState('');
  const [newCondition, setNewCondition] = useState('');

  // Populate form if editing existing patient
  useEffect(() => {
    if (patient) {
      setFormData({
        name: patient.name || '',
        prakriti: patient.prakriti || '',
        vikriti: patient.vikriti || '',
        agni: patient.agni || '',
        health_parameters: {
          age: patient.health_parameters?.age || '',
          weight: patient.health_parameters?.weight || '',
          height: patient.health_parameters?.height || '',
          allergies: patient.health_parameters?.allergies || [],
          conditions: patient.health_parameters?.conditions || []
        }
      });
    }
  }, [patient]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear specific error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleHealthParamChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      health_parameters: {
        ...prev.health_parameters,
        [name]: value
      }
    }));
  };

  const handleAddAllergy = () => {
    if (newAllergy.trim()) {
      setFormData(prev => ({
        ...prev,
        health_parameters: {
          ...prev.health_parameters,
          allergies: [...prev.health_parameters.allergies, newAllergy.trim()]
        }
      }));
      setNewAllergy('');
    }
  };

  const handleRemoveAllergy = (index) => {
    setFormData(prev => ({
      ...prev,
      health_parameters: {
        ...prev.health_parameters,
        allergies: prev.health_parameters.allergies.filter((_, i) => i !== index)
      }
    }));
  };

  const handleAddCondition = () => {
    if (newCondition.trim()) {
      setFormData(prev => ({
        ...prev,
        health_parameters: {
          ...prev.health_parameters,
          conditions: [...prev.health_parameters.conditions, newCondition.trim()]
        }
      }));
      setNewCondition('');
    }
  };

  const handleRemoveCondition = (index) => {
    setFormData(prev => ({
      ...prev,
      health_parameters: {
        ...prev.health_parameters,
        conditions: prev.health_parameters.conditions.filter((_, i) => i !== index)
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    // Validate form data
    const validation = patientService.validatePatientData(formData);
    if (!validation.isValid) {
      setErrors(validation.errors);
      setLoading(false);
      return;
    }

    try {
      let result;
      if (patient) {
        // Update existing patient
        result = await patientService.updatePatient(patient.id, formData);
      } else {
        // Create new patient
        result = await patientService.createPatient(formData);
      }

      if (result.success) {
        console.log('✅ Patient saved successfully:', result.data);
        if (onSuccess) {
          onSuccess(result.data);
        }
      } else {
        setErrors(result.error);
      }
    } catch (error) {
      console.error('❌ Form submission error:', error);
      setErrors({ general: 'Failed to save patient. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="patient-form-container">
      <div className="patient-form">
        <h2>{patient ? 'Edit Patient' : 'Add New Patient'}</h2>
        
        {errors.general && (
          <div className="error-message">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Basic Information */}
          <div className="form-section">
            <h3>Basic Information</h3>
            
            <div className="form-group">
              <label htmlFor="name">Patient Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                disabled={loading}
                placeholder="Enter patient's full name"
              />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>
          </div>

          {/* Ayurvedic Information */}
          <div className="form-section">
            <h3>Ayurvedic Assessment</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="prakriti">Prakriti (Constitution)</label>
                <select
                  id="prakriti"
                  name="prakriti"
                  value={formData.prakriti}
                  onChange={handleInputChange}
                  disabled={loading}
                >
                  <option value="">Select Prakriti</option>
                  <option value="Vata">Vata</option>
                  <option value="Pitta">Pitta</option>
                  <option value="Kapha">Kapha</option>
                </select>
                {errors.prakriti && <span className="error-text">{errors.prakriti}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="vikriti">Vikriti (Current State)</label>
                <select
                  id="vikriti"
                  name="vikriti"
                  value={formData.vikriti}
                  onChange={handleInputChange}
                  disabled={loading}
                >
                  <option value="">Select Vikriti</option>
                  <option value="Vata">Vata</option>
                  <option value="Pitta">Pitta</option>
                  <option value="Kapha">Kapha</option>
                </select>
                {errors.vikriti && <span className="error-text">{errors.vikriti}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="agni">Agni (Digestive Fire)</label>
                <select
                  id="agni"
                  name="agni"
                  value={formData.agni}
                  onChange={handleInputChange}
                  disabled={loading}
                >
                  <option value="">Select Agni</option>
                  <option value="Sama">Sama (Balanced)</option>
                  <option value="Tikshna">Tikshna (Sharp)</option>
                  <option value="Manda">Manda (Weak)</option>
                  <option value="Vishama">Vishama (Irregular)</option>
                </select>
                {errors.agni && <span className="error-text">{errors.agni}</span>}
              </div>
            </div>
          </div>

          {/* Health Parameters */}
          <div className="form-section">
            <h3>Health Parameters</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="age">Age</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.health_parameters.age}
                  onChange={handleHealthParamChange}
                  disabled={loading}
                  placeholder="Age in years"
                />
              </div>

              <div className="form-group">
                <label htmlFor="weight">Weight (kg)</label>
                <input
                  type="number"
                  id="weight"
                  name="weight"
                  value={formData.health_parameters.weight}
                  onChange={handleHealthParamChange}
                  disabled={loading}
                  placeholder="Weight in kg"
                />
              </div>

              <div className="form-group">
                <label htmlFor="height">Height (cm)</label>
                <input
                  type="number"
                  id="height"
                  name="height"
                  value={formData.health_parameters.height}
                  onChange={handleHealthParamChange}
                  disabled={loading}
                  placeholder="Height in cm"
                />
              </div>
            </div>

            {/* Allergies */}
            <div className="form-group">
              <label>Allergies</label>
              <div className="add-item-section">
                <input
                  type="text"
                  value={newAllergy}
                  onChange={(e) => setNewAllergy(e.target.value)}
                  placeholder="Add allergy"
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={handleAddAllergy}
                  disabled={loading || !newAllergy.trim()}
                >
                  Add
                </button>
              </div>
              <div className="item-list">
                {formData.health_parameters.allergies.map((allergy, index) => (
                  <span key={index} className="item-tag">
                    {allergy}
                    <button
                      type="button"
                      onClick={() => handleRemoveAllergy(index)}
                      disabled={loading}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Conditions */}
            <div className="form-group">
              <label>Health Conditions</label>
              <div className="add-item-section">
                <input
                  type="text"
                  value={newCondition}
                  onChange={(e) => setNewCondition(e.target.value)}
                  placeholder="Add health condition"
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={handleAddCondition}
                  disabled={loading || !newCondition.trim()}
                >
                  Add
                </button>
              </div>
              <div className="item-list">
                {formData.health_parameters.conditions.map((condition, index) => (
                  <span key={index} className="item-tag">
                    {condition}
                    <button
                      type="button"
                      onClick={() => handleRemoveCondition(index)}
                      disabled={loading}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Form Actions */}
          <div className="form-actions">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="cancel-button"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="submit-button"
            >
              {loading ? 'Saving...' : (patient ? 'Update Patient' : 'Create Patient')}
            </button>
          </div>
        </form>
      </div>

      <style jsx>{`
        .patient-form-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 2rem;
        }
        
        .patient-form {
          background: white;
          padding: 2rem;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .form-section {
          margin-bottom: 2rem;
        }
        
        .form-section h3 {
          margin-bottom: 1rem;
          color: #333;
          border-bottom: 2px solid #007bff;
          padding-bottom: 0.5rem;
        }
        
        .form-row {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }
        
        .form-group {
          margin-bottom: 1rem;
        }
        
        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: bold;
          color: #555;
        }
        
        input, select {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
          transition: border-color 0.3s;
        }
        
        input:focus, select:focus {
          outline: none;
          border-color: #007bff;
        }
        
        .add-item-section {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 0.5rem;
        }
        
        .add-item-section input {
          flex: 1;
        }
        
        .add-item-section button {
          padding: 0.75rem 1rem;
          background-color: #28a745;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        .item-list {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        
        .item-tag {
          background-color: #f8f9fa;
          border: 1px solid #dee2e6;
          border-radius: 20px;
          padding: 0.25rem 0.75rem;
          font-size: 0.875rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .item-tag button {
          background: none;
          border: none;
          color: #dc3545;
          cursor: pointer;
          font-weight: bold;
          padding: 0;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .form-actions {
          display: flex;
          gap: 1rem;
          justify-content: flex-end;
          margin-top: 2rem;
          padding-top: 2rem;
          border-top: 1px solid #eee;
        }
        
        .cancel-button {
          padding: 0.75rem 1.5rem;
          background-color: #6c757d;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        .submit-button {
          padding: 0.75rem 1.5rem;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        .error-message {
          background-color: #f8d7da;
          color: #721c24;
          padding: 0.75rem;
          border-radius: 4px;
          margin-bottom: 1rem;
        }
        
        .error-text {
          color: #dc3545;
          font-size: 0.875rem;
          margin-top: 0.25rem;
          display: block;
        }
      `}</style>
    </div>
  );
};

export default PatientForm;
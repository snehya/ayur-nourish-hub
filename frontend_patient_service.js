// frontend/src/services/patientService.js
// Patient Management Service for AyurDiet Pro

import apiClient from './axiosConfig';
import { API_ENDPOINTS } from '../config/api';

class PatientService {
  // Get all patients for the current practitioner
  async getPatients() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.PATIENTS);
      console.log('✅ Patients fetched successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to fetch patients:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to fetch patients' 
      };
    }
  }

  // Get single patient by ID
  async getPatient(patientId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.PATIENT_DETAIL(patientId));
      console.log('✅ Patient fetched successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to fetch patient:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to fetch patient' 
      };
    }
  }

  // Create new patient
  async createPatient(patientData) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.PATIENTS, patientData);
      console.log('✅ Patient created successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to create patient:', error);
      return { 
        success: false, 
        error: error.response?.data || 'Failed to create patient' 
      };
    }
  }

  // Update patient
  async updatePatient(patientId, patientData) {
    try {
      const response = await apiClient.put(API_ENDPOINTS.PATIENT_DETAIL(patientId), patientData);
      console.log('✅ Patient updated successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to update patient:', error);
      return { 
        success: false, 
        error: error.response?.data || 'Failed to update patient' 
      };
    }
  }

  // Delete patient
  async deletePatient(patientId) {
    try {
      await apiClient.delete(API_ENDPOINTS.PATIENT_DETAIL(patientId));
      console.log('✅ Patient deleted successfully');
      return { success: true };
    } catch (error) {
      console.error('❌ Failed to delete patient:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to delete patient' 
      };
    }
  }

  // Validate patient data before sending
  validatePatientData(patientData) {
    const errors = {};

    // Name validation
    if (!patientData.name || patientData.name.length < 2) {
      errors.name = 'Name must be at least 2 characters long';
    }

    // Prakriti validation
    const validPrakriti = ['Vata', 'Pitta', 'Kapha'];
    if (patientData.prakriti && !validPrakriti.includes(patientData.prakriti)) {
      errors.prakriti = 'Prakriti must be one of: Vata, Pitta, Kapha';
    }

    // Vikriti validation
    const validVikriti = ['Vata', 'Pitta', 'Kapha'];
    if (patientData.vikriti && !validVikriti.includes(patientData.vikriti)) {
      errors.vikriti = 'Vikriti must be one of: Vata, Pitta, Kapha';
    }

    // Agni validation
    const validAgni = ['Sama', 'Tikshna', 'Manda', 'Vishama'];
    if (patientData.agni && !validAgni.includes(patientData.agni)) {
      errors.agni = 'Agni must be one of: Sama, Tikshna, Manda, Vishama';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }

  // Helper method to format patient data for display
  formatPatientForDisplay(patient) {
    return {
      ...patient,
      createdAt: new Date(patient.created_at).toLocaleDateString(),
      healthSummary: this.getHealthSummary(patient),
    };
  }

  // Get health summary for patient
  getHealthSummary(patient) {
    const parts = [];
    
    if (patient.prakriti) parts.push(`Prakriti: ${patient.prakriti}`);
    if (patient.vikriti) parts.push(`Vikriti: ${patient.vikriti}`);
    if (patient.agni) parts.push(`Agni: ${patient.agni}`);
    
    return parts.join(' | ') || 'No health data';
  }
}

// Export singleton instance
const patientService = new PatientService();
export default patientService;
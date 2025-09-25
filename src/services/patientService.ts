// Patient management service for AyurDiet Pro
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/config';

// Types for patient management
export interface Patient {
  id?: number;
  name: string;
  prakriti: 'Vata' | 'Pitta' | 'Kapha' | null;
  vikriti: 'Vata' | 'Pitta' | 'Kapha' | null;
  agni: 'Sama' | 'Tikshna' | 'Manda' | 'Vishama' | null;
  health_parameters: {
    age?: number;
    weight?: number;
    height?: number;
    allergies?: string[];
    conditions?: string[];
    [key: string]: unknown;
  };
}

export interface PatientListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Patient[];
}

class PatientService {
  /**
   * Get all patients for the authenticated practitioner
   */
  async getPatients(): Promise<Patient[]> {
    try {
      const response = await apiClient.get<Patient[]>(API_ENDPOINTS.PATIENTS);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch patients');
    }
  }

  /**
   * Get a specific patient by ID
   */
  async getPatient(id: string | number): Promise<Patient> {
    try {
      const response = await apiClient.get<Patient>(API_ENDPOINTS.PATIENT_DETAIL(id));
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch patient with ID ${id}`);
    }
  }

  /**
   * Create a new patient
   */
  async createPatient(patientData: Omit<Patient, 'id'>): Promise<Patient> {
    try {
      // Validate patient data
      this.validatePatientData(patientData);
      
      const response = await apiClient.post<Patient>(API_ENDPOINTS.PATIENTS, patientData);
      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to create patient');
    }
  }

  /**
   * Update an existing patient
   */
  async updatePatient(id: string | number, patientData: Partial<Patient>): Promise<Patient> {
    try {
      // Validate patient data if provided
      if (patientData.name || patientData.prakriti || patientData.vikriti || patientData.agni) {
        this.validatePatientData(patientData as Patient);
      }
      
      const response = await apiClient.put<Patient>(API_ENDPOINTS.PATIENT_DETAIL(id), patientData);
      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(`Failed to update patient with ID ${id}`);
    }
  }

  /**
   * Delete a patient
   */
  async deletePatient(id: string | number): Promise<void> {
    try {
      await apiClient.delete(API_ENDPOINTS.PATIENT_DETAIL(id));
    } catch (error) {
      throw new Error(`Failed to delete patient with ID ${id}`);
    }
  }

  /**
   * Validate patient data
   */
  private validatePatientData(patientData: Partial<Patient>): void {
    // Validate name
    if (patientData.name && patientData.name.trim().length < 2) {
      throw new Error('Patient name must be at least 2 characters long');
    }

    if (patientData.name && patientData.name.length > 100) {
      throw new Error('Patient name cannot exceed 100 characters');
    }

    // Validate prakriti
    const validPrakritis = ['Vata', 'Pitta', 'Kapha'];
    if (patientData.prakriti && !validPrakritis.includes(patientData.prakriti)) {
      throw new Error(`Prakriti must be one of: ${validPrakritis.join(', ')}`);
    }

    // Validate vikriti
    const validVikritis = ['Vata', 'Pitta', 'Kapha'];
    if (patientData.vikriti && !validVikritis.includes(patientData.vikriti)) {
      throw new Error(`Vikriti must be one of: ${validVikritis.join(', ')}`);
    }

    // Validate agni
    const validAgni = ['Sama', 'Tikshna', 'Manda', 'Vishama'];
    if (patientData.agni && !validAgni.includes(patientData.agni)) {
      throw new Error(`Agni must be one of: ${validAgni.join(', ')}`);
    }

    // Validate health parameters
    if (patientData.health_parameters) {
      const { age, weight, height } = patientData.health_parameters;
      
      if (age !== undefined && (age < 0 || age > 150)) {
        throw new Error('Age must be between 0 and 150');
      }
      
      if (weight !== undefined && (weight < 0 || weight > 1000)) {
        throw new Error('Weight must be between 0 and 1000 kg');
      }
      
      if (height !== undefined && (height < 0 || height > 300)) {
        throw new Error('Height must be between 0 and 300 cm');
      }
    }
  }

  /**
   * Search patients by name
   */
  async searchPatients(query: string): Promise<Patient[]> {
    try {
      const allPatients = await this.getPatients();
      return allPatients.filter(patient => 
        patient.name.toLowerCase().includes(query.toLowerCase())
      );
    } catch (error) {
      throw new Error('Failed to search patients');
    }
  }

  /**
   * Get patients by dosha type
   */
  async getPatientsByDosha(dosha: 'Vata' | 'Pitta' | 'Kapha'): Promise<Patient[]> {
    try {
      const allPatients = await this.getPatients();
      return allPatients.filter(patient => 
        patient.prakriti === dosha || patient.vikriti === dosha
      );
    } catch (error) {
      throw new Error(`Failed to get patients with ${dosha} dosha`);
    }
  }

  /**
   * Get patient statistics
   */
  async getPatientStats(): Promise<{
    total: number;
    byPrakriti: Record<string, number>;
    byVikriti: Record<string, number>;
    byAgni: Record<string, number>;
  }> {
    try {
      const patients = await this.getPatients();
      
      const stats = {
        total: patients.length,
        byPrakriti: {} as Record<string, number>,
        byVikriti: {} as Record<string, number>,
        byAgni: {} as Record<string, number>,
      };

      patients.forEach(patient => {
        // Count by prakriti
        if (patient.prakriti) {
          stats.byPrakriti[patient.prakriti] = (stats.byPrakriti[patient.prakriti] || 0) + 1;
        }

        // Count by vikriti
        if (patient.vikriti) {
          stats.byVikriti[patient.vikriti] = (stats.byVikriti[patient.vikriti] || 0) + 1;
        }

        // Count by agni
        if (patient.agni) {
          stats.byAgni[patient.agni] = (stats.byAgni[patient.agni] || 0) + 1;
        }
      });

      return stats;
    } catch (error) {
      throw new Error('Failed to get patient statistics');
    }
  }
}

// Export singleton instance
export const patientService = new PatientService();
export default patientService;
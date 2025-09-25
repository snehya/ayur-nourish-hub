// Main exports for AyurDiet Pro services
export { default as authService } from './authService';
export { default as patientService } from './patientService';
export { default as dietPlanService } from './dietPlanService';

// Export types
export type { 
  LoginRequest, 
  LoginResponse, 
  User, 
  AuthState 
} from './authService';

export type { 
  Patient,
  PatientListResponse 
} from './patientService';

export type { 
  Food,
  MealPlan,
  DietPlan,
  GenerateDietPlanRequest,
  GenerateDietPlanResponse 
} from './dietPlanService';
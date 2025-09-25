/**
 * @fileoverview Core TypeScript types and interfaces for the Ayurvedic Practice Management System
 * @author AyurDiet Pro Team
 * @version 1.0.0
 */

/**
 * Ayurvedic thermal properties of food items
 */
export type ThermalProperty = 'Hot' | 'Cold' | 'Neutral';

/**
 * Digestibility levels for food items
 */
export type DigestibilityLevel = 'Easy' | 'Moderate' | 'Difficult';

/**
 * Six tastes (Rasa) in Ayurveda
 */
export type AyurvedicRasa = 'Sweet' | 'Sour' | 'Salty' | 'Pungent' | 'Bitter' | 'Astringent';

/**
 * Three doshas in Ayurveda
 */
export type Dosha = 'Vata' | 'Pitta' | 'Kapha';

/**
 * Constitution types (Prakriti) combinations
 */
export type Prakriti = Dosha | `${Dosha}-${Dosha}` | 'Tridoshic';

/**
 * Gender options
 */
export type Gender = 'Male' | 'Female' | 'Other';

/**
 * Patient status in the system
 */
export type PatientStatus = 'Active Treatment' | 'Follow-up Due' | 'New Patient' | 'Inactive';

/**
 * Meal completion status
 */
export type MealStatus = 'pending' | 'completed' | 'skipped' | 'discomfort';

/**
 * User roles in the system
 */
export type UserRole = 'patient' | 'practitioner' | 'dietitian' | 'doctor' | 'nutritionist' | 'student';

/**
 * Nutritional information for food items
 */
export interface NutritionData {
  /** Calories per 100g */
  calories: number;
  /** Protein content in grams */
  protein: number;
  /** Carbohydrate content in grams */
  carbs: number;
  /** Fat content in grams */
  fat: number;
  /** Fiber content in grams */
  fiber: number;
  /** List of vitamins present */
  vitamins: string[];
  /** List of minerals present */
  minerals: string[];
}

/**
 * Food item in the database
 */
export interface FoodItem {
  /** Unique identifier */
  id: number;
  /** Food item name */
  name: string;
  /** Food category */
  category: string;
  /** Ayurvedic thermal property */
  thermalProperty: ThermalProperty;
  /** Digestibility level */
  digestibility: DigestibilityLevel;
  /** Ayurvedic tastes present */
  rasa: AyurvedicRasa[];
  /** Nutritional information */
  nutrients: NutritionData;
  /** Medical contraindications */
  contraindications: string[];
  /** Health benefits */
  benefits: string[];
  /** Suitable seasons */
  season: string[];
  /** Preparation guidelines */
  preparationTips: string;
}

/**
 * Individual meal in a diet plan
 */
export interface MealItem {
  /** Unique meal identifier */
  id: string;
  /** Meal name */
  name: string;
  /** Scheduled time */
  time: string;
  /** Meal description */
  description: string;
  /** Preparation instructions */
  instructions: string;
  /** Ayurvedic tastes in this meal */
  rasa: AyurvedicRasa[];
  /** Ayurvedic properties */
  properties: string[];
  /** Health benefits */
  benefits: string[];
  /** Current completion status */
  status: MealStatus;
}

/**
 * Complete diet plan for a patient
 */
export interface DietPlan {
  /** Unique plan identifier */
  id: string;
  /** Prescribing doctor's name */
  doctorName: string;
  /** Plan creation date */
  createdDate: string;
  /** Plan expiration date */
  validUntil: string;
  /** Optional voice message from doctor */
  voiceNote?: string;
  /** Special dietary instructions */
  specialInstructions: string;
  /** List of meals in the plan */
  meals: MealItem[];
}

/**
 * Patient information
 */
export interface Patient {
  /** Unique patient identifier */
  id: string;
  /** Full name */
  name: string;
  /** Age in years */
  age: number;
  /** Gender */
  gender: Gender;
  /** Email address */
  email: string;
  /** Phone number */
  phone: string;
  /** Physical address */
  address: string;
  /** Ayurvedic constitution */
  prakriti: Prakriti;
  /** Alternative name for prakriti - for compatibility */
  constitution?: string;
  /** Current health condition */
  currentCondition: string;
  /** Medical history */
  medicalHistory: string;
  /** Current medications */
  medications: string;
  /** Food allergies */
  allergies: string;
  /** Lifestyle notes */
  lifestyle: string;
  /** Treatment goals */
  goals: string;
  /** Emergency contact name */
  emergencyContactName: string;
  /** Emergency contact phone */
  emergencyContactPhone: string;
  /** Current status */
  status: PatientStatus;
  /** Last visit date */
  lastVisit: string;
}

/**
 * Dashboard statistics
 */
export interface DashboardStats {
  /** Statistic title */
  title: string;
  /** Current value */
  value: string;
  /** Percentage change */
  change: string;
  /** Type of change (positive/negative) */
  changeType: 'positive' | 'negative';
  /** Icon component */
  icon: React.ComponentType<any>;
  /** Background color class */
  color: string;
}

/**
 * Activity log entry
 */
export interface ActivityEntry {
  /** Action description */
  action: string;
  /** Associated patient name */
  patient: string;
  /** Time of action */
  time: string;
  /** Icon component */
  icon: React.ComponentType<any>;
  /** Color class */
  color: string;
}

/**
 * Alias for ActivityEntry - used in Dashboard components
 */
export type ActivityItem = ActivityEntry;

/**
 * Component props for patient-related components
 */
export interface PatientProfileProps {
  /** Patient data */
  patient?: Patient;
  /** Edit mode flag */
  isEditing?: boolean;
  /** Save handler */
  onSave?: (patient: Patient) => void;
  /** Cancel handler */
  onCancel?: () => void;
}

/**
 * Filter options for food database
 */
export interface FoodFilters {
  /** Search term */
  searchTerm: string;
  /** Category filter */
  category: string;
  /** Thermal property filter */
  thermalProperty: string;
  /** Digestibility filter */
  digestibility: string;
}

/**
 * API response wrapper
 */
export interface ApiResponse<T> {
  /** Response data */
  data: T;
  /** Success flag */
  success: boolean;
  /** Error message if any */
  message?: string;
  /** HTTP status code */
  statusCode: number;
}

/**
 * Pagination parameters
 */
export interface PaginationParams {
  /** Current page number */
  page: number;
  /** Items per page */
  limit: number;
  /** Total items count */
  total: number;
  /** Total pages count */
  totalPages: number;
}

/**
 * Common component props
 */
export interface BaseComponentProps {
  /** Additional CSS classes */
  className?: string;
  /** Loading state */
  isLoading?: boolean;
  /** Error state */
  error?: string;
  /** Children elements */
  children?: React.ReactNode;
}
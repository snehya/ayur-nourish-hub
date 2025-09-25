/**
 * @fileoverview Application constants for the Ayurvedic Practice Management System
 * @author Somae Team
 * @version 1.0.0
 */

import { AyurvedicRasa, ThermalProperty, DigestibilityLevel, UserRole } from '@/types';

/**
 * Application metadata
 */
export const APP_CONFIG = {
  name: 'Somae',
  version: '1.0.0',
  description: 'Ayurvedic Practice Management Software',
  author: 'Somae Team',
} as const;

/**
 * API configuration
 */
export const API_CONFIG = {
  baseUrl: process.env.VITE_API_BASE_URL || 'http://localhost:3001',
  timeout: 10000,
  retryAttempts: 3,
} as const;

/**
 * Pagination defaults
 */
export const PAGINATION = {
  defaultPageSize: 20,
  maxPageSize: 100,
  pageSizeOptions: [10, 20, 50, 100],
} as const;

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  authToken: 'ayurdiet_auth_token',
  userPreferences: 'ayurdiet_user_preferences',
  recentPatients: 'ayurdiet_recent_patients',
  draftDietPlan: 'ayurdiet_draft_diet_plan',
} as const;

/**
 * Six tastes (Rasa) in Ayurveda with descriptions
 */
export const AYURVEDIC_RASAS: Record<AyurvedicRasa, { name: AyurvedicRasa; description: string; effects: string[] }> = {
  Sweet: {
    name: 'Sweet',
    description: 'Builds tissues, calms Vata and Pitta',
    effects: ['Nourishing', 'Strengthening', 'Calming']
  },
  Sour: {
    name: 'Sour',
    description: 'Stimulates appetite, aids digestion',
    effects: ['Digestive', 'Appetizing', 'Cleansing']
  },
  Salty: {
    name: 'Salty',
    description: 'Maintains electrolyte balance',
    effects: ['Hydrating', 'Softening', 'Lubricating']
  },
  Pungent: {
    name: 'Pungent',
    description: 'Increases heat and circulation',
    effects: ['Warming', 'Stimulating', 'Detoxifying']
  },
  Bitter: {
    name: 'Bitter',
    description: 'Detoxifies and purifies',
    effects: ['Cooling', 'Cleansing', 'Anti-inflammatory']
  },
  Astringent: {
    name: 'Astringent',
    description: 'Contracts and tones tissues',
    effects: ['Drying', 'Binding', 'Healing']
  }
} as const;

/**
 * Three doshas with their characteristics
 */
export const DOSHAS = {
  Vata: {
    name: 'Vata',
    elements: ['Air', 'Space'],
    qualities: ['Light', 'Cold', 'Dry', 'Mobile', 'Rough'],
    functions: ['Movement', 'Circulation', 'Breathing', 'Elimination']
  },
  Pitta: {
    name: 'Pitta',
    elements: ['Fire', 'Water'],
    qualities: ['Hot', 'Sharp', 'Light', 'Liquid', 'Acidic'],
    functions: ['Digestion', 'Metabolism', 'Temperature regulation', 'Intelligence']
  },
  Kapha: {
    name: 'Kapha',
    elements: ['Earth', 'Water'],
    qualities: ['Heavy', 'Cold', 'Moist', 'Stable', 'Smooth'],
    functions: ['Structure', 'Lubrication', 'Immunity', 'Growth']
  }
} as const;

/**
 * Food categories for classification
 */
export const FOOD_CATEGORIES = [
  'Grains',
  'Vegetables', 
  'Fruits',
  'Legumes',
  'Nuts',
  'Seeds',
  'Spices',
  'Herbs',
  'Dairy',
  'Oils',
  'Sweeteners',
  'Beverages'
] as const;

/**
 * Thermal properties with icons and colors
 */
export const THERMAL_PROPERTIES: Record<ThermalProperty, { name: ThermalProperty; icon: string; color: string }> = {
  Hot: { name: 'Hot', icon: '🔥', color: 'text-red-500' },
  Cold: { name: 'Cold', icon: '❄️', color: 'text-blue-500' },
  Neutral: { name: 'Neutral', icon: '⚖️', color: 'text-gray-500' }
} as const;

/**
 * Digestibility levels with descriptions
 */
export const DIGESTIBILITY_LEVELS: Record<DigestibilityLevel, { name: DigestibilityLevel; description: string; color: string }> = {
  Easy: { 
    name: 'Easy', 
    description: 'Light on digestion, suitable for weak digestive fire',
    color: 'text-green-500'
  },
  Moderate: { 
    name: 'Moderate', 
    description: 'Requires normal digestive capacity',
    color: 'text-yellow-500'
  },
  Difficult: { 
    name: 'Difficult', 
    description: 'Heavy foods requiring strong digestive fire',
    color: 'text-red-500'
  }
} as const;

/**
 * User roles and their permissions
 */
export const USER_ROLES: Record<UserRole, { name: string; permissions: string[] }> = {
  patient: {
    name: 'Patient',
    permissions: ['view_own_profile', 'view_own_diet_plan', 'update_meal_status']
  },
  practitioner: {
    name: 'Ayurvedic Practitioner',
    permissions: ['manage_patients', 'create_diet_plans', 'view_analytics', 'access_food_database']
  },
  dietitian: {
    name: 'Certified Dietitian',
    permissions: ['manage_patients', 'create_diet_plans', 'view_analytics', 'access_food_database']
  },
  doctor: {
    name: 'Medical Doctor',
    permissions: ['manage_patients', 'create_diet_plans', 'view_analytics', 'access_food_database', 'medical_consultations']
  },
  nutritionist: {
    name: 'Nutritionist',
    permissions: ['manage_patients', 'create_diet_plans', 'view_analytics', 'access_food_database']
  },
  student: {
    name: 'Student/Trainee',
    permissions: ['view_limited_data', 'access_food_database']
  }
} as const;

/**
 * Default meal times
 */
export const DEFAULT_MEAL_TIMES = {
  'Early Morning': '06:00',
  'Morning Breakfast': '07:30',
  'Mid-Morning Snack': '10:00',
  'Lunch': '12:30',
  'Afternoon Snack': '15:30',
  'Evening Snack': '17:00',
  'Dinner': '19:00',
  'Before Bed': '21:00'
} as const;

/**
 * Seasons in Ayurveda
 */
export const AYURVEDIC_SEASONS = [
  'Spring',
  'Summer', 
  'Monsoon',
  'Autumn',
  'Early Winter',
  'Late Winter'
] as const;

/**
 * Common contraindications
 */
export const COMMON_CONTRAINDICATIONS = [
  'Diabetes',
  'Hypertension',
  'Heart disease',
  'Kidney disease',
  'Liver disease',
  'Acid reflux',
  'IBS',
  'Food allergies',
  'Pregnancy',
  'Breastfeeding',
  'Weak digestion',
  'Vata excess',
  'Pitta excess',
  'Kapha excess'
] as const;

/**
 * Validation rules
 */
export const VALIDATION_RULES = {
  name: {
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s]+$/
  },
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  },
  phone: {
    pattern: /^[\+]?[1-9][\d]{0,15}$/,
    minLength: 10,
    maxLength: 15
  },
  age: {
    min: 0,
    max: 120
  },
  weight: {
    min: 1,
    max: 500
  },
  height: {
    min: 50,
    max: 250
  }
} as const;

/**
 * Color palette for charts and UI
 */
export const COLORS = {
  primary: '#22c55e',
  secondary: '#94a3b8',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  vata: '#8b5cf6',
  pitta: '#f97316', 
  kapha: '#06b6d4',
  neutral: '#6b7280'
} as const;

/**
 * Animation durations (in milliseconds)
 */
export const ANIMATIONS = {
  fast: 150,
  normal: 250,
  slow: 400,
  toast: 3000,
  modal: 300
} as const;

/**
 * Breakpoints for responsive design
 */
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536
} as const;
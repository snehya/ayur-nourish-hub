/**
 * @fileoverview Utility functions for the Ayurvedic Practice Management System
 * @author AyurDiet Pro Team
 * @version 1.0.0
 */

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { ThermalProperty, DigestibilityLevel, MealStatus, PatientStatus } from '@/types';

/**
 * Combines and merges Tailwind CSS classes
 * @param inputs - Class values to combine
 * @returns Merged class string
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Formats a date string into a readable format
 * @param dateString - ISO date string
 * @param locale - Locale for formatting (default: 'en-US')
 * @returns Formatted date string
 */
export function formatDate(dateString: string, locale: string = 'en-US'): string {
  return new Date(dateString).toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Formats a date into a relative time string (e.g., "2 hours ago")
 * @param dateString - ISO date string
 * @returns Relative time string
 */
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInMilliseconds = now.getTime() - date.getTime();
  const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));
  const diffInHours = Math.floor(diffInMinutes / 60);
  const diffInDays = Math.floor(diffInHours / 24);

  if (diffInMinutes < 60) {
    return `${diffInMinutes} minutes ago`;
  } else if (diffInHours < 24) {
    return `${diffInHours} hours ago`;
  } else if (diffInDays === 1) {
    return 'Yesterday';
  } else {
    return `${diffInDays} days ago`;
  }
}

/**
 * Capitalizes the first letter of a string
 * @param str - Input string
 * @returns Capitalized string
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Truncates text to a specified length with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @returns Truncated text
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Generates initials from a full name
 * @param name - Full name
 * @returns Initials (max 2 characters)
 */
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('');
}

/**
 * Validates email format
 * @param email - Email address to validate
 * @returns True if valid email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validates phone number format (supports Indian numbers)
 * @param phone - Phone number to validate
 * @returns True if valid phone format
 */
export function isValidPhone(phone: string): boolean {
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
  return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

/**
 * Gets the appropriate color class for thermal properties
 * @param property - Thermal property
 * @returns Color class string
 */
export function getThermalColor(property: ThermalProperty): string {
  switch (property) {
    case 'Hot':
      return 'text-red-500 bg-red-50 border-red-200';
    case 'Cold':
      return 'text-blue-500 bg-blue-50 border-blue-200';
    case 'Neutral':
      return 'text-gray-500 bg-gray-50 border-gray-200';
    default:
      return 'text-gray-500 bg-gray-50 border-gray-200';
  }
}

/**
 * Gets the appropriate color class for digestibility levels
 * @param level - Digestibility level
 * @returns Color class string
 */
export function getDigestibilityColor(level: DigestibilityLevel): string {
  switch (level) {
    case 'Easy':
      return 'text-green-500 bg-green-50 border-green-200';
    case 'Moderate':
      return 'text-yellow-500 bg-yellow-50 border-yellow-200';
    case 'Difficult':
      return 'text-red-500 bg-red-50 border-red-200';
    default:
      return 'text-gray-500 bg-gray-50 border-gray-200';
  }
}

/**
 * Gets the appropriate color class for meal status
 * @param status - Meal status
 * @returns Color class string
 */
export function getMealStatusColor(status: MealStatus): string {
  switch (status) {
    case 'completed':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'skipped':
      return 'text-red-600 bg-red-50 border-red-200';
    case 'discomfort':
      return 'text-orange-600 bg-orange-50 border-orange-200';
    case 'pending':
      return 'text-gray-600 bg-gray-50 border-gray-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
}

/**
 * Gets the appropriate color class for patient status
 * @param status - Patient status
 * @returns Color class string
 */
export function getPatientStatusColor(status: PatientStatus): string {
  switch (status) {
    case 'Active Treatment':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'Follow-up Due':
      return 'text-red-600 bg-red-50 border-red-200';
    case 'New Patient':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'Inactive':
      return 'text-gray-600 bg-gray-50 border-gray-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
}

/**
 * Calculates age from birth date
 * @param birthDate - Birth date string
 * @returns Age in years
 */
export function calculateAge(birthDate: string): number {
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
}

/**
 * Generates a unique ID with optional prefix
 * @param prefix - Optional prefix for the ID
 * @returns Unique ID string
 */
export function generateId(prefix: string = ''): string {
  const timestamp = Date.now().toString(36);
  const randomPart = Math.random().toString(36).substr(2, 5);
  return prefix ? `${prefix}_${timestamp}_${randomPart}` : `${timestamp}_${randomPart}`;
}

/**
 * Debounces a function call
 * @param func - Function to debounce
 * @param delay - Delay in milliseconds
 * @returns Debounced function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

/**
 * Filters an array of objects based on search term
 * @param items - Array of objects to filter
 * @param searchTerm - Search term
 * @param searchFields - Fields to search in
 * @returns Filtered array
 */
export function filterBySearch<T extends Record<string, any>>(
  items: T[],
  searchTerm: string,
  searchFields: (keyof T)[]
): T[] {
  if (!searchTerm.trim()) return items;
  
  const lowerSearchTerm = searchTerm.toLowerCase();
  
  return items.filter(item =>
    searchFields.some(field => {
      const value = item[field];
      if (typeof value === 'string') {
        return value.toLowerCase().includes(lowerSearchTerm);
      }
      if (Array.isArray(value)) {
        return value.some(v => 
          typeof v === 'string' && v.toLowerCase().includes(lowerSearchTerm)
        );
      }
      return false;
    })
  );
}

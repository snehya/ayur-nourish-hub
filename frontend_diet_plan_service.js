// frontend/src/services/dietPlanService.js
// Diet Plan Management Service for AyurDiet Pro

import apiClient from './axiosConfig';
import { API_ENDPOINTS } from '../config/api';

class DietPlanService {
  // Generate diet plan for a patient
  async generateDietPlan(patientId) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.GENERATE_DIET_PLAN, {
        patient_id: patientId
      });
      
      console.log('✅ Diet plan generated successfully');
      return { success: true, data: response.data };
      
    } catch (error) {
      console.error('❌ Failed to generate diet plan:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Failed to generate diet plan' 
      };
    }
  }

  // Get all diet plans for current practitioner
  async getDietPlans() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.DIET_PLANS);
      console.log('✅ Diet plans fetched successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to fetch diet plans:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to fetch diet plans' 
      };
    }
  }

  // Get single diet plan
  async getDietPlan(planId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.DIET_PLAN_DETAIL(planId));
      console.log('✅ Diet plan fetched successfully');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Failed to fetch diet plan:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to fetch diet plan' 
      };
    }
  }

  // Export diet plan as PDF
  async exportDietPlanPDF(planId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.EXPORT_PDF(planId), {
        responseType: 'blob', // Important for PDF download
      });
      
      // Create blob URL for download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const downloadUrl = window.URL.createObjectURL(blob);
      
      console.log('✅ PDF generated successfully');
      return { success: true, downloadUrl, blob };
      
    } catch (error) {
      console.error('❌ Failed to export PDF:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to export PDF' 
      };
    }
  }

  // Download PDF to user's device
  async downloadDietPlanPDF(planId, patientName) {
    const result = await this.exportDietPlanPDF(planId);
    
    if (result.success) {
      // Create temporary download link
      const link = document.createElement('a');
      link.href = result.downloadUrl;
      link.download = `diet_plan_${patientName}_${new Date().toISOString().split('T')[0]}.pdf`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up blob URL
      window.URL.revokeObjectURL(result.downloadUrl);
      
      return { success: true };
    }
    
    return result;
  }

  // Format diet plan for display
  formatDietPlanForDisplay(dietPlan) {
    return {
      ...dietPlan,
      planDate: new Date(dietPlan.plan_date).toLocaleDateString(),
      createdAt: new Date(dietPlan.created_at).toLocaleDateString(),
      meals: this.formatMeals(dietPlan),
    };
  }

  // Format meals from the diet plan
  formatMeals(dietPlan) {
    const meals = {};
    
    // Format breakfast
    if (dietPlan.breakfast) {
      meals.breakfast = this.formatMealData(dietPlan.breakfast);
    }
    
    // Format lunch
    if (dietPlan.lunch) {
      meals.lunch = this.formatMealData(dietPlan.lunch);
    }
    
    // Format dinner
    if (dietPlan.dinner) {
      meals.dinner = this.formatMealData(dietPlan.dinner);
    }
    
    return meals;
  }

  // Format individual meal data
  formatMealData(mealData) {
    // Handle both string and object formats
    if (typeof mealData === 'string') {
      try {
        mealData = JSON.parse(mealData);
      } catch (e) {
        return { foods: [mealData] };
      }
    }
    
    return {
      foods: mealData.foods || [],
      notes: mealData.notes || '',
      timing: mealData.timing || '',
      calories: mealData.calories || 0,
    };
  }

  // Get diet plan summary
  getDietPlanSummary(dietPlan) {
    const meals = this.formatMeals(dietPlan);
    const totalFoods = Object.values(meals).reduce((total, meal) => {
      return total + (meal.foods?.length || 0);
    }, 0);
    
    return {
      totalMeals: Object.keys(meals).length,
      totalFoods,
      hasBreakfast: !!meals.breakfast,
      hasLunch: !!meals.lunch,
      hasDinner: !!meals.dinner,
    };
  }

  // Validate diet plan data
  validateDietPlanData(dietPlanData) {
    const errors = {};

    if (!dietPlanData.patient_id) {
      errors.patient_id = 'Patient is required';
    }

    if (!dietPlanData.plan_date) {
      errors.plan_date = 'Plan date is required';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }
}

// Export singleton instance
const dietPlanService = new DietPlanService();
export default dietPlanService;
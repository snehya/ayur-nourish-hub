// Diet plan service for AyurDiet Pro
import apiClient from '../api/client';
import { API_ENDPOINTS } from '../api/config';

// Types for diet plan management
export interface Food {
  id?: number;
  name: string;
  calories?: number;
  protein?: number;
  rasa?: string;
  guna?: string;
  virya?: string;
}

export interface MealPlan {
  foods: string[];
  instructions?: string;
  timing?: string;
}

export interface DietPlan {
  id?: number;
  patient_id: number;
  patient_name?: string;
  plan_date?: string;
  breakfast: MealPlan | string;
  lunch: MealPlan | string;
  dinner: MealPlan | string;
  full_plan?: Record<string, unknown>;
}

export interface GenerateDietPlanRequest {
  patient_id: number;
}

export interface GenerateDietPlanResponse {
  generated_plan: DietPlan;
  ayurvedic_guidelines?: string[];
  message: string;
}

class DietPlanService {
  /**
   * Generate a new diet plan for a patient
   */
  async generateDietPlan(patientId: number): Promise<GenerateDietPlanResponse> {
    try {
      const requestData: GenerateDietPlanRequest = { patient_id: patientId };
      
      const response = await apiClient.post<GenerateDietPlanResponse>(
        API_ENDPOINTS.GENERATE_DIET_PLAN,
        requestData
      );
      
      return response.data;
    } catch (error) {
      throw new Error('Failed to generate diet plan. Please try again.');
    }
  }

  /**
   * Get all diet plans
   */
  async getDietPlans(): Promise<DietPlan[]> {
    try {
      const response = await apiClient.get<DietPlan[]>(API_ENDPOINTS.DIET_PLANS);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch diet plans');
    }
  }

  /**
   * Get a specific diet plan by ID
   */
  async getDietPlan(id: string | number): Promise<DietPlan> {
    try {
      const response = await apiClient.get<DietPlan>(API_ENDPOINTS.DIET_PLAN_DETAIL(id));
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch diet plan with ID ${id}`);
    }
  }

  /**
   * Export diet plan as PDF
   */
  async exportToPDF(planId: string | number): Promise<Blob> {
    try {
      const response = await apiClient.get(API_ENDPOINTS.EXPORT_PDF(planId), {
        responseType: 'blob',
        headers: {
          'Accept': 'application/pdf',
        },
      });
      
      return new Blob([response.data], { type: 'application/pdf' });
    } catch (error) {
      throw new Error('Failed to export diet plan to PDF');
    }
  }

  /**
   * Download PDF file
   */
  async downloadPDF(planId: string | number, filename?: string): Promise<void> {
    try {
      const pdfBlob = await this.exportToPDF(planId);
      
      // Create download link
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename || `diet-plan-${planId}.pdf`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      throw new Error('Failed to download PDF');
    }
  }

  /**
   * Get all foods from the database
   */
  async getFoods(): Promise<Food[]> {
    try {
      const response = await apiClient.get<Food[]>(API_ENDPOINTS.FOODS);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch foods');
    }
  }

  /**
   * Search foods by name
   */
  async searchFoods(query: string): Promise<Food[]> {
    try {
      const allFoods = await this.getFoods();
      return allFoods.filter(food => 
        food.name.toLowerCase().includes(query.toLowerCase())
      );
    } catch (error) {
      throw new Error('Failed to search foods');
    }
  }

  /**
   * Get foods by rasa (taste)
   */
  async getFoodsByRasa(rasa: string): Promise<Food[]> {
    try {
      const allFoods = await this.getFoods();
      return allFoods.filter(food => 
        food.rasa?.toLowerCase().includes(rasa.toLowerCase())
      );
    } catch (error) {
      throw new Error(`Failed to get foods with ${rasa} rasa`);
    }
  }

  /**
   * Get foods by virya (potency)
   */
  async getFoodsByVirya(virya: string): Promise<Food[]> {
    try {
      const allFoods = await this.getFoods();
      return allFoods.filter(food => 
        food.virya?.toLowerCase().includes(virya.toLowerCase())
      );
    } catch (error) {
      throw new Error(`Failed to get foods with ${virya} virya`);
    }
  }

  /**
   * Format meal plan for display
   */
  formatMealPlan(meal: MealPlan | string): { foods: string[]; instructions?: string } {
    if (typeof meal === 'string') {
      try {
        const parsed = JSON.parse(meal);
        return {
          foods: Array.isArray(parsed.foods) ? parsed.foods : [meal],
          instructions: parsed.instructions
        };
      } catch {
        return { foods: [meal] };
      }
    }
    
    return {
      foods: meal.foods || [],
      instructions: meal.instructions
    };
  }

  /**
   * Get diet plan statistics
   */
  async getDietPlanStats(): Promise<{
    total: number;
    recentPlans: DietPlan[];
    plansByPatient: Record<string, number>;
  }> {
    try {
      const plans = await this.getDietPlans();
      
      // Get recent plans (last 10)
      const recentPlans = plans
        .sort((a, b) => {
          const dateA = new Date(a.plan_date || '').getTime();
          const dateB = new Date(b.plan_date || '').getTime();
          return dateB - dateA;
        })
        .slice(0, 10);

      // Count plans by patient
      const plansByPatient: Record<string, number> = {};
      plans.forEach(plan => {
        const patientName = plan.patient_name || `Patient ${plan.patient_id}`;
        plansByPatient[patientName] = (plansByPatient[patientName] || 0) + 1;
      });

      return {
        total: plans.length,
        recentPlans,
        plansByPatient,
      };
    } catch (error) {
      throw new Error('Failed to get diet plan statistics');
    }
  }

  /**
   * Validate diet plan data
   */
  validateDietPlan(planData: Partial<DietPlan>): void {
    if (!planData.patient_id) {
      throw new Error('Patient ID is required');
    }

    if (planData.patient_id <= 0) {
      throw new Error('Invalid patient ID');
    }
  }
}

// Export singleton instance
export const dietPlanService = new DietPlanService();
export default dietPlanService;
import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Info } from 'lucide-react';

interface PatientData {
  name: string;
  age: string;
  gender: string;
  prakriti: string;
  agni: string;
  bowelMovement: string;
  healthCondition: string;
}

interface FoodItem {
  name: string;
  category: string;
  thermalProperty: 'Hot' | 'Cold' | 'Neutral';
  digestibility: 'Easy' | 'Moderate' | 'Difficult';
  rasa: string[];
  nutrients: {
    calories: number;
    protein: number;
    carbs: number;
    vitamins: string[];
  };
  contraindications: string[];
}

interface ContraIndicationAlertProps {
  patientData: PatientData;
  selectedFoods: FoodItem[];
}

export const ContraIndicationAlert: React.FC<ContraIndicationAlertProps> = ({
  patientData,
  selectedFoods
}) => {
  const checkContraIndications = () => {
    const alerts = [];
    
    for (const food of selectedFoods) {
      // Check thermal property conflicts
      if (patientData.prakriti === 'Vata' && food.thermalProperty === 'Cold') {
        alerts.push({
          type: 'warning' as const,
          food: food.name,
          reason: `${food.name} has a cold property which may aggravate Vata dosha. Consider warming spices or cooking methods.`,
          suggestion: 'Add ginger, cumin, or warm the food before serving.'
        });
      }
      
      if (patientData.prakriti === 'Pitta' && food.thermalProperty === 'Hot') {
        alerts.push({
          type: 'warning' as const,
          food: food.name,
          reason: `${food.name} has a hot property which may aggravate Pitta dosha. Consider cooling accompaniments.`,
          suggestion: 'Pair with cooling herbs like coriander or mint, or consume with ghee.'
        });
      }
      
      // Check digestibility conflicts
      if (patientData.agni === 'Weak' && food.digestibility === 'Difficult') {
        alerts.push({
          type: 'error' as const,
          food: food.name,
          reason: `${food.name} is difficult to digest and may strain weak Agni. Consider alternatives.`,
          suggestion: 'Replace with easily digestible options like kitchari or steamed vegetables.'
        });
      }
      
      // Check specific contraindications
      for (const contraindication of food.contraindications) {
        if (patientData.healthCondition.toLowerCase().includes(contraindication.toLowerCase().split(' ')[0])) {
          alerts.push({
            type: 'error' as const,
            food: food.name,
            reason: `${food.name} is contraindicated for ${contraindication.toLowerCase()}.`,
            suggestion: 'Remove from diet plan and consult alternatives.'
          });
        }
      }
    }
    
    return alerts;
  };

  const alerts = checkContraIndications();
  
  if (alerts.length === 0) {
    return (
      <Alert className="bg-success/5 border-success/20">
        <Info className="h-4 w-4 text-success" />
        <AlertTitle className="text-success">No Contra-indications Detected</AlertTitle>
        <AlertDescription>
          All selected foods are suitable for this patient's constitution and current condition.
        </AlertDescription>
      </Alert>
    );
  }

  const warningAlerts = alerts.filter(a => a.type === 'warning');
  const errorAlerts = alerts.filter(a => a.type === 'error');

  return (
    <div className="space-y-4">
      {errorAlerts.length > 0 && (
        <Alert className="bg-destructive/5 border-destructive/20">
          <AlertTriangle className="h-4 w-4 text-destructive" />
          <AlertTitle className="text-destructive">Critical Contra-indications Found</AlertTitle>
          <AlertDescription>
            <div className="space-y-3 mt-2">
              {errorAlerts.map((alert, index) => (
                <div key={index} className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="destructive" className="text-xs">{alert.food}</Badge>
                    <span className="text-sm">{alert.reason}</span>
                  </div>
                  <p className="text-xs text-muted-foreground pl-2 border-l-2 border-destructive/30">
                    💡 {alert.suggestion}
                  </p>
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}
      
      {warningAlerts.length > 0 && (
        <Alert className="bg-warning/5 border-warning/20">
          <AlertTriangle className="h-4 w-4 text-warning" />
          <AlertTitle className="text-warning">Dietary Cautions</AlertTitle>
          <AlertDescription>
            <div className="space-y-3 mt-2">
              {warningAlerts.map((alert, index) => (
                <div key={index} className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-xs border-warning/30">{alert.food}</Badge>
                    <span className="text-sm">{alert.reason}</span>
                  </div>
                  <p className="text-xs text-muted-foreground pl-2 border-l-2 border-warning/30">
                    💡 {alert.suggestion}
                  </p>
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Brain, Download, Eye, Lightbulb, Utensils } from 'lucide-react';
import { ContraIndicationAlert } from './ContraIndicationAlert';
import { RasaDistributionChart } from './RasaDistributionChart';

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

const mockFoodDatabase: FoodItem[] = [
  {
    name: 'Basmati Rice',
    category: 'Grains',
    thermalProperty: 'Neutral',
    digestibility: 'Easy',
    rasa: ['Sweet'],
    nutrients: { calories: 130, protein: 3, carbs: 28, vitamins: ['B1', 'B3'] },
    contraindications: ['Diabetes (large portions)']
  },
  {
    name: 'Ginger',
    category: 'Spices',
    thermalProperty: 'Hot',
    digestibility: 'Easy',
    rasa: ['Pungent', 'Sweet'],
    nutrients: { calories: 80, protein: 2, carbs: 18, vitamins: ['C', 'B6'] },
    contraindications: ['Pitta excess', 'Acid reflux']
  },
  {
    name: 'Cucumber',
    category: 'Vegetables',
    thermalProperty: 'Cold',
    digestibility: 'Easy',
    rasa: ['Sweet', 'Astringent'],
    nutrients: { calories: 16, protein: 1, carbs: 4, vitamins: ['K', 'C'] },
    contraindications: ['Vata excess', 'Poor digestion']
  }
];

export const DietChartGenerator: React.FC = () => {
  const [patientData, setPatientData] = useState<PatientData>({
    name: '',
    age: '',
    gender: '',
    prakriti: '',
    agni: '',
    bowelMovement: '',
    healthCondition: ''
  });

  const [generatedPlan, setGeneratedPlan] = useState<any>(null);
  const [showReasoning, setShowReasoning] = useState(false);

  const generateDietPlan = () => {
    // Mock diet plan generation logic
    const recommendedFoods = mockFoodDatabase.filter(food => {
      // Simple logic based on prakriti
      if (patientData.prakriti === 'Vata' && food.thermalProperty === 'Cold') return false;
      if (patientData.prakriti === 'Pitta' && food.thermalProperty === 'Hot') return false;
      if (patientData.agni === 'Weak' && food.digestibility === 'Difficult') return false;
      return true;
    });

    const plan = {
      breakfast: recommendedFoods.slice(0, 2),
      lunch: recommendedFoods.slice(1, 4),
      dinner: recommendedFoods.slice(0, 3),
      reasoning: {
        prakriti: `Based on ${patientData.prakriti} constitution, we've prioritized ${
          patientData.prakriti === 'Vata' ? 'warm, moist, and grounding foods' :
          patientData.prakriti === 'Pitta' ? 'cooling, mild, and soothing foods' :
          'light, warm, and stimulating foods'
        }.`,
        agni: `With ${patientData.agni.toLowerCase()} digestive fire, we've selected ${
          patientData.agni === 'Strong' ? 'substantial meals that can be properly processed' :
          patientData.agni === 'Weak' ? 'easy-to-digest, light foods' :
          'moderately complex foods to maintain digestive balance'
        }.`,
        rasa: 'The meal plan emphasizes Sweet, Sour, and Salty tastes to pacify Vata, while minimizing Bitter, Pungent, and Astringent tastes.'
      },
      rasaDistribution: {
        Sweet: 40,
        Sour: 20,
        Salty: 15,
        Pungent: 10,
        Bitter: 10,
        Astringent: 5
      }
    };

    setGeneratedPlan(plan);
    setShowReasoning(true);
  };

  return (
    <div className="space-y-6">
      {/* Patient Input Form */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Utensils className="w-5 h-5 text-primary" />
            Diet Chart Generator
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">Patient Name</Label>
              <Input
                id="name"
                value={patientData.name}
                onChange={(e) => setPatientData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter patient name"
              />
            </div>
            <div>
              <Label htmlFor="age">Age</Label>
              <Input
                id="age"
                value={patientData.age}
                onChange={(e) => setPatientData(prev => ({ ...prev, age: e.target.value }))}
                placeholder="Enter age"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Gender</Label>
              <Select value={patientData.gender} onValueChange={(value) => setPatientData(prev => ({ ...prev, gender: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Male">Male</SelectItem>
                  <SelectItem value="Female">Female</SelectItem>
                  <SelectItem value="Other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Prakriti (Constitution)</Label>
              <Select value={patientData.prakriti} onValueChange={(value) => setPatientData(prev => ({ ...prev, prakriti: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select prakriti" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Vata">Vata</SelectItem>
                  <SelectItem value="Pitta">Pitta</SelectItem>
                  <SelectItem value="Kapha">Kapha</SelectItem>
                  <SelectItem value="Vata-Pitta">Vata-Pitta</SelectItem>
                  <SelectItem value="Pitta-Kapha">Pitta-Kapha</SelectItem>
                  <SelectItem value="Vata-Kapha">Vata-Kapha</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Agni (Digestive Fire)</Label>
              <Select value={patientData.agni} onValueChange={(value) => setPatientData(prev => ({ ...prev, agni: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select agni" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Strong">Tikshna Agni (Strong)</SelectItem>
                  <SelectItem value="Moderate">Sama Agni (Moderate)</SelectItem>
                  <SelectItem value="Weak">Manda Agni (Weak)</SelectItem>
                  <SelectItem value="Variable">Vishama Agni (Variable)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Bowel Movement</Label>
              <Select value={patientData.bowelMovement} onValueChange={(value) => setPatientData(prev => ({ ...prev, bowelMovement: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select pattern" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Regular">Regular (1-2 times/day)</SelectItem>
                  <SelectItem value="Irregular">Irregular</SelectItem>
                  <SelectItem value="Constipated">Constipated</SelectItem>
                  <SelectItem value="Loose">Loose stools</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div>
            <Label htmlFor="healthCondition">Current Health Condition</Label>
            <Textarea
              id="healthCondition"
              value={patientData.healthCondition}
              onChange={(e) => setPatientData(prev => ({ ...prev, healthCondition: e.target.value }))}
              placeholder="Any specific health conditions, allergies, or dietary restrictions"
            />
          </div>

          <Button 
            onClick={generateDietPlan}
            className="w-full"
            disabled={!patientData.name || !patientData.prakriti || !patientData.agni}
          >
            <Brain className="w-4 h-4 mr-2" />
            Generate Personalized Diet Chart
          </Button>
        </CardContent>
      </Card>

      {/* Generated Diet Plan */}
      {generatedPlan && (
        <div className="space-y-6">
          {/* Contra-indication Alerts */}
          <ContraIndicationAlert 
            patientData={patientData}
            selectedFoods={[...generatedPlan.breakfast, ...generatedPlan.lunch, ...generatedPlan.dinner]}
          />

          {/* Diet Plan Display */}
          <Card className="medical-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Eye className="w-5 h-5 text-success" />
                  Personalized Diet Chart for {patientData.name}
                </CardTitle>
                <div className="flex gap-2">
                  <Button variant="outline" onClick={() => setShowReasoning(!showReasoning)}>
                    <Lightbulb className="w-4 h-4 mr-2" />
                    {showReasoning ? 'Hide' : 'Show'} Reasoning
                  </Button>
                  <Button variant="outline">
                    <Download className="w-4 h-4 mr-2" />
                    Export PDF
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Reasoning Section */}
              {showReasoning && (
                <Alert className="bg-primary/5 border-primary/20">
                  <Lightbulb className="h-4 w-4" />
                  <AlertDescription>
                    <div className="space-y-2">
                      <p><strong>Prakriti Consideration:</strong> {generatedPlan.reasoning.prakriti}</p>
                      <p><strong>Agni Assessment:</strong> {generatedPlan.reasoning.agni}</p>
                      <p><strong>Rasa Balance:</strong> {generatedPlan.reasoning.rasa}</p>
                    </div>
                  </AlertDescription>
                </Alert>
              )}

              {/* Rasa Distribution Chart */}
              <RasaDistributionChart rasaData={generatedPlan.rasaDistribution} />

              <Separator />

              {/* Meal Plans */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {['breakfast', 'lunch', 'dinner'].map((meal) => (
                  <div key={meal} className="space-y-3">
                    <h3 className="font-semibold text-lg capitalize">{meal}</h3>
                    <div className="space-y-2">
                      {generatedPlan[meal].map((food: FoodItem, index: number) => (
                        <Card key={index} className="p-3">
                          <div className="space-y-2">
                            <h4 className="font-medium">{food.name}</h4>
                            <div className="flex flex-wrap gap-1">
                              <Badge variant="secondary" className="text-xs">
                                {food.thermalProperty}
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {food.digestibility}
                              </Badge>
                              {food.rasa.map((r, i) => (
                                <Badge key={i} variant="secondary" className="text-xs">
                                  {r}
                                </Badge>
                              ))}
                            </div>
                            <p className="text-xs text-muted-foreground">
                              {food.nutrients.calories} cal | {food.nutrients.protein}g protein
                            </p>
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
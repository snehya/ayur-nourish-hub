import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  Play, 
  Pause,
  Utensils,
  Heart,
  MessageSquare
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface MealItem {
  id: string;
  name: string;
  time: string;
  description: string;
  instructions: string;
  rasa: string[];
  properties: string[];
  benefits: string[];
  status: 'pending' | 'completed' | 'skipped' | 'discomfort';
}

interface DietPlan {
  id: string;
  doctorName: string;
  createdDate: string;
  validUntil: string;
  voiceNote?: string;
  specialInstructions: string;
  meals: MealItem[];
}

export const PatientDietPlan = () => {
  const [playingVoiceNote, setPlayingVoiceNote] = useState(false);
  const { toast } = useToast();

  // Mock data - replace with real data from backend
  const dietPlan: DietPlan = {
    id: "dp_001",
    doctorName: "Dr. Priya Sharma",
    createdDate: "2024-01-15",
    validUntil: "2024-02-15",
    voiceNote: "Remember to eat slowly and mindfully. Drink warm water throughout the day.",
    specialInstructions: "Avoid cold foods and drinks. Take meals at regular intervals. Practice deep breathing before meals.",
    meals: [
      {
        id: "meal_1",
        name: "Morning Breakfast",
        time: "7:00 AM",
        description: "Warm oatmeal with ghee, almonds, and dates",
        instructions: "Cook oats in milk, add 1 tsp ghee, 5 soaked almonds, and 2 chopped dates. Eat warm.",
        rasa: ["Sweet", "Astringent"],
        properties: ["Warm", "Nourishing", "Easy to digest"],
        benefits: ["Strengthens digestion", "Provides sustained energy", "Calms Vata dosha"],
        status: "completed"
      },
      {
        id: "meal_2",
        name: "Mid-Morning Snack",
        time: "10:00 AM",
        description: "Fresh ginger tea with jaggery",
        instructions: "Boil fresh ginger slices in water for 5 minutes. Add jaggery to taste. Drink warm.",
        rasa: ["Pungent", "Sweet"],
        properties: ["Warming", "Digestive"],
        benefits: ["Improves digestion", "Boosts metabolism"],
        status: "completed"
      },
      {
        id: "meal_3",
        name: "Lunch",
        time: "12:30 PM",
        description: "Khichdi with vegetables and ghee",
        instructions: "Cook rice and moong dal together with turmeric, cumin, and seasonal vegetables. Top with ghee.",
        rasa: ["Sweet", "Salty"],
        properties: ["Warm", "Light", "Complete protein"],
        benefits: ["Easy digestion", "Balanced nutrition", "Detoxifying"],
        status: "pending"
      },
      {
        id: "meal_4",
        name: "Evening Snack",
        time: "4:00 PM",
        description: "Warm spiced milk with cardamom",
        instructions: "Heat milk with a pinch of cardamom powder and turmeric. Add honey after cooling slightly.",
        rasa: ["Sweet"],
        properties: ["Warm", "Calming", "Nutritious"],
        benefits: ["Strengthens tissues", "Promotes calmness"],
        status: "pending"
      },
      {
        id: "meal_5",
        name: "Dinner",
        time: "7:00 PM",
        description: "Light vegetable soup with chapati",
        instructions: "Prepare soup with seasonal vegetables, ginger, and mild spices. Serve with one warm chapati.",
        rasa: ["Sweet", "Salty", "Pungent"],
        properties: ["Light", "Warm", "Easy to digest"],
        benefits: ["Light on stomach", "Provides essential nutrients"],
        status: "pending"
      }
    ]
  };

  const handleMealAction = (mealId: string, action: 'completed' | 'skipped' | 'discomfort') => {
    const actionLabels = {
      completed: "meal as completed",
      skipped: "meal as skipped", 
      discomfort: "discomfort with meal"
    };

    toast({
      title: `Meal Updated`,
      description: `Marked ${actionLabels[action]}. Your doctor will be notified.`,
    });
  };

  const toggleVoiceNote = () => {
    setPlayingVoiceNote(!playingVoiceNote);
    // In real implementation, play/pause audio
    setTimeout(() => setPlayingVoiceNote(false), 3000); // Mock 3-second playback
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-success" />;
      case 'skipped':
        return <XCircle className="h-5 w-5 text-destructive" />;
      case 'discomfort':
        return <AlertTriangle className="h-5 w-5 text-warning" />;
      default:
        return <Clock className="h-5 w-5 text-muted-foreground" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-success text-success-foreground">Completed</Badge>;
      case 'skipped':
        return <Badge variant="destructive">Skipped</Badge>;
      case 'discomfort':
        return <Badge className="bg-warning text-warning-foreground">Discomfort</Badge>;
      default:
        return <Badge variant="outline">Pending</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <Card className="medical-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarFallback>PS</AvatarFallback>
              </Avatar>
              <div>
                <CardTitle className="text-lg">Your Personalized Diet Plan</CardTitle>
                <p className="text-sm text-muted-foreground">
                  Created by {dietPlan.doctorName} • Valid until {new Date(dietPlan.validUntil).toLocaleDateString()}
                </p>
              </div>
            </div>
            <Heart className="h-6 w-6 text-primary" />
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Voice Note */}
          {dietPlan.voiceNote && (
            <div className="p-4 bg-primary/5 rounded-lg border border-primary/20">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-primary">Personal Message from Your Doctor</h4>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={toggleVoiceNote}
                  className="flex items-center gap-2"
                >
                  {playingVoiceNote ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                  {playingVoiceNote ? "Playing..." : "Listen"}
                </Button>
              </div>
              <p className="text-sm text-muted-foreground italic">"{dietPlan.voiceNote}"</p>
            </div>
          )}

          {/* Special Instructions */}
          <div className="p-4 bg-accent/50 rounded-lg">
            <h4 className="font-medium mb-2 flex items-center gap-2">
              <MessageSquare className="h-4 w-4" />
              Special Instructions
            </h4>
            <p className="text-sm text-muted-foreground">{dietPlan.specialInstructions}</p>
          </div>
        </CardContent>
      </Card>

      {/* Meals List */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Utensils className="h-5 w-5" />
            Today's Meals
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[600px]">
            <div className="space-y-4">
              {dietPlan.meals.map((meal, index) => (
                <div key={meal.id}>
                  <div className="p-4 border border-border rounded-lg hover:bg-accent/20 transition-colors">
                    {/* Meal Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        {getStatusIcon(meal.status)}
                        <div>
                          <h3 className="font-semibold">{meal.name}</h3>
                          <p className="text-sm text-muted-foreground">{meal.time}</p>
                        </div>
                      </div>
                      {getStatusBadge(meal.status)}
                    </div>

                    {/* Meal Content */}
                    <div className="space-y-3">
                      <div>
                        <h4 className="font-medium text-primary mb-1">{meal.description}</h4>
                        <p className="text-sm text-muted-foreground">{meal.instructions}</p>
                      </div>

                      {/* Properties */}
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div>
                          <p className="font-medium text-muted-foreground mb-1">Rasa (Taste)</p>
                          <div className="flex flex-wrap gap-1">
                            {meal.rasa.map((r) => (
                              <Badge key={r} variant="secondary" className="text-xs">{r}</Badge>
                            ))}
                          </div>
                        </div>
                        <div>
                          <p className="font-medium text-muted-foreground mb-1">Properties</p>
                          <div className="flex flex-wrap gap-1">
                            {meal.properties.map((p) => (
                              <Badge key={p} variant="outline" className="text-xs">{p}</Badge>
                            ))}
                          </div>
                        </div>
                        <div>
                          <p className="font-medium text-muted-foreground mb-1">Benefits</p>
                          <ul className="text-xs text-muted-foreground space-y-1">
                            {meal.benefits.slice(0, 2).map((benefit, i) => (
                              <li key={i}>• {benefit}</li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {/* Action Buttons */}
                      {meal.status === 'pending' && (
                        <div className="flex gap-2 pt-2">
                          <Button
                            size="sm"
                            onClick={() => handleMealAction(meal.id, 'completed')}
                            className="flex items-center gap-2 bg-success text-success-foreground hover:bg-success/90"
                          >
                            <CheckCircle className="h-4 w-4" />
                            Completed
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleMealAction(meal.id, 'skipped')}
                            className="flex items-center gap-2"
                          >
                            <XCircle className="h-4 w-4" />
                            Skipped
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleMealAction(meal.id, 'discomfort')}
                            className="flex items-center gap-2 text-warning border-warning hover:bg-warning/10"
                          >
                            <AlertTriangle className="h-4 w-4" />
                            Discomfort
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                  {index < dietPlan.meals.length - 1 && <Separator className="my-4" />}
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
};
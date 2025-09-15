import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { User, Calendar, Activity, Heart, TrendingUp, FileText, Edit3, Save, X } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Patient {
  id: string;
  name: string;
  age: number;
  gender: string;
  email: string;
  phone: string;
  address: string;
  
  // Ayurvedic Assessment
  prakriti: string;
  vikriti: string;
  agni: string;
  bowelMovement: string;
  sleep: string;
  stress: string;
  
  // Health Details
  weight: number;
  height: number;
  bmi: number;
  bloodPressure: string;
  allergies: string[];
  medications: string[];
  healthConditions: string[];
  
  // Lifestyle
  activityLevel: string;
  dietPreference: string;
  cookingSkill: string;
  
  // Progress Tracking
  compliance: number;
  lastVisit: string;
  nextVisit: string;
  notes: string;
}

interface PatientProfileProps {
  patient?: Patient;
  onSave?: (patient: Patient) => void;
  mode?: 'view' | 'edit' | 'create';
}

const defaultPatient: Patient = {
  id: '',
  name: '',
  age: 0,
  gender: '',
  email: '',
  phone: '',
  address: '',
  prakriti: '',
  vikriti: '',
  agni: '',
  bowelMovement: '',
  sleep: '',
  stress: '',
  weight: 0,
  height: 0,
  bmi: 0,
  bloodPressure: '',
  allergies: [],
  medications: [],
  healthConditions: [],
  activityLevel: '',
  dietPreference: '',
  cookingSkill: '',
  compliance: 0,
  lastVisit: '',
  nextVisit: '',
  notes: ''
};

export const PatientProfile: React.FC<PatientProfileProps> = ({
  patient = defaultPatient,
  onSave,
  mode = 'view'
}) => {
  const [editMode, setEditMode] = useState(mode === 'edit' || mode === 'create');
  const [formData, setFormData] = useState<Patient>(patient);
  const { toast } = useToast();

  const updateField = (field: keyof Patient, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Auto-calculate BMI when weight or height changes
    if (field === 'weight' || field === 'height') {
      const weight = field === 'weight' ? value : formData.weight;
      const height = field === 'height' ? value : formData.height;
      if (weight && height) {
        const bmi = weight / ((height / 100) ** 2);
        setFormData(prev => ({ ...prev, bmi: Math.round(bmi * 10) / 10 }));
      }
    }
  };

  const handleSave = () => {
    if (!formData.name || !formData.age || !formData.prakriti) {
      toast({
        title: "Missing Information",
        description: "Please fill in name, age, and prakriti assessment.",
        variant: "destructive"
      });
      return;
    }

    onSave?.(formData);
    setEditMode(false);
    
    toast({
      title: "Patient Profile Saved",
      description: `${formData.name}'s profile has been updated successfully.`,
    });
  };

  const handleCancel = () => {
    setFormData(patient);
    setEditMode(false);
  };

  const getPrakritiColor = (prakriti: string) => {
    switch (prakriti.toLowerCase()) {
      case 'vata': return 'element-air';
      case 'pitta': return 'element-fire';
      case 'kapha': return 'element-earth';
      default: return 'element-space';
    }
  };

  const getBMIStatus = (bmi: number) => {
    if (bmi < 18.5) return { status: 'Underweight', color: 'text-warning' };
    if (bmi < 25) return { status: 'Normal', color: 'text-success' };
    if (bmi < 30) return { status: 'Overweight', color: 'text-warning' };
    return { status: 'Obese', color: 'text-destructive' };
  };

  const getComplianceColor = (compliance: number) => {
    if (compliance >= 80) return 'text-success';
    if (compliance >= 60) return 'text-warning';
    return 'text-destructive';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="medical-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <User className="w-5 h-5 text-primary" />
              {editMode ? (mode === 'create' ? 'New Patient Profile' : 'Edit Patient Profile') : 'Patient Profile'}
            </CardTitle>
            <div className="flex gap-2">
              {!editMode ? (
                <Button variant="outline" onClick={() => setEditMode(true)}>
                  <Edit3 className="w-4 h-4 mr-2" />
                  Edit Profile
                </Button>
              ) : (
                <>
                  <Button variant="outline" onClick={handleCancel}>
                    <X className="w-4 h-4 mr-2" />
                    Cancel
                  </Button>
                  <Button onClick={handleSave}>
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </Button>
                </>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Basic Information */}
        <Card className="medical-card lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-primary" />
              Basic Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">Full Name</Label>
                {editMode ? (
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => updateField('name', e.target.value)}
                    placeholder="Enter patient name"
                  />
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.name || 'Not specified'}</p>
                )}
              </div>
              <div>
                <Label htmlFor="age">Age</Label>
                {editMode ? (
                  <Input
                    id="age"
                    type="number"
                    value={formData.age}
                    onChange={(e) => updateField('age', parseInt(e.target.value) || 0)}
                    placeholder="Enter age"
                  />
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.age || 'Not specified'} years</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Gender</Label>
                {editMode ? (
                  <Select value={formData.gender} onValueChange={(value) => updateField('gender', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select gender" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Male">Male</SelectItem>
                      <SelectItem value="Female">Female</SelectItem>
                      <SelectItem value="Other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.gender || 'Not specified'}</p>
                )}
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                {editMode ? (
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => updateField('email', e.target.value)}
                    placeholder="Enter email"
                  />
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.email || 'Not specified'}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="phone">Phone Number</Label>
                {editMode ? (
                  <Input
                    id="phone"
                    value={formData.phone}
                    onChange={(e) => updateField('phone', e.target.value)}
                    placeholder="Enter phone number"
                  />
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.phone || 'Not specified'}</p>
                )}
              </div>
              <div>
                <Label>Diet Preference</Label>
                {editMode ? (
                  <Select value={formData.dietPreference} onValueChange={(value) => updateField('dietPreference', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select preference" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Vegetarian">Vegetarian</SelectItem>
                      <SelectItem value="Vegan">Vegan</SelectItem>
                      <SelectItem value="Non-vegetarian">Non-vegetarian</SelectItem>
                      <SelectItem value="Jain">Jain</SelectItem>
                      <SelectItem value="Eggetarian">Eggetarian</SelectItem>
                    </SelectContent>
                  </Select>
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.dietPreference || 'Not specified'}</p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card className="medical-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-primary" />
              Health Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* BMI */}
            <div className="p-3 rounded-lg bg-muted/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">BMI</span>
                <span className={`font-semibold ${getBMIStatus(patient.bmi).color}`}>
                  {patient.bmi ? patient.bmi : '--'}
                </span>
              </div>
              {patient.bmi && (
                <div>
                  <Progress value={Math.min((patient.bmi / 30) * 100, 100)} className="h-2" />
                  <p className={`text-xs mt-1 ${getBMIStatus(patient.bmi).color}`}>
                    {getBMIStatus(patient.bmi).status}
                  </p>
                </div>
              )}
            </div>

            {/* Compliance */}
            <div className="p-3 rounded-lg bg-muted/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Diet Compliance</span>
                <span className={`font-semibold ${getComplianceColor(patient.compliance)}`}>
                  {patient.compliance}%
                </span>
              </div>
              <Progress value={patient.compliance} className="h-2" />
            </div>

            {/* Prakriti */}
            <div className="p-3 rounded-lg bg-muted/30">
              <span className="text-sm font-medium block mb-2">Constitution</span>
              {patient.prakriti ? (
                <Badge className={`${getPrakritiColor(patient.prakriti)} border`}>
                  {patient.prakriti}
                </Badge>
              ) : (
                <p className="text-xs text-muted-foreground">Not assessed</p>
              )}
            </div>

            {/* Next Visit */}
            <div className="p-3 rounded-lg bg-muted/30">
              <div className="flex items-center gap-2 mb-1">
                <Calendar className="w-4 h-4 text-primary" />
                <span className="text-sm font-medium">Next Visit</span>
              </div>
              <p className="text-xs text-muted-foreground">
                {patient.nextVisit || 'Not scheduled'}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Ayurvedic Assessment */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary" />
            Ayurvedic Assessment
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { key: 'prakriti', label: 'Prakriti', options: ['Vata', 'Pitta', 'Kapha', 'Vata-Pitta', 'Pitta-Kapha', 'Vata-Kapha'] },
              { key: 'agni', label: 'Agni', options: ['Strong', 'Moderate', 'Weak', 'Variable'] },
              { key: 'bowelMovement', label: 'Bowel Movement', options: ['Regular', 'Irregular', 'Constipated', 'Loose'] },
              { key: 'sleep', label: 'Sleep Quality', options: ['Excellent', 'Good', 'Fair', 'Poor'] }
            ].map(({ key, label, options }) => (
              <div key={key}>
                <Label>{label}</Label>
                {editMode ? (
                  <Select value={formData[key as keyof Patient] as string} onValueChange={(value) => updateField(key as keyof Patient, value)}>
                    <SelectTrigger>
                      <SelectValue placeholder={`Select ${label.toLowerCase()}`} />
                    </SelectTrigger>
                    <SelectContent>
                      {options.map(option => (
                        <SelectItem key={option} value={option}>{option}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : (
                  <p className="text-sm mt-1 p-2 bg-muted/30 rounded">
                    {patient[key as keyof Patient] || 'Not assessed'}
                  </p>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Physical Measurements */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Heart className="w-5 h-5 text-primary" />
            Physical Measurements
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <Label htmlFor="weight">Weight (kg)</Label>
              {editMode ? (
                <Input
                  id="weight"
                  type="number"
                  value={formData.weight}
                  onChange={(e) => updateField('weight', parseFloat(e.target.value) || 0)}
                  placeholder="Enter weight"
                />
              ) : (
                <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.weight || '--'} kg</p>
              )}
            </div>
            <div>
              <Label htmlFor="height">Height (cm)</Label>
              {editMode ? (
                <Input
                  id="height"
                  type="number"
                  value={formData.height}
                  onChange={(e) => updateField('height', parseFloat(e.target.value) || 0)}
                  placeholder="Enter height"
                />
              ) : (
                <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.height || '--'} cm</p>
              )}
            </div>
            <div>
              <Label>BMI</Label>
              <p className={`text-sm mt-1 p-2 bg-muted/30 rounded font-medium ${getBMIStatus(formData.bmi || patient.bmi).color}`}>
                {formData.bmi || patient.bmi || '--'}
              </p>
            </div>
            <div>
              <Label htmlFor="bloodPressure">Blood Pressure</Label>
              {editMode ? (
                <Input
                  id="bloodPressure"
                  value={formData.bloodPressure}
                  onChange={(e) => updateField('bloodPressure', e.target.value)}
                  placeholder="e.g., 120/80"
                />
              ) : (
                <p className="text-sm mt-1 p-2 bg-muted/30 rounded">{patient.bloodPressure || 'Not recorded'}</p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notes */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle>Clinical Notes</CardTitle>
        </CardHeader>
        <CardContent>
          {editMode ? (
            <Textarea
              value={formData.notes}
              onChange={(e) => updateField('notes', e.target.value)}
              placeholder="Add clinical observations, treatment notes, or patient feedback..."
              rows={4}
            />
          ) : (
            <p className="text-sm p-2 bg-muted/30 rounded min-h-[100px] whitespace-pre-wrap">
              {patient.notes || 'No notes available.'}
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
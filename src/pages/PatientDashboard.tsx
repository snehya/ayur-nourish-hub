/**
 * @fileoverview Patient Dashboard page for AyurDiet Pro application
 * @author AyurDiet Pro Team
 * @version 1.0.0
 * @description Patient-facing dashboard for diet plan management, progress tracking, and profile information
 */

import React, { memo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  User, 
  Calendar, 
  Activity, 
  Bell, 
  Settings,
  Heart,
  TrendingUp,
  Clock,
  CheckCircle,
  MessageSquare,
  Phone,
  Utensils,
  ArrowLeft
} from "lucide-react";
import { PatientDietPlan } from "@/components/PatientDietPlan";
import { OshvaLogo } from "@/components/OshvaLogo";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "@/hooks/useOptimizations";
import { ActivityItem } from "@/types";
import { formatDate, cn } from "@/lib/utils";

/**
 * Patient data interface for the dashboard
 */
interface PatientDashboardData {
  name: string;
  age: number;
  gender: string;
  prakriti: string;
  phone: string;
  email: string;
  doctorName: string;
  doctorPhone: string;
  nextAppointment: string;
  planStartDate: string;
  planDuration: number;
  currentDay: number;
}

/**
 * Today's progress statistics
 */
interface TodayStats {
  mealsCompleted: number;
  totalMeals: number;
  complianceRate: number;
  streak: number;
}

/**
 * Props for StatCard component
 */
interface StatCardProps {
  icon: React.ComponentType<any>;
  iconColor: string;
  title: string;
  value: string | number;
  subtitle?: string;
  progress?: number;
  className?: string;
}

/**
 * Memoized stat card component
 */
const StatCard = memo<StatCardProps>(({ 
  icon: Icon, 
  iconColor, 
  title, 
  value, 
  subtitle, 
  progress,
  className 
}) => (
  <Card className={cn("medical-card", className)}>
    <CardContent className="p-4">
      <div className="flex items-center gap-2 mb-2">
        <Icon className={cn("h-4 w-4", iconColor)} />
        <span className="text-sm font-medium">{title}</span>
      </div>
      <div className="text-2xl font-bold">{value}</div>
      {progress !== undefined && (
        <Progress value={progress} className="mt-2" />
      )}
      {subtitle && (
        <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
      )}
    </CardContent>
  </Card>
));

StatCard.displayName = 'StatCard';

StatCard.displayName = 'StatCard';

/**
 * Props for ActivityCard component
 */
interface ActivityCardProps {
  activities: ActivityItem[];
}

/**
 * Memoized activity card component
 */
const ActivityCard = memo<ActivityCardProps>(({ activities }) => (
  <Card className="medical-card">
    <CardHeader>
      <CardTitle>Recent Activity</CardTitle>
    </CardHeader>
    <CardContent>
      <div className="space-y-4">
        {activities.map((activity, index) => (
          <div key={index} className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent/50 transition-colors">
            <activity.icon className={cn("h-5 w-5 mt-0.5", activity.color)} />
            <div className="flex-1">
              <p className="text-sm font-medium">{activity.action}</p>
              <p className="text-xs text-muted-foreground">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </CardContent>
  </Card>
));

ActivityCard.displayName = 'ActivityCard';

/**
 * Props for PatientInfoCard component
 */
interface PatientInfoCardProps {
  patient: PatientDashboardData;
}

/**
 * Memoized patient information card
 */
const PatientInfoCard = memo<PatientInfoCardProps>(({ patient }) => (
  <Card className="medical-card">
    <CardHeader>
      <CardTitle>Personal Information</CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="flex items-center gap-4">
        <Avatar className="h-16 w-16">
          <AvatarImage src="/placeholder-avatar.jpg" alt={patient.name} />
          <AvatarFallback className="text-xl">
            {patient.name.split(' ').map(n => n[0]).join('')}
          </AvatarFallback>
        </Avatar>
        <div>
          <h3 className="text-xl font-semibold">{patient.name}</h3>
          <p className="text-muted-foreground">{patient.age} years • {patient.gender}</p>
          <Badge className="mt-1 bg-primary text-primary-foreground">
            Prakriti: {patient.prakriti}
          </Badge>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <p className="text-sm font-medium text-muted-foreground">Phone</p>
          <p>{patient.phone}</p>
        </div>
        <div>
          <p className="text-sm font-medium text-muted-foreground">Email</p>
          <p>{patient.email}</p>
        </div>
      </div>
    </CardContent>
  </Card>
));

PatientInfoCard.displayName = 'PatientInfoCard';

/**
 * Props for DoctorInfoCard component
 */
interface DoctorInfoCardProps {
  doctorName: string;
  nextAppointment: string;
  onContactDoctor?: () => void;
}

/**
 * Memoized doctor information card
 */
const DoctorInfoCard = memo<DoctorInfoCardProps>(({ 
  doctorName, 
  nextAppointment, 
  onContactDoctor 
}) => {
  const handleContactClick = React.useCallback(() => {
    onContactDoctor?.();
  }, [onContactDoctor]);

  return (
    <Card className="medical-card">
      <CardHeader>
        <CardTitle>Your Ayurvedic Practitioner</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <Avatar>
            <AvatarFallback>PS</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <h3 className="font-semibold">{doctorName}</h3>
            <p className="text-sm text-muted-foreground">Certified Ayurvedic Practitioner</p>
          </div>
          <Button variant="outline" size="sm" onClick={handleContactClick}>
            <Phone className="h-4 w-4 mr-2" />
            Contact
          </Button>
        </div>

        <div className="pt-2">
          <p className="text-sm text-muted-foreground mb-1">Next Appointment</p>
          <p className="font-medium">
            {new Date(nextAppointment).toLocaleDateString('en-IN', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </p>
        </div>
      </CardContent>
    </Card>
  );
});

DoctorInfoCard.displayName = 'DoctorInfoCard';

/**
 * Main PatientDashboard component
 */
const PatientDashboard = () => {
  const navigate = useNavigate();
  
  // Use local storage for active tab persistence
  const [activeTab, setActiveTab] = useLocalStorage('patient-dashboard-tab', 'diet-plan');

  // Mock patient data
  const patientData: PatientDashboardData = {
    name: "Rajesh Kumar",
    age: 45,
    gender: "Male",
    prakriti: "Vata-Pitta",
    phone: "+91 98765 43210",
    email: "rajesh.kumar@email.com",
    doctorName: "Dr. Priya Sharma",
    doctorPhone: "+91 98765 12345",
    nextAppointment: "2024-01-25",
    planStartDate: "2024-01-15",
    planDuration: 30,
    currentDay: 10
  };

  const todayStats: TodayStats = {
    mealsCompleted: 3,
    totalMeals: 5,
    complianceRate: 85,
    streak: 7
  };

  const recentActivity: ActivityItem[] = [
    {
      action: "Completed Morning Breakfast",
      time: "2 hours ago",
      patient: patientData.name,
      icon: CheckCircle,
      color: "text-success"
    },
    {
      action: "Reported mild discomfort after lunch",
      time: "Yesterday",
      patient: patientData.name,
      icon: MessageSquare,
      color: "text-warning"
    },
    {
      action: "Perfect day - all meals completed",
      time: "2 days ago",
      patient: patientData.name,
      icon: Heart,
      color: "text-primary"
    }
  ];

  // Memoized callbacks
  const handleBackClick = React.useCallback(() => {
    navigate(-1);
  }, [navigate]);

  const handleContactDoctor = React.useCallback(() => {
    console.log('Contacting doctor:', patientData.doctorName);
    // Implement contact functionality
  }, [patientData.doctorName]);

  // Memoized computed values
  const mealProgress = React.useMemo(() => 
    (todayStats.mealsCompleted / todayStats.totalMeals) * 100,
    [todayStats.mealsCompleted, todayStats.totalMeals]
  );

  const planProgress = React.useMemo(() => 
    (patientData.currentDay / patientData.planDuration) * 100,
    [patientData.currentDay, patientData.planDuration]
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-10 border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="flex h-16 items-center gap-4 px-6">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleBackClick}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>
          
          <div className="flex-1 flex items-center gap-2">
            <OshvaLogo size={24} />
            <h1 className="text-2xl font-bold text-primary">Somae</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="outline" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            
            <Avatar>
              <AvatarImage src="/placeholder-avatar.jpg" alt={patientData.name} />
              <AvatarFallback>
                {patientData.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b bg-card">
        <div className="px-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full max-w-md grid-cols-3">
              <TabsTrigger value="diet-plan" className="flex items-center gap-2">
                <Utensils className="h-4 w-4" />
                Diet Plan
              </TabsTrigger>
              <TabsTrigger value="progress" className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                Progress
              </TabsTrigger>
              <TabsTrigger value="profile" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Profile
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsContent value="diet-plan" className="p-6">
            {/* Welcome Section */}
            <div className="mb-6">
              <h2 className="text-3xl font-bold text-foreground">
                Welcome back, {patientData.name.split(' ')[0]}
              </h2>
              <p className="text-muted-foreground">
                Day {patientData.currentDay} of your personalized Ayurvedic diet plan
              </p>
            </div>

            {/* Today's Progress */}
            <div className="grid gap-4 md:grid-cols-4 mb-6">
              <StatCard
                icon={Utensils}
                iconColor="text-primary"
                title="Today's Meals"
                value={`${todayStats.mealsCompleted}/${todayStats.totalMeals}`}
                progress={mealProgress}
              />

              <StatCard
                icon={TrendingUp}
                iconColor="text-success"
                title="Compliance Rate"
                value={`${todayStats.complianceRate}%`}
                subtitle="This week average"
                className="text-success"
              />

              <StatCard
                icon={Heart}
                iconColor="text-primary"
                title="Current Streak"
                value={`${todayStats.streak} days`}
                subtitle="Keep it up!"
              />

              <StatCard
                icon={Calendar}
                iconColor="text-earth"
                title="Next Appointment"
                value={formatDate(patientData.nextAppointment)}
                subtitle={`With ${patientData.doctorName}`}
              />
            </div>

            {/* Diet Plan Component */}
            <PatientDietPlan />
          </TabsContent>

          <TabsContent value="progress" className="p-6">
            <div className="space-y-6">
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Weekly Progress</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>Overall Compliance</span>
                      <Badge className="bg-success text-success-foreground">
                        {todayStats.complianceRate}%
                      </Badge>
                    </div>
                    <Progress value={todayStats.complianceRate} className="h-2" />
                    
                    <div className="text-center py-12">
                      <TrendingUp className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                      <h3 className="text-lg font-semibold mb-2">Detailed Analytics Coming Soon</h3>
                      <p className="text-muted-foreground">
                        View your daily compliance trends, dosha balance improvements, and health metrics over time.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Recent Activity */}
              <ActivityCard activities={recentActivity} />
            </div>
          </TabsContent>

          <TabsContent value="profile" className="p-6">
            <div className="space-y-6">
              {/* Patient Info */}
              <PatientInfoCard patient={patientData} />

              {/* Doctor Info */}
              <DoctorInfoCard 
                doctorName={patientData.doctorName}
                nextAppointment={patientData.nextAppointment}
                onContactDoctor={handleContactDoctor}
              />

              {/* Plan Info */}
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Current Diet Plan</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Plan Started</p>
                      <p>{formatDate(patientData.planStartDate)}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Duration</p>
                      <p>{patientData.planDuration} days</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Current Day</p>
                      <p>Day {patientData.currentDay} of {patientData.planDuration}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Progress</p>
                      <div className="flex items-center gap-2">
                        <Progress value={planProgress} className="flex-1" />
                        <span className="text-sm">{Math.round(planProgress)}%</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default PatientDashboard;
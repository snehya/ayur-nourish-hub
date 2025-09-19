import React, { useState } from "react";
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
import { useNavigate } from "react-router-dom";

const PatientDashboard = () => {
  const [activeTab, setActiveTab] = useState("diet-plan");
  const navigate = useNavigate();

  // Mock patient data
  const patientData = {
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

  const todayStats = {
    mealsCompleted: 3,
    totalMeals: 5,
    complianceRate: 85,
    streak: 7
  };

  const recentActivity = [
    {
      action: "Completed Morning Breakfast",
      time: "2 hours ago",
      icon: CheckCircle,
      color: "text-success"
    },
    {
      action: "Reported mild discomfort after lunch",
      time: "Yesterday",
      icon: MessageSquare,
      color: "text-warning"
    },
    {
      action: "Perfect day - all meals completed",
      time: "2 days ago",
      icon: Heart,
      color: "text-primary"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-10 border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="flex h-16 items-center gap-4 px-6">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => navigate(-1)}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>
          
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-primary">AyurDiet Pro</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="outline" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            
            <Avatar>
              <AvatarImage src="/placeholder-avatar.jpg" alt={patientData.name} />
              <AvatarFallback>{patientData.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
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
              <h2 className="text-3xl font-bold text-foreground">Welcome back, {patientData.name.split(' ')[0]}</h2>
              <p className="text-muted-foreground">Day {patientData.currentDay} of your personalized Ayurvedic diet plan</p>
            </div>

            {/* Today's Progress */}
            <div className="grid gap-4 md:grid-cols-4 mb-6">
              <Card className="medical-card">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Utensils className="h-4 w-4 text-primary" />
                    <span className="text-sm font-medium">Today's Meals</span>
                  </div>
                  <div className="text-2xl font-bold">{todayStats.mealsCompleted}/{todayStats.totalMeals}</div>
                  <Progress value={(todayStats.mealsCompleted / todayStats.totalMeals) * 100} className="mt-2" />
                </CardContent>
              </Card>

              <Card className="medical-card">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="h-4 w-4 text-success" />
                    <span className="text-sm font-medium">Compliance Rate</span>
                  </div>
                  <div className="text-2xl font-bold text-success">{todayStats.complianceRate}%</div>
                  <p className="text-xs text-muted-foreground mt-1">This week average</p>
                </CardContent>
              </Card>

              <Card className="medical-card">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Heart className="h-4 w-4 text-primary" />
                    <span className="text-sm font-medium">Current Streak</span>
                  </div>
                  <div className="text-2xl font-bold text-primary">{todayStats.streak} days</div>
                  <p className="text-xs text-muted-foreground mt-1">Keep it up!</p>
                </CardContent>
              </Card>

              <Card className="medical-card">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Calendar className="h-4 w-4 text-earth" />
                    <span className="text-sm font-medium">Next Appointment</span>
                  </div>
                  <div className="text-sm font-bold">{new Date(patientData.nextAppointment).toLocaleDateString()}</div>
                  <p className="text-xs text-muted-foreground mt-1">With {patientData.doctorName}</p>
                </CardContent>
              </Card>
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
                      <Badge className="bg-success text-success-foreground">{todayStats.complianceRate}%</Badge>
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
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent/50 transition-colors">
                        <activity.icon className={`h-5 w-5 mt-0.5 ${activity.color}`} />
                        <div className="flex-1">
                          <p className="text-sm font-medium">{activity.action}</p>
                          <p className="text-xs text-muted-foreground">{activity.time}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="profile" className="p-6">
            <div className="space-y-6">
              {/* Patient Info */}
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Personal Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center gap-4">
                    <Avatar className="h-16 w-16">
                      <AvatarImage src="/placeholder-avatar.jpg" alt={patientData.name} />
                      <AvatarFallback className="text-xl">{patientData.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="text-xl font-semibold">{patientData.name}</h3>
                      <p className="text-muted-foreground">{patientData.age} years • {patientData.gender}</p>
                      <Badge className="mt-1 bg-primary text-primary-foreground">
                        Prakriti: {patientData.prakriti}
                      </Badge>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Phone</p>
                      <p>{patientData.phone}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Email</p>
                      <p>{patientData.email}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Doctor Info */}
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
                      <h3 className="font-semibold">{patientData.doctorName}</h3>
                      <p className="text-sm text-muted-foreground">Certified Ayurvedic Practitioner</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Phone className="h-4 w-4 mr-2" />
                      Contact
                    </Button>
                  </div>

                  <div className="pt-2">
                    <p className="text-sm text-muted-foreground mb-1">Next Appointment</p>
                    <p className="font-medium">{new Date(patientData.nextAppointment).toLocaleDateString('en-IN', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}</p>
                  </div>
                </CardContent>
              </Card>

              {/* Plan Info */}
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Current Diet Plan</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Plan Started</p>
                      <p>{new Date(patientData.planStartDate).toLocaleDateString()}</p>
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
                        <Progress value={(patientData.currentDay / patientData.planDuration) * 100} className="flex-1" />
                        <span className="text-sm">{Math.round((patientData.currentDay / patientData.planDuration) * 100)}%</span>
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
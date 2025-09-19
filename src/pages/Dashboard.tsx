import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Users, 
  Calendar, 
  Activity, 
  TrendingUp, 
  Search, 
  Bell, 
  Plus,
  FileText,
  Heart,
  Clock,
  MessageSquare,
  Settings,
  Utensils,
  Database,
  Brain,
  BarChart3,
  ArrowLeft
} from "lucide-react";
import { DietChartGenerator } from "@/components/DietChartGenerator";
import { FoodDatabase } from "@/components/FoodDatabase";
import { PatientProfile } from "@/components/PatientProfile";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("dashboard");
  const navigate = useNavigate();

  // Mock data - replace with real data from your backend
  const stats = [
    {
      title: "Total Patients",
      value: "284",
      change: "+12%",
      changeType: "positive" as const,
      icon: Users,
      color: "bg-primary"
    },
    {
      title: "Active Diet Plans", 
      value: "156",
      change: "+8%",
      changeType: "positive" as const,
      icon: FileText,
      color: "bg-earth"
    },
    {
      title: "This Month Consultations",
      value: "89",
      change: "+23%", 
      changeType: "positive" as const,
      icon: Calendar,
      color: "bg-success"
    },
    {
      title: "Avg. Compliance Rate",
      value: "87%",
      change: "+5%",
      changeType: "positive" as const,
      icon: TrendingUp,
      color: "bg-warning"
    }
  ];

  const recentPatients = [
    {
      name: "Rajesh Kumar",
      age: 45,
      gender: "Male",
      prakriti: "Vata-Pitta",
      constitution: "Vata-Pitta",
      status: "Active Treatment",
      lastVisit: "2024-01-15"
    },
    {
      name: "Priya Sharma", 
      age: 32,
      gender: "Female",
      prakriti: "Pitta",
      constitution: "Pitta",
      status: "Follow-up Due",
      lastVisit: "2024-01-10"
    },
    {
      name: "Amit Singh",
      age: 28,
      gender: "Male", 
      prakriti: "Kapha",
      constitution: "Kapha",
      status: "New Patient",
      lastVisit: "2024-01-20"
    },
    {
      name: "Sunita Patel",
      age: 55,
      gender: "Female",
      prakriti: "Vata",
      constitution: "Vata", 
      status: "Active Treatment",
      lastVisit: "2024-01-18"
    }
  ];

  const recentActivity = [
    {
      action: "Diet chart generated",
      patient: "Rajesh Kumar",
      time: "2 hours ago",
      icon: FileText,
      color: "bg-primary"
    },
    {
      action: "Follow-up scheduled",
      patient: "Priya Sharma", 
      time: "4 hours ago",
      icon: Calendar,
      color: "bg-success"
    },
    {
      action: "New patient registered",
      patient: "Amit Singh",
      time: "1 day ago", 
      icon: Users,
      color: "bg-earth"
    },
    {
      action: "Compliance updated",
      patient: "Sunita Patel",
      time: "2 days ago",
      icon: Activity,
      color: "bg-warning"
    }
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Active Treatment":
        return <Badge variant="default" className="bg-success text-success-foreground">Active</Badge>;
      case "Follow-up Due":
        return <Badge variant="destructive">Follow-up Due</Badge>;
      case "New Patient":
        return <Badge variant="secondary">New Patient</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  const getConstitutionColor = (constitution: string) => {
    switch (constitution.toLowerCase()) {
      case "vata":
        return "bg-air";
      case "pitta": 
        return "bg-fire";
      case "kapha":
        return "bg-earth";
      default:
        return "bg-primary";
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Sticky Header */}
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
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search patients, diets, foods..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64 pl-10"
              />
            </div>
            
            <Button variant="outline" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            
            <Avatar>
              <AvatarImage src="/placeholder-avatar.jpg" alt="Dr. Priya Sharma" />
              <AvatarFallback>PS</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b bg-card">
        <div className="px-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full max-w-lg grid-cols-5">
              <TabsTrigger value="dashboard" className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                Dashboard
              </TabsTrigger>
              <TabsTrigger value="patients" className="flex items-center gap-2">
                <Users className="h-4 w-4" />
                Patients
              </TabsTrigger>
              <TabsTrigger value="diet-generator" className="flex items-center gap-2">
                <Brain className="h-4 w-4" />
                Diet Generator
              </TabsTrigger>
              <TabsTrigger value="food-database" className="flex items-center gap-2">
                <Database className="h-4 w-4" />
                Food Database
              </TabsTrigger>
              <TabsTrigger value="analytics" className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                Analytics
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      {/* Tab Contents */}
      <div className="flex-1">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsContent value="dashboard" className="p-6">
            {/* Welcome Section */}
            <div className="mb-6">
              <h2 className="text-3xl font-bold text-foreground">Welcome back, Dr. Sharma</h2>
              <p className="text-muted-foreground">Here's what's happening with your practice today.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid gap-4 md:grid-cols-4 mb-6">
              {stats.map((stat, index) => (
                <Card key={index} className="medical-card">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-lg ${stat.color}`}>
                        <stat.icon className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <p className="text-2xl font-bold">{stat.value}</p>
                        <p className="text-xs text-muted-foreground">{stat.title}</p>
                      </div>
                    </div>
                    <div className="mt-4 flex items-center text-sm">
                      <TrendingUp className="mr-1 h-4 w-4 text-success" />
                      <span className="text-success">{stat.change}</span>
                      <span className="ml-1 text-muted-foreground">from last month</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid gap-6 md:grid-cols-3">
              {/* Recent Patients */}
              <Card className="md:col-span-2 medical-card">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-base font-medium">Recent Patients</CardTitle>
                  <Button variant="outline" size="sm" onClick={() => setActiveTab("patients")}>
                    <Plus className="h-4 w-4 mr-2" />
                    Add Patient
                  </Button>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-[400px]">
                    <div className="space-y-4">
                      {recentPatients.map((patient, index) => (
                        <div key={index} className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-accent/50 transition-colors">
                          <div className="flex items-center gap-3">
                            <Avatar>
                              <AvatarFallback>{patient.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                            </Avatar>
                            <div>
                              <p className="font-medium">{patient.name}</p>
                              <p className="text-sm text-muted-foreground">Age: {patient.age} • {patient.gender}</p>
                              <p className="text-xs text-muted-foreground">Prakriti: {patient.prakriti}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {getStatusBadge(patient.status)}
                            <div className={`w-3 h-3 rounded-full ${getConstitutionColor(patient.constitution)}`} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Quick Actions */}
                <Card className="medical-card">
                  <CardHeader>
                    <CardTitle className="text-base">Quick Actions</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <Button className="w-full justify-start" variant="outline" onClick={() => setActiveTab("patients")}>
                      <Plus className="mr-2 h-4 w-4" />
                      New Patient Registration
                    </Button>
                    <Button className="w-full justify-start" variant="outline" onClick={() => setActiveTab("diet-generator")}>
                      <Utensils className="mr-2 h-4 w-4" />
                      Generate Diet Chart
                    </Button>
                    <Button className="w-full justify-start" variant="outline">
                      <Calendar className="mr-2 h-4 w-4" />
                      Schedule Appointment
                    </Button>
                    <Button className="w-full justify-start" variant="outline" onClick={() => setActiveTab("analytics")}>
                      <Activity className="mr-2 h-4 w-4" />
                      View Analytics
                    </Button>
                  </CardContent>
                </Card>

                {/* Recent Activity */}
                <Card className="medical-card">
                  <CardHeader>
                    <CardTitle className="text-base">Recent Activity</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ScrollArea className="h-[250px]">
                      <div className="space-y-4">
                        {recentActivity.map((activity, index) => (
                          <div key={index} className="flex items-start gap-3">
                            <div className={`p-2 rounded-full ${activity.color}`}>
                              <activity.icon className="h-3 w-3 text-white" />
                            </div>
                            <div className="flex-1 space-y-1">
                              <p className="text-sm font-medium">{activity.action}</p>
                              <p className="text-xs text-muted-foreground">{activity.patient}</p>
                              <p className="text-xs text-muted-foreground">{activity.time}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="patients" className="p-6">
            <PatientProfile mode="create" />
          </TabsContent>

          <TabsContent value="diet-generator" className="p-6">
            <DietChartGenerator />
          </TabsContent>

          <TabsContent value="food-database" className="p-6">
            <FoodDatabase />
          </TabsContent>

          <TabsContent value="analytics" className="p-6">
            <div className="space-y-6">
              <Card className="medical-card">
                <CardHeader>
                  <CardTitle>Analytics Dashboard</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12">
                    <TrendingUp className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">Analytics Coming Soon</h3>
                    <p className="text-muted-foreground">
                      Patient compliance tracking, diet effectiveness metrics, and practice insights will be available once connected to Supabase.
                    </p>
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

export default Dashboard;
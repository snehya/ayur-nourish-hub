import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { 
  Users, 
  FileText, 
  Calendar, 
  TrendingUp, 
  Search,
  Plus,
  Bell,
  Settings,
  Leaf,
  Heart,
  Clock,
  Activity,
  AlertCircle,
  CheckCircle,
  UserPlus,
  ChefHat,
  Database,
  BarChart3,
  Filter
} from "lucide-react";

const Dashboard = () => {
  const [searchQuery, setSearchQuery] = useState("");

  // Mock data - replace with real data from your backend
  const stats = [
    {
      title: "Total Patients",
      value: "284",
      change: "+12%",
      changeType: "positive" as const,
      icon: Users,
      color: "text-primary"
    },
    {
      title: "Active Diet Plans",
      value: "156",
      change: "+8%",
      changeType: "positive" as const,
      icon: FileText,
      color: "text-earth"
    },
    {
      title: "Consultations Today",
      value: "12",
      change: "+3",
      changeType: "positive" as const,
      icon: Calendar,
      color: "text-fire"
    },
    {
      title: "Success Rate",
      value: "94%",
      change: "+2%",
      changeType: "positive" as const,
      icon: TrendingUp,
      color: "text-success"
    }
  ];

  const recentPatients = [
    {
      id: 1,
      name: "Priya Sharma",
      age: 32,
      constitution: "Kapha",
      lastVisit: "2 hours ago",
      status: "active",
      condition: "Weight Management"
    },
    {
      id: 2,
      name: "Raj Patel",
      age: 45,
      constitution: "Pitta",
      lastVisit: "1 day ago",
      status: "followup",
      condition: "Digestive Issues"
    },
    {
      id: 3,
      name: "Anita Mehta",
      age: 28,
      constitution: "Vata",
      lastVisit: "3 days ago",
      status: "active",
      condition: "Anxiety & Sleep"
    },
    {
      id: 4,
      name: "Vikram Singh",
      age: 55,
      constitution: "Kapha-Pitta",
      lastVisit: "1 week ago",
      status: "inactive",
      condition: "Diabetes Management"
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: "diet_plan",
      message: "Created new diet plan for Priya Sharma",
      time: "2 hours ago",
      icon: ChefHat,
      color: "text-primary"
    },
    {
      id: 2,
      type: "consultation",
      message: "Completed consultation with Raj Patel",
      time: "5 hours ago",
      icon: Heart,
      color: "text-success"
    },
    {
      id: 3,
      type: "followup",
      message: "Follow-up scheduled for Anita Mehta",
      time: "1 day ago",
      icon: Calendar,
      color: "text-warning"
    },
    {
      id: 4,
      type: "analysis",
      message: "Nutritional analysis completed for 3 patients",
      time: "2 days ago",
      icon: BarChart3,
      color: "text-earth"
    }
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-success/10 text-success border-success/20">Active</Badge>;
      case "followup":
        return <Badge className="bg-warning/10 text-warning border-warning/20">Follow-up</Badge>;
      case "inactive":
        return <Badge className="bg-muted text-muted-foreground">Inactive</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  const getConstitutionColor = (constitution: string) => {
    if (constitution.includes("Vata")) return "text-air";
    if (constitution.includes("Pitta")) return "text-fire";
    if (constitution.includes("Kapha")) return "text-earth";
    return "text-muted-foreground";
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <Leaf className="h-8 w-8 text-primary" />
                <span className="text-xl font-bold text-foreground">AyurDiet Pro</span>
              </div>
              
              <div className="relative max-w-md">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search patients, conditions, or plans..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-80"
                />
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <Button variant="wellness" size="sm">
                <Plus className="h-4 w-4 mr-2" />
                New Patient
              </Button>
              
              <Button variant="ghost" size="sm" className="relative">
                <Bell className="h-4 w-4" />
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-fire rounded-full"></div>
              </Button>
              
              <Button variant="ghost" size="sm">
                <Settings className="h-4 w-4" />
              </Button>
              
              <Avatar>
                <AvatarFallback className="bg-primary text-primary-foreground">
                  Dr
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">Good morning, Dr. Sharma!</h1>
          <p className="text-muted-foreground">Here's an overview of your practice today.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="medical-card">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">{stat.title}</p>
                    <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                    <div className="flex items-center space-x-1">
                      <TrendingUp className={`h-3 w-3 ${stat.color}`} />
                      <span className={`text-xs font-medium ${stat.color}`}>
                        {stat.change} from last month
                      </span>
                    </div>
                  </div>
                  <div className={`p-3 rounded-lg bg-background ${stat.color}`}>
                    <stat.icon className="h-6 w-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Patients */}
          <div className="lg:col-span-2">
            <Card className="medical-card">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div>
                  <CardTitle className="text-xl">Recent Patients</CardTitle>
                  <CardDescription>Latest patient consultations and updates</CardDescription>
                </div>
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm">
                    <Filter className="h-4 w-4" />
                  </Button>
                  <Button variant="healing" size="sm">
                    <UserPlus className="h-4 w-4 mr-2" />
                    Add Patient
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentPatients.map((patient) => (
                  <div key={patient.id} className="flex items-center justify-between p-4 rounded-lg border border-border/50 hover:bg-muted/30 transition-gentle cursor-pointer">
                    <div className="flex items-center space-x-4">
                      <Avatar>
                        <AvatarFallback className="bg-muted text-muted-foreground">
                          {patient.name.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      
                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <h3 className="font-medium text-foreground">{patient.name}</h3>
                          <span className="text-sm text-muted-foreground">({patient.age}y)</span>
                        </div>
                        <div className="flex items-center space-x-3">
                          <span className={`text-xs font-medium ${getConstitutionColor(patient.constitution)}`}>
                            {patient.constitution}
                          </span>
                          <span className="text-xs text-muted-foreground">{patient.condition}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      {getStatusBadge(patient.status)}
                      <div className="text-right">
                        <div className="text-xs text-muted-foreground">{patient.lastVisit}</div>
                      </div>
                    </div>
                  </div>
                ))}
                
                <Button variant="soft" className="w-full mt-4">
                  View All Patients
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity & Quick Actions */}
          <div className="space-y-8">
            {/* Quick Actions */}
            <Card className="medical-card">
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="healing" className="w-full justify-start">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Diet Plan
                </Button>
                <Button variant="earth" className="w-full justify-start">
                  <Database className="h-4 w-4 mr-2" />
                  Browse Food Database
                </Button>
                <Button variant="wellness" className="w-full justify-start">
                  <Calendar className="h-4 w-4 mr-2" />
                  Schedule Consultation
                </Button>
                <Button variant="soft" className="w-full justify-start">
                  <BarChart3 className="h-4 w-4 mr-2" />
                  View Reports
                </Button>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card className="medical-card">
              <CardHeader>
                <CardTitle className="text-lg">Recent Activity</CardTitle>
                <CardDescription>Your latest actions and updates</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className={`p-2 rounded-lg bg-background ${activity.color}`}>
                      <activity.icon className="h-4 w-4" />
                    </div>
                    <div className="space-y-1 flex-1">
                      <p className="text-sm text-foreground">{activity.message}</p>
                      <p className="text-xs text-muted-foreground">{activity.time}</p>
                    </div>
                  </div>
                ))}
                
                <Button variant="ghost" className="w-full mt-4 text-xs">
                  View All Activity
                </Button>
              </CardContent>
            </Card>

            {/* System Status */}
            <Card className="medical-card">
              <CardHeader>
                <CardTitle className="text-lg">System Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-success" />
                    <span className="text-sm">Database Sync</span>
                  </div>
                  <Badge className="bg-success/10 text-success border-success/20">Online</Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-success" />
                    <span className="text-sm">HIPAA Compliance</span>
                  </div>
                  <Badge className="bg-success/10 text-success border-success/20">Active</Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Activity className="h-4 w-4 text-primary" />
                    <span className="text-sm">API Status</span>
                  </div>
                  <Badge className="bg-primary/10 text-primary border-primary/20">Healthy</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
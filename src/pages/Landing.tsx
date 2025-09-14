import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { 
  Users, 
  Heart, 
  Database, 
  FileText, 
  Stethoscope, 
  Leaf, 
  Brain,
  Shield,
  Clock,
  Target,
  Award,
  ArrowRight
} from "lucide-react";
import heroImage from "@/assets/hero-ayurveda.jpg";

const Landing = () => {
  const features = [
    {
      icon: Users,
      title: "Comprehensive Patient Management",
      description: "Manage patient profiles with Ayurvedic parameters, health history, and constitutional analysis.",
      color: "text-primary"
    },
    {
      icon: Database,
      title: "8,000+ Food Database",
      description: "Extensive database covering Indian, multicultural, and international cuisines with Ayurvedic properties.",
      color: "text-earth"
    },
    {
      icon: FileText,
      title: "Automated Diet Charts",
      description: "Generate scientifically balanced diet plans aligned with Ayurvedic principles and patient needs.",
      color: "text-fire"
    },
    {
      icon: Heart,
      title: "Ayurvedic Integration",
      description: "Incorporate traditional concepts like Rasa (6 tastes), food properties, and constitutional balance.",
      color: "text-water"
    },
    {
      icon: Brain,
      title: "Recipe-Based Planning",
      description: "Create detailed meal plans with automated nutrient analysis and cooking instructions.",
      color: "text-space"
    },
    {
      icon: Shield,
      title: "HIPAA Compliant",
      description: "Secure, encrypted patient data management meeting healthcare privacy standards.",
      color: "text-success"
    }
  ];

  const benefits = [
    {
      icon: Clock,
      title: "Save 70% Time",
      description: "Reduce diet chart creation time from hours to minutes"
    },
    {
      icon: Target,
      title: "Precise Nutrition",
      description: "Accurate macro and micronutrient calculations for all age groups"
    },
    {
      icon: Award,
      title: "Evidence-Based",
      description: "Scientifically backed recommendations rooted in Ayurvedic wisdom"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Leaf className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold text-foreground">AyurDiet Pro</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-muted-foreground hover:text-primary transition-gentle cursor-pointer">Features</a>
              <a href="#benefits" className="text-muted-foreground hover:text-primary transition-gentle cursor-pointer">Benefits</a>
              <a href="#pricing" className="text-muted-foreground hover:text-primary transition-gentle cursor-pointer">Pricing</a>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/signup">
                <Button variant="healing" size="lg">Get Started</Button>
              </Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-24 overflow-hidden">
        <div className="absolute inset-0 wellness-gradient opacity-50"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <div className="inline-flex items-center space-x-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium">
                  <Stethoscope className="h-4 w-4" />
                  <span>Ministry of AYUSH Approved</span>
                </div>
                <h1 className="text-4xl lg:text-6xl font-bold text-foreground leading-tight">
                  Revolutionize Your 
                  <span className="text-primary block">Ayurvedic Practice</span>
                </h1>
                <p className="text-lg text-muted-foreground max-w-lg">
                  Transform manual diet chart creation into intelligent, evidence-based nutrition planning. 
                  Combine ancient Ayurvedic wisdom with modern nutritional science.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/signup">
                  <Button variant="healing" size="xl" className="group">
                    Start Free Trial
                    <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
                <Button variant="wellness" size="xl">
                  Watch Demo
                </Button>
              </div>

              <div className="flex items-center space-x-8 pt-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">8,000+</div>
                  <div className="text-sm text-muted-foreground">Food Items</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">500+</div>
                  <div className="text-sm text-muted-foreground">Practitioners</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">95%</div>
                  <div className="text-sm text-muted-foreground">Time Saved</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="relative rounded-2xl overflow-hidden shadow-floating">
                <img 
                  src={heroImage} 
                  alt="Ayurvedic healthcare consultation" 
                  className="w-full h-[600px] object-cover"
                />
                <div className="absolute inset-0 healing-gradient opacity-20"></div>
              </div>
              {/* Floating elements */}
              <div className="absolute -top-4 -right-4 bg-white p-4 rounded-xl shadow-elevated">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-success rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium">Live Analysis</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
              Comprehensive Practice Management
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Everything you need to deliver exceptional Ayurvedic dietary care, 
              backed by modern technology and traditional wisdom.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="medical-card group">
                <div className="space-y-4">
                  <div className={`inline-flex p-3 rounded-lg bg-background ${feature.color}`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
              How It Works
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Transform your Ayurvedic practice with three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 text-primary mb-6 group-hover:scale-110 transition-transform">
                <Users className="h-8 w-8" />
              </div>
              <div className="space-y-3">
                <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold mx-auto mb-4">1</div>
                <h3 className="text-xl font-semibold text-foreground">Onboard a Patient</h3>
                <p className="text-muted-foreground">
                  Create a patient profile by entering their details and Ayurvedic parameters including constitution, health history, and dietary preferences.
                </p>
              </div>
            </div>

            <div className="text-center group">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 text-primary mb-6 group-hover:scale-110 transition-transform">
                <Brain className="h-8 w-8" />
              </div>
              <div className="space-y-3">
                <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold mx-auto mb-4">2</div>
                <h3 className="text-xl font-semibold text-foreground">Generate Diet Plan</h3>
                <p className="text-muted-foreground">
                  Use our intelligent engine to auto-generate a personalized, Ayurveda-compliant diet chart with precise nutritional analysis.
                </p>
              </div>
            </div>

            <div className="text-center group">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 text-primary mb-6 group-hover:scale-110 transition-transform">
                <FileText className="h-8 w-8" />
              </div>
              <div className="space-y-3">
                <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold mx-auto mb-4">3</div>
                <h3 className="text-xl font-semibold text-foreground">Share with Patient</h3>
                <p className="text-muted-foreground">
                  Instantly share the diet chart with your patient and track their progress through our integrated patient portal.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-24">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
                  Why Choose AyurDiet Pro?
                </h2>
                <p className="text-lg text-muted-foreground">
                  Join hundreds of Ayurvedic practitioners who have transformed their practice 
                  with our intelligent diet management platform.
                </p>
              </div>

              <div className="space-y-6">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="flex-shrink-0 p-2 rounded-lg bg-primary/10">
                      <benefit.icon className="h-5 w-5 text-primary" />
                    </div>
                    <div className="space-y-1">
                      <h3 className="font-semibold text-foreground">{benefit.title}</h3>
                      <p className="text-muted-foreground">{benefit.description}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="pt-4">
                <Link to="/signup">
                  <Button variant="earth" size="lg">
                    Start Your Journey
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
              </div>
            </div>

            <div className="relative">
              <div className="medical-card">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Patient: Priya Sharma</h3>
                    <div className="px-3 py-1 bg-success/10 text-success rounded-full text-sm">
                      Kapha Constitution
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <div className="text-sm text-muted-foreground">Morning</div>
                      <div className="text-sm font-medium">Warm Spiced Oats</div>
                      <div className="text-xs text-muted-foreground">320 kcal • Light to digest</div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-sm text-muted-foreground">Afternoon</div>
                      <div className="text-sm font-medium">Quinoa Vegetable Bowl</div>
                      <div className="text-xs text-muted-foreground">450 kcal • Balancing</div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="text-sm font-medium">Ayurvedic Properties:</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2 py-1 bg-fire/10 text-fire rounded text-xs">Warming</span>
                      <span className="px-2 py-1 bg-earth/10 text-earth rounded text-xs">Grounding</span>
                      <span className="px-2 py-1 bg-primary/10 text-primary rounded text-xs">Easy Digest</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
              Trusted by Leading Practitioners
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              See how AyurDiet Pro is transforming Ayurvedic practices across the country
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="medical-card text-center">
              <div className="space-y-4">
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <Stethoscope className="h-8 w-8 text-primary" />
                </div>
                <blockquote className="text-muted-foreground italic">
                  "AyurDiet Pro has revolutionized my practice. I now create comprehensive diet charts in minutes instead of hours, and my patients love the detailed explanations."
                </blockquote>
                <div className="space-y-1">
                  <div className="font-semibold text-foreground">Dr. Anjali Sharma</div>
                  <div className="text-sm text-muted-foreground">Senior Ayurvedic Physician, AIIMS Delhi</div>
                </div>
              </div>
            </Card>

            <Card className="medical-card text-center">
              <div className="space-y-4">
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <Heart className="h-8 w-8 text-primary" />
                </div>
                <blockquote className="text-muted-foreground italic">
                  "The integration of traditional Ayurvedic principles with modern nutrition science is remarkable. My patient outcomes have improved significantly."
                </blockquote>
                <div className="space-y-1">
                  <div className="font-semibold text-foreground">Dr. Ramesh Patel</div>
                  <div className="text-sm text-muted-foreground">Chief Dietitian, Patanjali Ayurveda Hospital</div>
                </div>
              </div>
            </Card>

            <Card className="medical-card text-center">
              <div className="space-y-4">
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <Leaf className="h-8 w-8 text-primary" />
                </div>
                <blockquote className="text-muted-foreground italic">
                  "The extensive food database covering multicultural cuisines has made it easy to cater to patients from diverse backgrounds while maintaining Ayurvedic principles."
                </blockquote>
                <div className="space-y-1">
                  <div className="font-semibold text-foreground">Dr. Priya Nair</div>
                  <div className="text-sm text-muted-foreground">Consultant Ayurvedic Nutritionist, Kerala Ayurveda</div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Patient Features Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <div className="inline-flex items-center space-x-2 bg-success/10 text-success px-3 py-1 rounded-full text-sm font-medium">
                  <Heart className="h-4 w-4" />
                  <span>For Patients</span>
                </div>
                <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
                  Empower Your Patients
                </h2>
                <p className="text-lg text-muted-foreground">
                  Give your patients the tools they need to succeed with their Ayurvedic journey through our patient-friendly mobile interface.
                </p>
              </div>

              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 p-2 rounded-lg bg-success/10">
                    <FileText className="h-5 w-5 text-success" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="font-semibold text-foreground">Easy-to-Read Diet Charts</h3>
                    <p className="text-muted-foreground">Beautiful, printable diet charts with recipes and shopping lists</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 p-2 rounded-lg bg-success/10">
                    <Target className="h-5 w-5 text-success" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="font-semibold text-foreground">Progress Tracking</h3>
                    <p className="text-muted-foreground">Track symptoms, energy levels, and dietary adherence</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 p-2 rounded-lg bg-success/10">
                    <Clock className="h-5 w-5 text-success" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="font-semibold text-foreground">Meal Reminders</h3>
                    <p className="text-muted-foreground">Smart notifications for optimal meal timing and hydration</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="medical-card bg-gradient-to-br from-success/5 to-primary/5">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Today's Plan</h3>
                    <div className="px-3 py-1 bg-success text-success-foreground rounded-full text-sm">
                      Day 7
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-success rounded-full"></div>
                      <div className="flex-1">
                        <div className="text-sm font-medium">Morning (6:30 AM)</div>
                        <div className="text-xs text-muted-foreground">Warm water with lemon and honey</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-primary rounded-full"></div>
                      <div className="flex-1">
                        <div className="text-sm font-medium">Breakfast (8:00 AM)</div>
                        <div className="text-xs text-muted-foreground">Spiced oats with almonds</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-muted-foreground rounded-full"></div>
                      <div className="flex-1">
                        <div className="text-sm font-medium">Lunch (12:30 PM)</div>
                        <div className="text-xs text-muted-foreground">Quinoa vegetable bowl</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-border/50">
                    <div className="text-sm text-muted-foreground">Progress</div>
                    <div className="text-sm font-medium text-success">85% Complete</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 healing-gradient">
        <div className="container mx-auto px-4 text-center">
          <div className="space-y-6 max-w-3xl mx-auto">
            <h2 className="text-3xl lg:text-4xl font-bold text-white">
              Ready to Transform Your Practice?
            </h2>
            <p className="text-lg text-white/90">
              Join the future of Ayurvedic healthcare. Start creating intelligent, 
              personalized diet charts that honor traditional wisdom.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link to="/signup">
                <Button variant="outline" size="xl" className="bg-white text-primary hover:bg-white/90">
                  Start Free Trial
                </Button>
              </Link>
              <Button variant="ghost" size="xl" className="text-white border-white/20 hover:bg-white/10">
                Contact Sales
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-muted/50 border-t border-border/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Leaf className="h-6 w-6 text-primary" />
                <span className="text-lg font-bold">AyurDiet Pro</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Bridging ancient Ayurvedic wisdom with modern nutritional science 
                for comprehensive healthcare.
              </p>
            </div>
            
            <div className="space-y-3">
              <h4 className="font-semibold">Product</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div>Features</div>
                <div>Pricing</div>
                <div>Demo</div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold">Support</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div>Documentation</div>
                <div>Help Center</div>
                <div>Contact</div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold">Legal</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div>Privacy Policy</div>
                <div>Terms of Service</div>
                <div>HIPAA Compliance</div>
              </div>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-border/50 text-center text-sm text-muted-foreground">
            <p>&copy; 2024 AyurDiet Pro. All rights reserved. Approved by Ministry of AYUSH.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
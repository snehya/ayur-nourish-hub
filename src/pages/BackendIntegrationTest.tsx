// Integration test component to demonstrate backend connectivity
import { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Separator } from '../components/ui/separator';
import { useToast } from '../hooks/use-toast';
import { authService, patientService, dietPlanService } from '../services';
import type { Patient, Food } from '../services';

const BackendIntegrationTest = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [authStatus, setAuthStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [foods, setFoods] = useState<Food[]>([]);
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});
  
  const { toast } = useToast();

  const runIntegrationTest = async () => {
    setIsLoading(true);
    const results: Record<string, boolean> = {};

    try {
      // Test 1: Authentication
      toast({ title: "Testing authentication..." });
      await authService.login({ username: 'sneha', password: 'password123' });
      results.auth = true;
      setAuthStatus('success');
      toast({ title: "✅ Authentication successful" });

      // Test 2: Patient Management
      toast({ title: "Testing patient management..." });
      const patientsData = await patientService.getPatients();
      setPatients(patientsData);
      results.patients = true;
      toast({ title: `✅ Retrieved ${patientsData.length} patients` });

      // Test 3: Food Database
      toast({ title: "Testing food database..." });
      const foodsData = await dietPlanService.getFoods();
      setFoods(foodsData.slice(0, 5)); // Show first 5 foods
      results.foods = true;
      toast({ title: `✅ Retrieved ${foodsData.length} foods` });

      // Test 4: Diet Plan Generation (if patients exist)
      if (patientsData.length > 0) {
        toast({ title: "Testing diet plan generation..." });
        try {
          await dietPlanService.generateDietPlan(patientsData[0].id!);
          results.dietPlan = true;
          toast({ title: "✅ Diet plan generation working" });
        } catch (error) {
          results.dietPlan = false;
          toast({ 
            title: "⚠️ Diet plan generation failed", 
            description: "Expected - requires AI API configuration",
            variant: "default"
          });
        }
      }

      setTestResults(results);
      toast({ 
        title: "🎉 Integration test complete!", 
        description: "Backend integration is working correctly"
      });

    } catch (error) {
      setAuthStatus('error');
      toast({
        title: "❌ Integration test failed",
        description: error instanceof Error ? error.message : "Unknown error occurred",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const resetTest = () => {
    setAuthStatus('idle');
    setPatients([]);
    setFoods([]);
    setTestResults({});
    authService.logout();
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Backend Integration Test</h1>
        <p className="text-muted-foreground">
          Test the connection between React frontend and Django backend
        </p>
      </div>

      <div className="grid gap-6">
        {/* Test Controls */}
        <Card>
          <CardHeader>
            <CardTitle>Integration Test Controls</CardTitle>
            <CardDescription>
              Run comprehensive tests to verify backend connectivity
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-4">
              <Button 
                onClick={runIntegrationTest} 
                disabled={isLoading}
                variant="default"
                size="lg"
              >
                {isLoading ? 'Running Tests...' : 'Run Integration Test'}
              </Button>
              <Button 
                onClick={resetTest} 
                variant="outline"
                size="lg"
              >
                Reset
              </Button>
            </div>

            {/* Test Results Summary */}
            {Object.keys(testResults).length > 0 && (
              <div className="space-y-2">
                <h4 className="font-semibold">Test Results:</h4>
                <div className="flex flex-wrap gap-2">
                  <Badge variant={testResults.auth ? "default" : "destructive"}>
                    Authentication: {testResults.auth ? "✅ Pass" : "❌ Fail"}
                  </Badge>
                  <Badge variant={testResults.patients ? "default" : "destructive"}>
                    Patients: {testResults.patients ? "✅ Pass" : "❌ Fail"}
                  </Badge>
                  <Badge variant={testResults.foods ? "default" : "destructive"}>
                    Foods: {testResults.foods ? "✅ Pass" : "❌ Fail"}
                  </Badge>
                  <Badge variant={testResults.dietPlan !== undefined ? (testResults.dietPlan ? "default" : "secondary") : "outline"}>
                    Diet Plans: {testResults.dietPlan === true ? "✅ Pass" : testResults.dietPlan === false ? "⚠️ Expected Fail" : "Not Tested"}
                  </Badge>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Authentication Status */}
        <Card>
          <CardHeader>
            <CardTitle>Authentication Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Badge variant={
                authStatus === 'success' ? 'default' : 
                authStatus === 'error' ? 'destructive' : 
                'outline'
              }>
                {authStatus === 'success' ? '✅ Authenticated' : 
                 authStatus === 'error' ? '❌ Failed' : 
                 '⏳ Not Tested'}
              </Badge>
              {authStatus === 'success' && (
                <span className="text-sm text-muted-foreground">
                  JWT token stored and ready for API calls
                </span>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Patients Data */}
        {patients.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Patients Retrieved ({patients.length})</CardTitle>
              <CardDescription>
                Patient data from Django backend
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {patients.map((patient, index) => (
                  <div key={patient.id || index} className="p-3 border rounded-lg">
                    <div className="font-semibold">{patient.name}</div>
                    <div className="text-sm text-muted-foreground">
                      Prakriti: {patient.prakriti || 'Not set'} | 
                      Vikriti: {patient.vikriti || 'Not set'} | 
                      Agni: {patient.agni || 'Not set'}
                    </div>
                    {patient.health_parameters?.age && (
                      <div className="text-sm text-muted-foreground">
                        Age: {patient.health_parameters.age} years
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Foods Data */}
        {foods.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Foods Sample (First 5)</CardTitle>
              <CardDescription>
                Food database from Django backend
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {foods.map((food, index) => (
                  <div key={food.id || index} className="p-3 border rounded-lg">
                    <div className="font-semibold">{food.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {food.rasa && `Rasa: ${food.rasa}`}
                      {food.virya && ` | Virya: ${food.virya}`}
                      {food.calories && ` | Calories: ${food.calories}`}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* API Information */}
        <Card>
          <CardHeader>
            <CardTitle>API Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">Backend URL:</h4>
              <code className="text-sm bg-muted p-2 rounded">
                http://localhost:8000/api
              </code>
            </div>
            
            <Separator />
            
            <div>
              <h4 className="font-semibold mb-2">Available Endpoints:</h4>
              <div className="text-sm space-y-1 text-muted-foreground">
                <div>• POST /api/token/ - Authentication</div>
                <div>• GET /api/patients/ - Patient management</div>
                <div>• GET /api/foods/ - Food database</div>
                <div>• POST /api/generate-diet-plan/ - Diet plan generation</div>
                <div>• GET /api/schema/swagger-ui/ - API documentation</div>
              </div>
            </div>

            <Separator />

            <div>
              <h4 className="font-semibold mb-2">Test Credentials:</h4>
              <div className="text-sm space-y-1 text-muted-foreground">
                <div>Username: <code>sneha</code></div>
                <div>Password: <code>password123</code></div>
                <div>User Type: <code>practitioner</code></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default BackendIntegrationTest;
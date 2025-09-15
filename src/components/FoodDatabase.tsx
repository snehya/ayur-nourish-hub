import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Search, Database, Plus, Filter, Thermometer, Zap, Utensils } from 'lucide-react';

interface FoodItem {
  id: number;
  name: string;
  category: string;
  thermalProperty: 'Hot' | 'Cold' | 'Neutral';
  digestibility: 'Easy' | 'Moderate' | 'Difficult';
  rasa: string[];
  nutrients: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    fiber: number;
    vitamins: string[];
    minerals: string[];
  };
  contraindications: string[];
  benefits: string[];
  season: string[];
  preparationTips: string;
}

const mockFoodDatabase: FoodItem[] = [
  {
    id: 1,
    name: 'Basmati Rice',
    category: 'Grains',
    thermalProperty: 'Neutral',
    digestibility: 'Easy',
    rasa: ['Sweet'],
    nutrients: {
      calories: 130,
      protein: 3,
      carbs: 28,
      fat: 0.3,
      fiber: 0.4,
      vitamins: ['B1', 'B3', 'B6'],
      minerals: ['Manganese', 'Selenium']
    },
    contraindications: ['Diabetes (large portions)', 'Weight gain concerns'],
    benefits: ['Energy boost', 'Easy digestion', 'Satisfying'],
    season: ['All seasons'],
    preparationTips: 'Soak for 30 mins before cooking. Add ghee and cumin for better digestion.'
  },
  {
    id: 2,
    name: 'Fresh Ginger',
    category: 'Spices',
    thermalProperty: 'Hot',
    digestibility: 'Easy',
    rasa: ['Pungent', 'Sweet'],
    nutrients: {
      calories: 80,
      protein: 2,
      carbs: 18,
      fat: 0.8,
      fiber: 2,
      vitamins: ['C', 'B6'],
      minerals: ['Potassium', 'Magnesium']
    },
    contraindications: ['Pitta excess', 'Acid reflux', 'Bleeding disorders'],
    benefits: ['Digestive fire enhancement', 'Nausea relief', 'Circulation improvement'],
    season: ['Winter', 'Monsoon'],
    preparationTips: 'Use fresh, peel before use. Start with small amounts for sensitive digestion.'
  },
  {
    id: 3,
    name: 'Cucumber',
    category: 'Vegetables',
    thermalProperty: 'Cold',
    digestibility: 'Easy',
    rasa: ['Sweet', 'Astringent'],
    nutrients: {
      calories: 16,
      protein: 1,
      carbs: 4,
      fat: 0.1,
      fiber: 0.5,
      vitamins: ['K', 'C', 'A'],
      minerals: ['Potassium', 'Magnesium']
    },
    contraindications: ['Vata excess', 'Poor digestion', 'Cold conditions'],
    benefits: ['Hydration', 'Cooling effect', 'Skin health'],
    season: ['Summer'],
    preparationTips: 'Remove seeds for better digestion. Pair with warming spices in winter.'
  },
  {
    id: 4,
    name: 'Almonds',
    category: 'Nuts',
    thermalProperty: 'Hot',
    digestibility: 'Moderate',
    rasa: ['Sweet', 'Astringent'],
    nutrients: {
      calories: 576,
      protein: 21,
      carbs: 22,
      fat: 49,
      fiber: 12,
      vitamins: ['E', 'B2', 'B3'],
      minerals: ['Magnesium', 'Calcium', 'Iron']
    },
    contraindications: ['Weak digestion', 'Kapha excess', 'Nut allergies'],
    benefits: ['Brain health', 'Heart health', 'Bone strength'],
    season: ['Winter', 'Spring'],
    preparationTips: 'Soak overnight and remove skin. Limit to 5-10 pieces per day.'
  },
  {
    id: 5,
    name: 'Turmeric',
    category: 'Spices',
    thermalProperty: 'Hot',
    digestibility: 'Easy',
    rasa: ['Bitter', 'Pungent', 'Astringent'],
    nutrients: {
      calories: 312,
      protein: 10,
      carbs: 67,
      fat: 3,
      fiber: 22,
      vitamins: ['C', 'B6', 'E'],
      minerals: ['Iron', 'Potassium', 'Manganese']
    },
    contraindications: ['Gallstones', 'Blood thinning medications', 'Surgery (2 weeks prior)'],
    benefits: ['Anti-inflammatory', 'Immune support', 'Joint health'],
    season: ['All seasons'],
    preparationTips: 'Use with black pepper and ghee for better absorption. Fresh is preferred over powder.'
  }
];

export const FoodDatabase: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [thermalFilter, setThermalFilter] = useState<string>('all');
  const [digestibilityFilter, setDigestibilityFilter] = useState<string>('all');
  const [selectedFood, setSelectedFood] = useState<FoodItem | null>(null);

  const categories = useMemo(() => {
    const cats = Array.from(new Set(mockFoodDatabase.map(food => food.category)));
    return ['all', ...cats];
  }, []);

  const filteredFoods = useMemo(() => {
    return mockFoodDatabase.filter(food => {
      const matchesSearch = food.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           food.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           food.rasa.some(r => r.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesCategory = categoryFilter === 'all' || food.category === categoryFilter;
      const matchesThermal = thermalFilter === 'all' || food.thermalProperty === thermalFilter;
      const matchesDigestibility = digestibilityFilter === 'all' || food.digestibility === digestibilityFilter;

      return matchesSearch && matchesCategory && matchesThermal && matchesDigestibility;
    });
  }, [searchTerm, categoryFilter, thermalFilter, digestibilityFilter]);

  const getThermalIcon = (property: string) => {
    switch (property) {
      case 'Hot': return <Thermometer className="w-4 h-4 text-fire" />;
      case 'Cold': return <Thermometer className="w-4 h-4 text-water" />;
      default: return <Thermometer className="w-4 h-4 text-muted-foreground" />;
    }
  };

  const getDigestibilityIcon = (digestibility: string) => {
    switch (digestibility) {
      case 'Easy': return <Zap className="w-4 h-4 text-success" />;
      case 'Moderate': return <Zap className="w-4 h-4 text-warning" />;
      case 'Difficult': return <Zap className="w-4 h-4 text-destructive" />;
      default: return <Zap className="w-4 h-4 text-muted-foreground" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="medical-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5 text-primary" />
            Curated Food Database
            <Badge variant="secondary" className="ml-2">
              {mockFoodDatabase.length} Items
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="md:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search foods, categories, or tastes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map(category => (
                  <SelectItem key={category} value={category}>
                    {category === 'all' ? 'All Categories' : category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Select value={thermalFilter} onValueChange={setThermalFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Thermal Property" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Properties</SelectItem>
                <SelectItem value="Hot">Hot</SelectItem>
                <SelectItem value="Cold">Cold</SelectItem>
                <SelectItem value="Neutral">Neutral</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={digestibilityFilter} onValueChange={setDigestibilityFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Digestibility" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="Easy">Easy</SelectItem>
                <SelectItem value="Moderate">Moderate</SelectItem>
                <SelectItem value="Difficult">Difficult</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Food Table */}
      <Card className="medical-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Food Item</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Thermal</TableHead>
                <TableHead>Digestibility</TableHead>
                <TableHead>Rasa (Tastes)</TableHead>
                <TableHead>Nutrients</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredFoods.map((food) => (
                <TableRow key={food.id} className="cursor-pointer hover:bg-muted/50">
                  <TableCell>
                    <div>
                      <p className="font-medium">{food.name}</p>
                      <p className="text-xs text-muted-foreground">{food.season.join(', ')}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{food.category}</Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      {getThermalIcon(food.thermalProperty)}
                      <span className="text-sm">{food.thermalProperty}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      {getDigestibilityIcon(food.digestibility)}
                      <span className="text-sm">{food.digestibility}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {food.rasa.map((taste, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {taste}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="text-xs">
                      <p>{food.nutrients.calories} cal</p>
                      <p>{food.nutrients.protein}g protein</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => setSelectedFood(food)}
                    >
                      <Utensils className="w-3 h-3 mr-1" />
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Detailed Food View */}
      {selectedFood && (
        <Card className="medical-card">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Utensils className="w-5 h-5 text-primary" />
                {selectedFood.name} - Detailed Information
              </CardTitle>
              <Button variant="outline" onClick={() => setSelectedFood(null)}>
                Close
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Ayurvedic Properties */}
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Ayurvedic Properties</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 rounded-lg bg-muted/30">
                    <p className="text-sm font-medium">Thermal Property</p>
                    <div className="flex items-center gap-2 mt-1">
                      {getThermalIcon(selectedFood.thermalProperty)}
                      <span>{selectedFood.thermalProperty}</span>
                    </div>
                  </div>
                  <div className="p-3 rounded-lg bg-muted/30">
                    <p className="text-sm font-medium">Digestibility</p>
                    <div className="flex items-center gap-2 mt-1">
                      {getDigestibilityIcon(selectedFood.digestibility)}
                      <span>{selectedFood.digestibility}</span>
                    </div>
                  </div>
                </div>
                
                <div className="p-3 rounded-lg bg-muted/30">
                  <p className="text-sm font-medium mb-2">Rasa (Six Tastes)</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedFood.rasa.map((taste, index) => (
                      <Badge key={index} variant="secondary">
                        {taste}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-muted/30">
                  <p className="text-sm font-medium mb-2">Best Seasons</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedFood.season.map((season, index) => (
                      <Badge key={index} variant="outline">
                        {season}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>

              {/* Nutritional Information */}
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Nutritional Profile (per 100g)</h3>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-2 rounded bg-muted/20">
                    <p className="text-xs text-muted-foreground">Calories</p>
                    <p className="font-semibold">{selectedFood.nutrients.calories}</p>
                  </div>
                  <div className="p-2 rounded bg-muted/20">
                    <p className="text-xs text-muted-foreground">Protein</p>
                    <p className="font-semibold">{selectedFood.nutrients.protein}g</p>
                  </div>
                  <div className="p-2 rounded bg-muted/20">
                    <p className="text-xs text-muted-foreground">Carbs</p>
                    <p className="font-semibold">{selectedFood.nutrients.carbs}g</p>
                  </div>
                  <div className="p-2 rounded bg-muted/20">
                    <p className="text-xs text-muted-foreground">Fat</p>
                    <p className="font-semibold">{selectedFood.nutrients.fat}g</p>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-muted/30">
                  <p className="text-sm font-medium mb-2">Key Vitamins</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedFood.nutrients.vitamins.map((vitamin, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        Vitamin {vitamin}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-muted/30">
                  <p className="text-sm font-medium mb-2">Key Minerals</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedFood.nutrients.minerals.map((mineral, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {mineral}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Benefits & Precautions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <h3 className="font-semibold text-success">Health Benefits</h3>
                <ul className="space-y-2">
                  {selectedFood.benefits.map((benefit, index) => (
                    <li key={index} className="flex items-center gap-2 text-sm">
                      <div className="w-2 h-2 rounded-full bg-success" />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold text-destructive">Contraindications</h3>
                <ul className="space-y-2">
                  {selectedFood.contraindications.map((contraindication, index) => (
                    <li key={index} className="flex items-center gap-2 text-sm">
                      <div className="w-2 h-2 rounded-full bg-destructive" />
                      {contraindication}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Preparation Tips */}
            <div className="p-4 rounded-lg bg-primary/5 border border-primary/20">
              <h3 className="font-semibold mb-2 text-primary">Ayurvedic Preparation Tips</h3>
              <p className="text-sm">{selectedFood.preparationTips}</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
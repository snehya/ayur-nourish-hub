import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Palette } from 'lucide-react';

interface RasaDistributionChartProps {
  rasaData: {
    Sweet: number;
    Sour: number;
    Salty: number;
    Pungent: number;
    Bitter: number;
    Astringent: number;
  };
}

const RASA_COLORS = {
  Sweet: '#10b981',      // Green - cooling, building
  Sour: '#f59e0b',       // Amber - warming, stimulating  
  Salty: '#ef4444',      // Red - heating, heavy
  Pungent: '#dc2626',    // Dark red - very heating
  Bitter: '#6366f1',     // Indigo - cooling, light
  Astringent: '#8b5cf6'  // Purple - cooling, drying
};

const RASA_PROPERTIES = {
  Sweet: { effect: 'Nourishing & Cooling', dosha: 'Balances Vata & Pitta' },
  Sour: { effect: 'Stimulating & Warming', dosha: 'Balances Vata' },
  Salty: { effect: 'Heavy & Warming', dosha: 'Balances Vata' },
  Pungent: { effect: 'Light & Heating', dosha: 'Balances Kapha' },
  Bitter: { effect: 'Light & Cooling', dosha: 'Balances Pitta & Kapha' },
  Astringent: { effect: 'Dry & Cooling', dosha: 'Balances Pitta & Kapha' }
};

export const RasaDistributionChart: React.FC<RasaDistributionChartProps> = ({ rasaData }) => {
  const chartData = Object.entries(rasaData).map(([rasa, percentage]) => ({
    name: rasa,
    value: percentage,
    color: RASA_COLORS[rasa as keyof typeof RASA_COLORS]
  }));

  const barData = Object.entries(rasaData).map(([rasa, percentage]) => ({
    rasa,
    percentage,
    fill: RASA_COLORS[rasa as keyof typeof RASA_COLORS]
  }));

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    if (percent < 0.05) return null; // Hide labels for very small slices
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        className="text-xs font-medium"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <Card className="medical-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Palette className="w-5 h-5 text-primary" />
          Rasa (Six Tastes) Distribution Analysis
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pie Chart */}
          <div className="space-y-4">
            <h3 className="font-semibold text-center">Taste Balance Overview</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={renderCustomizedLabel}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value: number) => [`${value}%`, 'Percentage']}
                  labelStyle={{ color: '#000' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart */}
          <div className="space-y-4">
            <h3 className="font-semibold text-center">Detailed Breakdown</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="rasa" 
                  tick={{ fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  formatter={(value: number) => [`${value}%`, 'Percentage']}
                  labelStyle={{ color: '#000' }}
                />
                <Bar dataKey="percentage" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Rasa Properties Legend */}
        <div className="mt-6 space-y-4">
          <h3 className="font-semibold">Ayurvedic Properties of Each Rasa</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(RASA_PROPERTIES).map(([rasa, properties]) => {
              const percentage = rasaData[rasa as keyof typeof rasaData];
              return (
                <div 
                  key={rasa} 
                  className="p-3 rounded-lg border"
                  style={{ 
                    borderColor: RASA_COLORS[rasa as keyof typeof RASA_COLORS] + '40',
                    backgroundColor: RASA_COLORS[rasa as keyof typeof RASA_COLORS] + '10'
                  }}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: RASA_COLORS[rasa as keyof typeof RASA_COLORS] }}
                    />
                    <span className="font-medium">{rasa}</span>
                    <span className="text-sm text-muted-foreground">({percentage}%)</span>
                  </div>
                  <p className="text-xs text-muted-foreground mb-1">{properties.effect}</p>
                  <p className="text-xs text-muted-foreground">{properties.dosha}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recommendations */}
        <div className="mt-6 p-4 bg-primary/5 rounded-lg border border-primary/20">
          <h4 className="font-semibold mb-2 text-primary">Ayurvedic Analysis</h4>
          <div className="space-y-2 text-sm">
            {rasaData.Sweet > 30 && (
              <p>✓ Good balance of Sweet taste for nourishment and satisfaction.</p>
            )}
            {rasaData.Sweet < 20 && (
              <p>⚠️ Consider adding more Sweet taste for better nourishment and Vata pacification.</p>
            )}
            {rasaData.Pungent + rasaData.Bitter + rasaData.Astringent > 40 && (
              <p>⚠️ High proportion of light tastes - ensure adequate nourishment for Vata types.</p>
            )}
            {rasaData.Sour + rasaData.Salty + rasaData.Pungent > 50 && (
              <p>⚠️ High heating tastes - may aggravate Pitta in sensitive individuals.</p>
            )}
            <p className="text-xs text-muted-foreground mt-2">
              Ideal Ayurvedic meals contain all six tastes with emphasis based on individual constitution and season.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
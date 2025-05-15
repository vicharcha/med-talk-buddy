
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const BmiCalculator: React.FC = () => {
  const [height, setHeight] = useState<number | ''>('');
  const [weight, setWeight] = useState<number | ''>('');
  const [bmi, setBmi] = useState<number | null>(null);
  const [category, setCategory] = useState<string>('');

  const calculateBmi = () => {
    if (height && weight && height > 0 && weight > 0) {
      // Convert height from cm to meters
      const heightInMeters = height / 100;
      const bmiValue = weight / (heightInMeters * heightInMeters);
      setBmi(parseFloat(bmiValue.toFixed(1)));
      
      // Determine BMI category
      if (bmiValue < 18.5) {
        setCategory('Underweight');
      } else if (bmiValue >= 18.5 && bmiValue < 25) {
        setCategory('Normal weight');
      } else if (bmiValue >= 25 && bmiValue < 30) {
        setCategory('Overweight');
      } else {
        setCategory('Obesity');
      }
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-center">BMI Calculator</CardTitle>
        <CardDescription className="text-center">
          Calculate your Body Mass Index (BMI)
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="height">Height (cm)</Label>
            <Input
              id="height"
              type="number"
              placeholder="Enter your height"
              value={height}
              onChange={(e) => setHeight(e.target.value ? parseFloat(e.target.value) : '')}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="weight">Weight (kg)</Label>
            <Input
              id="weight"
              type="number"
              placeholder="Enter your weight"
              value={weight}
              onChange={(e) => setWeight(e.target.value ? parseFloat(e.target.value) : '')}
            />
          </div>
          
          <Button 
            className="w-full bg-medical-primary hover:bg-medical-secondary"
            onClick={calculateBmi}
            disabled={!height || !weight || height <= 0 || weight <= 0}
          >
            Calculate BMI
          </Button>
          
          {bmi !== null && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-xl font-semibold text-center">Your BMI</h3>
              <div className="text-3xl font-bold text-center text-medical-primary mt-2">{bmi}</div>
              <div className="text-center mt-2">
                Category: <span className="font-medium">{category}</span>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <p><span className="font-medium">Underweight</span>: BMI less than 18.5</p>
                <p><span className="font-medium">Normal weight</span>: BMI 18.5–24.9</p>
                <p><span className="font-medium">Overweight</span>: BMI 25–29.9</p>
                <p><span className="font-medium">Obesity</span>: BMI 30 or greater</p>
              </div>
            </div>
          )}
          
          <div className="text-xs text-gray-500 mt-2">
            Note: BMI is a screening tool, not a diagnostic tool. Consult a healthcare provider for proper health assessment.
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default BmiCalculator;

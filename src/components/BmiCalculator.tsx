import React, { useState, useCallback } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface BmiCategory {
  category: string;
  description: string;
  range: string;
  color: string;
  healthRisk: string;
}

const BMI_CATEGORIES: BmiCategory[] = [
  {
    category: 'Severe Underweight',
    description: 'Significantly below healthy weight range',
    range: 'Less than 16.0',
    color: 'text-red-600',
    healthRisk: 'Very high risk of health problems'
  },
  {
    category: 'Moderate Underweight',
    description: 'Below healthy weight range',
    range: '16.0 - 16.9',
    color: 'text-orange-500',
    healthRisk: 'High risk of health problems'
  },
  {
    category: 'Mild Underweight',
    description: 'Slightly below healthy weight range',
    range: '17.0 - 18.4',
    color: 'text-yellow-500',
    healthRisk: 'Moderate risk of health problems'
  },
  {
    category: 'Normal Weight',
    description: 'Healthy weight range',
    range: '18.5 - 24.9',
    color: 'text-green-600',
    healthRisk: 'Low risk of health problems'
  },
  {
    category: 'Overweight',
    description: 'Above healthy weight range',
    range: '25.0 - 29.9',
    color: 'text-yellow-500',
    healthRisk: 'Increased risk of health problems'
  },
  {
    category: 'Obesity Class I',
    description: 'Moderately above healthy weight range',
    range: '30.0 - 34.9',
    color: 'text-orange-500',
    healthRisk: 'High risk of health problems'
  },
  {
    category: 'Obesity Class II',
    description: 'Significantly above healthy weight range',
    range: '35.0 - 39.9',
    color: 'text-red-500',
    healthRisk: 'Very high risk of health problems'
  },
  {
    category: 'Obesity Class III',
    description: 'Severely above healthy weight range',
    range: '40.0 or higher',
    color: 'text-red-700',
    healthRisk: 'Extremely high risk of health problems'
  }
];

const VALID_RANGES = {
  metric: {
    height: { min: 100, max: 250, unit: 'cm' }, // cm (realistic human height range)
    weight: { min: 20, max: 300, unit: 'kg' }  // kg (realistic human weight range)
  },
  imperial: {
    height: { min: 39, max: 98, unit: 'in' }, // inches (equivalent to ~100-250cm)
    weight: { min: 44, max: 660, unit: 'lbs' } // pounds (equivalent to ~20-300kg)
  }
};

const BmiCalculator: React.FC = () => {
  const [isMetric, setIsMetric] = useState(true);
  const [height, setHeight] = useState<string>('');
  const [heightInches, setHeightInches] = useState<string>('');
  const [weight, setWeight] = useState<string>('');
  const [bmi, setBmi] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState<BmiCategory | null>(null);
  const [conversionInfo, setConversionInfo] = useState<{ height: string; weight: string }>({ height: '', weight: '' });

  const validateInput = useCallback((value: string, type: 'height' | 'weight'): boolean => {
    const num = parseFloat(value);
    const ranges = isMetric ? VALID_RANGES.metric : VALID_RANGES.imperial;
    
    if (isNaN(num) || num <= 0) {
      setError(`Please enter a valid ${type}`);
      return false;
    }
    
    if (type === 'height') {
      const range = ranges.height;
      if (num < range.min || num > range.max) {
        if (isMetric) {
          setError(`Height should be between ${range.min}${range.unit} (3ft 3in) and ${range.max}${range.unit} (8ft 2in). If you're entering a child's height, please consult a pediatrician for proper BMI assessment.`);
        } else {
          setError(`Height should be between ${Math.floor(range.min/12)}ft ${range.min%12}in and ${Math.floor(range.max/12)}ft ${range.max%12}in. If you're entering a child's height, please consult a pediatrician for proper BMI assessment.`);
        }
        return false;
      }
      if (!isMetric && heightInches) {
        const inches = parseFloat(heightInches);
        if (isNaN(inches) || inches < 0 || inches >= 12) {
          setError('Inches should be between 0 and 11');
          return false;
        }
      }
    }
    
    if (type === 'weight') {
      const range = ranges.weight;
      if (num < range.min || num > range.max) {
        if (isMetric) {
          setError(`Weight should be between ${range.min}${range.unit} (44 lbs) and ${range.max}${range.unit} (660 lbs). If you're entering a child's weight, please consult a pediatrician for proper BMI assessment.`);
        } else {
          setError(`Weight should be between ${range.min}${range.unit} (${Math.round(range.min * 0.453592)} kg) and ${range.max}${range.unit} (${Math.round(range.max * 0.453592)} kg). If you're entering a child's weight, please consult a pediatrician for proper BMI assessment.`);
        }
        return false;
      }
    }
    
    // Additional validation for realistic BMI range
    if (type === 'weight' && height) {
      const heightInMeters = isMetric ? parseFloat(height) / 100 : ((parseFloat(height) * 12 + (parseFloat(heightInches) || 0)) * 0.0254);
      const weightInKg = isMetric ? num : (num * 0.453592);
      const bmiValue = weightInKg / (heightInMeters * heightInMeters);
      
      if (bmiValue < 12 || bmiValue > 100) {
        setError('The combination of height and weight would result in an unrealistic BMI. Please check your measurements.');
        return false;
      }
    }
    
    return true;
  }, [isMetric, heightInches, height]);

  const getBmiCategory = useCallback((bmiValue: number): BmiCategory | null => {
    if (bmiValue < 10 || bmiValue > 100) {
      setError('The calculated BMI appears to be outside normal ranges. Please check your inputs.');
      return null;
    }
    return BMI_CATEGORIES.find((cat, index, arr) => {
      if (index === arr.length - 1) return true;
      const nextCatThreshold = parseFloat(arr[index + 1].range.split(' ')[0]);
      return bmiValue < nextCatThreshold;
    }) || null;
  }, []);

  const calculateBmi = useCallback(() => {
    setError(null);
    
    try {
      if (!height || !weight || (!isMetric && !heightInches)) {
        throw new Error('Please enter all required measurements.');
      }

      const heightNum = parseFloat(height);
      const weightNum = parseFloat(weight);
      
      if (!validateInput(height, 'height') || !validateInput(weight, 'weight')) {
        return;
      }

      let heightInMeters: number;
      let weightInKg: number;

      if (isMetric) {
        heightInMeters = heightNum / 100;
        weightInKg = weightNum;
      } else {
        // Convert feet and inches to meters
        const inches = parseFloat(heightInches) || 0;
        const totalInches = (heightNum * 12) + inches;
        heightInMeters = totalInches * 0.0254;
        // Convert pounds to kg
        weightInKg = weightNum * 0.453592;
      }

      const bmiValue = weightInKg / (heightInMeters * heightInMeters);
      const roundedBmi = parseFloat(bmiValue.toFixed(1));
      
      const bmiCategory = getBmiCategory(roundedBmi);
      if (bmiCategory) {
        setBmi(roundedBmi);
        setCategory(bmiCategory);
      } else {
        setBmi(null);
        setCategory(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while calculating BMI.');
      setBmi(null);
      setCategory(null);
    }
  }, [height, weight, heightInches, isMetric, validateInput, getBmiCategory]);

  const convertHeight = useCallback((value: string, fromMetric: boolean): string => {
    const num = parseFloat(value);
    if (isNaN(num) || num <= 0) return '';
    
    if (fromMetric) {
      // Convert cm to feet and inches
      const totalInches = num / 2.54;
      const feet = Math.floor(totalInches / 12);
      const inches = Math.round(totalInches % 12);
      return `${feet}'${inches}" (${num} cm)`;
    } else {
      // Convert feet to cm
      const inches = parseFloat(heightInches) || 0;
      const totalInches = (num * 12) + inches;
      const cm = Math.round(totalInches * 2.54);
      return `${cm} cm (${num}'${inches}")`;
    }
  }, [heightInches]);

  const convertWeight = useCallback((value: string, fromMetric: boolean): string => {
    const num = parseFloat(value);
    if (isNaN(num) || num <= 0) return '';
    
    if (fromMetric) {
      // Convert kg to lbs
      const lbs = Math.round(num * 2.20462 * 10) / 10;
      return `${lbs} lbs (${num} kg)`;
    } else {
      // Convert lbs to kg
      const kg = Math.round(num / 2.20462 * 10) / 10;
      return `${kg} kg (${num} lbs)`;
    }
  }, []);

  const handleInputChange = useCallback((value: string, type: 'height' | 'weight') => {
    const setValue = type === 'height' ? setHeight : setWeight;
    setValue(value);
    setError(null);
    setBmi(null);
    setCategory(null);

    // Update conversion information
    if (value) {
      setConversionInfo(prev => ({
        ...prev,
        [type]: type === 'height' 
          ? convertHeight(value, isMetric)
          : convertWeight(value, isMetric)
      }));
    } else {
      setConversionInfo(prev => ({ ...prev, [type]: '' }));
    }
  }, [isMetric, convertHeight, convertWeight]);

  const getHealthyWeightRange = useCallback((): string | null => {
    if (!height || (!isMetric && !heightInches)) return null;
    
    let heightInMeters: number;
    if (isMetric) {
      heightInMeters = parseFloat(height) / 100;
    } else {
      const inches = parseFloat(heightInches) || 0;
      const totalInches = (parseFloat(height) * 12) + inches;
      heightInMeters = totalInches * 0.0254;
    }

    const minWeight = 18.5 * heightInMeters * heightInMeters;
    const maxWeight = 24.9 * heightInMeters * heightInMeters;
    
    if (isMetric) {
      return `${minWeight.toFixed(1)} - ${maxWeight.toFixed(1)} kg`;
    } else {
      const minLbs = minWeight * 2.20462;
      const maxLbs = maxWeight * 2.20462;
      return `${minLbs.toFixed(1)} - ${maxLbs.toFixed(1)} lbs`;
    }
  }, [height, heightInches, isMetric]);

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
          <div className="flex items-center justify-between mb-4">
            <Label>Unit System</Label>
            <div className="flex items-center space-x-2">
              <Label>Imperial</Label>
              <Switch
                checked={isMetric}
                onCheckedChange={(checked) => {
                  setIsMetric(checked);
                  // Convert existing values if they exist
                  if (height) {
                    const heightNum = parseFloat(height);
                    if (!isNaN(heightNum)) {
                      if (checked) {
                        // Converting from imperial to metric
                        const inches = parseFloat(heightInches) || 0;
                        const totalInches = (heightNum * 12) + inches;
                        setHeight((totalInches * 2.54).toFixed(1));
                        setHeightInches('');
                      } else {
                        // Converting from metric to imperial
                        const totalInches = heightNum / 2.54;
                        setHeight(Math.floor(totalInches / 12).toString());
                        setHeightInches((Math.round(totalInches % 12)).toString());
                      }
                    }
                  }
                  if (weight) {
                    const weightNum = parseFloat(weight);
                    if (!isNaN(weightNum)) {
                      if (checked) {
                        // Converting from lbs to kg
                        setWeight((weightNum / 2.20462).toFixed(1));
                      } else {
                        // Converting from kg to lbs
                        setWeight((weightNum * 2.20462).toFixed(1));
                      }
                    }
                  }
                  setBmi(null);
                  setCategory(null);
                  setError(null);
                  // Update conversion info
                  if (height) {
                    handleInputChange(height, 'height');
                  }
                  if (weight) {
                    handleInputChange(weight, 'weight');
                  }
                }}
              />
              <Label>Metric</Label>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="height">
              Height ({isMetric ? 'cm' : 'ft'})
              {conversionInfo.height && (
                <span className="ml-2 text-sm text-muted-foreground">
                  ≈ {conversionInfo.height}
                </span>
              )}
            </Label>
            {isMetric ? (
              <div className="space-y-1">
                <Input
                  id="height"
                  type="number"
                  placeholder="Enter height in centimeters"
                  value={height}
                  onChange={(e) => handleInputChange(e.target.value, 'height')}
                  min={VALID_RANGES.metric.height.min}
                  max={VALID_RANGES.metric.height.max}
                  step="0.1"
                />
                <p className="text-xs text-muted-foreground">
                  Common heights: 150cm (4'11") | 160cm (5'3") | 170cm (5'7") | 180cm (5'11") | 190cm (6'3")
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                <Input
                  id="height-feet"
                  type="number"
                  placeholder="Feet"
                  value={height}
                  onChange={(e) => handleInputChange(e.target.value, 'height')}
                  min={1}
                  max={9}
                  step="1"
                />
                <Input
                  id="height-inches"
                  type="number"
                  placeholder="Inches"
                  value={heightInches}
                  onChange={(e) => {
                    setHeightInches(e.target.value);
                    setError(null);
                    setBmi(null);
                    setCategory(null);
                  }}
                  min={0}
                  max={11}
                  step="1"
                />
              </div>
            )}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="weight">
              Weight ({isMetric ? 'kg' : 'lbs'})
              {conversionInfo.weight && (
                <span className="ml-2 text-sm text-muted-foreground">
                  ≈ {conversionInfo.weight}
                </span>
              )}
            </Label>
            <div className="space-y-1">
              <Input
                id="weight"
                type="number"
                placeholder={`Enter weight in ${isMetric ? 'kilograms' : 'pounds'}`}
                value={weight}
                onChange={(e) => handleInputChange(e.target.value, 'weight')}
                min={isMetric ? VALID_RANGES.metric.weight.min : VALID_RANGES.imperial.weight.min}
                max={isMetric ? VALID_RANGES.metric.weight.max : VALID_RANGES.imperial.weight.max}
                step="0.1"
              />
              <p className="text-xs text-muted-foreground">
                {isMetric 
                  ? "Common weights: 50kg (110lbs) | 60kg (132lbs) | 70kg (154lbs) | 80kg (176lbs) | 90kg (198lbs)"
                  : "Common weights: 100lbs (45kg) | 125lbs (57kg) | 150lbs (68kg) | 175lbs (79kg) | 200lbs (91kg)"
                }
              </p>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          <Button 
            className="w-full"
            onClick={calculateBmi}
            disabled={!height || !weight}
          >
            Calculate BMI
          </Button>
          
          {bmi !== null && category && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg space-y-4">
              <h3 className="text-xl font-semibold text-center">Your BMI</h3>
              <div className="text-3xl font-bold text-center mt-2">
                <span className={category.color}>{bmi}</span>
              </div>

              <Progress
                value={(bmi / 40) * 100}
                className="w-full h-2"
              />
              
              <div className="text-center mt-2">
                <p className="font-medium">Category: <span className={category.color}>{category.category}</span></p>
                <p className="text-sm mt-1">{category.description}</p>
                <p className="text-sm mt-1">Health Risk: <span className={category.color}>{category.healthRisk}</span></p>
              </div>

              {height && (
                <div className="mt-4 text-sm">
                  <p className="font-medium">Healthy Weight Range for Your Height:</p>
                  <p className="text-center mt-1">{getHealthyWeightRange()}</p>
                </div>
              )}

              <div className="mt-4 text-sm text-gray-600 space-y-1">
                {BMI_CATEGORIES.map((cat) => (
                  <p key={cat.category}>
                    <span className={`font-medium ${cat.color}`}>{cat.category}</span>: 
                    BMI {cat.range}
                  </p>
                ))}
              </div>
            </div>
          )}
          
          <Alert className="mt-4">
            <AlertDescription className="text-xs space-y-2">
              <p>BMI is a screening tool, not a diagnostic tool. It may not be accurate for:</p>
              <ul className="list-disc pl-4 space-y-1">
                <li>Athletes and bodybuilders (due to high muscle mass)</li>
                <li>Pregnant or nursing women</li>
                <li>The elderly</li>
                <li>Growing children and teenagers</li>
              </ul>
              <p>Other important factors not considered by BMI include:</p>
              <ul className="list-disc pl-4 space-y-1">
                <li>Muscle mass and bone density</li>
                <li>Overall body composition</li>
                <li>Ethnic and racial differences</li>
                <li>Age and gender</li>
                <li>Body fat distribution</li>
              </ul>
              <p className="font-medium mt-2">Always consult a healthcare provider for a complete health assessment.</p>
            </AlertDescription>
          </Alert>
        </div>
      </CardContent>
    </Card>
  );
};

export default BmiCalculator;


import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import BmiCalculator from '@/components/BmiCalculator';

const Bmi = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow py-8 px-4">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-2 text-center">BMI Calculator</h1>
          <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto">
            Calculate your Body Mass Index (BMI) to determine if your weight is within a healthy range for your height.
          </p>
          
          <div className="max-w-md mx-auto">
            <BmiCalculator />
          </div>
          
          <div className="mt-12 max-w-2xl mx-auto bg-white p-6 rounded-lg shadow border">
            <h2 className="text-xl font-semibold mb-4">Understanding BMI</h2>
            <p className="text-gray-600 mb-4">
              BMI is a measure of body fat based on height and weight. While it can be a useful screening tool, 
              it's not a diagnostic tool for body fatness or health.
            </p>
            
            <h3 className="text-lg font-medium mb-2">BMI Categories:</h3>
            <ul className="list-disc pl-5 space-y-1 text-gray-600">
              <li>Underweight: BMI less than 18.5</li>
              <li>Normal weight: BMI 18.5–24.9</li>
              <li>Overweight: BMI 25–29.9</li>
              <li>Obesity: BMI 30 or greater</li>
            </ul>
            
            <div className="mt-4 p-3 bg-medical-light rounded-md text-sm">
              <p>
                <strong>Note:</strong> BMI does not account for muscle mass, bone density, body composition, 
                or racial and sex differences. Athletes, for instance, may have a high BMI due to increased 
                muscle mass rather than body fat. Always consult with a healthcare provider for a complete 
                assessment of your health.
              </p>
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Bmi;

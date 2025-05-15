
import React from 'react';
import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-gray-50 py-8 border-t">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="flex flex-col">
            <Link to="/" className="flex items-center gap-2 text-medical-primary font-bold text-xl">
              <Heart className="h-5 w-5 fill-medical-primary text-white" />
              <span>Healthcare ChatBot</span>
            </Link>
            <p className="mt-2 text-sm text-gray-600">
              Providing intelligent healthcare assistance through advanced AI technology
            </p>
          </div>
          
          <div>
            <h3 className="font-medium text-lg mb-4">Quick Links</h3>
            <div className="flex flex-col gap-2">
              <Link to="/" className="text-gray-600 hover:text-medical-primary">Home</Link>
              <Link to="/chat" className="text-gray-600 hover:text-medical-primary">Chat</Link>
              <Link to="/bmi" className="text-gray-600 hover:text-medical-primary">BMI Calculator</Link>
              <Link to="/team" className="text-gray-600 hover:text-medical-primary">Team</Link>
            </div>
          </div>
          
          <div>
            <h3 className="font-medium text-lg mb-4">Contact</h3>
            <p className="text-gray-600">Email: contact@healthcarechatbot.com</p>
          </div>
        </div>
        
        <div className="mt-8 pt-4 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} Healthcare ChatBot. All rights reserved.</p>
          <p className="mt-1 text-xs">
            Note: This is for informational purposes only and not a substitute for professional medical advice.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;


import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Header: React.FC = () => {
  const location = useLocation();
  
  const isActive = (path: string): boolean => {
    return location.pathname === path;
  };

  return (
    <header className="w-full px-4 py-4 border-b">
      <div className="container mx-auto flex flex-col sm:flex-row items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-medical-primary font-bold text-2xl">
          <Heart className="h-6 w-6 fill-medical-primary text-white" />
          <span>Healthcare ChatBot</span>
        </Link>

        <nav className="flex mt-4 sm:mt-0 space-x-6">
          <Link 
            to="/" 
            className={`${isActive('/') ? 'text-medical-primary font-medium' : 'text-gray-600 hover:text-medical-primary'}`}
          >
            Home
          </Link>
          <Link 
            to="/chat" 
            className={`${isActive('/chat') ? 'text-medical-primary font-medium' : 'text-gray-600 hover:text-medical-primary'}`}
          >
            Chat
          </Link>
          <Link 
            to="/bmi" 
            className={`${isActive('/bmi') ? 'text-medical-primary font-medium' : 'text-gray-600 hover:text-medical-primary'}`}
          >
            BMI
          </Link>
          <Link 
            to="/team" 
            className={`${isActive('/team') ? 'text-medical-primary font-medium' : 'text-gray-600 hover:text-medical-primary'}`}
          >
            Team
          </Link>
        </nav>

        <div className="mt-4 sm:mt-0">
          <Button className="bg-medical-primary hover:bg-medical-secondary">
            Log In
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;

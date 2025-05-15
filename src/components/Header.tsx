
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Heart, LogOut, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';

const Header: React.FC = () => {
  const location = useLocation();
  const { currentUser, logout } = useAuth();
  
  const isActive = (path: string): boolean => {
    return location.pathname === path;
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Error logging out:", error);
    }
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
          {currentUser ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center gap-2 hover:bg-gray-100">
                  <User className="h-4 w-4" />
                  {currentUser.email?.split('@')[0] || 'User'}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={handleLogout} className="cursor-pointer">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Logout</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Link to="/login">
              <Button className="bg-medical-primary hover:bg-medical-secondary">
                Log In
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;

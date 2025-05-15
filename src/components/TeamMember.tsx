
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar } from '@/components/ui/avatar';

interface TeamMemberProps {
  name: string;
  role: string;
  image: string;
  bio: string;
}

const TeamMember: React.FC<TeamMemberProps> = ({ name, role, image, bio }) => {
  return (
    <Card className="overflow-hidden transition-all hover:shadow-lg">
      <CardContent className="p-6">
        <div className="flex flex-col items-center">
          <Avatar className="w-24 h-24 border-4 border-medical-light mb-4">
            <img 
              src={image} 
              alt={name} 
              className="object-cover"
              onError={(e) => {
                // Fallback to initials if image fails to load
                (e.target as HTMLImageElement).style.display = 'none';
                (e.target as HTMLImageElement).parentElement!.innerHTML = name.split(' ').map(n => n[0]).join('');
                (e.target as HTMLImageElement).parentElement!.classList.add('flex', 'items-center', 'justify-center', 'bg-medical-primary', 'text-white', 'text-xl');
              }}
            />
          </Avatar>
          <h3 className="font-semibold text-lg">{name}</h3>
          <p className="text-medical-primary font-medium text-sm mb-2">{role}</p>
          <p className="text-gray-600 text-center text-sm">{bio}</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default TeamMember;

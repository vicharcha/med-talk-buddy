
import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import TeamMember from '@/components/TeamMember';

const teamMembers = [
  {
    name: 'Dr. Sarah Johnson',
    role: 'Chief Medical Advisor',
    image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80&w=300&auto=format&fit=crop',
    bio: 'Dr. Johnson specializes in internal medicine with over 15 years of experience. She oversees the medical content of our chatbot.'
  },
  {
    name: 'Alex Martinez',
    role: 'AI Development Lead',
    image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=300&auto=format&fit=crop',
    bio: 'Alex has a background in machine learning and healthcare informatics, focusing on creating intelligent healthcare solutions.'
  },
  {
    name: 'Dr. Michael Chen',
    role: 'Medical Content Specialist',
    image: 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?q=80&w=300&auto=format&fit=crop',
    bio: 'Dr. Chen ensures that all information provided by our chatbot is medically accurate and follows best healthcare practices.'
  },
  {
    name: 'Emma Wilson',
    role: 'User Experience Designer',
    image: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=300&auto=format&fit=crop',
    bio: 'Emma creates the intuitive and accessible interface that makes our healthcare chatbot easy to use for all patients.'
  },
  {
    name: 'Dr. James Taylor',
    role: 'Healthcare Ethics Advisor',
    image: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=300&auto=format&fit=crop',
    bio: 'Dr. Taylor ensures our AI adheres to healthcare ethics standards and prioritizes patient wellbeing in all interactions.'
  },
  {
    name: 'Sophia Rodriguez',
    role: 'Data Privacy Specialist',
    image: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=300&auto=format&fit=crop',
    bio: 'Sophia ensures that all user interactions with our chatbot maintain the highest standards of data security and privacy.'
  }
];

const Team = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow py-8 px-4">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-2 text-center">Our Team</h1>
          <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto">
            Meet the dedicated professionals behind our Healthcare ChatBot who work to provide you with accurate and helpful medical information.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {teamMembers.map((member, index) => (
              <TeamMember
                key={index}
                name={member.name}
                role={member.role}
                image={member.image}
                bio={member.bio}
              />
            ))}
          </div>
          
          <div className="mt-16 text-center">
            <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Our team is committed to making healthcare information more accessible through technology. 
              We combine medical expertise with artificial intelligence to provide helpful guidance while 
              always emphasizing the importance of consulting healthcare professionals for proper diagnosis and treatment.
            </p>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Team;

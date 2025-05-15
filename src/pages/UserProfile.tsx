
import React, { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { User, History, Calendar, FileText } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface MedicalRecord {
  id: string;
  date: string;
  title: string;
  description: string;
}

const UserProfile: React.FC = () => {
  const { currentUser } = useAuth();
  const { toast } = useToast();
  const [newRecord, setNewRecord] = useState({
    title: '',
    description: ''
  });
  
  // Mock medical records - in a real app, these would come from a database
  const [medicalRecords, setMedicalRecords] = useState<MedicalRecord[]>([
    {
      id: '1',
      date: '2024-05-10',
      title: 'Annual Checkup',
      description: 'Blood pressure: 120/80, Heart rate: 72bpm, Weight: 70kg. Overall health is good.'
    },
    {
      id: '2',
      date: '2024-03-15',
      title: 'Flu Symptoms',
      description: 'Patient reported fever, cough, and fatigue. Prescribed rest and fluids.'
    }
  ]);

  const handleAddRecord = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newRecord.title || !newRecord.description) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }
    
    const record: MedicalRecord = {
      id: Date.now().toString(),
      date: new Date().toISOString().split('T')[0],
      title: newRecord.title,
      description: newRecord.description
    };
    
    setMedicalRecords([record, ...medicalRecords]);
    setNewRecord({ title: '', description: '' });
    
    toast({
      title: "Record Added",
      description: "Your medical record has been added successfully.",
    });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow py-8 px-4">
        <div className="container mx-auto max-w-4xl">
          <h1 className="text-3xl font-bold mb-8 text-center">My Health Profile</h1>
          
          <div className="flex flex-col md:flex-row gap-6">
            {/* User Profile Card */}
            <Card className="w-full md:w-1/3">
              <CardHeader>
                <div className="flex justify-center">
                  <div className="h-24 w-24 rounded-full bg-medical-light flex items-center justify-center">
                    <User className="h-12 w-12 text-medical-primary" />
                  </div>
                </div>
                <CardTitle className="text-center mt-4">
                  {currentUser?.displayName || currentUser?.email?.split('@')[0] || 'User'}
                </CardTitle>
                <CardDescription className="text-center">
                  {currentUser?.email}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-medical-primary" />
                    <span>Member since: {currentUser?.metadata.creationTime ? 
                      new Date(currentUser.metadata.creationTime).toLocaleDateString() : 'N/A'}</span>
                  </div>
                  <Button className="w-full bg-medical-primary hover:bg-medical-secondary">
                    Edit Profile
                  </Button>
                </div>
              </CardContent>
            </Card>
            
            {/* Medical Records */}
            <Card className="w-full md:w-2/3">
              <CardHeader>
                <CardTitle>Medical History</CardTitle>
                <CardDescription>
                  Your health records and medical history
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="records">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="records">Records</TabsTrigger>
                    <TabsTrigger value="add">Add New Record</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="records" className="space-y-4 mt-4">
                    {medicalRecords.length > 0 ? (
                      medicalRecords.map((record) => (
                        <Card key={record.id}>
                          <CardHeader className="py-3">
                            <div className="flex justify-between items-center">
                              <CardTitle className="text-lg">{record.title}</CardTitle>
                              <span className="text-sm text-gray-500">{record.date}</span>
                            </div>
                          </CardHeader>
                          <CardContent className="pt-0">
                            <p className="text-gray-600">{record.description}</p>
                          </CardContent>
                        </Card>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <FileText className="mx-auto h-12 w-12 text-gray-300" />
                        <p className="mt-2 text-gray-500">No medical records yet</p>
                      </div>
                    )}
                  </TabsContent>
                  
                  <TabsContent value="add" className="mt-4">
                    <form onSubmit={handleAddRecord} className="space-y-4">
                      <div>
                        <Label htmlFor="title">Record Title</Label>
                        <Input 
                          id="title"
                          placeholder="e.g., Annual Checkup, Vaccination, Specialist Visit"
                          value={newRecord.title}
                          onChange={(e) => setNewRecord({...newRecord, title: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label htmlFor="description">Description</Label>
                        <Textarea 
                          id="description"
                          placeholder="Enter details about your medical record"
                          value={newRecord.description}
                          onChange={(e) => setNewRecord({...newRecord, description: e.target.value})}
                          rows={5}
                        />
                      </div>
                      <Button 
                        type="submit" 
                        className="w-full bg-medical-primary hover:bg-medical-secondary"
                      >
                        Add Record
                      </Button>
                    </form>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default UserProfile;

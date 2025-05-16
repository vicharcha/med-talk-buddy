
import React, { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ChatInterface from '@/components/ChatInterface';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { InfoCircle } from 'lucide-react';

const Chat = () => {
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow py-8 px-4">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-4 text-center">Chat with our Healthcare Assistant</h1>
          
          {showDisclaimer && (
            <Alert className="mb-6 max-w-4xl mx-auto">
              <InfoCircle className="h-4 w-4" />
              <AlertTitle>Medical AI Disclaimer</AlertTitle>
              <AlertDescription>
                This AI assistant is trained on medical datasets to provide information, but it is not a substitute for professional medical advice. 
                Always consult with a healthcare professional for medical concerns. To train the medical model, run <code>./start_app.sh --train-model</code> in your terminal.
              </AlertDescription>
              <button 
                onClick={() => setShowDisclaimer(false)} 
                className="text-sm text-blue-600 hover:underline mt-2"
              >
                Dismiss
              </button>
            </Alert>
          )}
          
          <div className="max-w-4xl mx-auto">
            <ChatInterface />
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Chat;

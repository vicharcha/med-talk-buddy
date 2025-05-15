
import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ChatInterface from '@/components/ChatInterface';

const Chat = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow py-8 px-4">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold mb-8 text-center">Chat with our Healthcare Assistant</h1>
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

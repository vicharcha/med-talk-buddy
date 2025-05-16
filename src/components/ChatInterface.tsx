
import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import ChatMessage, { ChatMessageProps } from './ChatMessage';
import { auth } from '@/lib/firebase';

// Format current time for message timestamps
const getCurrentTime = (): string => {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessageProps[]>([
    {
      message: "Hello! I'm MedTalkBuddy, your healthcare assistant. How can I help you today?",
      type: 'bot',
      timestamp: getCurrentTime()
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // Auto scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to UI immediately
    const userMessage: ChatMessageProps = {
      message: input,
      type: 'user',
      timestamp: getCurrentTime()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    // Show typing indicator
    setIsTyping(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          message: input,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      
      // Save conversation ID for future messages
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }
      
      const botMessage: ChatMessageProps = {
        message: data.message,
        type: 'bot',
        timestamp: getCurrentTime()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Show error message to user
      toast({
        title: "Connection Error",
        description: "Failed to connect to the medical chat service. Please try again later.",
        variant: "destructive"
      });
      
      const botMessage: ChatMessageProps = {
        message: "I'm sorry, there was an error connecting to the server. Please check your connection and try again.",
        type: 'bot',
        timestamp: getCurrentTime()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[70vh] bg-white rounded-lg shadow-md border">
      <div className="p-4 bg-medical-primary text-white rounded-t-lg">
        <h2 className="text-xl font-semibold">MedTalkBuddy</h2>
        <p className="text-sm text-medical-light">Ask me about your symptoms or health concerns</p>
      </div>
      
      <div className="flex-grow p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <ChatMessage 
            key={index}
            message={msg.message}
            type={msg.type}
            timestamp={msg.timestamp}
          />
        ))}
        
        {isTyping && (
          <div className="flex items-center text-gray-500 text-sm mb-4">
            <div className="flex space-x-1 items-center">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-100"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-200"></div>
            </div>
            <span className="ml-2">MedTalkBuddy is typing...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            placeholder="Type your symptoms or health question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-grow"
          />
          <Button 
            onClick={handleSendMessage} 
            className="bg-medical-primary hover:bg-medical-secondary"
            disabled={!input.trim() || isTyping}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Note: This is for informational purposes only and not a substitute for professional medical advice.
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;

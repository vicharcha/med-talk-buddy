
import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Loader2 } from 'lucide-react';
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
  const [modelStatus, setModelStatus] = useState<'loading' | 'ready' | 'unavailable'>('loading');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // Auto scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/health');
        if (response.ok) {
          const data = await response.json();
          setModelStatus(data.model_loaded ? 'ready' : 'unavailable');
          
          if (!data.model_loaded) {
            toast({
              title: "Model Not Loaded",
              description: "The medical model is not currently loaded. Some features may be limited.",
              variant: "warning"
            });
          }
        } else {
          setModelStatus('unavailable');
          throw new Error('Backend health check failed');
        }
      } catch (error) {
        console.error('Backend health check error:', error);
        setModelStatus('unavailable');
        toast({
          title: "Connection Error",
          description: "Could not connect to the backend. Please ensure the backend server is running.",
          variant: "destructive"
        });
      }
    };
    
    checkBackendHealth();
  }, [toast]);

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
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold">MedTalkBuddy</h2>
            <p className="text-sm text-medical-light">Ask me about your symptoms or health concerns</p>
          </div>
          {modelStatus === 'loading' && (
            <div className="flex items-center text-medical-light">
              <Loader2 className="animate-spin mr-2 h-4 w-4" />
              <span className="text-sm">Connecting...</span>
            </div>
          )}
          {modelStatus === 'ready' && (
            <div className="text-medical-light text-sm flex items-center">
              <span className="h-2 w-2 bg-green-400 rounded-full mr-2"></span>
              Model Ready
            </div>
          )}
          {modelStatus === 'unavailable' && (
            <div className="text-medical-light text-sm flex items-center">
              <span className="h-2 w-2 bg-red-400 rounded-full mr-2"></span>
              Limited Mode
            </div>
          )}
        </div>
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
            <span className="ml-2">MedTalkBuddy is thinking...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            placeholder={modelStatus === 'unavailable' 
              ? "Backend connection issue - demo mode only" 
              : "Type your symptoms or health question..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-grow"
            disabled={modelStatus === 'loading'}
          />
          <Button 
            onClick={handleSendMessage} 
            className="bg-medical-primary hover:bg-medical-secondary"
            disabled={!input.trim() || isTyping || modelStatus === 'loading'}
          >
            {isTyping ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </div>
        <div className="flex justify-between mt-2">
          <p className="text-xs text-gray-500">
            Note: This is for informational purposes only and not a substitute for professional medical advice.
          </p>
          
          {conversationId && (
            <p className="text-xs text-gray-400">
              Conversation ID: {conversationId.substring(0, 8)}...
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;

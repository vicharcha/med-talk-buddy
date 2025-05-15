
import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send } from 'lucide-react';
import ChatMessage, { ChatMessageProps } from './ChatMessage';

// Mock bot responses based on user input
const getBotResponse = (message: string): string => {
  const lowercaseMessage = message.toLowerCase();
  
  if (lowercaseMessage.includes('hello') || lowercaseMessage.includes('hi')) {
    return "Hello! I'm your healthcare assistant. How can I help you today?";
  }
  
  if (lowercaseMessage.includes('headache') || lowercaseMessage.includes('head pain')) {
    return "I understand you're experiencing headaches. This could be due to various factors like stress, dehydration, or eye strain. Try resting in a dark, quiet room, stay hydrated, and consider over-the-counter pain relievers if necessary. If headaches persist or are severe, please consult a healthcare professional.";
  }
  
  if (lowercaseMessage.includes('fever') || lowercaseMessage.includes('temperature')) {
    return "I see you're concerned about fever. For adults, a fever is typically considered a temperature above 100.4°F (38°C). Rest, stay hydrated, and take acetaminophen or ibuprofen to reduce fever. Seek medical attention if your fever is very high, lasts more than three days, or is accompanied by severe symptoms.";
  }
  
  if (lowercaseMessage.includes('cold') || lowercaseMessage.includes('flu') || lowercaseMessage.includes('cough')) {
    return "For cold or flu symptoms, rest, stay hydrated, and consider over-the-counter medications for symptom relief. Honey can help with cough (for adults and children over 1 year). See a doctor if symptoms are severe or persist beyond a week. Remember, this is general information and not a substitute for professional medical advice.";
  }

  if (lowercaseMessage.includes('thank')) {
    return "You're welcome! If you have any other health-related questions, feel free to ask. Remember, I'm here to provide general information, but always consult a healthcare professional for personalized medical advice.";
  }

  return "I understand you're concerned about your health. Could you provide more specific symptoms so I can offer better guidance? Remember, I'm here to provide general information, but for serious concerns, please consult a healthcare professional.";
};

// Format current time for message timestamps
const getCurrentTime = (): string => {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessageProps[]>([
    {
      message: "Hello! I'm your healthcare assistant. How can I help you today?",
      type: 'bot',
      timestamp: getCurrentTime()
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: ChatMessageProps = {
      message: input,
      type: 'user',
      timestamp: getCurrentTime()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    // Simulate bot typing
    setIsTyping(true);
    
    // Delay bot response to simulate thinking/typing
    setTimeout(() => {
      const botMessage: ChatMessageProps = {
        message: getBotResponse(input),
        type: 'bot',
        timestamp: getCurrentTime()
      };
      
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[70vh] bg-white rounded-lg shadow-md border">
      <div className="p-4 bg-medical-primary text-white rounded-t-lg">
        <h2 className="text-xl font-semibold">Healthcare Assistant</h2>
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
            <span className="ml-2">AI is typing...</span>
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

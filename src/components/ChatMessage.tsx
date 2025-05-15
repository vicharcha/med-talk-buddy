
import React from 'react';
import { Avatar } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';

export type MessageType = 'bot' | 'user';

export interface ChatMessageProps {
  message: string;
  type: MessageType;
  timestamp: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, type, timestamp }) => {
  return (
    <div className={cn(
      "flex w-full mb-4 animate-fade-in",
      type === 'user' ? 'justify-end' : 'justify-start'
    )}>
      {type === 'bot' && (
        <div className="flex-shrink-0 mr-3">
          <Avatar className="h-8 w-8 bg-medical-primary text-white">
            <span className="text-xs">AI</span>
          </Avatar>
        </div>
      )}
      
      <div className={cn(
        "max-w-[80%] sm:max-w-[70%] rounded-lg px-4 py-3",
        type === 'user' 
          ? 'bg-medical-primary text-white' 
          : 'bg-gray-100 text-gray-800'
      )}>
        <div className="whitespace-pre-wrap break-words">{message}</div>
        <div className={cn(
          "text-xs mt-1",
          type === 'user' ? 'text-medical-light' : 'text-gray-500'
        )}>
          {timestamp}
        </div>
      </div>
      
      {type === 'user' && (
        <div className="flex-shrink-0 ml-3">
          <Avatar className="h-8 w-8 bg-gray-400 text-white">
            <span className="text-xs">You</span>
          </Avatar>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

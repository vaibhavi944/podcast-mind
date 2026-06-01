import React from 'react';
import { User, Settings2 } from 'lucide-react';
import { cn } from '../lib/utils';

const TasteProfileBadge = ({ interests, onEdit }) => {
  if (!interests || interests.length === 0) return null;

  return (
    <div className="inline-flex items-center gap-3 rounded-2xl border bg-card/50 px-4 py-2 text-sm shadow-sm">
      <div className="flex -space-x-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary ring-2 ring-background">
          <User className="h-4 w-4" />
        </div>
      </div>
      <div className="flex flex-col">
        <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">My Profile</span>
        <span className="font-medium max-w-[200px] truncate">
          {interests.join(', ')}
        </span>
      </div>
      <button 
        onClick={onEdit}
        className="ml-2 rounded-lg p-1 hover:bg-secondary text-muted-foreground hover:text-foreground transition-colors"
        title="Edit interests"
      >
        <Settings2 className="h-4 w-4" />
      </button>
    </div>
  );
};

export default TasteProfileBadge;

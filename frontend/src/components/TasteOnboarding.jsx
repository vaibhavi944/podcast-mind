import React, { useState } from 'react';
import { Check, ArrowRight } from 'lucide-react';
import { cn } from '../lib/utils';

const CATEGORIES = [
  "AI", "Technology", "History", "Psychology", "Comedy", 
  "Business", "Science", "Philosophy", "Health", "Productivity",
  "True Crime", "Arts", "Fiction", "Society & Culture"
];

const TasteOnboarding = ({ onComplete }) => {
  const [selected, setSelected] = useState([]);

  const toggleInterest = (cat) => {
    setSelected(prev => 
      prev.includes(cat) 
        ? prev.filter(c => c !== cat) 
        : [...prev, cat]
    );
  };

  const handleFinish = () => {
    localStorage.setItem('podcast-mind-interests', JSON.stringify(selected));
    onComplete(selected);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
      <div className="w-full max-w-2xl rounded-3xl border bg-card p-8 shadow-2xl space-y-8">
        <div className="space-y-2 text-center">
          <h2 className="text-3xl font-bold tracking-tight">Tune your feed.</h2>
          <p className="text-muted-foreground">Pick a few topics you enjoy. No accounts, just better recommendations.</p>
        </div>

        <div className="flex flex-wrap gap-3 justify-center">
          {CATEGORIES.map((cat) => {
            const isSelected = selected.includes(cat);
            return (
              <button
                key={cat}
                onClick={() => toggleInterest(cat)}
                className={cn(
                  "inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold transition-all border-2",
                  isSelected 
                    ? "bg-primary border-primary text-primary-foreground scale-105 shadow-md" 
                    : "bg-background border-border hover:border-primary/50 text-muted-foreground"
                )}
              >
                {isSelected && <Check className="h-4 w-4" />}
                {cat}
              </button>
            );
          })}
        </div>

        <div className="flex items-center justify-between pt-4">
          <button 
            onClick={() => onComplete([])}
            className="text-sm font-medium text-muted-foreground hover:text-foreground underline underline-offset-4"
          >
            Skip for now
          </button>
          
          <button
            onClick={handleFinish}
            disabled={selected.length === 0}
            className={cn(
              "flex items-center gap-2 rounded-full bg-primary px-8 py-3 font-bold text-primary-foreground shadow-lg transition-all hover:opacity-90 active:scale-95",
              selected.length === 0 && "opacity-50 cursor-not-allowed"
            )}
          >
            Start Discovering
            <ArrowRight className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TasteOnboarding;

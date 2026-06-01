import React from 'react';
import { Info, BarChart, User } from 'lucide-react';
import { cn } from '../lib/utils';

const PodcastCard = ({ 
  podcast, 
  onClick, 
  isSelected = false,
  className 
}) => {
  const { title, author, categories, explanation, blended_score } = podcast;

  return (
    <div 
      onClick={() => onClick && onClick(podcast)}
      className={cn(
        "group relative flex flex-col rounded-xl border bg-card p-5 transition-all hover:shadow-md cursor-pointer",
        isSelected ? "border-primary ring-1 ring-primary" : "border-border",
        className
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 space-y-1">
          <h3 className="font-semibold leading-tight text-lg group-hover:text-primary transition-colors line-clamp-2">
            {title}
          </h3>
          {author && (
            <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <User className="h-3.5 w-3.5" />
              <span className="truncate">{author}</span>
            </div>
          )}
          <div className="flex flex-wrap gap-1 pt-1">
            {categories.split(',').slice(0, 2).map((cat, i) => (
              <span 
                key={i} 
                className="inline-flex items-center rounded-full bg-secondary px-2.5 py-0.5 text-xs font-medium text-secondary-foreground"
              >
                {cat.trim()}
              </span>
            ))}
          </div>
        </div>
        
        {blended_score > 0 && (
          <div className="flex flex-col items-center gap-0.5">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/5 text-primary border border-primary/10">
              <span className="text-xs font-bold">{Math.round(blended_score * 100)}%</span>
            </div>
            <span className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">Match</span>
          </div>
        )}
      </div>

      {explanation && (
        <div className="mt-4 rounded-lg bg-primary/[0.03] border border-primary/5 p-3 text-sm text-muted-foreground flex gap-2 items-start">
          <Info className="h-4 w-4 shrink-0 mt-0.5 text-primary/50" />
          <p className="italic leading-relaxed text-foreground/80">"{explanation}"</p>
        </div>
      )}

      <div className="mt-auto pt-4 flex items-center justify-between text-muted-foreground">
        <div className="flex items-center gap-1.5 text-xs font-medium">
          <BarChart className="h-3.5 w-3.5" />
          <span>Hybrid Match</span>
        </div>
      </div>
    </div>
  );
};

export default PodcastCard;

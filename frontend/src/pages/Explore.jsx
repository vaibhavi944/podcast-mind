import React, { useState, useEffect } from 'react';
import { podcastApi } from '../api/client';
import PodcastCard from '../components/PodcastCard';
import { Loader2 } from 'lucide-react';
import { cn } from '../lib/utils';

const Explore = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeCategory, setActiveCategory] = useState(null);

  const categories = [
    "Technology", "Science", "Business", "Health", "History", 
    "True Crime", "Comedy", "Society & Culture", "Education"
  ];

  const handleCategoryClick = async (category) => {
    setActiveCategory(category);
    setLoading(true);
    try {
      const data = await podcastApi.searchPodcasts(category, 12);
      setResults(data.results);
    } catch (error) {
      console.error("Explore failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleCategoryClick(categories[0]);
  }, []);

  return (
    <div className="space-y-10">
      <section className="space-y-4">
        <h1 className="text-3xl font-bold tracking-tight text-center sm:text-left">Explore Categories</h1>
        <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => handleCategoryClick(cat)}
              className={cn(
                "px-4 py-2 rounded-xl text-sm font-medium transition-all",
                activeCategory === cat 
                  ? "bg-primary text-primary-foreground shadow-md" 
                  : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </section>

      <section className="space-y-6">
        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary/50" />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {results.map((pod) => (
              <PodcastCard
                key={pod.podcast_id}
                podcast={pod}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default Explore;

import React, { useState, useEffect } from 'react';
import { podcastApi } from '../api/client';
import PodcastCard from '../components/PodcastCard';
import TasteOnboarding from '../components/TasteOnboarding';
import TasteProfileBadge from '../components/TasteProfileBadge';
import { Sparkles, Loader2, RefreshCw } from 'lucide-react';
import { cn } from '../lib/utils';

const Discover = () => {
  const [initialPodcasts, setInitialPodcasts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedPodcast, setSelectedPodcast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [recLoading, setRecLoading] = useState(false);
  const [interests, setInterests] = useState(null);
  const [showOnboarding, setShowOnboarding] = useState(false);

  useEffect(() => {
    const savedInterests = localStorage.getItem('podcast-mind-interests');
    if (savedInterests) {
      const parsed = JSON.parse(savedInterests);
      setInterests(parsed);
      fetchInitialPodcasts(parsed);
    } else {
      setShowOnboarding(true);
      fetchInitialPodcasts([]);
    }
  }, []);

  const fetchInitialPodcasts = async (userInterests = interests) => {
    setLoading(true);
    try {
      // Use recommend endpoint with interests for better personalization
      const data = await podcastApi.getRecommendations({
        query: userInterests?.length > 0 ? userInterests.join(' ') : 'interesting podcasts',
        limit: 12,
        preferred_categories: userInterests
      });
      setInitialPodcasts(data.results);
    } catch (error) {
      console.error("Failed to fetch initial podcasts:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleOnboardingComplete = (selected) => {
    setInterests(selected);
    setShowOnboarding(false);
    fetchInitialPodcasts(selected);
  };

  const handlePodcastClick = async (podcast) => {
    setSelectedPodcast(podcast);
    setRecLoading(true);
    
    // Dynamic Taste Profile Evolution
    updateTasteProfile(podcast);

    try {
      const data = await podcastApi.getRecommendations({
        podcast_id: podcast.podcast_id,
        limit: 6,
        preferred_categories: interests
      });
      setRecommendations(data.results);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setRecLoading(false);
    }
  };

  const updateTasteProfile = (podcast) => {
    if (!interests) return;
    
    const podCats = podcast.categories.split(',').map(c => c.trim());
    const newInterests = [...interests];
    let changed = false;

    podCats.forEach(cat => {
      if (!newInterests.includes(cat) && newInterests.length < 10) {
        newInterests.push(cat);
        changed = true;
      }
    });

    if (changed) {
      setInterests(newInterests);
      localStorage.setItem('podcast-mind-interests', JSON.stringify(newInterests));
    }
  };

  return (
    <div className="space-y-12">
      {showOnboarding && <TasteOnboarding onComplete={handleOnboardingComplete} />}

      <section className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-semibold text-primary">
            <Sparkles className="h-4 w-4" />
            <span>Intelligent Discovery</span>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">
            Find your next favorite show.
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl leading-relaxed">
            Select a podcast you like, and our hybrid engine will discover semantically and behaviorally related gems just for you.
          </p>
        </div>
        
        <TasteProfileBadge 
          interests={interests} 
          onEdit={() => setShowOnboarding(true)} 
        />
      </section>

      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold tracking-tight">Start Here</h2>
          <button 
            onClick={fetchInitialPodcasts}
            className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
          >
            <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary/50" />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {initialPodcasts.map((pod) => (
              <PodcastCard
                key={pod.podcast_id}
                podcast={pod}
                onClick={handlePodcastClick}
                isSelected={selectedPodcast?.podcast_id === pod.podcast_id}
              />
            ))}
          </div>
        )}
      </section>

      {(recLoading || recommendations.length > 0) && (
        <section className="space-y-8 pt-16 mt-8 border-t">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">For You</h2>
            <p className="text-muted-foreground">
              {selectedPodcast 
                ? `Because you showed interest in "${selectedPodcast.title}"`
                : "Personalized hybrid recommendations."}
            </p>
          </div>

          {recLoading ? (
            <div className="flex h-64 items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary/50" />
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {recommendations.map((pod) => (
                <PodcastCard
                  key={pod.podcast_id}
                  podcast={pod}
                  className="bg-primary/[0.02] border-primary/10"
                />
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  );
};

export default Discover;

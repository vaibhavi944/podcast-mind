import React, { useState } from 'react';
import { podcastApi } from '../api/client';
import SearchBar from '../components/SearchBar';
import PodcastCard from '../components/PodcastCard';
import { Loader2, Search as SearchIcon } from 'lucide-react';

const Search = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [interests, setInterests] = useState([]);

  React.useEffect(() => {
    const saved = localStorage.getItem('podcast-mind-interests');
    if (saved) setInterests(JSON.parse(saved));
  }, []);

  const handleSearch = async (query) => {
    setLoading(true);
    setHasSearched(true);
    try {
      const data = await podcastApi.searchPodcasts(query, 12, interests);
      setResults(data.results);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-10">
      <section className="space-y-4">
        <h1 className="text-3xl font-bold tracking-tight">Semantic Search</h1>
        <p className="text-muted-foreground max-w-2xl">
          Search using natural language. Try "podcasts about history and technology" or "modern philosophy for beginners".
        </p>
        <SearchBar onSearch={handleSearch} className="mt-6" />
      </section>

      <section className="space-y-6">
        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary/50" />
          </div>
        ) : results.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {results.map((pod) => (
              <PodcastCard
                key={pod.podcast_id}
                podcast={pod}
              />
            ))}
          </div>
        ) : hasSearched ? (
          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground space-y-2">
            <SearchIcon className="h-10 w-10 opacity-20" />
            <p>No podcasts found matching your query.</p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed rounded-2xl bg-muted/30 text-muted-foreground space-y-2">
            <SearchIcon className="h-8 w-8 opacity-20" />
            <p>Enter a query to explore the semantic space.</p>
          </div>
        )}
      </section>
    </div>
  );
};

export default Search;

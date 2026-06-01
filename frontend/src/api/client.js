import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const podcastApi = {
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  getRecommendations: async (params = {}) => {
    // FastAPI handles multiple query params with same name for lists
    // axios handles this by default for arrays in params
    const response = await apiClient.get('/recommend', { params });
    return response.data;
  },

  getSimilar: async (podcastId, limit = 5) => {
    const response = await apiClient.get('/similar', {
      params: { podcast_id: podcastId, limit },
    });
    return response.data;
  },

  searchPodcasts: async (query, limit = 10, preferredCategories = []) => {
    const response = await apiClient.get('/search', {
      params: { query, limit, preferred_categories: preferredCategories },
    });
    return response.data;
  },
};

export default apiClient;

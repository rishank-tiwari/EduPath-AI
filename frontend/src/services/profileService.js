import api from './api';

export const profileService = {
  getProfile: async (userId = 'demo_user_1') => {
    try {
      const response = await api.get(`/profile?user_id=${userId}`);
      return response.data;
    } catch (err) {
      if (err.status === 404 || err.code === 404) return null;
      throw err;
    }
  },

  saveProfile: async (payload) => {
    const response = await api.post('/profile', payload);
    return response.data;
  },

  analyzeProfile: async (payload) => {
    const response = await api.post('/profile/analyze', payload);
    return response.data;
  },
};

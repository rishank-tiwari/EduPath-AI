import api from './api';

export const adaptationService = {
  analyzeAndAdapt: async (userId, skillName = null, topic = null) => {
    const response = await api.post('/adaptation/analyze', {
      user_id: userId,
      skill_name: skillName,
      topic: topic,
    });
    return response.data;
  },

  getHistory: async (userId) => {
    const response = await api.get(`/adaptation/history?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },
};


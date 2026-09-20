import api from './api';

export const skillGapService = {
  analyzeSkillGaps: async (userId) => {
    const response = await api.post(`/skill-gaps/analyze?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getSkillGaps: async (userId) => {
    const response = await api.get(`/skill-gaps?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },
};


import api from './api';

export const planService = {
  generatePlan: async (userId) => {
    const response = await api.post(`/plans/generate?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getLatestPlan: async (userId) => {
    const response = await api.get(`/plans?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getPlanById: async (planId) => {
    const response = await api.get(`/plans/${encodeURIComponent(planId)}`);
    return response.data;
  },
};


import api from './api';

export const progressService = {
  recordEvent: async (userId, eventType, skillName, topic, metadata = {}) => {
    const response = await api.post('/progress/record', {
      user_id: userId,
      event_type: eventType,
      skill_name: skillName,
      topic: topic,
      metadata: metadata,
    });
    return response.data;
  },

  getUserProgress: async (userId) => {
    const response = await api.get(`/progress?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getSkillProgress: async (userId) => {
    const response = await api.get(`/progress/skills?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getHistory: async (userId) => {
    const response = await api.get(`/progress/history?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },
};


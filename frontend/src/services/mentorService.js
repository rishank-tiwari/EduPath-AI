import api from './api';

export const mentorService = {
  sendMessage: async (userId, message) => {
    const response = await api.post('/mentor/chat', {
      user_id: userId,
      message: message,
    });
    return response.data;
  },

  getContext: async (userId) => {
    const response = await api.get(`/mentor/context?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },
};

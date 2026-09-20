import api from './api';

export const healthService = {
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

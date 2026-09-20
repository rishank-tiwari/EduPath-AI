import api from './api';

export const resourceService = {
  recommendResources: async (taskId, skillName, difficulty = 'beginner', userId = null) => {
    const response = await api.post('/resources/recommend', {
      task_id: taskId,
      skill_name: skillName,
      difficulty: difficulty,
      user_id: userId,
    });
    return response.data;
  },
};


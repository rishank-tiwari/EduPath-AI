import api from './api';

export const practiceService = {
  generatePractice: async (userId, taskId, skillName, difficulty = 'beginner', practiceMode = 'general', moduleId = null) => {
    const response = await api.post('/practice/generate', {
      user_id: userId,
      task_id: taskId,
      module_id: moduleId,
      skill_name: skillName,
      difficulty: difficulty,
      practice_mode: practiceMode,
    });
    return response.data;
  },

  submitPractice: async (practiceId, userId, answers) => {
    const response = await api.post(`/practice/${encodeURIComponent(practiceId)}/submit`, {
      user_id: userId,
      answers: answers,
    });
    return response.data;
  },

  getHistory: async (userId) => {
    const response = await api.get(`/practice/history?user_id=${encodeURIComponent(userId)}`);
    return response.data;
  },

  getPracticeResult: async (identifier) => {
    const response = await api.get(`/practice/results/${encodeURIComponent(identifier)}`);
    return response.data;
  },
};


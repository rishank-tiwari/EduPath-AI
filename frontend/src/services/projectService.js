import api from './api';

export const projectService = {
  async generateProjects(userId = 'demo_user_1', targetRole = null, skillGaps = null) {
    const res = await api.post('/projects/generate', {
      user_id: userId,
      target_role: targetRole,
      skill_gaps: skillGaps,
    });
    return res.data;
  },

  async getRecommendedProjects(userId = 'demo_user_1') {
    const res = await api.get(`/projects?user_id=${encodeURIComponent(userId)}`);
    return res.data;
  },
};

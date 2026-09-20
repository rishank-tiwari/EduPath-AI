import api from './api';

export const documentService = {
  async uploadDocument(file, userId = 'demo_user_1', documentType = 'resume') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);
    formData.append('document_type', documentType);

    try {
      const res = await api.post('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return res.data;
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || "We couldn't read this file. Please try another PDF or DOCX.";
      throw new Error(detail);
    }
  },

  async analyzeText(contentText, userId = 'demo_user_1', documentType = 'portfolio', filename = 'portfolio_text.txt') {
    try {
      const res = await api.post('/documents/analyze', {
        user_id: userId,
        document_type: documentType,
        content_text: contentText,
        filename: filename,
      });
      return res.data;
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || "Unable to analyze document text. Please try again.";
      throw new Error(detail);
    }
  },

  async getProfileEvidence(userId = 'demo_user_1') {
    try {
      const res = await api.get(`/profile/evidence?user_id=${encodeURIComponent(userId)}`);
      return res.data;
    } catch (err) {
      return { evidence_cards: [], total_skills: 0 };
    }
  },
};

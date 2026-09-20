import api from './api';

export const authService = {
  login: async (usernameOrEmail, password) => {
    const response = await api.post('/auth/login', {
      username_or_email: usernameOrEmail,
      password: password,
    });
    return response.data;
  },

  register: async (username, email, password) => {
    const response = await api.post('/auth/register', {
      username: username,
      email: email,
      password: password,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

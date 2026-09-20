import axios from 'axios';
import { APP_CONFIG } from '../constants/config';

const api = axios.create({
  baseURL: APP_CONFIG.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor to attach JWT auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('edupath_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for structured error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorResponse = {
      message: error.response?.data?.error?.message || error.message || 'An unexpected error occurred.',
      status: error.response?.status || 500,
      code: error.response?.data?.error?.code || 'NETWORK_ERROR',
    };
    return Promise.reject(errorResponse);
  }
);

export default api;

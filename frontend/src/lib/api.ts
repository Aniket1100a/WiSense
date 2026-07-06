import axios from 'axios';

// Create a configured Axios instance
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://b5eb-152-59-63-46.ngrok-free.app',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // In a real app, inject auth token here
    const token = localStorage.getItem('wisense_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle global API errors (e.g., 401 Unauthorized -> redirect to login)
    if (error.response?.status === 401) {
      localStorage.removeItem('wisense_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

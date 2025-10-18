import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Adjust this to your backend's URL
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const register = (userData) => apiClient.post('/register/', userData);
export const login = (credentials) => apiClient.post('/token/', credentials);
export const refreshToken = (refresh) => apiClient.post('/token/refresh/', { refresh });

export const instagramLogin = (credentials) => apiClient.post('/instagram/login/', credentials);
export const getInstagramPosts = () => apiClient.get('/instagram/posts/');

export const getAutomationRules = (post_id) => apiClient.get(`/rules/?post_id=${post_id}`);
export const createAutomationRule = (ruleData) => apiClient.post('/rules/', ruleData);
export const updateAutomationRule = (ruleId, ruleData) => apiClient.put(`/rules/${ruleId}/`, ruleData);
export const deleteAutomationRule = (ruleId) => apiClient.delete(`/rules/${ruleId}/`);

export const getTaskLogs = (ruleId) => apiClient.get(`/logs/?rule_id=${ruleId}`);
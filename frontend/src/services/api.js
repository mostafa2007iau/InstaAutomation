import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // This will be proxied by Nginx in production
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
export const instagramSessionLogin = (sessionData) => apiClient.post('/instagram/login-session/', sessionData);
export const getInstagramAccounts = () => apiClient.get('/instagram-accounts/');
export const deleteInstagramAccount = (accountId) => apiClient.delete(`/instagram-accounts/${accountId}/`);
export const getInstagramPosts = (accountId) => apiClient.get(`/instagram/posts/?account_id=${accountId}`);

export const getAutomationRules = (post_id) => apiClient.get(`/rules/?post_id=${post_id}`);
export const createAutomationRule = (ruleData) => apiClient.post('/rules/', ruleData);
export const updateAutomationRule = (ruleId, ruleData) => apiClient.put(`/rules/${ruleId}/`, ruleData);
export const deleteAutomationRule = (ruleId) => apiClient.delete(`/rules/${ruleId}/`);

export const getTaskLogs = (ruleId) => apiClient.get(`/logs/?rule_id=${ruleId}`);
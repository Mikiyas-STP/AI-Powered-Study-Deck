import axios from 'axios';

const apiClient = axios.create({
  baseURL: "https://va7t3b6xb8thasp7c2kmjyko.grads.hosting.cyf.academy/api/v1",
});

// Automatically add JWT token to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 Unauthorized globally (e.g., redirect to login if token expires)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
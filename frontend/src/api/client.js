import axios from 'axios';

const apiClient = axios.create({
  baseURL:'https://pxu9curapm5d32qtvl8avfms.hosting.codeyourfuture.io/api/v1' ,
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
import axios from 'axios';
import Cookies from 'js-cookie';

// Create an axios instance with base URL and credentials configuration
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',  // Fallback to local URL if env variable isn't set
  withCredentials: true, // Ensure cookies are sent with requests
});

// Request interceptor to add Authorization and CSRF tokens to the headers
axiosInstance.interceptors.request.use((config) => {
  // Retrieve the access token from cookies
  const accessToken = Cookies.get('access_token');
  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`;
  }

  // Retrieve the CSRF token (if it's used in your setup)
  const csrfToken = Cookies.get('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }

  // Handle file upload case by setting the correct content-type
  if (config.headers['Content-Type'] === 'multipart/form-data') {
    config.headers['Content-Type'] = 'multipart/form-data';  // Necessary for file uploads
  }

  return config;
}, (error) => {
  return Promise.reject(error); // Return the error if the request fails
});

// Response interceptor to handle authorization errors (401)
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized request, redirect to login
      Cookies.remove('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

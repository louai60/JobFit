import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Utility to get the access token from cookies
const getTokenFromCookies = () => {
    const token = Cookies.get('access_token');
    if (!token) {
        throw new Error('Authentication token not found. Please log in.');
    }
    return token;
};

// Reusable axios configuration
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add Authorization header to each request
axiosInstance.interceptors.request.use(
    (config) => {
        const token = getTokenFromCookies();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Function to upload a resume
export const uploadResume = async (formData: FormData) => {
    try {
        const response = await axiosInstance.post('/resumes/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data', // Override default content type
            },
        });
        return response.data;
    } catch (error: any) {
        handleError(error);
    }
};

// Function to get resume details
export const getResumeDetails = async (resumeId: number) => {
    try {
        const response = await axiosInstance.get(`/resumes/${resumeId}/`);
        return response.data;
    } catch (error: any) {
        handleError(error);
    }
};

// Common error handler for API requests
const handleError = (error: any) => {
    if (error.response) {
        // Server responded with a status code outside 2xx
        const { status, data } = error.response;
        if (status === 401) {
            throw new Error('Unauthorized access. Please log in again.');
        } else if (status === 403) {
            throw new Error('Forbidden. You do not have permission to perform this action.');
        } else {
            throw new Error(data?.message || 'An error occurred while processing your request.');
        }
    } else if (error.request) {
        // No response received
        throw new Error('No response from the server. Please check your network connection.');
    } else {
        // Something else caused the error
        throw new Error(error.message || 'An unexpected error occurred.');
    }
};

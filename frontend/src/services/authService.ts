import axios from '../lib/axiosInstance';
import Cookies from 'js-cookie';

interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  user: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
  };
  access: string;
  refresh: string;
}

const authService = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await axios.post('/users/register/', data);
    console.log('Register response:', response.data);
    if (response.data.access) {
      // Set tokens in cookies
      Cookies.set('access_token', response.data.access, { expires: 7, secure: true, sameSite: 'Strict' });
      Cookies.set('refresh_token', response.data.refresh, { expires: 7, secure: true, sameSite: 'Strict' });
    } else {
      console.error('Access token not found in response:', response.data);
    }
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await axios.post('/users/login/', data);
    console.log('Login response:', response.data);
    if (response.data.access) {
      // Set tokens in cookies
      Cookies.set('access_token', response.data.access, { expires: 7, secure: true, sameSite: 'Strict' });
      Cookies.set('refresh_token', response.data.refresh, { expires: 7, secure: true, sameSite: 'Strict' });
    } else {
      console.error('Access token not found in response:', response.data);
    }
    return response.data;
  },

  logout: () => {
    // Remove cookies on logout
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
  },
};

export default authService;
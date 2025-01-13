import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginSuccess, loginFailure } from '../../features/auth/authSlice';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import authService from '../../services/authService';

export const LoginForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await authService.login({
        email: formData.email,
        password: formData.password,
      });

      dispatch(loginSuccess(response.user));
      toast.success('Successfully logged in!');
      navigate('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Login failed';
      dispatch(loginFailure(errorMessage));
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white text-black">
      <div className="w-[400px]">
        <div className="space-y-1 text-center mb-6">
          <h1 className="text-2xl font-bold">Sign In</h1>
          <p className="text-sm text-gray-500">Enter your email and password to sign in!</p>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Button className="w-full bg-gray-100 text-black border border-gray-300 hover:bg-gray-200">
              <span className="flex items-center justify-center">
                <img src="/path/to/google-icon.png" alt="Google" className="h-5 w-5 mr-2" />
                Sign In with Google
              </span>
            </Button>
            <div className="flex items-center justify-between my-4">
              <hr className="w-full border-gray-300" />
              <span className="px-2 text-sm text-gray-500">or</span>
              <hr className="w-full border-gray-300" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-700">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="mail@example.com"
                value={formData.email}
                onChange={handleChange}
                required
                disabled={isLoading}
                className="bg-white border border-gray-300"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-gray-700">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="Min. 8 characters"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={isLoading}
                className="bg-white border border-gray-300"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="remember"
                  checked={rememberMe}
                  onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                />
                <Label htmlFor="remember" className="text-sm text-gray-700">
                  Keep me logged in
                </Label>
              </div>
              <Link to="/forgot-password" className="text-sm text-[#422AFB] hover:underline">
                Forgot Password?
              </Link>
            </div>
          </div>
          
          <div className="flex flex-col space-y-4 mt-6">
            <Button 
              type="submit" 
              className="w-full bg-[#422AFB] hover:bg-[#3521c9] text-white"
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
            <p className="text-center text-sm text-gray-500">
              Not registered yet?{' '}
              <Link to="/register" className="text-[#422AFB] hover:underline">
                Create an account
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import { Dashboard } from './pages/Dashboard';
import { Toaster } from '@/components/ui/sonner';
import Home from './pages/Home';
import { ResumeDetails } from './components/ResumeDetails';
function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {/* Login Route (outside the Layout) */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        
        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/resume/:resumeId" element={<ResumeDetails />} />

      </Routes>
    </Router>
  );
}

export default App;


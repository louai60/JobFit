import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowRight, Star } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-[#0A0A0B] text-white">
      <header className="px-6 lg:px-8 h-20 flex items-center justify-between border-b border-gray-800">
        <Link className="flex items-center" to="/">
          <span className="text-xl font-bold bg-gradient-to-r from-[#422AFB] to-blue-500 bg-clip-text text-transparent">
            JobMatch AI
          </span>
        </Link>
        <nav className="hidden md:flex gap-8">
          <Link className="text-sm font-medium text-gray-300 hover:text-[#422AFB] transition-colors" to="/features">
            Features
          </Link>
          <Link className="text-sm font-medium text-gray-300 hover:text-[#422AFB] transition-colors" to="/jobs">
            Jobs
          </Link>
          <Link className="text-sm font-medium text-gray-300 hover:text-[#422AFB] transition-colors" to="/employers">
            For Employers
          </Link>
          <Link className="text-sm font-medium text-gray-300 hover:text-[#422AFB] transition-colors" to="/blog">
            Blog
          </Link>
          <Link className="text-sm font-medium text-gray-300 hover:text-[#422AFB] transition-colors" to="/pricing">
            Pricing
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <Link to="/login" className="text-sm font-medium text-gray-300 hover:text-[#422AFB]">
            Sign in
          </Link>
          <Button className="bg-[#422AFB] hover:bg-[#3521c9] text-white transition-colors">
            Upload Resume
          </Button>
        </div>
      </header>
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-20">
        <div className="inline-flex items-center gap-2 bg-[#422AFB]/10 text-[#422AFB] px-4 py-1.5 rounded-full mb-8 hover:bg-[#422AFB]/20 transition-colors cursor-pointer">
          <span className="text-sm font-medium">New: AI-Powered Skill Matching</span>
          <ArrowRight className="h-4 w-4" />
        </div>
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
            Your Perfect Job Match
            <br />
            Powered by AI
          </h1>
          <p className="text-lg md:text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            Upload your resume and let our AI match you with your ideal job opportunities. Get personalized job recommendations based on your skills, experience, and career goals.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Input 
              className="max-w-sm bg-gray-800/50 border-gray-700 text-white placeholder:text-gray-500"
              placeholder="Enter your email to get started"
              type="email"
            />
            <Button className="bg-[#422AFB] hover:bg-[#3521c9] text-white px-8 py-6 transition-colors">
              Start Job Search
            </Button>
          </div>
          <div className="flex flex-col items-center gap-4">
            <div className="flex -space-x-2">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="w-8 h-8 rounded-full bg-gray-800 border-2 border-[#0A0A0B]" />
              ))}
            </div>
            <div className="flex items-center gap-2">
              <div className="flex">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Star key={i} className="w-4 h-4 fill-[#422AFB] text-[#422AFB]" />
                ))}
              </div>
              <span className="text-sm text-gray-400">
                50,000+ successful job matches (4.9 of 5)
              </span>
            </div>
          </div>
        </div>
        <section className="mt-16 max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8">Success Stories</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-800 p-6 rounded-lg">
              <p className="text-lg text-gray-300">"JobMatch AI found me the perfect role in just 2 weeks. The AI accurately matched my skills with my dream company!"</p>
              <span className="block mt-4 text-sm text-gray-500">- Michael Chen, Software Engineer at Google</span>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <p className="text-lg text-gray-300">"The AI recommendations were spot-on. I got interviews at top companies that perfectly matched my experience."</p>
              <span className="block mt-4 text-sm text-gray-500">- Emily Rodriguez, Product Manager at Meta</span>
            </div>
          </div>
        </section>
      </main>
      <footer className="py-8 px-6 lg:px-8 border-t border-gray-800">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center">
          <p className="text-sm text-gray-500">
            © 2024 JobMatch AI. All rights reserved.
          </p>
          <nav className="flex gap-6 mt-4 sm:mt-0">
            <Link className="text-sm text-gray-500 hover:text-[#422AFB]" to="/terms">
              Terms
            </Link>
            <Link className="text-sm text-gray-500 hover:text-[#422AFB]" to="/privacy">
              Privacy
            </Link>
            <Link className="text-sm text-gray-500 hover:text-[#422AFB]" to="/contact">
              Contact
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  );
}
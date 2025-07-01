import React from 'react'
import { Link } from 'react-router-dom'
import { Video, Sparkles, Github, Zap } from 'lucide-react'

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-dark-500/90 backdrop-blur-xl border-b border-dark-600/40">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link 
            to="/" 
            className="flex items-center space-x-3 text-xl font-bold text-gray-200 group hover:scale-105 transition-transform duration-300"
          >
            <div className="relative">
              <div className="absolute inset-0 bg-button-gradient rounded-xl blur opacity-20 group-hover:opacity-30 transition-opacity duration-300"></div>
              <div className="relative bg-button-gradient p-2 rounded-xl shadow-glow-subtle">
                <Video className="w-6 h-6 text-white" />
              </div>
            </div>
            <span className="gradient-text">
              AI Video Studio
            </span>
            <div className="animate-float">
              <Sparkles className="w-5 h-5 text-amber-400/80" />
            </div>
          </Link>
          
          <nav className="flex items-center space-x-8">
            <Link 
              to="/" 
              className="relative group text-gray-300 hover:text-gray-100 transition-colors duration-300 font-medium"
            >
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4" />
                <span>Generate</span>
              </div>
              <div className="absolute -bottom-1 left-0 w-0 h-0.5 bg-button-gradient group-hover:w-full transition-all duration-300"></div>
            </Link>
            
            <a 
              href="https://github.com/your-repo" 
              target="_blank" 
              rel="noopener noreferrer"
              className="group flex items-center space-x-2 text-gray-300 hover:text-gray-100 transition-colors duration-300 font-medium"
            >
              <Github className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" />
              <span>GitHub</span>
            </a>
            
            <div className="hidden md:flex items-center space-x-2 bg-dark-600/50 backdrop-blur-sm px-3 py-2 rounded-full border border-dark-700/30">
              <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-gray-300">Online</span>
            </div>
          </nav>
        </div>
      </div>
    </header>
  )
} 
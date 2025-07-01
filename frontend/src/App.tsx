import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { VideoGenerator } from './components/VideoGenerator'
import { JobStatus } from './components/JobStatus'
import { Header } from './components/Header'

function App() {
  return (
    <Router 
      future={{ 
        v7_relativeSplatPath: true,
        v7_startTransition: true,
      }}
    >
      <div className="min-h-screen bg-deep-dark relative overflow-hidden">
        <Header />
        
        {/* Subtle animated background elements */}
        <div className="absolute inset-0 overflow-hidden -z-10">
          {/* Main deep dark overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-dark-300 via-dark-200 to-dark-100 opacity-95"></div>
          
          {/* Very subtle floating elements */}
          <div className="absolute top-32 left-16 w-48 h-48 bg-gradient-to-r from-sunset-800/10 to-amber-700/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute top-64 right-32 w-64 h-64 bg-gradient-to-r from-amber-800/8 to-sunset-700/8 rounded-full blur-3xl animate-float" style={{animationDelay: '3s'}}></div>
          <div className="absolute bottom-32 left-1/3 w-56 h-56 bg-gradient-to-r from-sunset-700/6 to-amber-600/6 rounded-full blur-3xl animate-float" style={{animationDelay: '6s'}}></div>
          
          {/* Minimal accent dots */}
          <div className="absolute top-1/4 right-1/4 w-2 h-2 bg-amber-600/40 rounded-full animate-pulse opacity-30"></div>
          <div className="absolute bottom-1/4 left-1/5 w-1 h-1 bg-sunset-600/30 rounded-full animate-pulse opacity-20" style={{animationDelay: '2s'}}></div>
          <div className="absolute top-3/4 right-1/5 w-1.5 h-1.5 bg-amber-700/35 rounded-full animate-pulse opacity-25" style={{animationDelay: '4s'}}></div>
          
          {/* Subtle texture overlay */}
          <div className="absolute inset-0 bg-gradient-radial from-transparent via-dark-300/10 to-dark-400/20"></div>
        </div>
        
        <main className="container mx-auto px-4 py-12 relative z-10">
          <Routes>
            <Route path="/" element={<VideoGenerator />} />
            <Route path="/job/:jobId" element={<JobStatus />} />
          </Routes>
        </main>
        
        {/* Footer with professional dark styling */}
        <footer className="bg-dark-500/60 backdrop-blur-lg border-t border-dark-600/40 mt-16 relative z-10">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center">
              <p className="mb-2 text-gray-400">
                Built with ❤️ using cutting-edge AI technology
              </p>
              <p className="text-sm text-gray-500">
                © 2024 AI Video Studio. All rights reserved.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App 
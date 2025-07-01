/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        accent: {
          50: '#fefce8',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        success: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
        },
        danger: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
        },
        // Enhanced deep dark colors
        dark: {
          50: '#0a0a0a',   // Even darker
          100: '#080808',  // Deeper black
          200: '#050505',  // Near black
          300: '#030303',  // Pure dark
          400: '#0d0d0d',  // Dark gray
          500: '#1a1a1a',  // Medium dark
          600: '#2d2d2d',  // Lighter dark
          700: '#404040',  // Gray dark
          800: '#525252',  // Medium gray
          900: '#666666',  // Light gray
        },
        // More muted sunset colors
        sunset: {
          50: '#fef7f0',   // Very light
          100: '#fdeee0',  // Light
          200: '#fad5b8',  // Muted light orange
          300: '#f7b98a',  // Soft orange
          400: '#f39c5c',  // Medium orange
          500: '#e67e22',  // Muted primary orange
          600: '#cc6600',  // Darker orange
          700: '#b85500',  // Deep orange
          800: '#a34400',  // Very deep orange
          900: '#8f3300',  // Darkest orange
        },
        // More subtle amber
        amber: {
          50: '#fefbf7',   // Very subtle
          100: '#fef6e7',  // Light amber
          200: '#fde8c8',  // Soft amber
          300: '#fbd7a8',  // Medium amber
          400: '#f9c178',  // Warm amber
          500: '#f7a834',  // Main amber (more muted)
          600: '#e8940f',  // Deeper amber
          700: '#d17f0a',  // Dark amber
          800: '#b86a08',  // Very dark amber
          900: '#9f5506',  // Darkest amber
        },
        // Professional grays for text
        gray: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        // More subtle and professional gradients
        'deep-dark': 'linear-gradient(135deg, #030303 0%, #0a0a0a 25%, #0d0d0d 50%, #1a1a1a 75%, #2d2d2d 100%)',
        'subtle-sunset': 'linear-gradient(135deg, #030303 0%, #080808 30%, #8f3300 70%, #b85500 85%, #cc6600 100%)',
        'professional-dark': 'linear-gradient(145deg, #030303 0%, #050505 20%, #0a0a0a 40%, #0d0d0d 60%, #1a1a1a 80%, #2d2d2d 100%)',
        'muted-amber': 'linear-gradient(135deg, #0a0a0a 0%, #0d0d0d 40%, #9f5506 80%, #d17f0a 100%)',
        'card-dark': 'linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #2d2d2d 100%)',
        'button-gradient': 'linear-gradient(135deg, #cc6600 0%, #e67e22 50%, #f7a834 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow-subtle': 'glowSubtle 3s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glowSubtle: {
          '0%': { boxShadow: '0 0 10px rgba(231, 126, 34, 0.1)' },
          '100%': { boxShadow: '0 0 20px rgba(247, 168, 52, 0.2)' },
        },
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.3), 0 10px 20px -2px rgba(0, 0, 0, 0.2)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3)',
        'strong': '0 10px 40px -10px rgba(0, 0, 0, 0.6), 0 2px 20px -2px rgba(0, 0, 0, 0.4)',
        'glow-subtle': '0 0 15px rgba(231, 126, 34, 0.15)',
        'glow-amber': '0 0 20px rgba(247, 168, 52, 0.2)',
        'inner-dark': 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [],
} 
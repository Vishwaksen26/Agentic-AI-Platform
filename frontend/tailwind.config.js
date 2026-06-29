/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Core backgrounds
        'af-bg': '#0a0a0f',
        'af-surface': '#111118',
        'af-surface-2': '#16161f',
        'af-card': '#1a1a28',
        'af-border': 'rgba(255, 255, 255, 0.06)',
        'af-border-strong': 'rgba(255, 255, 255, 0.12)',

        // Brand colors
        primary: {
          DEFAULT: '#6366f1',
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        secondary: {
          DEFAULT: '#8b5cf6',
          500: '#8b5cf6',
          600: '#7c3aed',
        },
        accent: {
          DEFAULT: '#06b6d4',
          500: '#06b6d4',
          600: '#0891b2',
        },

        // Status colors
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',

        // Text
        'text-primary': '#f4f4f8',
        'text-secondary': '#c0c0d0',
        'text-muted': '#a0a0b0',
        'text-disabled': '#606070',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'ui-sans-serif', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
      },
      animation: {
        shimmer: 'shimmer 2s linear infinite',
        float: 'float 3s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        glow: 'pulse-glow 2s ease-in-out infinite',
        'spin-slow': 'spin 3s linear infinite',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 8px rgba(99, 102, 241, 0.3)' },
          '50%': { opacity: '0.8', boxShadow: '0 0 24px rgba(99, 102, 241, 0.7)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
        'gradient-accent': 'linear-gradient(135deg, #06b6d4 0%, #6366f1 100%)',
        'gradient-success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        'gradient-card': 'linear-gradient(135deg, rgba(26,26,40,0.8) 0%, rgba(22,22,31,0.9) 100%)',
        'shimmer-gradient': 'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%)',
      },
      boxShadow: {
        'glow-primary': '0 0 20px rgba(99, 102, 241, 0.3)',
        'glow-accent': '0 0 20px rgba(6, 182, 212, 0.3)',
        'glow-success': '0 0 20px rgba(16, 185, 129, 0.3)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.4)',
        'card-hover': '0 8px 40px rgba(0, 0, 0, 0.6)',
        'modal': '0 25px 60px rgba(0, 0, 0, 0.8)',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};

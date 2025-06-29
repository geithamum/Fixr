/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      animation: {
        'wave-travel': 'wave-travel 12s linear infinite',
        'wave-travel-slow': 'wave-travel-slow 18s linear infinite',
        'wave-travel-reverse': 'wave-travel-reverse 15s linear infinite',
        'glow-pulse': 'glow-pulse 3s ease-in-out infinite',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(circle, var(--tw-gradient-stops))',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};
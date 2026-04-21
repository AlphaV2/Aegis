import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        aegis: {
          bg: '#0B0B0C',
          surface: '#111113',
          text: '#FFFFFF',
          accent: '#4F8CFF'
        }
      }
    }
  },
  plugins: []
}

export default config

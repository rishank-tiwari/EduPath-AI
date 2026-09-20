/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand Base Colors
        canvas: '#FFF8F0',
        surface: {
          DEFAULT: '#FFFFFF',
          soft: '#F7EFE6',
          dark: '#25252A',
          hover: '#FAF3EB',
        },
        content: {
          primary: '#25252A',
          secondary: '#505058',
          muted: '#8C8C94',
          inverse: '#FFF8F0',
        },
        border: {
          subtle: '#EBDED0',
          medium: '#DCCCC0',
        },
        // Primary Action Color
        orange: {
          DEFAULT: '#FF9F43',
          hover: '#E58E3C',
          light: '#FFF3E6',
          border: '#FFD0A1',
          text: '#C86E1B',
        },
        // Secondary AI / Learning Color
        skyblue: {
          DEFAULT: '#87CEEB',
          hover: '#72BDE0',
          light: '#F0F8FC',
          border: '#BCE3F5',
          text: '#2278A3',
        },
        // Dark Neutral
        dark: {
          DEFAULT: '#25252A',
          hover: '#34343A',
          card: '#1E1E22',
        },
        // Muted Green Success
        sage: {
          DEFAULT: '#71866F',
          light: '#F0F4EF',
          border: '#C3D0C1',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'subtle': '0 2px 6px rgba(37, 37, 42, 0.04)',
        'card': '0 4px 20px -2px rgba(37, 37, 42, 0.06), 0 2px 6px -1px rgba(37, 37, 42, 0.04)',
        'floating': '0 12px 32px -4px rgba(37, 37, 42, 0.12)',
      },
      borderRadius: {
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
      },
    },
  },
  plugins: [],
};

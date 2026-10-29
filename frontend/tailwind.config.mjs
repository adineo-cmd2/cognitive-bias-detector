/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        cream: '#f6f0e3',
        sand: '#ddcfb4',
        rust: '#9c2f24',
        charcoal: '#2a2520',
        panel: '#fffaf0',
        ink: '#2a2520',
        soft: '#756b5d',
        oxblood: '#9c2f24',
        teal: '#1f6f64',
        rule: '#ddcfb4',
        highlighter: '#e9c46a',
        white: '#fffaf0',
        black: '#2a2520',
      },
      fontFamily: {
        display: ["'Newsreader'", 'Georgia', 'serif'],
        body: ["'Karla'", 'system-ui', 'sans-serif'],
        mono: ["'IBM Plex Mono'", 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '2px',
        sm: '2px',
        md: '2px',
        lg: '2px',
        xl: '2px',
        '2xl': '2px',
        '3xl': '2px',
      },
    },
  },
  plugins: [],
};

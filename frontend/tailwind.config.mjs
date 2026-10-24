/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        cream: '#faf6ee',
        sand: '#e8dcc3',
        rust: '#b3402a',
        charcoal: '#292524',
      },
    },
  },
  plugins: [],
};

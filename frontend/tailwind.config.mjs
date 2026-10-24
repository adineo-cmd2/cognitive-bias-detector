/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        "cream": "#faf6ee",
        "sand": "#e8dcc3",
        "rust": "#b23a26",
        "charcoal": "#2b2622"
},
      fontFamily: {
        "display": [
                "'Fraunces'",
                "Georgia",
                "serif"
        ],
        "body": [
                "'Inter'",
                "system-ui",
                "sans-serif"
        ],
        "mono": [
                "'JetBrains Mono'",
                "ui-monospace",
                "monospace"
        ]
},
    },
  },
  plugins: [],
};

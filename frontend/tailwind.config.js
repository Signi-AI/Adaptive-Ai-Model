/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        learn: {
          bg: "var(--l-bg)",
          side: "var(--l-side)",
          panel: "var(--l-panel)",
          ink: "var(--l-ink)",
          muted: "var(--l-muted)",
          line: "var(--l-line)",
          hover: "var(--l-hover)",
          user: "var(--l-user)",
          accent: "var(--l-accent)",
        },
      },
      fontFamily: {
        display: ["Newsreader", "Georgia", "serif"],
        body: ["Figtree", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
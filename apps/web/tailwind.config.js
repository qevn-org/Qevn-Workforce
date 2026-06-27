/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: "#030303",      // Deep slate pitch black background
        foreground: "#f4f4f5",      // High contrast text
        card: "#09090b",            // Dark zinc cards
        border: "#1e1e24",          // Fine zinc borders
        primary: {
          DEFAULT: "#8b5cf6",       // Deep neon purple
          hover: "#7c3aed"
        },
        secondary: {
          DEFAULT: "#18181b",       // Medium zinc
          accent: "#c084fc"         // Lavender accent highlight
        },
        success: "#10b981",         // Emerald green
        warning: "#f59e0b",         // Amber warning
        danger: "#ef4444"           // High contrast red
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"]
      }
    },
  },
  plugins: [],
}

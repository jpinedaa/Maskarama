import { type Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";

export default {
  content: ["./src/**/*.tsx"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-geist-sans)", ...fontFamily.sans],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#1E3E5C",
          secondary: "#9ca3af",
          accent: "#352623",
          neutral: "#1f2937",
          "base-100": "#f3f4f6",
          info: "#60a5fa",
          success: "#34d399",
          warning: "#fbbf24",
          error: "#f87171",
          'bistre': "#352623",
          'parchment': "#F5EDD6",
        },
      },
    ],
  },
} satisfies Config;

/** @type {import('tailwindcss').Config} */
export default {
  // Dark mode class එකෙන් පාලනය වේ
  darkMode: 'class',

  // Tailwind අදාළ විය යුතු ෆයිල්ස්
  content: [
    './src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}',
  ],

  theme: {
    extend: {},
  },

  // මෙන්න අලුත් වෙනස්කම: Typography Plugin එක එකතු කළා
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
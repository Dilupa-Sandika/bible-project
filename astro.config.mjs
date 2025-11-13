import { defineConfig } from 'astro/config';

// Tailwind integration එක import කරගන්නවා
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  // Tailwind integration එක Astro වලට add කරනවා
  integrations: [tailwind()]
});
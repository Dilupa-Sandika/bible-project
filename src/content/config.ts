import { defineCollection, z } from 'astro:content';

const articlesCollection = defineCollection({
  type: 'content', // Markdown files
  schema: z.object({
    title: z.string(),
    description: z.string(), // SEO Description
    pubDate: z.date(),
    author: z.string().default('ScriptureHub Team'),
    image: z.string().optional(), // Cover image
    tags: z.array(z.string()), // Keywords for SEO
  }),
});

export const collections = {
  'articles': articlesCollection,
};
import { defineCollection, z } from 'astro:content';

// 1. Articles Collection (කලින් තිබුන එක)
const articlesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string().default('ScriptureHub Team'),
    image: z.string().optional(),
    tags: z.array(z.string()),
  }),
});

// 2. Family (Printables) Collection (අලුත් එක)
const familyCollection = defineCollection({
  type: 'content', 
  schema: z.object({
    title: z.string(),
    type: z.enum(['book', 'card', 'backdrop']), // Category types
    filter_tag: z.string(), // kids, adults, birthday, etc.
    gallery: z.array(z.string()), // List of images
    file_link: z.string(), // PDF or Etsy link
    is_premium: z.boolean(),
    price: z.string().optional(),
    short_desc: z.string(), // For the card view
  }),
});

export const collections = {
  'articles': articlesCollection,
  'family': familyCollection, // Register the new collection
};
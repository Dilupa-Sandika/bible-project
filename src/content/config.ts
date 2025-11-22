import { defineCollection, z } from 'astro:content';

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

// Family Collection (UPDATED)
const familyCollection = defineCollection({
  type: 'content', 
  schema: z.object({
    // --- Language Fields ---
    title_en: z.string(), 
    title_es: z.string(), // New
    short_desc_en: z.string(), 
    short_desc_es: z.string(), // New
    print_label_en: z.string().optional(),
    print_label_es: z.string().optional(), // New
    // -----------------------

    type: z.enum(['book', 'card', 'backdrop']),
    filter_tag: z.string(),
    gallery: z.array(z.string()),
    digital_link: z.string(),
    print_link: z.string().optional(),
    is_premium: z.boolean(),
    price: z.string().optional(),
  }),
});

export const collections = {
  'articles': articlesCollection,
  'family': familyCollection,
};
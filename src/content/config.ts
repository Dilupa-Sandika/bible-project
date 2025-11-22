import { defineCollection, z } from 'astro:content';

// 1. Articles Collection
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

// 2. Family Collection (Updated Schema)
const familyCollection = defineCollection({
  type: 'content', 
  schema: z.object({
    title: z.string(),
    type: z.enum(['book', 'card', 'backdrop']),
    filter_tag: z.string(), // kids, adults, baptism, etc.
    gallery: z.array(z.string()),
    
    // --- LINK CONFIGURATION ---
    // Gumroad Link එක (Free or Paid Digital) - අනිවාර්යයි
    digital_link: z.string(), 
    
    // Physical Link එක (Amazon/Etsy/Zazzle) - නැති වෙන්න පුලුවන් (Optional)
    print_link: z.string().optional(),
    print_label: z.string().optional(), // Button එකේ නම (උදා: Buy on Amazon)
    // --------------------------
    
    is_premium: z.boolean(), // True නම් "Premium" ටැග් එක වැටෙනවා
    price: z.string().optional(),
    short_desc: z.string(),
  }),
});

export const collections = {
  'articles': articlesCollection,
  'family': familyCollection,
};
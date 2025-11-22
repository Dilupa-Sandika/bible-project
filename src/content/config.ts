import { defineCollection, z } from 'astro:content';

// 1. Articles Collection (UPDATED)
const articlesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    // පරණ title/description වෙනුවට අලුත් භාෂා ෆීල්ඩ්ස්
    title_en: z.string(),
    title_es: z.string(),
    description_en: z.string(),
    description_es: z.string(),
    
    pubDate: z.date(),
    author: z.string().default('ScriptureHub Team'),
    image: z.string().optional(),
    tags: z.array(z.string()),
  }),
});

// 2. Family Collection (කලින් හදපු එක - වෙනසක් නෑ)
const familyCollection = defineCollection({
  type: 'content', 
  schema: z.object({
    title_en: z.string(),
    title_es: z.string(),
    type: z.enum(['book', 'card', 'backdrop']),
    filter_tag: z.string(),
    gallery: z.array(z.string()),
    digital_link: z.string(),
    print_link: z.string().optional(),
    print_label_en: z.string().optional(),
    print_label_es: z.string().optional(),
    is_premium: z.boolean(),
    price: z.string().optional(),
    short_desc_en: z.string(),
    short_desc_es: z.string(),
  }),
});

export const collections = {
  'articles': articlesCollection,
  'family': familyCollection,
};
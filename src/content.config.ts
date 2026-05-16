import { defineCollection, reference, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.date(),
    updatedAt: z.date().optional(),
    category: z.enum(['release', 'research', 'tutorial', 'news']),
    tags: z.array(z.string()).default([]),
    authors: z.array(reference('authors')).min(1),
    cover: image().optional(),
    draft: z.boolean().default(false),
  })
});

const DOC_SECTIONS = ['getting-started', 'system', 'guides', 'signers', 'specs', 'security'] as const;

const docs = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    section: z.enum(DOC_SECTIONS),
    order: z.number().default(100),
    updatedAt: z.date(),
    status: z.enum(['stable', 'draft', 'research']).default('stable'),
  })
});

const FAMILY_KEYS = ['raspberry-qr', 'esp32-qr', 'esp32-usb', 'smartcard', 'custom-wallet'] as const;
const CAPABILITY_STATUS = [
  'target', 'present', 'absent', 'disabled', 'partial', 'planned', 'research',
  'forbidden', 'not_applicable', 'implemented', 'disabled_until_gates_pass',
  'required', 'optional'
] as const;

const signers = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/signers' }),
  schema: z.object({
    family: z.enum(FAMILY_KEYS),
    displayName: z.string(),
    tagline: z.string(),
    repo: z.string().url(),
    productGoal: z.string(),
    maturity: z.enum(['research', 'prototype', 'alpha', 'beta']),
    capabilities: z.array(z.object({
      id: z.string(),
      target: z.enum(CAPABILITY_STATUS),
      current: z.enum(CAPABILITY_STATUS),
      contractId: z.string().optional(),
      notes: z.string().optional()
    })),
    requiredText: z.array(z.string()).default([]),
    order: z.number()
  })
});

const authors = defineCollection({
  loader: file('src/content/authors/_authors.json'),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    bio: z.string().optional(),
    links: z.object({
      github: z.string().url().optional(),
      nostr: z.string().optional(),
      web: z.string().url().optional(),
    }).default({})
  })
});

export const collections = { blog, docs, signers, authors };

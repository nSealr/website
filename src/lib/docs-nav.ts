import { getCollection } from 'astro:content';

export const DOC_SECTION_ORDER = ['getting-started', 'system', 'guides', 'signers', 'specs', 'security'] as const;
export const DOC_SECTION_LABEL: Record<typeof DOC_SECTION_ORDER[number], string> = {
  'getting-started': 'Getting Started',
  'system': 'System',
  'guides': 'Guides',
  'signers': 'Signers',
  'specs': 'Specs & Reference',
  'security': 'Security'
};

export async function getDocsNav() {
  const docs = await getCollection('docs');
  const signers = await getCollection('signers');

  const fromDocs = docs.map(d => ({
    id: d.id,
    href: `/docs/${d.id}/`,
    title: d.data.title,
    section: d.data.section,
    order: d.data.order
  }));

  const fromSigners = signers.map(s => ({
    id: `signers/${s.id}`,
    href: `/docs/signers/${s.id}/`,
    title: s.data.displayName,
    section: 'signers' as const,
    order: s.data.order
  }));

  const all = [...fromDocs, ...fromSigners];

  return DOC_SECTION_ORDER.map(section => ({
    section,
    label: DOC_SECTION_LABEL[section],
    items: all.filter(e => e.section === section).sort((a, b) => a.order - b.order)
  }));
}

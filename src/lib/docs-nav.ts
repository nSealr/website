import { getCollection } from 'astro:content';
export async function getDocsNav() {
  const docs = await getCollection('docs');
  return [{ section: 'guide', label: 'Guide', items: docs
    .sort((a,b) => a.data.order - b.data.order)
    .map(d => ({ id:d.id, href:`/docs/${d.id}/`, title:d.data.title })) }];
}

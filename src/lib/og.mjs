import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { readFileSync } from 'node:fs';

const monoFont = readFileSync('scripts/og-fonts/JetBrainsMono-Bold.ttf');

export async function renderOgPng(input) {
  const { title, eyebrow, category } = input;
  const tree = {
    type: 'div',
    props: {
      style: {
        width: '1200px', height: '630px',
        background: '#07060d', color: '#dcd4f0',
        padding: '64px', display: 'flex', flexDirection: 'column',
        justifyContent: 'space-between', fontFamily: 'JetBrainsMono'
      },
      children: [
        {
          type: 'div',
          props: {
            style: { display: 'flex', alignItems: 'center', gap: '14px' },
            children: [
              {
                type: 'div',
                props: {
                  style: {
                    width: '34px', height: '34px',
                    border: '1px solid #2d2440', borderRadius: '6px',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: '#b388ff', fontSize: '14px'
                  },
                  children: 'ns'
                }
              },
              {
                type: 'div',
                props: { style: { fontSize: '22px', color: '#ffffff' }, children: 'nsealr' }
              }
            ]
          }
        },
        {
          type: 'div',
          props: {
            style: { display: 'flex', flexDirection: 'column', gap: '18px' },
            children: [
              {
                type: 'div',
                props: {
                  style: { color: '#b388ff', fontSize: '20px' },
                  children: eyebrow ?? '// nsealr · blog'
                }
              },
              {
                type: 'div',
                props: {
                  style: { color: '#ffffff', fontSize: '72px', lineHeight: 1, letterSpacing: '-1.5px' },
                  children: title
                }
              },
              category
                ? {
                    type: 'div',
                    props: { style: { color: '#7be0a8', fontSize: '20px' }, children: `# ${category}` }
                  }
                : null
            ].filter(Boolean)
          }
        },
        {
          type: 'div',
          props: {
            style: { color: '#7e7393', fontSize: '18px' },
            children: 'open-source · non-profit · pre-production'
          }
        }
      ]
    }
  };

  const svg = await satori(tree, {
    width: 1200,
    height: 630,
    fonts: [
      { name: 'JetBrainsMono', data: monoFont, style: 'normal', weight: 700 }
    ]
  });
  const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } });
  return Buffer.from(resvg.render().asPng());
}

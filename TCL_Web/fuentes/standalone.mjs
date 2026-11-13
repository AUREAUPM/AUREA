import { readFile, writeFile, mkdir } from 'node:fs/promises';

// Empaqueta la compilación de Vite para publicarla desde el editor de GitHub.
const dist = new URL('./dist/', import.meta.url);
let html = await readFile(new URL('index.html', dist), 'utf8');
const script = html.match(/<script[^>]*src="([^"]+)"[^>]*><\/script>/);
const stylesheet = html.match(/<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/);
if (!script || !stylesheet) throw new Error('Faltan los recursos de Vite: ejecuta primero la compilación.');
const js = await readFile(new URL(script[1], dist), 'utf8');
const css = await readFile(new URL(stylesheet[1], dist), 'utf8');
html = html.replace(script[0], '').replace(stylesheet[0], () => `<style>${css}</style>`)
  .replace('</body>', () => `<script type="module">${js.replace(/<\/script/gi, '<\\/script')}</script></body>`);
const output = new URL('../', import.meta.url);
await mkdir(output, { recursive: true });
await writeFile(new URL('index.html', output), html);
console.log('Versión independiente preparada en TCL_Web/index.html');

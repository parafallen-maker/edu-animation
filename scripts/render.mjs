#!/usr/bin/env node
// Motion Canvas renderer - launches Chrome via Puppeteer and triggers built-in render
// Usage: node render.mjs <project-dir> <chrome-path>
import puppeteer from 'puppeteer-core';
import { createServer } from 'vite';
import fs from 'fs';
import path from 'path';

const dir = process.argv[2];
const chrome = process.argv[3];

if (!dir || !chrome) {
  console.error('Usage: node render.mjs <project-dir> <chrome-path>');
  process.exit(1);
}

const server = await createServer({
  root: dir,
  configFile: path.join(dir, 'vite.config.ts'),
  server: { fs: { allow: ['/', '/tmp', dir] } },
});

const PORT = 3470 + Math.floor(Math.random() * 100);
await server.listen(PORT);
console.log(`[RENDER] Dev server on port ${PORT}`);

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: false,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--autoplay-policy=no-user-gesture-required',
    '--window-size=1920,1080',
  ],
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });

page.on('console', (msg) => {
  const t = msg.text();
  if (/render|error|saved/i.test(t)) console.log('[MC]', t);
});

await page.goto(`http://localhost:${PORT}`, {
  waitUntil: 'networkidle0',
  timeout: 60000,
});
await new Promise((r) => setTimeout(r, 8000));

// Click the render button in the Motion Canvas UI
await page.evaluate(() => {
  for (const btn of document.querySelectorAll('button, [role=button]')) {
    const text = btn.textContent?.trim().toLowerCase() ?? '';
    if (text.includes('render') || text.includes('渲染')) {
      btn.click();
      return;
    }
  }
});

console.log('[RENDER] Waiting for completion (max 3 min)...');
await new Promise((r) => setTimeout(r, 180000));

const outputDir = path.join(dir, 'output');
let mp4 = '';
if (fs.existsSync(outputDir)) {
  const files = fs.readdirSync(outputDir).filter((f) => f.endsWith('.mp4'));
  if (files.length > 0) {
    mp4 = path.join(outputDir, files[0]);
    const stat = fs.statSync(mp4);
    console.log(`[OK] ${mp4} (${(stat.size / 1024 / 1024).toFixed(1)} MB)`);
  }
}

await server.close();
await browser.close();

if (!mp4) {
  console.error('[WARN] No MP4 in output/. Check Motion Canvas UI for errors.');
  process.exit(1);
}

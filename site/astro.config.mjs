import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://carspecfix.com',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  compressHTML: true,
});

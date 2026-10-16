import { PREVIEW } from '../lib/gate.mjs';
export function GET() {
  return new Response(PREVIEW ? 'User-agent: *\nDisallow: /\n' : 'User-agent: *\nAllow: /\n\nSitemap: https://carspecfix.com/sitemap.xml\n');
}

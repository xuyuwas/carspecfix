import { liveVehicles, liveIssues, liveHubs, vehicleUrl, issueUrl, isIndexable, SITE, PREVIEW , liveIssueHub } from '../lib/gate.mjs';
import { images } from '../lib/images.mjs';
// lastmod = real data/content change date. Only live pages. image:image only for signed photos (never silhouettes).
const STATIC_DATE = '2026-10-15';
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
export function GET() {
  const urls: [string, string, string?][] = [];
  if (!PREVIEW) {
    const v = liveVehicles.filter(isIndexable), i = liveIssues.filter(isIndexable);
    const all = [...v.map(x => x.dataUpdated), ...i.map(x => x.dataUpdated), STATIC_DATE].sort().at(-1)!;
    urls.push(['/', all]); if (liveIssueHub('code')) urls.push(['/codes/', all]); if (liveIssueHub('symptom')) urls.push(['/symptoms/', all]);
    for (const p of ['/about/', '/sources/', '/authors/editor/', '/contact/', '/privacy/']) urls.push([p, STATIC_DATE]);
    for (const h of liveHubs()) urls.push([`/specs/${h.makeSlug}/${h.modelSlug}/`, h.years.map(y => y.dataUpdated).sort().at(-1)]);
    v.forEach(x => urls.push([vehicleUrl(x), x.dataUpdated, x.slug])); i.forEach(x => urls.push([issueUrl(x), x.dataUpdated]));
  }
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n${urls.map(([u, d, slug]) => {
    const img = slug && images[slug];
    return `<url><loc>${SITE}${u}</loc><lastmod>${d}</lastmod>${img ? `<image:image><image:loc>${SITE}${esc(img.set.at(-1).url)}</image:loc></image:image>` : ''}</url>`;
  }).join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}

// Parse grade-A oil capacity strings into per-engine figures (same rules as the year-page oil card).
import { usOnly } from './title.mjs';

const noRefs = t => String(t || '').replace(/\s*\[[A-Z0-9]{6,}[^\]]*\]/g, '').trim();

/** Short display label for an engine/variant name. */
export function shortOilLabel(label) {
  if (!label) return null;
  if (/hybrid/i.test(label)) return 'Hybrid';
  if (/hatchback/i.test(label)) return 'Hatchback';
  const v = label.match(/\b(V[68])\b/i);
  if (v) return v[1].toUpperCase();
  const d = label.match(/([\d.]+L)(?:\s+(turbo))?/i);
  if (d) return d[2] ? `${d[1]} turbo` : d[1];
  return label.split(/\s+/)[0];
}

/**
 * Split a capacity value into per-engine { label, w, wo }.
 * Unlabeled "with; without" pairs (RAV4 style) are merged into one engine.
 */
export function parseOilCapacity(value) {
  const text = usOnly(noRefs(value));
  const segs = text.split(/\s*;\s*|\s+\|\s+/).map(x => x.trim()).filter(Boolean)
    .reduce((a, x) => {
      if (/^with-filter not stated$/i.test(x) && a.length) a[a.length - 1] += '; with-filter not stated';
      else a.push(x);
      return a;
    }, []);
  const parsed = segs.map(x => {
    // Drop viscosity/grade trailers so they never become a fake segment or label
    const cleaned = x
      .replace(/,?\s*SAE\b.*$/i, '')
      .replace(/,?\s*GF-[\w.]+\s*$/i, '')
      .trim();
    if (/^not yet verified$/i.test(cleaned)) return { label: null, w: null, wo: null, unverified: true, raw: cleaned };
    const label = cleaned.includes(':') ? cleaned.slice(0, cleaned.indexOf(':')).trim() : null;
    const body = (label ? cleaned.slice(cleaned.indexOf(':') + 1) : cleaned).trim();
    if (/^not yet verified$/i.test(body)) return { label, w: null, wo: null, unverified: true, raw: cleaned };
    const w = (body.match(/([\d.]+) (?:US )?qt\b(?:\s*\([^)]*\))?\s*(?:with|incl\.?|including) filter/i) || [])[1];
    const wo = (body.match(/([\d.]+) (?:US )?qt\b(?:\s*\([^)]*\))?\s*(?:change\s+)?without/i) || [])[1];
    return { label, w: w ? +w : null, wo: wo ? +wo : null, unverified: false, raw: cleaned };
  });
  const merged = [];
  for (let i = 0; i < parsed.length; i++) {
    const cur = parsed[i], next = parsed[i + 1];
    if (!cur.label && !cur.unverified && cur.w && !cur.wo && next && !next.label && !next.unverified && next.wo && !next.w) {
      merged.push({ label: null, w: cur.w, wo: next.wo, unverified: false, raw: `${cur.raw}; ${next.raw}` });
      i++;
    } else {
      merged.push(cur);
    }
  }
  return merged;
}

/**
 * Hub table cell: short without-filter amounts only, e.g. "2.5L 4.4 qt · V6 5.6 qt · Hybrid 4.4 qt".
 * Engines with no without-filter figure show "Not yet verified" (never fall back to with-filter).
 */
export function oilHubShort(value) {
  const engines = parseOilCapacity(value);
  if (!engines.length) return null;
  const parts = engines.map(o => {
    const lb = shortOilLabel(o.label);
    if (o.wo != null) return lb ? `${lb} ${o.wo} qt` : `${o.wo} qt`;
    return lb ? `${lb} Not yet verified` : 'Not yet verified';
  });
  return parts.join(' · ');
}

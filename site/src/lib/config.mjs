// Configuration model for the "find your numbers" selector.
//
// The reason this exists: a year page used to answer one question — "what is the
// tyre pressure for a 2024 RAV4?" — with a range (33–36 psi) and no way for the
// reader to see which value was theirs. The manual does not say "XLE = 35 psi";
// it says "vehicles with 17-inch wheels type A", and the type letters are not
// mapped to trims anywhere in the document. So the page has to let the reader
// narrow by what they can actually read off their own car (tyre size, engine,
// drive) and must say "your build is one of these" when the document leaves it
// open. It must never print a single number the source does not support.
import { parseOilCapacity } from './oil.mjs';

const DRIVE_SHORT = {
  'Front-Wheel Drive': 'FWD',
  'All-Wheel Drive': 'AWD',
  'Rear-Wheel Drive': 'RWD',
  'Part-time 4-Wheel Drive': '4WD',
  '4-Wheel Drive': '4WD',
};
export const driveShort = d => DRIVE_SHORT[d] || (/4-Wheel|AWD|4WD/.test(d || '') ? '4WD' : d || '—');

const isHybridText = t => /hybrid|prime|plug-in|\bphev\b/i.test(t || '');
const dispOf = t => { const m = String(t || '').match(/(\d\.\d)\s*L\b/i); return m ? +m[1] : null; };
const engineLabel = (l, cyl, hybrid) => `${l ? `${l}L ` : ''}${cyl ? `${cyl}-cylinder ` : ''}${hybrid ? 'hybrid' : 'gasoline'}`.trim();

// Engines come from the EPA records (that is where the reader's own car is
// described: displacement, cylinders, hybrid or not). A manual oil entry is
// attached only when its displacement and hybrid flag agree; when the page has a
// single engine on both sides they are paired regardless, because there is
// nothing else the figure could belong to.
export function configModel(v) {
  const s = v.specs || {};
  const ev = v.powertrain === 'ev';
  const sourced = f => f && f.value && f.source && f.sourceGrade === 'A';
  const oil = !ev && sourced(s.oilCapacity) ? parseOilCapacity(s.oilCapacity.value) : [];
  const oilMeta = oil.map(o => ({
    label: o.label || '',
    disp: dispOf(o.label || o.raw),
    hybrid: isHybridText(o.label || '') || isHybridText(s.oilCapacity.appliesTo),
    w: o.unverified ? null : o.w,
    wo: o.unverified ? null : o.wo,
    unverified: !!o.unverified,
    raw: o.raw,
  }));

  const fe = (v.fuelEconomy || []).filter(c => c.mpgComb);
  const engines = [];
  for (const c of fe) {
    const hybrid = c.powertrain === 'hybrid' || isHybridText(c.model) || isHybridText(c.option);
    const key = `${c.engineL ?? dispOf(c.option) ?? '?'}|${c.cyl ?? '?'}|${hybrid ? 'h' : 'g'}`;
    if (!engines.some(e => e.key === key)) engines.push({ key, disp: c.engineL ?? dispOf(c.option), cyl: c.cyl ?? null, hybrid });
  }
  if (!engines.length && oilMeta.length) engines.push({ key: 'oil', disp: oilMeta[0].disp, cyl: null, hybrid: oilMeta[0].hybrid });

  const tires = (v.tires?.rows || []).filter(t => t.source && t.sourceGrade === 'A' && t.tireSize);

  const out = engines.map((e, i) => {
    const own = fe.filter(c => {
      const hybrid = c.powertrain === 'hybrid' || isHybridText(c.model) || isHybridText(c.option);
      return (c.engineL ?? dispOf(c.option)) === e.disp && hybrid === e.hybrid;
    });
    // Oil pairing: displacement + hybrid flag, falling back to position only when
    // both sides have exactly one candidate.
    let oi = oilMeta.findIndex(o => o.disp === e.disp && o.hybrid === e.hybrid);
    if (oi < 0 && oilMeta.length === 1 && engines.length === 1) oi = 0;
    const o = oi >= 0 ? oilMeta[oi] : null;
    return {
      id: `e${i}`,
      label: engineLabel(e.disp, e.cyl, e.hybrid),
      hybrid: e.hybrid,
      oil: o ? { w: o.w, wo: o.wo, unverified: o.unverified, raw: o.raw } : null,
      drives: [...new Set(own.map(c => c.drive))].map(d => ({ id: d, label: driveShort(d) })),
      mpg: own.map(c => ({ drive: c.drive, city: c.mpgCity, hwy: c.mpgHwy, comb: c.mpgComb, option: c.option, model: c.model, feId: c.feId })),
    };
  });

  const sizes = [];
  for (const t of tires) {
    const id = t.tireSize;
    let g = sizes.find(x => x.id === id);
    if (!g) sizes.push((g = { id, size: id, wheel: t.wheel || (id.match(/R(\d\d)/) || [])[1] || null, psi: [] }));
    if (t.frontPsi && t.rearPsi) {
      const k = `${t.frontPsi}/${t.rearPsi}`;
      if (!g.psi.some(p => p.k === k)) g.psi.push({ k, front: t.frontPsi, rear: t.rearPsi, types: [] });
      const row = g.psi.find(p => p.k === k);
      const m = String(t.config || '').match(/type\s+([A-Z])/i);
      if (m && !row.types.includes(m[1].toUpperCase())) row.types.push(m[1].toUpperCase());
    }
  }
  sizes.forEach(g => g.psi.sort((a, b) => a.front - b.front || a.rear - b.rear));

  const psiAll = [...new Set(sizes.flatMap(g => g.psi.flatMap(p => [p.front, p.rear])))].sort((a, b) => a - b);
  return {
    ev,
    engines: out,
    sizes: sizes.sort((a, b) => (a.wheel || 0) - (b.wheel || 0) || a.id.localeCompare(b.id)),
    oilScope: s.oilCapacity?.appliesTo || null,
    oilUnverified: s.oilCapacity?.unverifiedNote || null,
    viscosity: sourced(s.oilViscosity) ? s.oilViscosity.value : null,
    placard: !!(v.tires?.psiOnLabel && v.tires.psiOnLabel.source),
    psiRange: psiAll.length ? [psiAll[0], psiAll[psiAll.length - 1]] : null,
    // "Same pressure for every configuration" is only true when every printed
    // row agrees; anything else is a range the reader has to narrow themselves.
    singlePsi: psiAll.length === 1 ? psiAll[0] : null,
  };
}

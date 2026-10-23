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

// "non-hybrid" contains "hybrid". Without the negative look-ahead the 2024 CR-V's
// "1.5L turbo (non-hybrid)" oil row was classified as a hybrid figure and matched no
// engine at all, so the capacity vanished from the selector entirely.
const isHybridText = t => /hybrid|prime|plug-in|\bphev\b/i.test(t || '') && !/non-?hybrid/i.test(t || '');
const dispOf = t => { const m = String(t || '').match(/(\d\.\d)\s*L\b/i); return m ? +m[1] : null; };
const engineLabel = (l, cyl, hybrid) => `${l ? `${l}L ` : ''}${cyl ? `${cyl}-cylinder ` : ''}${hybrid ? 'hybrid' : 'gasoline'}`.trim();
// Some manuals split the oil capacity by drivetrain rather than by engine — the 2022
// Equinox prints 4.2 qt for FWD and 5.3 qt for AWD under the same 1.5L engine. Collapsing
// those into "the 1.5L figure" silently dropped the AWD number, so the drive token is
// read out of the manual's own label and kept as a separate selectable option.
const DRIVE_TOKEN = t => {
  const s = String(t || '');
  if (/\bAWD\b|All-Wheel/i.test(s)) return 'AWD';
  if (/\bFWD\b|Front-Wheel/i.test(s)) return 'FWD';
  if (/\bRWD\b|Rear-Wheel/i.test(s)) return 'RWD';
  if (/\b4WD\b|4-Wheel|4x4/i.test(s)) return '4WD';
  return null;
};

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
    drive: DRIVE_TOKEN(o.label || ''),
    // Per-entry only. The page-level `appliesTo` string ("2.5L gasoline and 2.5L
    // hybrid engines") names both powertrains at once, so reading the hybrid flag out
    // of it marked every row as hybrid and left the 2020 RAV4 with no oil figure.
    hybrid: isHybridText(o.label || o.raw),
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
    let cands = oilMeta.filter(o => o.disp === e.disp && o.hybrid === e.hybrid);
    if (!cands.length && oilMeta.length === 1 && engines.length === 1) cands = oilMeta.slice();
    const pick = o => ({ w: o.w, wo: o.wo, unverified: o.unverified, raw: o.raw, drive: o.drive, label: o.label });
    // One candidate -> a single figure for this engine. Several -> keep every one of
    // them, tagged with the drive the manual named, so the drive selector can narrow.
    // They are never merged into one number: the difference is the answer.
    const oilOne = cands.length === 1 ? pick(cands[0]) : null;
    const oilList = cands.length > 1 ? cands.map(pick) : null;
    // A drivetrain the manual names for oil but EPA does not list still has to be
    // selectable, or the AWD figure becomes unreachable.
    const oilDrives = [...new Set((oilList || []).map(o => o.drive).filter(Boolean))];
    const drives = [...new Set([...own.map(c => c.drive), ...oilDrives.map(d => ({ AWD: 'All-Wheel Drive', FWD: 'Front-Wheel Drive', RWD: 'Rear-Wheel Drive', '4WD': 'Part-time 4-Wheel Drive' })[d]).filter(Boolean)])];
    return {
      id: `e${i}`,
      label: engineLabel(e.disp, e.cyl, e.hybrid),
      hybrid: e.hybrid,
      oil: oilOne,
      oilList,
      drives: drives.map(d => ({ id: d, label: driveShort(d) })),
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

// What the selector can actually narrow — and therefore what the quick answer is
// allowed to print. The rule is a count of *distinct printed figures*, not a count of
// engines or wheel sizes: a year with two engines but one published oil capacity has
// an unambiguous oil answer, and hiding it behind a selector would be theatre. A year
// that prints 33 / 35 / 36 psi across unnamed wheel packages has no single answer, so
// the selector owns the number and the quick answer must not repeat a range as if it
// were one. `placard` (`psiOnLabel`) is a third state: no figure is printed anywhere,
// so the only honest answer is the door-jamb label and that is not "narrowing".
export function configNarrows(m) {
  // Only a row the manual actually prints a number for counts. Two "not yet checked"
  // rows are one answer ("not published"), not two options to choose between.
  const hasFig = o => o && !o.unverified && (o.w != null || o.wo != null);
  const oilOptions = m.engines.reduce((n, e) => n + (e.oilList ? e.oilList.filter(hasFig).length : hasFig(e.oil) ? 1 : 0), 0);
  const psiOptions = new Set(m.sizes.flatMap(s => s.psi.map(p => p.k))).size;
  return {
    oil: oilOptions > 1,
    psi: psiOptions > 1,
    any: oilOptions > 1 || psiOptions > 1,
    oilOptions,
    psiOptions,
  };
}

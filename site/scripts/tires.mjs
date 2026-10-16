// Parse legacy free-text tire size / pressure into rows:
// { wheel, config, tireSize, frontPsi, rearPsi, page, source, sourceGrade }
// Conservative: anything not matched is dropped (renders as "Not yet verified"), never guessed.
const CFG = /^(?:(\d\.\d ?[LT](?: turbo)?)|([A-Z][\w-]*(?: [A-Z][\w-]*)*)):?\s*/;
const wheelOf = s => (s.match(/(\d{2})(?:"|-in|″)/) || [])[1] || null;
export function parseTires(sizeRaw, psiRaw, source, grade, page = null) {
  const rows = [];
  const key = (c, w) => `${c || ''}|${w || ''}`;
  const get = (c, w) => { let r = rows.find(x => key(x.config, x.wheel) === key(c, w)); if (!r) { r = { wheel: w, config: c, tireSize: null, frontPsi: null, rearPsi: null, page, source, sourceGrade: grade }; rows.push(r); } return r; };
  let cfg = null;
  for (const seg of (sizeRaw || '').split(/;\s*/)) {
    const m = seg.match(/^(\d\.\d ?[LT]|2WD|4WD|AWD)(?: turbo)?:\s*/); if (m) cfg = m[1].replace(' ', '');
    for (const t of seg.matchAll(/(P?\d{3}\/\d{2}R\d{2}(?: \d{2,3}[A-Z])?)((?: or P?\d{3}\/\d{2}R\d{2}(?: \d{2,3}[A-Z])?)?)\s*(?:\(([^)]*)\))?(?:\s*(\d{2}) ?F? ?\/ ?(\d{2}) ?R?(?: psi)?)?/g)) {
      t[1] = t[1] + (t[2] || ''); // keep manual's "A or B" alternatives verbatim
      if (/spare/i.test(t[3] || '') || /spare\s*$/i.test(seg.slice(0, t.index))) continue;
      const w = wheelOf(t[3] || '') || (t[1].match(/R(\d{2})/) || [])[1];
      const extra = (t[3] || '').replace(/\d{2}(?:"|-in)\s*,?\s*/, '').trim();
      const row = get(extra && !/^type/i.test(extra) ? (cfg ? cfg + ' ' : '') + extra : cfg, w);
      if (row.tireSize && row.tireSize !== t[1]) { const r2 = { ...row, tireSize: t[1], frontPsi: null, rearPsi: null }; rows.push(r2); if (t[4]) { r2.frontPsi = +t[4]; r2.rearPsi = +t[5]; } continue; }
      row.tireSize = t[1]; if (t[4]) { row.frontPsi = +t[4]; row.rearPsi = +t[5]; }
    }
  }
  cfg = null;
  for (const seg of (psiRaw || '').split(/;\s*/)) {
    const m = seg.match(/^(\d\.\d ?[LT])\b\s*/); if (m) cfg = m[1].replace(' ', '');
    const w = wheelOf(seg); if (!w) continue;
    let f, r; const fr = seg.match(/(\d{2}) ?F ?\/ ?(\d{2}) ?R/), same = seg.match(/(\d{2})\/(\d{2}) psi/);
    if (fr) [f, r] = [fr[1], fr[2]]; else if (same) [f, r] = [same[1], same[2]]; else continue;
    const target = rows.find(x => x.wheel === w && (x.config === cfg || (!cfg && rows.filter(y => y.wheel === w).length === 1))) || get(cfg, w);
    target.frontPsi = +f; target.rearPsi = +r;
  }
  return rows.sort((a, b) => (a.config || '').localeCompare(b.config || '') || a.wheel - b.wheel);
}

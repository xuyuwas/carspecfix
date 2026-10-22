// Action plan: turn sourced advice into "if this, do that".
//
// The safety content used to arrive as one paragraph mixing a steady warning
// light, a flashing one and a brand-specific instruction. A reader in a car park
// could not tell which sentence was about their car. Every source item may now
// carry a `verdict`:
//
//   "verdict": { "condition": "Steady check-engine light", "level": "soon",
//                "action": "Keep driving; book service" }
//
// level: stop > now > soon > ok. The item keeps its own document, page and URL,
// so the table and the evidence list cite the same thing — there is no second
// copy of the source that could drift.
export const LEVELS = ['stop', 'now', 'soon', 'ok'];
export const LEVEL_LABEL = {
  stop: 'Stop driving',
  now: 'Inspect now',
  soon: 'Service soon',
  ok: 'Keep driving',
};

// Same scope wording as the brand-only block: "vehicle-specific: Toyota Camry 2022"
// -> "Toyota only".
export const scopeTag = g => (g.appliesTo || '')
  .replace(/^vehicle-specific:\s*/i, '')
  .replace(/^(\w+).*?(\d{4}).*$/, (m, a, y) => (/Toyota/.test(m) ? 'Toyota only' : `${y} ${a} only`))
  .trim();

const forThisIssue = (x, i) => !x.onlyCodes || (!!i.code && x.onlyCodes.includes(i.code));

export function actionPlan(i) {
  const items = [...(i.urgency || []), ...(i.guidance || [])]
    .filter(x => x && x.verdict && x.verdict.condition && x.verdict.action && x.url && x.sourceGrade === 'A' && forThisIssue(x, i));
  const seen = new Set();
  return items
    .map(x => ({
      condition: x.verdict.condition,
      action: x.verdict.action,
      level: LEVELS.includes(x.verdict.level) ? x.verdict.level : 'soon',
      detail: x.verdict.detail || null,
      scope: x.allBrands ? null : scopeTag(x),
      general: !!x.allBrands,
      item: x,
    }))
    .filter(p => { const k = p.condition.toLowerCase(); if (seen.has(k)) return false; seen.add(k); return true; })
    // All-vehicle rows first, then severity. Sorting on severity alone put a
    // Toyota-only instruction above the federal one on a generic code page, which
    // reads as if every reader should follow it.
    .sort((a, b) => (Number(b.general) - Number(a.general)) || LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level));
}

export const hasActionPlan = i => actionPlan(i).length > 0;

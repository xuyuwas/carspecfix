// R-M2 v2: title <= 60 visible chars. Degrade: drop " | CarSpecFix", then trailing module words. Never ellipsis.
export const MAX_TITLE = 60;
const join = (head, mods, sep) => mods.length ? head + sep + mods.join(', ').replace(/, ([^,]*)$/, mods.length > 1 ? ' & $1' : ', $1') : head;
export function fitTitle(head, modules = [], { sep = ': ', brand = true } = {}) {
  const mods = [...modules];
  let t = join(head, mods, sep) + (brand ? ' | CarSpecFix' : '');
  if (t.length <= MAX_TITLE) return t;
  t = join(head, mods, sep); 
  while (t.length > MAX_TITLE && mods.length) { mods.pop(); t = join(head, mods, sep); }
  return t;
}
// US units only: drop metric conversions like " (3.5 L)" from source text for display
export const usOnly = s => String(s).replace(/\s*\(\d+(?:\.\d+)? ?L\)/g, '').replace(/\s*\/\s*\d+(?:\.\d+)? ?(?:kPa|bar)\b/g, '');

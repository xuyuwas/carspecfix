// Per-page numbered source list ([n] footnotes -> #ref-n)
export function makeRefs() {
  const list = [];
  const ref = (key, label, url) => { let i = list.findIndex(r => r.key === key); if (i < 0) { list.push({ key, label, url }); i = list.length - 1; } return i + 1; };
  return { list, ref };
}
export const SEGMENT = { rav4: 'suv', 'cr-v': 'suv', equinox: 'suv', 'model-y': 'suv', 'f-150': 'truck', 'silverado-1500': 'truck', tacoma: 'truck' };

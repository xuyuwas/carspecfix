// Evidence tiers. The methodology page used to claim that every value comes from a
// manufacturer or government original — true for specifications, but the brake
// symptom page also cites a consumer-education article, and calling that "an
// official source" alongside a manual page number is the kind of blur that costs a
// site its credibility. Three tiers, labelled wherever a citation appears:
//
//   oem      — the manufacturer's own document (owner's manual, service bulletin,
//              support page). Required for any specification number.
//   gov      — a U.S. federal record (NHTSA, EPA, DOE/BLS statistics).
//   guidance — recognised consumer-safety education (Car Care Council). May support
//              "what to do" wording, never a specification value.
import { sources } from './gate.mjs';

const GOV = ['u.s. epa', 'epa', 'nhtsa', 'u.s. dot', 'dot', 'doe', 'u.s. doe', 'bls', 'u.s. bureau of labor statistics', 'fueleconomy.gov', 'nhtsa odi'];
const OEM = ['toyota', 'lexus', 'gm', 'general motors', 'chevrolet', 'buick', 'gmc', 'cadillac', 'honda', 'acura', 'ford', 'lincoln', 'tesla', 'hyundai', 'kia', 'nissan', 'infiniti', 'subaru', 'mazda', 'volkswagen', 'audi', 'bmw', 'mercedes-benz', 'stellantis', 'ram', 'jeep', 'dodge', 'chrysler', 'volvo', 'mitsubishi', 'porsche', 'jaguar', 'land rover', 'mini', 'genesis'];

export const TIER_LABEL = {
  oem: 'Manufacturer document',
  gov: 'Government record',
  guidance: 'General safety guidance',
};
export const TIER_SHORT = { oem: 'Manufacturer', gov: 'Government', guidance: 'Safety guidance' };

export function tierOf(item) {
  if (!item) return 'guidance';
  const maker = String(item.maker || '').toLowerCase().trim();
  if (GOV.includes(maker)) return 'gov';
  if (OEM.includes(maker)) return 'oem';
  // Fall back to the registered source record when one exists for this URL.
  const rec = Object.values(sources).find(s => s.url && item.url && s.url === item.url);
  if (rec?.type === 'government' || rec?.grade === 'A' && /nhtsa|epa|fueleconomy/i.test(rec.url || '')) return 'gov';
  if (rec?.maker && OEM.includes(String(rec.maker).toLowerCase())) return 'oem';
  return 'guidance';
}

/** May this item be quoted as the basis of a specification number? */
export const specGrade = item => ['oem', 'gov'].includes(tierOf(item));

import fs from 'node:fs'; import path from 'node:path';
export const images = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'data/images.json'), 'utf8'));
// ImageObject only for signed photos (never for silhouettes); caption names the pictured vehicle.
// Google's image metadata wants creator / creditText / copyrightNotice / license / acquireLicensePage:
// a missing copyrightNotice triggers the non-critical "Missing field copyrightNotice" report.
// All photos are CC BY-SA, so the photographer keeps the copyright — the notice names them, and
// the licence terms live in `license` + `creditText`.
export function imageObject(slug, SITE) {
  const i = images[slug]; if (!i) return null;
  return { '@type': 'ImageObject', contentUrl: SITE + i.set.at(-1).url, width: i.width, height: i.height, caption: i.shownOverride ? i.shownOverride.replace(/^Shown: /, '') : i.shown,
    creator: { '@type': 'Person', name: i.author }, copyrightNotice: `© ${i.author}`,
    license: i.licenseUrl, creditText: `Photo: ${i.author} / ${i.license}${i.cropped ? ', cropped' : ''}`, acquireLicensePage: i.sourceUrl };
}

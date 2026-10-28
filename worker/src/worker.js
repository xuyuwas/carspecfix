/**
 * carspecfix feedback relay
 *
 * POST /api/feedback
 *   {type, page, field?, value?, text, email?, date, hp?}
 *
 * Receives every on-site message form — the "ask about this page" box that sits at
 * the bottom of every page, the data-error report on /contact/, and the one-tap
 * "was this page helpful" vote — and emails it to the site owner through the
 * Cloudflare `send_email` binding.
 *
 * Delivery is two-step on purpose. hello@carspecfix.com is the address the site
 * publishes; Cloudflare only lets a binding send to a verified destination or to an
 * address on the same zone that Email Routing forwards. If the primary address is
 * ever rejected the message is re-sent to the verified fallback instead of being
 * dropped — a form that silently loses submissions is worse than one that lands in
 * the second inbox, and the subject line says which path was taken.
 *
 * The client-side contract (payload shape) lives in site/public/feedback.js.
 * Nothing is stored: no database, no IP, no user agent, no cookies.
 */

const TO = 'hello@carspecfix.com'; // address published on the site
const TO_FALLBACK = 'xuyu8813@gmail.com'; // verified Email Routing destination
const FROM = { email: 'noreply@carspecfix.com', name: 'CarSpecFix' };

const ALLOWED_ORIGIN = 'https://carspecfix.com';
const MAX_BODY_BYTES = 8192;
const TYPES = new Set(['report', 'feedback', 'feedback-detail', 'contact']);

// Control characters that have no business in a plain-text email body.
const CTRL = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g;
// A reply address has to survive being put in a header: one @, no spaces, no CR/LF.
const EMAIL_RE = /^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(\.[A-Za-z0-9-]{1,63})+$/;

const CORS = {
  'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

function reply(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...CORS,
    },
  });
}

function clip(value, max) {
  if (typeof value !== 'string') return '';
  return value.replace(CTRL, '').trim().slice(0, max);
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }
    if (request.method !== 'POST') {
      return reply({ ok: false, error: 'method_not_allowed' }, 405);
    }

    const contentType = request.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
      return reply({ ok: false, error: 'unsupported_media_type' }, 415);
    }

    const raw = await request.text();
    if (raw.length > MAX_BODY_BYTES) {
      return reply({ ok: false, error: 'payload_too_large' }, 413);
    }

    let payload;
    try {
      payload = JSON.parse(raw);
    } catch {
      return reply({ ok: false, error: 'bad_json' }, 400);
    }
    if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
      return reply({ ok: false, error: 'bad_json' }, 400);
    }

    // Honeypot: a real visitor never fills a field that is hidden from view.
    // Accept silently so bots cannot tell they were filtered.
    if (clip(payload.hp, 100)) {
      return reply({ ok: true }, 200);
    }

    const type = clip(payload.type, 32) || 'feedback';
    if (!TYPES.has(type)) {
      return reply({ ok: false, error: 'bad_type' }, 400);
    }

    const page = clip(payload.page, 200);
    const field = clip(payload.field, 200);
    const value = clip(payload.value, 32);
    const text = clip(payload.text, 2000);
    const date = clip(payload.date, 32) || new Date().toISOString().slice(0, 10);
    const rawEmail = clip(payload.email, 254);
    // An unusable address is dropped rather than rejected: the question is still
    // worth an email, it just arrives without a way to answer it.
    const replyTo = EMAIL_RE.test(rawEmail) ? rawEmail : '';

    if (!text && !value) {
      return reply({ ok: false, error: 'empty' }, 400);
    }

    const lines = [
      `type:    ${type}`,
      `page:    ${page || '-'}`,
      field ? `field:   ${field}` : null,
      value ? `value:   ${value}` : null,
      replyTo ? `reply to: ${replyTo}` : 'reply to: (not given)',
      `date:    ${date}`,
      '',
      text || '(no detail provided)',
      '',
      '---',
      `received: ${new Date().toISOString()}`,
    ].filter((line) => line !== null);

    const subject = `[CarSpecFix] ${type === 'contact' ? 'question' : type}${page ? ` — ${page}` : ''}`.slice(0, 900);
    const message = { from: FROM, subject, text: lines.join('\n') };
    if (replyTo) message.replyTo = replyTo;

    try {
      await env.EMAIL.send({ ...message, to: TO });
      return reply({ ok: true }, 200);
    } catch (primaryError) {
      const code = (primaryError && primaryError.code) || 'E_UNKNOWN';
      console.error('send_email primary failed', code, (primaryError && primaryError.message) || primaryError);
      try {
        await env.EMAIL.send({ ...message, to: TO_FALLBACK, subject: `${subject} [via fallback]` });
        return reply({ ok: true, delivered: 'fallback' }, 200);
      } catch (fallbackError) {
        const fallbackCode = (fallbackError && fallbackError.code) || 'E_UNKNOWN';
        console.error('send_email fallback failed', fallbackCode, (fallbackError && fallbackError.message) || fallbackError);
        return reply({ ok: false, error: 'send_failed', code, fallback: fallbackCode }, 502);
      }
    }
  },
};

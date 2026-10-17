/**
 * carspecfix feedback relay
 *
 * POST /api/feedback   {type, page, field, value, text, date, hp?}
 *
 * Receives the CarSpecFix on-site feedback / data-error report form and emails it
 * to a verified Cloudflare Email Routing destination using the `send_email` binding.
 * Sends to verified destinations are free on any plan and do not require the
 * sending domain to be onboarded to Email Service.
 *
 * The client-side contract (payload shape) lives in site/public/feedback.js.
 * Deliberately stores no personal data: no IP, no user agent, no cookies.
 */

const TO = 'xuyu8813@gmail.com';
const FROM = { email: 'noreply@carspecfix.com', name: 'CarSpecFix' };

const ALLOWED_ORIGIN = 'https://carspecfix.com';
const MAX_BODY_BYTES = 8192;
const TYPES = new Set(['report', 'feedback', 'feedback-detail']);

// Control characters that have no business in a plain-text email body.
const CTRL = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g;

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

    if (!text && !value) {
      return reply({ ok: false, error: 'empty' }, 400);
    }

    const body = [
      `type:    ${type}`,
      `page:    ${page || '-'}`,
      field ? `field:   ${field}` : null,
      value ? `value:   ${value}` : null,
      `date:    ${date}`,
      '',
      text || '(no detail provided)',
      '',
      '---',
      `received: ${new Date().toISOString()}`,
    ].filter((line) => line !== null).join('\n');

    const subject = `[CarSpecFix] ${type}${page ? ` — ${page}` : ''}`.slice(0, 900);

    try {
      await env.EMAIL.send({ to: TO, from: FROM, subject, text: body });
    } catch (error) {
      const code = (error && error.code) || 'E_UNKNOWN';
      console.error('send_email failed', code, (error && error.message) || error);
      return reply({ ok: false, error: 'send_failed', code }, 502);
    }

    return reply({ ok: true }, 200);
  },
};

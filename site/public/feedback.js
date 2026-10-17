// Feedback / data-error reporting.
// Backend: the Cloudflare Worker at /api/feedback (see worker/src/worker.js), which
// relays each submission to email via Cloudflare Email Routing's send_email binding.
// Override the endpoint by setting window.CSF_FEEDBACK_ENDPOINT before this script loads.
// Payload carries no personal data: {type, page, field, value, text, date, hp}.
window.CSF = window.CSF || {};
CSF.endpoint = window.CSF_FEEDBACK_ENDPOINT || '/api/feedback';
CSF.send = function (payload, scope) {
  payload.date = new Date().toISOString().slice(0, 10);
  // Honeypot: a visually hidden field a real visitor never fills. Accept silently
  // so automated submitters cannot tell they were filtered.
  var hp = scope && scope.querySelector ? scope.querySelector('input[name="hp"]') : null;
  if (hp && hp.value) return Promise.resolve(true);
  return fetch(CSF.endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    keepalive: true
  }).then(function (r) { return r.ok; }, function () { return false; });
};

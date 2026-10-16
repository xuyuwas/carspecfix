// Pluggable feedback/report storage. No backend yet (队长 to choose the tool).
// To activate: set window.CSF_FEEDBACK_ENDPOINT = 'https://…' before this script, or replace send().
// Payload has no personal data: {type, page, value, text, field, date}.
window.CSF = window.CSF || {};
CSF.send = function (payload) {
  payload.date = new Date().toISOString().slice(0, 10);
  if (window.CSF_FEEDBACK_ENDPOINT) {
    return fetch(window.CSF_FEEDBACK_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), keepalive: true })
      .then(function (r) { return r.ok; }, function () { return false; });
  }
  // stub: keep a local queue so the flow can be tested end-to-end without a service
  try { var q = JSON.parse(localStorage.getItem('csf_queue') || '[]'); q.push(payload); localStorage.setItem('csf_queue', JSON.stringify(q)); } catch (e) {}
  return Promise.resolve(true);
};

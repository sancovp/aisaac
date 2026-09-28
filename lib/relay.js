/* lib/relay.js — THE RELAY's shared half (00-SITE-CANON § HOSTING AND AUTOMATIONS).
 *
 * The relay pushes; it never stores and never sends mail. Everything after the push
 * (the contact, the pipeline, the texts, the commission) is the destination's own work.
 *
 * Destinations are a list in the Worker's secret env var DESTINATIONS (JSON), never in
 * a page:
 *   [{"name": "ghl", "url": "https://…", "events": ["lead", "payment", "refund"],
 *     "headers": {"Authorization": "Bearer …"},      // optional: a destination's key
 *     "rename": {"email": "contact_email"}}]         // optional: its field names
 * Adding a destination edits that list; no page and no code changes.
 */

export function destinations(env) {
  try {
    const list = JSON.parse(env.DESTINATIONS || '[]');
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function renamed(payload, rename) {
  if (!rename) return payload;
  const out = {};
  for (const [k, v] of Object.entries(payload)) out[rename[k] || k] = v;
  return out;
}

/* Push one event to every destination that takes it. Returns one line per destination;
 * a destination that fails never stops the others. */
export async function push(env, event, payload) {
  const body = { event, ...payload };
  const targets = destinations(env).filter((d) => !d.events || d.events.includes(event));
  const results = await Promise.allSettled(
    targets.map((d) =>
      fetch(d.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(d.headers || {}) },
        body: JSON.stringify(renamed(body, d.rename)),
      }).then((r) => ({ name: d.name, status: r.status, ok: r.ok })),
    ),
  );
  return results.map((r, i) =>
    r.status === 'fulfilled' ? r.value : { name: targets[i].name, ok: false, error: String(r.reason) },
  );
}

export const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } });

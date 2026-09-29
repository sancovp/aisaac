/* lib/ghl.js — THE RELAY WRITES THE CRM (docs/ghl-integration.md).
 *
 * GoHighLevel's API cannot create workflows, but it can write everything the lead and the payment need:
 * the contact, the deal, the task. So the relay does that work itself — in code, testable, one place —
 * instead of a hand-built workflow. It needs the Worker secret GHL_TOKEN (a Private Integration Token for
 * the sub-account); with none set every function here answers { skipped: true } and the relay behaves as
 * it did before.
 *
 * The IDs below are not secrets: they name the sub-account "Ribcage Solutions" and the things built in it
 * (the pipeline "TWI Sales", the eight contact fields). A rebuilt pipeline or field means new IDs here.
 */

const API = 'https://services.leadconnectorhq.com';
const LOCATION = 'QiGqa8pmvzip0ldiPkyM';
const OWNER = 'ElpCQkbVSIbhtgGjIOo2'; // Isaac — the user tasks are assigned to
const PIPELINE = 'EXCU2SBIw94qJ9TSt2Og'; // TWI Sales
const STAGE_NEW = 'b93c44b7-6e99-4359-8f10-4c8cffc715a6';
const STAGE_WON = 'b9ce73a3-7c9e-4141-bbc2-daf472de234c';

// contact custom fields (Settings → Custom Fields, folder "Additional Info")
const FIELD = {
  partner_code: '6feUvSN7Tc6R769gv6zv',
  form: '7RdAV8SXoZ0mohzgkvRI',
  revenue: '7GZn20lOrDajMgYPmKYn',
  focus: 'QwC0PPCX2RLl4zyapOl8',
  page: 'L8RyP6TEniQ7YzY1DbAU',
  consent_record: 'sn0pwaZz0zAXxzI0yCpW',
  consent_version: 'TnXbH0UdHAGTStajYgp3',
  last_payment_id: 'VoISY5Sj2M4QlYa1J5X4',
};

const COMMISSION = 1000; // dollars, flat, per referred client's first payment (00-SITE-CANON § REFERRAL PARTNERS)
const TAG_COMMISSION = 'partner-commission-task';

export class GhlError extends Error {}

async function call(env, method, path, body) {
  const res = await fetch(API + path, {
    method,
    headers: {
      Authorization: `Bearer ${env.GHL_TOKEN}`,
      Version: '2021-07-28',
      Accept: 'application/json',
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 200) }; }
  if (!res.ok) throw new GhlError(`${method} ${path} → ${res.status} ${text.slice(0, 200)}`);
  return data;
}

const enabled = (env) => Boolean(env.GHL_TOKEN);
const fieldList = (values) =>
  Object.entries(values)
    .filter(([, v]) => v !== undefined && v !== null && String(v) !== '')
    .map(([k, v]) => ({ id: FIELD[k], value: String(v) }));

function splitName(name) {
  const parts = String(name || '').trim().split(/\s+/).filter(Boolean);
  return { firstName: parts[0] || '', lastName: parts.slice(1).join(' ') };
}

const inMinutes = (m) => new Date(Date.now() + m * 60000).toISOString();

async function task(env, contactId, title, body, dueInMinutes) {
  return call(env, 'POST', `/contacts/${contactId}/tasks`, {
    title, body, dueDate: inMinutes(dueInMinutes), completed: false, assignedTo: OWNER,
  });
}

async function upsertContact(env, c) {
  const body = { locationId: LOCATION, ...c };
  try {
    return (await call(env, 'POST', '/contacts/upsert', body)).contact;
  } catch (e) {
    // a phone GHL cannot read must not lose the lead
    if (body.phone) return (await call(env, 'POST', '/contacts/upsert', { ...body, phone: undefined })).contact;
    throw e;
  }
}

/* THE LEAD — a form was submitted: the contact, the deal at "New lead", the note, the call task. */
export async function recordLead(env, p) {
  if (!enabled(env)) return { skipped: true };
  const { firstName, lastName } = splitName(p.name);
  const contact = await upsertContact(env, {
    email: p.email, firstName, lastName, phone: p.phone || undefined, companyName: p.company || undefined,
    source: 'website', tags: ['website lead', `form:${p.form || 'unknown'}`],
    customFields: fieldList({
      partner_code: p.ref, form: p.form, revenue: p.revenue, focus: p.focus, page: p.page,
      consent_record: p.consent_record, consent_version: p.consent_version,
    }),
  });
  const contactId = contact.id;
  const title = [firstName || p.email, p.company].filter(Boolean).join(' — ');

  const lines = [
    `Form: ${p.form || 'unknown'}`, p.company && `Company: ${p.company}`, p.revenue && `Revenue: ${p.revenue}`,
    p.focus && `Focus: ${p.focus}`, p.phone && `Phone: ${p.phone}`, p.ref && `Partner: ${p.ref}`,
    p.description && `\n${p.description}`,
  ].filter(Boolean);
  await Promise.all([
    call(env, 'POST', '/opportunities/upsert', {
      locationId: LOCATION, pipelineId: PIPELINE, contactId, name: title, status: 'open', pipelineStageId: STAGE_NEW,
      source: p.ref ? `partner:${p.ref}` : 'website',
    }),
    call(env, 'POST', `/contacts/${contactId}/notes`, { body: lines.join('\n') }),
    task(env, contactId, 'Call new lead now', lines.join('\n'), 2),
  ]);
  return { ok: true, contactId };
}

/* The contact's deal in the TWI Sales pipeline, moved to Won at the payment's amount; one is created when the
 * contact never had one. The deal keeps the name the lead gave it. */
async function winDeal(env, contactId, p) {
  const found = await call(env, 'GET',
    `/opportunities/search?location_id=${LOCATION}&contact_id=${contactId}&pipeline_id=${PIPELINE}`);
  const deal = (found.opportunities || [])[0];
  const won = { pipelineStageId: STAGE_WON, status: 'won', monetaryValue: p.amount };
  if (deal) return call(env, 'PUT', `/opportunities/${deal.id}`, won);
  return call(env, 'POST', '/opportunities/', {
    locationId: LOCATION, pipelineId: PIPELINE, contactId, name: `${p.name || p.email} — won`, ...won,
  });
}

/* THE PAYMENT — Stripe says money moved. `p` is the relay's normalized event (functions/api/stripe.js):
 * { event: 'payment'|'refund', payment_id, email, name, amount (dollars), ref, billing_reason }.
 * Safe to run twice for one sale: a payment arrives as a checkout AND an invoice with the same payment_id. */
export async function recordPayment(env, p) {
  if (!enabled(env)) return { skipped: true };
  const email = (p.email || '').toLowerCase();
  if (!email) throw new GhlError(`payment ${p.payment_id} has no email`);

  const found = await call(env, 'GET', `/contacts/search/duplicate?locationId=${LOCATION}&email=${encodeURIComponent(email)}`);
  let contact = found.contact;
  let unmatched = false;
  if (!contact) {
    const { firstName, lastName } = splitName(p.name);
    contact = await upsertContact(env, {
      email, firstName, lastName, source: 'stripe', tags: ['unmatched-payment'],
      customFields: fieldList({ partner_code: p.ref }),
    });
    unmatched = true;
  }
  const contactId = contact.id;
  const value = (key) => (contact.customFields || []).find((f) => f.id === FIELD[key])?.value || '';
  const tags = new Set(contact.tags || []);

  if (p.event === 'refund') {
    await task(env, contactId, `Refund $${p.amount} — check the partner commission`,
      `Stripe refunded $${p.amount} (${p.payment_id}). If a partner commission task exists and is unpaid, cancel it.`, 60);
    return { ok: true, contactId, refund: true };
  }

  const duplicate = value('last_payment_id') === p.payment_id;
  if (!duplicate) {
    // the deal is won by the first payment; a renewal never touches it (its value stays the first payment)
    if (p.billing_reason !== 'subscription_cycle') await winDeal(env, contactId, p);
    await call(env, 'PUT', `/contacts/${contactId}`, {
      customFields: [{ id: FIELD.last_payment_id, value: p.payment_id }],
    });
    if (unmatched) {
      await task(env, contactId, 'Unmatched payment — find this person',
        `$${p.amount} arrived from ${email} (${p.payment_id}) and no contact matched. A contact was created; match it to the right person.`, 60);
    }
  }

  // THE COMMISSION: once per contact, on the first payment that is not a renewal. It is decided apart from the
  // duplicate check because the checkout copy carries the partner code and the invoice copy does not.
  const partner = p.ref || value('partner_code');
  let commission = false;
  if (partner && p.billing_reason !== 'subscription_cycle' && !tags.has(TAG_COMMISSION)) {
    await task(env, contactId, `Pay partner ${partner} $${COMMISSION}`,
      `${p.name || email} paid $${p.amount} (${p.payment_id}); referred by partner ${partner}. Pay the flat $${COMMISSION}, then close this task.`, 24 * 60);
    await call(env, 'POST', `/contacts/${contactId}/tags`, { tags: [TAG_COMMISSION] });
    commission = true;
  }
  return { ok: true, contactId, duplicate, commission };
}

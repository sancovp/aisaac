# The restaurant list automation, run by AI — and the toggle-on automations partner model

Two business ideas from transcripts *USER* handed over (`references/yt-transcripts/`, out of git),
plus one product note. None of it is an offer yet: offers are *USER*'s alone
(`.claude/rules/00-SITE-CANON.md` HARD LAW 1), and the questions that decide it are at the bottom.

## 1. The play (Hamza Automates, `hamza-automates-restaurant-qr.md`)

A restaurant learns nothing about the people who eat there, so it has no way to bring them back.
The automation gives it a list it can text.

```
table card with a QR code: "free appetizer — sign up"
  → a landing page with a form (name · email · phone), in the restaurant's logo and colours
  → the contact lands in the restaurant's CRM, tagged by where it came from
  → a confirmation text: "show this to your server"
  → the list grows every service
  → on a slow day (Monday 3pm) the restaurant texts the list a time-limited deal, and the seats fill
     (also birthdays, weekly specials, events, a new location)
```

- **Price:** $399 a month, up to $500 for busy or upscale places. His case: about 50 extra covers a
  month pays for it.
- **Built on GoHighLevel:** a funnel template (one already exists for a free appetizer), a popup
  form, a workflow (form submitted → tag), and GHL's own QR-code builder with the restaurant's logo
  on the code. He says it takes 10–30 minutes per restaurant.
- **His selling move:** build it in the restaurant's own logo BEFORE the first conversation, print
  the cards, and walk in with them.
- **His lock-in line:** "if they stop paying, they lose the list." We do not use it. The customers
  are the restaurant's, and holding them hostage costs the trust our whole positioning rests on.
  We sell "we run it for you".

## 2. The same play run 100% by AI — what is and isn't possible

| step | AI does it? | how |
|---|---|---|
| find restaurants | yes | maps/places data, filtered by the market we pick |
| build their version before contact | yes | ONE GHL snapshot (funnel + form + workflow + QR) loaded into each restaurant's sub-account; the logo and colours set as custom values. GHL's API cannot create workflows (`docs/ghl-integration.md`), but a snapshot carries them |
| a personal first touch | yes | email/DM with a mockup of THEIR table card, in their logo |
| the call that closes | partly | the voice agent (`docs/vapi-agent-design.md`); a human for the close until it is proven |
| the printed cards | no, but outsourced | print-on-demand mailed to the restaurant |
| texting the list | **blocked per restaurant** | each restaurant needs its own A2P 10DLC registration (its legal name and EIN) before GHL can send texts; this is already OPEN for *USER*'s own number |
| consent | must be built in | the form carries explicit opt-in wording for marketing texts (US law — the TCPA — requires it) and keeps the record |
| the monthly campaigns | yes | the slow-hour, birthday and event texts written and scheduled by an agent |

The two hard edges are A2P registration and the physical cards. Everything else is software.

## 3. How Hamza makes money (it matches our framework funnel)

A free Skool community (~48k), a free course, coaching calls. **Signing up to HighLevel through him
unlocks a private mastermind (~300)**, which makes his HighLevel affiliate link the actual product.
That is the structure *USER* already ruled for `framework.html`: a free community, with GoHighLevel
(the snapshot + the affiliate link) sold inside it (`00-SITE-CANON.md`, framework.html row and OPEN).
His channel is evidence that this funnel works at scale.

## 4. *USER*'s idea: a partner model for toggle-on automations

Free training that teaches anyone to look at a business, see its model, and know which of OUR
automations it needs ("this is their model… which automations does TWI have for this?"). Workshops
are paid, and assume the free frameworks are known. The product is the automations themselves,
switched on per business from our snapshots. The restaurant list is the first automation in that
catalogue.

- It is Hormozi's affiliate lead-getter (`hormozi-lead-getters` skill) with TWI as the SUPPLIER,
  where Hamza is the TEACHER.
- It would be a SECOND partner tier beside `partners.html`. Today's tier: agencies refer the big
  transformation, $1,000 per signed client. The new tier: resellers of low-ticket automations, paid
  per business switched on.
- Against it, from *USER*'s own canon: the education/community product comes AFTER a working
  operating business, never instead of one (`docs/business-context-2026-09-15-first-client.md`).

## 5. Product note: Compiled Sanity → HealthWorld (`tom-noske-digital-products.md`)

Tom has filled in a $9 net-worth sheet (Compiled Sanity) every month since 2019, and says he has
sent about a thousand buyers to it, because it is a habit. For HealthWorld the lesson is the
mechanism, not the finance: one number logged every day, a view that makes logging it worth it,
and a finish line you can see. This belongs to HealthWorld's own design when its owner takes it up;
it is recorded here only as where the idea came from.

## OPEN — *USER*'s

- Run the restaurant play at all, and when: before or after the first transformation clients?
- Who registers A2P for each restaurant, and who pays for it?
- The partner tier for toggle-on automations: yes or no, and what a partner earns per business.
- Which low-ticket digital product to make first. Score the candidates with the
  `low-ticket-digital-product` skill before choosing.

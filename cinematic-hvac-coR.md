# CoR: Edwards Heating & Air — Cinematic HVAC Demo

**Niche:** HVAC (emergency-services vertical, same playbook as plumbing)
**Prospect:** Edwards Heating & Air, LLC
**City:** Acworth, GA (Cobb County, same area as Dickinson demo)
**Demo target:** $250/mo managed, $2,500 build

---

## THE BELIEF STACK — every section mapped

| Section | Installs | Removes |
|---|---|---|
| **Veo 3.1 hero video** (NATE tech on a roof, condenser, summer light) | "Real tech, real rooftop, real sun — not a stock photo" | "AI sites look fake" |
| **License CR109219 + Carrier Factory Authorized Dealer** in trust bar | "Credentialed above the floor — not a handyman with a Google listing" | "HVAC 'guys' are unlicensed" |
| **"Since 2001 — that's 25 summers we've kept Cobb County cool"** | "Established, accountable, still here 25 years later" | "HVAC companies disappear after 2-3 years" |
| **"Bryan drove 1.5 hours in July to fix our A/C"** (hero review) | "These people will go further than the job requires" | "HVAC techs leave you waiting days" |
| **"Same tech every visit — Bryan, Scott, Billy"** | "You'll know who's coming" | "I'll get a different stranger each time" |
| **Service cards as "what it PREVENTS"** (AC Service → "Prevents: July 4th weekend breakdown, $1,200 emergency install, sleepless nights") | "These techs think like a homeowner" | "HVAC just upsells a new unit" |
| **2AM-ish emergency image** (suburban house at night, Edwards van in driveway, work light, summer heat haze) | "They actually answer when A/C dies in July" | "After hours = call center / next-day appointment" |
| **"Free second opinion on replacements"** (a new differentiator, not in their current copy) | "We diagnose first, recommend second" | "HVAC companies push replacement on every visit" |
| **$89 diagnostic, waived with repair** | "Low-stakes way to find out what's wrong" | "$150 service call just to walk in the door" |
| **Service area pills: 7 cities, all 5-letter short** | "We actually serve all these places — local, not regional" | "Service area pages are fake" |

---

## COPIED CO-R TEMPLATE (filled in from SKILL.md)

> "Now I'll build **Edwards Heating & Air**'s site in **Acworth, GA**. Their best review says **'Bryan drove 1.5 hours in July to fix our A/C'** — that's the voice I write copy in. Their **Class II Refrigerant License #CR109219** + **Carrier Factory Authorized Dealer** go in the trust bar. Hero headline: **'AC Died in July? We Answer.'** because their customers' #1 fear is **'my family will suffer through a 100° house waiting for a tech'**. Color: extract from their current site (deep blue + red Carrier-like accent). Generating hero image with **Imagen 4 Ultra**: '[rooftop tech prompt]', animating with **Veo 3.1**: '[NATE tech on roof, slight turn, golden summer light]'. Deploying to **sancovp.github.io/edwards-heating-air/**. **Building Niche: HVAC.** **Demo price: $250/mo managed.**"

✅ All blanks filled. SCRAPE step is complete.

---

## IMAGE / VIDEO PROMPT LIST (next step if you say fire)

### Hero video reference (Imagen 4 Ultra, $0.06) → Veo 3.1 ($3.20)

**Reference image prompt:**
```
Documentary photograph of an HVAC service technician in his 40s,
NATE certification patch on his vest, kneeling beside a residential
condenser unit on a shingled roof in mid-July afternoon. Multimeter
leads in one hand, gauge manifold resting on the unit. Hard hat
slightly tilted back, safety glasses pushed up on forehead, sun
on his weathered face. Slight smile, the look of "found the
problem." Soft hazy overcast sky, even light, working-class
realism. 24mm wide, deep focus, paint-stains on the unit, dust
on the vest. Shot on Canon EOS R5, 35mm, f/5.6, deep focus with
hazy sky detail. No HDR, no golden hour, no cinematic grade.
```

**Veo 3.1 animation prompt:**
```
The NATE-certified HVAC tech lifts his head from the condenser
unit, looks directly into the camera, and gives a small confident
nod. Slight breeze moves the tree leaves in the background.
Dust motes drift in the late afternoon light. Subtle camera
push-in. Cinematic, smooth, broadcast-quality motion.
```

### Site images (Imagen 4, ~$0.40 total)

1. **Owner portrait** (Bryan, in shop uniform, 4/3 aspect, $0.06)
2. **Hero action** (tech on roof, golden afternoon, $0.06)
3. **Van exterior** (Edwards-branded van in suburban driveway, 24mm, $0.02)
4. **Tools still life** (manifold gauges, multimeter, refrigerant tank, knolling, $0.025)
5. **July emergency** (suburban house, A/C condenser working hard, sweat on glass, 90° heat haze, $0.06)
6. **About / service truck** (interior shot, organized truck bed with Carrier boxes, $0.04)
7. **Family / warmth** (family in cool living room during July, ceiling fan, ice tea, real photojournalism, $0.04)

**Total: ~$3.50** (well under the $5/site budget)

---

## COPY ANGLES (for the HTML build)

**Hero h1:** "AC Died in July? *We Answer.*" (echoes Dickinson's "2AM Pipe Burst? We Answer.")
**Hero sub:** "Family-owned since 2001. NATE-certified, Carrier Factory Authorized. **$89 diagnostic waived with repair.** A real person picks up. A real tech shows up."
**Trust bar:** 25+ Years · Carrier Factory Authorized · NATE-Certified · License CR109219 · 4.5★
**Service cards (6, "what it PREVENTS"):**
1. AC Repair → "Prevents: sleepless July nights, $1,200 emergency install, mold from prolonged humidity"
2. AC Install → "Prevents: 20-year-old system dying mid-summer, surprise $8K replacement"
3. Heating Repair → "Prevents: January pipe-freeze, $4K water damage, family in coats indoors"
4. Heat Pumps → "Prevents: 2-system replacement, $15K utility bills over 10 years"
5. Indoor Air Quality → "Prevents: kid's asthma flare-ups, dust buildup, daily congestion"
6. Maintenance Plan → "Prevents: emergency visits, 30% shorter system lifespan, voided warranty"

**Reviews (3 cards, real platform pills):**
1. The Bryan-July-1.5-hours story (Google)
2. Scott the no-heat tech (service contract customer) (Angi)
3. Victoria P. first-call-to-install experience (HomeAdvisor)

**Final CTA:** "AC out? **Call (770) 685-7521**" + "Free second opinion on any replacement quote."

---

## READY TO FIRE

Approve and I'll:
1. Generate the Veo 3.1 hero video (~45s) + 1 reference image
2. Generate 6 site images (parallel where possible, ~3-4 min)
3. Copy them to aisaac/, git commit
4. Build cinematic-hvac.html (single file, same architecture as plumbing, adapted)
5. Screenshot full page
6. Commit + lessons.md entry

**Estimated time:** 8-12 min of generation + 5 min of HTML writing + 1 min of commit/screenshot = **~15 min total**
**Estimated cost:** ~$3.50 in Imagen 4 + Veo 3.1 calls

Say "fire" and I'll start. Or "adjust [X]" if anything in the CoR feels off.

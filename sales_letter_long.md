# Long-Form Direct-Response Sales Page Grammar

## Purpose

This is an **LLM prompt-program**, not a list of vague section labels.

The generator MUST instantiate explicit sentence forms. Bracketed symbols are typed variables defined in the schema below. A symbol such as `[URGENCY]` is illegal unless its internal structure is separately defined.

The grammar is reconstructed from the supplied sales-page copy at the level of **rhetorical and sentence structure**, while keeping the template domain-neutral.

---

# 0. GLOBAL OBJECTS

Before writing the page, construct this object:

```yaml

AUDIENCE:

  singular_noun:

  plural_noun:

  self_description:

  desired_identity:

  rejected_identity:

PROBLEM:

  current_state:

  recurring_frustration:

  visible_symptoms: [3-7]

  conventional_explanation:

  conventional_solutions: [3-7]

DESIRE:

  primary_outcome:

  vivid_after_state:

  status_outcome:

  emotional_outcome:

  avoided_cost:

  avoided_effort:

MECHANISM:

  ordinary_description:

  proprietary_name:

  one_sentence_claim:

  old_model:

  new_model:

  causal_steps: [3-7]

  surprising_implication:

AUTHOR:

  before_state:

  humiliating_or_frustrating_incident:

  discovery_source:

  research_sources: [3-7]

  first_test:

  first_result:

  later_results:

PROOF:

  cases:

    - subject:

      apparent_disadvantage:

      mechanism_expression:

      surprising_result:

  demonstrations:

  testimonials:

OFFER:

  product_name:

  category:

  core_transformation:

  modules:

    - name:

      capability:

      techniques:

  bonuses:

  delivery_format:

  access_terms:

PRICE:

  high_anchor:

  middle_anchor:

  normal_price:

  launch_price:

  daily_equivalent:

  launch_reason:

GUARANTEE:

  period_days:

  required_actions:

  measurable_result:

  refund_action:

URGENCY:

  present_event:

  consequence:

  future_price:

  availability_risk:

CTA:

  action_verb:

  button_object:

```

---

# 1. FANTASY HEADLINE

Choose one.

```text

Who Else Wants [POSSESSIVE_DESIRE_OBJECT] [INTENSIFIER] [DESIRED_OUTCOME]?

```

```text

Who Else Wants To [DESIRED_ACTION] — Without [EXPECTED_PREREQUISITE]?

```

Immediately expand the fantasy using fragments:

```text

Imagine having [DESIRED_OBJECT].

No, not [WEAKER_OR_ORDINARY_VERSION].

I mean [EXTREME_OR_SPECIFIC_VERSION].

[SHORT_DESCRIPTIVE_FRAGMENT].

[SHORT_DESCRIPTIVE_FRAGMENT].

[SHORT_DESCRIPTIVE_FRAGMENT].

And you get to [PRIMARY_BENEFIT].

```

Constraint: each descriptive fragment is a noun phrase or adjective phrase, not a generic summary.

---

# 2. DIRECT ADDRESS + SCENE CONSTRUCTION

```text

Dear [AUDIENCE_SINGULAR],

Imagine [PRESENT_PARTICIPLE_SCENE_SETUP].

[CONCRETE_VISUAL_DETAIL].

[CONCRETE_VISUAL_DETAIL].

And [DESIRED_EVENT].

```

Then:

```text

Can you picture that scene?

Is that [ADJECTIVE] enough for you?

```

Then a hard declarative transition:

```text

This is YOUR REALITY now.

```

---

# 3. CONTRAST LADDER

Generate 3-5 repetitions of this exact relation:

```text

While other [AUDIENCE_PLURAL] [CURRENT_FRUSTRATION]...

You're [CONTRASTING_DESIRED_RESULT].

```

Escalate each pair. The final pair should be the strongest.

Then:

```text

Why?

Because [FALSE_OR_PLAYFUL_EXPLANATION].

Just kidding.

It's because [DISCOVERY_OR_MECHANISM_TEASE].

```

---

# 4. PRODUCT REVEAL

```text

INTRODUCING—

# [PRODUCT_NAME]

## The [SUPERLATIVE_OR_CATEGORY] Guide To [CORE_TRANSFORMATION]

```

Alternative:

```text

# How To Become [DESIRED_IDENTITY]

...and [PRIMARY_RESULT].

Even if you're [OBJECTION_1], [OBJECTION_2], [OBJECTION_3], and [OBJECTION_4]?

```

---

# 5. ORIGIN-STORY OPEN

```text

## How A [LOW_STATUS_SELF_DESCRIPTION] [ACHIEVED_IMPROBABLE_RESULT]...

Hop in your time machine with me and picture this:

The year is [YEAR], and I'm [ORDINARY_SCENE]...

```

Continue:

```text

I was [AGE_OR_LIFE_STAGE], [PROBLEM_DESCRIPTION].

[ONE CONCRETE INCIDENT THAT EMBODIES THE PROBLEM].

By the time I got to [NEXT_STAGE], [PROBLEM] had [IMPROVED_OR_CHANGED],

but my [INTERNAL_STATE] was [LOW_POINT].

```

Do **not** use an anecdote involving a minor in a sexual context.

---

# 6. DISCOVERY PIVOT

Use this sentence exactly as the structural pivot:

```text

But then, I stumbled on a bizarre secret...

```

Then:

```text

It was [DISCOVERY_OBJECT_OR_SOURCE].

[ONE STRANGE DETAIL ABOUT SOURCE].

The [SOURCE] was about [PERSON / PHENOMENON / SYSTEM].

And yet oddly, [COUNTERINTUITIVE_FACT].

Instead...

[WHAT ACTUALLY HAPPENED].

```

Close with the central question:

```text

So how the hell did [SUBJECT_WITH_DISADVANTAGES] [ACHIEVE_RESULT]?

```

---

# 7. RESEARCH MONTAGE

```text

And that's what I wanted to know, too...

So I began to [RESEARCH_VERB] everything I could get my hands on about...

# [RESEARCH_DOMAIN]

```

Then:

```text

First, I studied [CASE_1]. I [RESEARCH_ACTION]...

I [RESEARCH_ACTION], [RESEARCH_ACTION], and [RESEARCH_ACTION]...

Then I studied [CASE_2]...

[CASE_3]...

And throughout my research, I started to notice a few patterns...

```

Then the proprietary-mechanism bridge:

```text

The one thing all these [CASE_CATEGORY] had in common...

It's a technique they all used...

An almost "[METAPHORICAL_ADJECTIVE]" power they all possessed...

It's something I've come to call the...

# [PROPRIETARY_MECHANISM]

```

---

# 8. EXHIBIT PROOF STACK

Repeat 3-7 times:

```text

## Exhibit [LETTER]: [CASE_NAME]

[CASE_NAME] was [APPARENT_DISADVANTAGE].

And yet [SURPRISING_RESULT].

[ONE OR TWO CONCRETE SUPPORTING DETAILS].

```

After the final exhibit:

```text

Now here's the point:

None of these [CASE_CATEGORY] [CONVENTIONAL_SUCCESS_REQUIREMENT].

In fact, [STRONGER_CONTRAST].

And yet [COMMON_SURPRISING_RESULT].

```

Then:

```text

So how did they do it?

My research has convinced me it comes down to [NUMBER] things that every single one of these [CASE_CATEGORY] had in common:

```

---

# 9. MECHANISM DEFINITION

```text

# So what the hell is the "[PROPRIETARY_MECHANISM]"?

It all boils down to [NUMBER] little [WORD / PRINCIPLE / DISTINCTION], my friend.

That [WORD / PRINCIPLE] is...

# [CORE_CONCEPT]

```

Then:

```text

The [PROPRIETARY_MECHANISM] gives you the power to [MECHANISM_EFFECT]...

Such as [EXAMPLE_EFFECT].

```

Definition structure:

```text

A "[CORE_CONCEPT]" is [PLAIN_DEFINITION]...

And this is the real secret behind [DESIRED_PHENOMENON].

```

---

# 10. DESTROY THE OLD MODEL

```text

But before I answer that, I need to destroy the single biggest LIE you've been fed about [DOMAIN].

I'm talking, of course, about [OLD_MODEL].

You see, what my research into [EVIDENCE_CLASS] convinced me once and for all was that—

# "[OLD_MODEL]" IS [EXTREME_REJECTION]

```

Then proof by contradiction:

```text

And here's the proof...

```

Follow with exhibits.

---

# 11. MECHANISM → CUSTOMER BRIDGE

Use the source-like objection line:

```text

"SOUNDS GREAT BUT... HOW DOES IT [PRODUCE_MY_DESIRED_RESULT]?"

```

Then:

```text

I'm glad you asked...

And it's quite simple, really...

Just as you can use [MECHANISM] to [DEMONSTRATED_EFFECT]...

You can also use it to [CUSTOMER_EFFECT].

```

Then analogy:

```text

It's the same principle that makes [FAMILIAR_ANALOGY] work...

```

Follow with:

```text

Well—

Just as [ANALOGY_CAUSE] can [ANALOGY_EFFECT]...

You can also [TARGET_APPLICATION].

```

---

# 12. PERSONAL DEMONSTRATION STORY

```text

The next time I [RETURNED_TO_OLD_PROBLEM], I wasn't [OLD_BEHAVIOR] any more...

Instead, I was 100% focused on [NEW_VARIABLE]...

```

Then behavioral sequence:

```text

I [ACTION_1].

Normally I'd have [OLD_RESPONSE]...

But instead of [OLD_RESPONSE], I [NEW_RESPONSE].

Just like I'd learned from [SOURCE],

I [APPLIED_MECHANISM].

```

Then incremental evidence:

```text

And to my amazement... this bullshit actually started to work!

[SMALL_RESULT].

[SECOND_RESULT].

[THIRD_RESULT].

```

Do not invent sexual details; when adapting a sexual source, abstract the result to consensual dating/relationship outcomes.

---

# 13. RESULT ESCALATION

```text

From that day forth, [OLD_PROBLEM] was [TRANSFORMED].

[RESULT_1].

[RESULT_2].

[RESULT_3].

```

Then retrospective contrast:

```text

It was almost unbelievable to me that just [TIME_PERIOD] ago [BEFORE_STATE].

And since [FIRST_SUCCESS], I [ONGOING_TRANSFORMATION].

```

Then:

```text

Flash forward to today:

Here are just a few [CURRENT_PROOF_OBJECTS]...

```

---

# 14. TWO-IDENTITY BINARY

```text

At the end of the day...

There are really only 2 kinds of [AUDIENCE_PLURAL] in this world:

# 1. [DESIRED_IDENTITY_PLURAL]

and...

# 2. [REJECTED_IDENTITY_PLURAL]

```

Define each with parallel syntax:

```text

[DESIRED_IDENTITY_PLURAL] do [DESIRED_BEHAVIOR].

We [BELIEF].

We don't [REJECTED_BEHAVIOR].

We [POSITIVE_BEHAVIOR].

```

Versus:

```text

[REJECTED_IDENTITY_PLURAL] do the opposite.

They [BEHAVIOR].

They [BEHAVIOR].

They don't [DESIRED_BEHAVIOR].

Instead, they [DEPENDENCY_OR_FAILURE].

```

Then:

```text

[DESIRED_IDENTITY_PLURAL] TURN THIS DYNAMIC ON ITS HEAD...

```

---

# 15. PRODUCT AS IMPLEMENTATION OF MECHANISM

```text

And I am going to show you exactly how to do that inside my groundbreaking new program...

# THE [PRODUCT_NAME]

```

Then:

```text

[PRODUCT_NAME] is the first and only [PRODUCT_CATEGORY] which shows you how to [CORE_RESULT] by [MECHANISM]... just like I did.

It's based on my [NUMBER]+ year study of [RESEARCH_DOMAIN]...

Such as [CASE_1], [CASE_2], [CASE_3], and others...

```

Then:

```text

But this isn't some dry, boring "[WRONG_CATEGORY]".

And it's NOT just [COMMODITIZED_ALTERNATIVE].

I did all the hard work, so you don't have to.

I [RESEARCH_EFFORT_1]...

I [RESEARCH_EFFORT_2]...

And I collected only the very best [TOOLS_CATEGORY] which [EXPERT_CLASS] used to [RESULT].

Then—I refined all this "raw data"...

And turned it into a simple, STEP-BY-STEP system that ANY [AUDIENCE_SINGULAR] can easily follow and apply in [POSSESSIVE_CONTEXT], to get...

# [EXTREME_CORE_RESULT]

```

---

# 16. MODULE INTRODUCTION

```text

IN THE "[PRODUCT_NAME]" SYSTEM... YOU WILL DISCOVER:

```

Generate 5-12 benefit bullets before module detail:

```text

HOW TO [CAPABILITY]

HOW TO [CAPABILITY]

HOW TO [CAPABILITY]

HOW TO [REMOVE_OBJECTION]... AND...

HOW TO [HIGHLY_SPECIFIC_RESULT]

```

---

# 17. MODULE GRAMMAR

Every module uses:

```text

# MODULE #[N]

## [MODULE_NAME]

"[VIVID_ONE_SENTENCE_MODULE_PROMISE]"

```

Then 4-12 bullets. Every bullet MUST instantiate one of these forms:

```text

[NAMED_TECHNIQUE]: How to [ACTION] so [RESULT].

```

```text

HOW TO [RESULT], using [MECHANISM_OR_CONSTRAINT].

```

```text

THE [NUMBER] [NOUN] OF [CONCEPT]: [EXPLANATION_OR_RESULT].

```

```text

NEVER [UNDESIRED_ACTION] AGAIN: how to [PREVENTION_METHOD].

```

```text

MAKE [TARGET] [RESULT]. Just [SMALL_ACTION] to [LARGER_RESULT].

```

```text

THE "[PROPER_NOUN]" SECRET: how [CASE] [ACHIEVED_RESULT], using [MECHANISM].

```

```text

[MEMORABLE_OPERATION_NAME]. How to [ACTION] until [RESULT].

```

```text

[NUMBER] "[MAGIC_WORDS / QUESTIONS / STEPS]" that [RESULT].

```

```text

[COUNTERINTUITIVE_CLAIM]. Do [ALTERNATIVE_ACTION] instead...

```

No placeholder may merely say `[BENEFIT]`, `[TIP]`, `[URGENCY]`, `[DETAIL]`, or `[EXAMPLE]`.

---

# 18. "NOT FOR EVERYONE" FILTER

```text

[PRODUCT_NAME] IS NOT FOR EVERYONE

```

Then:

```text

In fact, there are [NUMBER] specific types of [AUDIENCE_PLURAL] who [SHOULD_NOT_BUY]...

And if [ENFORCEMENT_OR_CONSEQUENCE]...

```

For each:

```text

# [N]: THIS SYSTEM IS NOT FOR YOU IF YOU [DISQUALIFIER]

It's not for you if [SPECIFIC_BEHAVIOR].

And it's definitely not for you if [STRONGER_SPECIFIC_BEHAVIOR].

```

Then describe the alternative they should choose.

---

# 19. CONTRARIAN MANIFESTO

```text

Let's be honest.

[NUMBER]% of [ALTERNATIVE_CATEGORY] are [NEGATIVE_JUDGMENT].

Everything is just a copy, of a copy, of a copy.

It's all [REHASH_METAPHOR]. The same [OLD_THING] that's been [REPEATED] since [ERA], reworded, packaged slightly differently.

What I'm offering you here is something that is completely...

[ONE_WORD_LINE].

[ONE_WORD_LINE].

[ONE_WORD_LINE].

```

Then:

```text

This is not about becoming [OLD_IDENTITY].

It's about becoming [NEW_IDENTITY].

```

---

# 20. OFFER INVENTORY

```text

HERE'S A TINY TASTE OF WHAT'S INSIDE...

```

After modules:

```text

This is a graphical representation of the products offered, when purchased you will be given [DELIVERY_MECHANISM] for instant access to all content.

```

Inventory:

```text

Part #1: [COMPONENT]

Part #2: [COMPONENT]

Part #3: [COMPONENT]

...

The [WORKBOOK_NAME]: [NUMBER] Questions Which Guide You Through How To [WORKBOOK_TRANSFORMATION]

```

---

# 21. PRICE REVEAL DELAY

```text

"SOUNDS GREAT! BUT HOW MUCH DOES IT COST?"

Good question. And I'll answer it in a second.

But first, I need to [FINAL_OBJECTION_OR_FILTER].

```

After objection handling:

```text

Now I'm about to reveal the price of [PRODUCT_NAME] in a second.

But before I do...

I want you to visualize something.

```

---

# 22. VALUE VISUALIZATION

```text

Imagine That You Are Now

# [EXTREME_AFTER_STATE]

```

Then:

```text

What sort of [OUTCOME_OBJECT] do you want?

Picture [IT / THEM / YOURSELF] now. As vividly as you can.

[ATTRIBUTE].

[ATTRIBUTE].

[ATTRIBUTE].

Imagine [AFTER_STATE_EVENT].

How much would that be worth to you?

```

Escalate:

```text

But now imagine you don't just have "[ONE_UNIT]".

You have [MULTIPLIED_RESULT]...

```

---

# 23. PRICE ANCHOR LADDER

```text

Would you pay $[HIGH_ANCHOR]?

What about $[MIDDLE_ANCHOR]?

Would you pay just $[LOWER_ANCHOR] to [PERMANENT_RESULT]?

```

Then:

```text

Well here's the good news.

You're not going to pay $[HIGH_ANCHOR] for [PRODUCT_NAME].

You won't even pay $[MIDDLE_ANCHOR].

In fact, you won't even pay $[NORMAL_PRICE].

I've decided to price [PRODUCT_NAME] at just $[PRICE_BEFORE_DISCOUNT].

```

Then optional second drop:

```text

And so, for a very short time...

You can get all of this for just...

~~$[ANCHOR_1]~~

~~$[ANCHOR_2]~~

~~$[NORMAL_PRICE]~~

# $[LAUNCH_PRICE]

```

---

# 24. DAILY-EQUIVALENT REFRAME

```text

Break that down over the next [PERIOD]...

And it comes out to just

# $[DAILY_EQUIVALENT] per day

Less than the price of [LOW_COST_REFERENCE].

```

---

# 25. REASON FOR DISCOUNT + FUTURE PRICE

```text

HOWEVER.

I appreciate that [MARKET_CONDITION].

For a lot of people out there, $[NORMAL_PRICE] is [OBJECTION].

And because I want [AUDIENCE] to [BENEFIT]...

I am temporarily lowering the price of the system...

But only during this brief "[LAUNCH_NAME]" period.

```

Then:

```text

Once [LAUNCH_CONDITION]...

I will be raising the price to $[FUTURE_PRICE].

```

Give a reason:

```text

Why?

Because truthfully, this product is worth far more than that.

This is my [MAGNUM_OPUS_PHRASE].

I've spent the past [YEARS] [ACCUMULATING / DEVELOPING] [ASSET].

```

---

# 26. URGENCY COMPILER

Never emit `[SHORT URGENCY REMINDER]`.

Construct urgency from these explicit fields:

```yaml

URGENCY_INSTANCE:

  trigger_event: "launch ends / enrollment fills / production capacity is reached / scheduled price review"

  current_advantage: "current price / bonus / access condition"

  post_trigger_change: "price increases / bonus disappears / enrollment closes"

  uncertainty_clause: "optional genuine uncertainty, only if supportable"

  action_deadline_phrase: "before [trigger_event]"

```

Sentence forms:

```text

If you want [PRODUCT_NAME] at this [CURRENT_ADVANTAGE]...

YOU MUST ACT [BEFORE_TRIGGER].

```

```text

Once [TRIGGER_EVENT]...

[POST_TRIGGER_CHANGE].

```

```text

And there's also one other reason why you should get this NOW, not later:

[GENUINE_EXTERNAL_CONSTRAINT].

```

Do not fabricate scarcity, legal threats, inventory limits, or deadlines.

---

# 27. GUARANTEE COMPILER

Never emit `[GUARANTEED CONDITION]`.

Construct:

```yaml

GUARANTEE_INSTANCE:

  trial_period_days:

  completion_action_1:

  completion_action_2:

  success_metric:

  success_threshold:

  alternative_satisfaction_clause:

  refund_window_days:

  refund_method:

```

Sentence form:

```text

Get [PRODUCT_NAME]...

[COMPLETION_ACTION_1]...

[COMPLETION_ACTION_2]...

If you're not [SUCCESS_METRIC] within [TRIAL_PERIOD]...

Or if [ALTERNATIVE_SATISFACTION_CLAUSE]...

Just [REFUND_METHOD] any time within [REFUND_WINDOW] of ordering, and I'll [REFUND_ACTION].

No questions asked.

```

---

# 28. CROSSROADS CLOSE

```text

You're at a crossroads right now:

And either we go on together... or you will go it alone.

Either you:

[OPTION_A_ACTION], and [OPTION_A_RESULT]...

or

[OPTION_B_ACTION], and [OPTION_B_RESULT].

```

Then return to pains:

```text

[PAIN_FRAGMENT].

[PAIN_FRAGMENT].

And [PAIN_FRAGMENT].

```

Then:

```text

You can go back to that if you like.

But [FINAL_REASON_TO_CHANGE].

```

---

# 29. FINAL CTA

```text

Now is the time for action.

Do it now.

[SHORT_CONFIDENCE_CLAIM].

```

Then:

```text

Click the button below...

[CTA_ACTION]...

And [IDENTITY_MEMBERSHIP + CORE_RESULT].

```

Button:

```text

[CTA_ACTION_VERB] [PRODUCT_NAME]

```

---

# 30. P.S. STACK

```text

P.S. [RESTATED_PRIMARY_OUTCOME + MECHANISM].

```

```text

P.P.S. [GUARANTEE_SENTENCE USING GUARANTEE_INSTANCE].

```

```text

P.P.P.S. [URGENCY SENTENCE USING URGENCY_INSTANCE].

```

---

# 31. GENERATION ALGORITHM

The LLM MUST NOT draft from top to bottom immediately.

```text

1. Parse offer into GLOBAL_OBJECTS.

2. Refuse to continue internally until PROBLEM, DESIRE, MECHANISM, OFFER,

   PRICE, GUARANTEE, and URGENCY contain concrete values.

3. Generate 5 candidate proprietary mechanism names.

4. Select one mechanism whose causal explanation can recur throughout page.

5. Generate origin story as BEFORE → DISCOVERY → RESEARCH → MECHANISM → TEST.

6. Generate proof cases that each attack a different conventional objection.

7. Generate identity binary from acceptance/rejection of the mechanism.

8. Decompose OFFER into modules.

9. For every module, generate bullets ONLY from MODULE_GRAMMAR sentence forms.

10. Compile PRICE from PRICE_ANCHOR_LADDER.

11. Compile GUARANTEE from GUARANTEE_INSTANCE.

12. Compile URGENCY from URGENCY_INSTANCE.

13. Compile CROSSROADS_CLOSE using pains introduced earlier.

14. Verify every bracketed variable is typed and instantiated.

15. Delete any sentence containing an undefined meta-placeholder such as:

    [DETAIL], [BENEFIT], [URGENCY], [EXAMPLE], [SHORT REMINDER], [STORY],

    [PROOF], or [GUARANTEED CONDITION].

16. Verify claims of evidence, scarcity, guarantees, and results are supported

    by supplied facts rather than invented.

```

---

# 32. CORE INVARIANT

The page is not a sequence of unrelated sections. The same mechanism must recursively explain the story, proof, identity, product, modules, objections, and close:

```text

PROBLEM

  ↓

OLD MODEL FAILS

  ↓

DISCOVERY

  ↓

NAMED MECHANISM

  ↓

CASES DEMONSTRATE MECHANISM

  ↓

AUTHOR DEMONSTRATES MECHANISM

  ↓

READER ADOPTS MECHANISM

  ↓

PRODUCT IMPLEMENTS MECHANISM

  ↓

MODULES DECOMPOSE IMPLEMENTATION

  ↓

OFFER PACKAGES IMPLEMENTATION

  ↓

CTA INITIATES IMPLEMENTATION

```

If a section cannot be derived from the same mechanism, either rewrite it or remove it.

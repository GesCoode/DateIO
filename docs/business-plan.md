# Visagely — Business Plan

> Status: working draft. Figures (market sizes, API costs, competitor revenues, token
> economics) are illustrative, tunable models derived from 2026 market research — treat
> them as a framework, not fixed claims.

## 1. Executive summary

Visagely is a **privacy-first, EU-compliant AI dating-photo studio** for men. Users train a
personal, high-fidelity model of their own face (a per-user **LoRA**) and generate realistic,
well-composed dating photos using a **curated template library** (each template = a
black-and-white composition control image + a structured JSON scene recipe).

The differentiation is **fidelity + interesting, controllable compositions** (LoRA beats the
IP-Adapter/InstantID approach most competitors use) wrapped in an **EU privacy** promise and a
**verification-safe, "looks like the real you"** guarantee.

Monetization is **token-based, no subscription**. Generation previews are cheap/soft-free and
**users only spend meaningful tokens when they choose to upscale (upres) a final image** — they
pay for value, not attempts. Training also costs tokens (tiered by fidelity). Gross margins are
~80–90%.

The market is validated (competitors like Aragon reached ~$10M ARR; Photo AI ~$105K/mo solo at
~76% profit), acquisition is SEO-led, and unit economics are excellent. The plan is capital-light
and executable by a very small team.

## 2. Problem & opportunity

- Photos are the single biggest driver of dating-app outcomes, and **men are the underserved,
  high-intent, willing-to-pay segment** (apps skew ~60–65% male; Tinder ~75/25). Most men have
  poor, unvaried photos and low match rates.
- Existing AI tools mostly use fast **IP-Adapter/InstantID** identity injection — cheap but lower
  fidelity (~65–90%), drifty, and repetitive ("rarely interesting"), which fuels the "looks fake /
  doesn't look like me / catfish" backlash seen across Reddit and reviews.
- Simultaneously, dating apps are rolling out **mandatory biometric Face Check** (Tinder US Oct
  2025, UK Mar 2026; Hinge global liveness Feb 2026). This **kills face-altering tools but rewards
  identity-preserving ones** — exactly Visagely's approach.
- The adjacent AI-headshot market is ~$500M in 2026 growing ~30–60%/yr; the dating sub-niche is
  the fastest-moving slice.

## 3. Product & differentiation

**What it is:** a portal where a man trains a personal LoRA and generates dating-ready photos of
himself in curated, controllable scenes.

**Four pillars of differentiation (moats, in order of durability):**

1. **Owned template library** — B&W composition + JSON scene recipes (scene, colors, subject
   placement, clothing, emotion, pose). Produces *interesting, on-brand* compositions competitors
   can't easily copy, and is rights-clean (abstracted, AI-generated).
2. **LoRA-first fidelity** — highest identity accuracy and the ability to generalize to novel
   scenes; optional higher-fidelity training tiers.
3. **EU privacy-first** — your model lives in the EU, is never shared, deletable in one click.
   Almost no US competitor can match this.
4. **Trust / verification-safe promise** — "looks like the real you, passes Face Check." Rides the
   mandatory-verification wave and answers the catfish objection.

## 4. User workflow

**Entry & account.** User visits **visagely.com**, creates an account behind a **hard 18+ age
gate** and **explicit consent**. On signup they receive **a few free credits + a base LoRA** to
test the system immediately (activation before any purchase).

**Portal layout.** Simple, premium. **Value actions front-and-center** — (1) Train, (2) My
Models → Generate, (3) Library — with utility tiles in the header/nav: **Buy tokens**,
**Privacy/Legal**, **Account & Settings**.

1. **Buy tokens** → payment portal, one-time token purchases, **no subscription**, **tokens don't
   expire** (option to introduce expiry later if needed). Always shows price and current balance.
2. **Privacy/Legal** → policies, consent records, and data controls.
3. **Account & Settings** → profile, notification prefs (**email/push for training completion**),
   and **data controls** (delete model(s), delete all data, export data, withdraw consent).

**Container A — Train a LoRA.**

- Upload photos → system checks **fidelity, size, usability** (and runs the safety gate:
  **NSFW/underage detection blocks disallowed images**).
- **Ownership check (MVP):** a **checkbox where the user affirms the photos are of himself**
  (selfie-match verification added later only if abuse appears).
- Choose **training tier** (higher fidelity = more tokens).
- Accept T&C/consent (at this step and/or at signup).
- Start training → returns to portal.

**Container B — My Models → Generate.**

- See trained LoRAs and in-progress ones **with estimated time remaining**; notified on
  completion.
- Click a model → **Generation**:
  - **Prompt-driven (MVP core):** pick a **template**, add **keywords**, or write your own
    **specifications**; structured controls (pose, lighting, clothing, emotion) exposed from the
    template JSON.
  - Click **Generate → 4 preview images** (low-res, watermarked — cheap/soft-free).
  - **Adjust the prompt** or **pick a favorite**.
  - **You pay tokens only when you choose to upres** the favorite (hi-res, watermark removed).
  - From an upressed image: **"Generate similar"** for more, or **refine by prompt** until happy,
    then **download**.
  - **Packs** (beach, restaurant, etc.) = **curated bundles of templates** for one-click batch
    generation — **post-MVP**, not required for launch.

**Container C — Library.**

- All images stored; **favorite, delete, download**. Delete doubles as GDPR erasure at the image
  level. (Grouping by model/session and a "download my set" export are easy adds.)

## 5. Website style & brand

**Premium, high-end-fashion editorial.** This directly counters the "is this a cheap scam / will
it look fake" fear — polish signals trust.

- Dark, editorial palette with restrained luxury accents; generous whitespace.
- A refined **serif display** paired with a clean **sans** for UI.
- Large, high-quality hero imagery and a curated **before/after and sample gallery** (crucial
  social proof).
- Subtle, tasteful motion; no clutter.
- **Emotionally safe tone** — given the audience, the UX must feel private, encouraging, and
  non-judgmental at every step.

## 6. Target audience & positioning

**Primary:** men, **EU and USA**, who struggle with dating photos — low match rates, few good
pictures, low photo confidence. A large, underserved, high-willingness-to-pay group.

**Positioning (public messaging):**

> "Look like the **best real version of you**." — better lighting, styling, scenes, and
> confidence, not a different or fake person.

This framing is important on three fronts at once: it's **ethically sound**, it's
**Face-Check-safe** (identity preserved), and it defuses the catfish narrative. Never market as
"become better-looking than you are" — that breaks the trust promise and invites the exact
backlash competitors get.

**Brand principles:** private, respectful, confidence-building, results-focused. The product
should make an insecure first-time user feel safe and in control.

## 7. Tech stack

> Aligns with the SvelteKit + PostgreSQL foundation already scaffolded in the repo.

- **Frontend & app:** SvelteKit (SSR + API routes), Tailwind, `adapter-node`. Premium design
  system.
- **Auth & accounts:** email + OAuth; **18+ age gate** and consent capture at signup; sessions.
- **Database:** PostgreSQL (users, consent records, models, jobs, generations, token ledger).
  Store **immutable consent + token transactions** for auditability.
- **Object storage:** **EU-region S3-compatible** (e.g., Scaleway/OVH/Cloudflare R2 EU) for
  uploads, LoRA files, and generated images. Encryption at rest; lifecycle rules for
  retention/deletion.
- **Payments:** **Stripe** (one-time token purchases), **Stripe Tax** for EU VAT, EU methods
  (iDEAL/SEPA/cards), **PSD2/SCA**. Token ledger in Postgres.
- **AI infrastructure (the core):**
  - **Compute in the EU for GDPR** — either self-hosted GPUs on an **EU cloud** (Scaleway/OVHcloud,
    or RunPod EU region) running a **ComfyUI/diffusers** serving layer, or a managed API **only
    with a signed DPA and EU data residency**. For an EU-first privacy brand, EU-hosted
    inference/training is the safer default.
  - **Base model + licensing (decision needed):** FLUX.1 [dev] has the most mature LoRA tooling
    **but its weights are non-commercial** — commercial use needs a **Black Forest Labs license**,
    or use **FLUX.1 [pro] via API**, or a commercially-licensed **SDXL**-family model. This choice
    affects cost and legal posture.
  - **Pipeline:** per-user **LoRA (identity)** + **ControlNet (OpenPose/Depth)** driven by the
    template's B&W composition, applied for the first ~50–65% of denoising then released (avoids
    the "plastic/pencil-sketch" look), + an **upscaler** (Real-ESRGAN/SUPIR) for the upres step.
  - **Template engine:** JSON scene recipe → prompt compiler + control-map selection; structured
    UI controls map to JSON fields.
  - **Quality control:** automated **face-similarity check** (ArcFace cosine ≳0.65),
    **broken-image detection**, and the **NSFW/underage classifier** gate. Reject bad candidates
    before the user sees them.
  - **AI Act marking:** **C2PA / invisible watermark** on all outputs.
- **Async jobs & notifications:** a job queue (e.g., Redis + worker) for training and generation;
  **email (Resend/Postmark) + push** on completion.
- **Ops:** logging/metrics, backups, per-user data-deletion routines, abuse/audit logs.

## 8. Financial model

**Monetization:** one-time **credit (token)** purchases; **no subscription**; **credits don't
expire**. Revenue = **training** + **upres** (previews are cheap/soft-free).

**Illustrative token economy** (tune to taste):

- 1 credit ≈ **€0.12** list; bundles: **100/€15**, **350/€45**, **1000/€99** (volume discount).
- **Free on signup:** ~25 credits + a base LoRA.
- **Prices:** Train standard **80 cr**, high-fidelity **150 cr**, max **250 cr**; **Upres (final
  image) 10 cr**; **preview batches free** (low-res, watermarked, soft-rate-limited).

**Unit economics (COGS from current API rates):**

| Action | Your cost | Price (credits → €) | Gross margin |
| --- | --- | --- | --- |
| LoRA train (standard) | ~$2 | 80 cr ≈ €9.6 | ~80% |
| LoRA train (high/max) | ~$3–5 | 150–250 cr | ~80% |
| Preview (4 low-res imgs) | ~$0.02–0.10 | free (CAC) | — |
| Upres (final image) | ~$0.06–0.15 | 10 cr ≈ €1.2 | ~90% |

Blended gross margin **~85%+**.

**ARPU:** first purchase ≈ training (~€10) + ~15 upres (~€15) ≈ **€25**; repeat buyers higher.

**Cost structure (lean/solo, monthly):** EU GPU/API €500–1,500 (semi-variable), storage/CDN
€50–150, Stripe ~3–4% of revenue, tooling/email/monitoring €100–200, one-time legal/DPO/DPIA setup
€1–3k, marketing (variable). Baseline fixed ≈ **€1.5–3k/mo**.

**Break-even:** at ~85% margin and ~€25 ARPU (contribution ~€21), covering €3k fixed ≈ **~145
paying customers/month**.

**Key financial guardrail:** free previews have real COGS. Mitigate with **low-res + watermark +
daily soft caps**, and rely on the fact that anyone who wants their photos will upres. Monitor
"preview-to-upres" conversion as a core metric; if abuse appears, add a tiny preview micro-cost
after the free tier.

## 9. SEO & go-to-market

SEO is the **proven** channel (Aragon and DatePhotos grew almost entirely on search), but it's
**saturating** and AI Overviews are compressing clicks — so pair it with other levers:

- **SEO / programmatic pages:** rank for "AI dating photos," "Tinder/Hinge/Bumble photos," "how to
  get more matches," plus city/scenario landing pages. Tool/landing pages convert; generic blog
  posts often don't — prioritize conversion pages over content volume.
- **Affiliate (Aragon's highest-ROI move):** pay "best AI dating photo" roundup sites/creators on
  commission.
- **Community & creators:** male-dating YouTube/TikTok coaches, Reddit (authentic, non-spammy),
  before/after demos (inherently shareable).
- **Activation loop:** the **free credits + base LoRA** is the strongest conversion mechanic — "try
  it on your own face before paying."
- **Trust content:** "verification-safe," "passes Face Check," "your data stays in the EU."

## 10. Privacy, legal & compliance (EU-first)

- **GDPR Article 9 (biometric):** training on a user's face is special-category data → **explicit,
  granular, contextual consent** at the training step (plus general T&C at signup), **recorded**
  immutably; strict **purpose limitation** (dating only); no shared-model training.
- **Data controls in Account/Settings:** delete model(s), **erase all data**, **export data**
  (portability), **withdraw consent**. Deletion must remove the **LoRA + training images +
  generations**.
- **Retention & residency:** defined retention windows, auto-deletion, **EU hosting** for storage
  *and* compute, DPAs with any vendor, **DPIA** on file, encryption at rest.
- **EU AI Act Art. 50** (from 2 Aug 2026): **mark generated images as AI** (C2PA/watermark).
- **Age assurance:** **hard self-declared 18+ gate** + **underage-image detection**. Per current
  scope, **no legal-document/ID verification** at MVP; some markets may later expect stronger age
  assurance — revisit on expansion.
- **Content policy:** **strictly no NSFW** (also keeps Stripe happy and simplifies compliance).

## 11. Trust & safety / abuse prevention

- **"Prove it's you" (MVP):** affirmation checkbox + **NSFW/underage classifier** blocking
  disallowed uploads. Residual risk: a checkbox won't stop a determined user training on an
  ex/celebrity — so also rely on **T&C, watermarking, abuse reporting, and audit logs**, and be
  ready to add **selfie-match verification** if abuse materializes.
- **Output safety:** NSFW output filter; block impersonation; QC rejects broken images.
- **Body-fidelity guardrail:** keep the user's real body proportions to avoid re-introducing the
  catfish problem and to protect the trust promise.

## 12. MVP scope vs. roadmap

**MVP (launch):**

- Accounts + 18+ gate + consent; premium portal.
- Train LoRA (with input QC + safety gate + tiers) → My Models (status/ETA + notify).
- Prompt-driven generation with templates/keywords/free-text → 4 previews → **pay-on-upres** →
  refine/generate-similar → download.
- Library (favorite/delete/download).
- Tokens (Stripe, VAT, no subscription, non-expiring) + free starter credits + base LoRA.
- EU hosting, data controls, watermarking.

**Post-MVP:**

- **Packs** (curated template bundles, one-click batch).
- **Video support.**
- **Profile-building** (Tinder/Hinge/Bumble presets, slot ordering, lead-photo logic).
- **Coaching** (feedback on the set / "what works").
- **Selfie-match verification** (if/when needed).

## 13. Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Commoditization / base-model parity | Moat on template library + control UX + EU privacy + trust, not raw fidelity alone |
| Platform risk (Match/Bumble build it; policy tightening) | Lean into verification-safe positioning; own the EU/privacy niche |
| SEO saturation | Diversify to affiliate + creators + free-trial loop |
| Model licensing (FLUX dev non-commercial) | Resolve base-model/license before launch |
| Free-preview COGS abuse | Low-res/watermark/soft caps; watch preview→upres conversion |
| Reputational (catfishing/AI backlash) | "Best real you" framing + body fidelity + watermarking |
| Compliance load (Art. 9 / AI Act) | Build consent/erasure/marking in from day one |

## 14. Open decisions & next steps

1. **Base model + license:** FLUX (pro/API or licensed dev) vs. commercially-licensed SDXL.
2. **Compute:** self-hosted EU GPUs vs. EU-region managed API + DPA.
3. **Token values:** confirm credit price, tier costs, and upres price (§8 is a starting point).
4. **Preview policy:** fully free vs. soft-capped vs. tiny micro-cost after a daily free allowance.
5. **Primary launch market:** EU-first for compliance/brand, with US as fast-follow.

**Recommended next deliverables:**

- **JSON template schema** (the heart of the differentiation) — see `docs/templates/`.
- **Site map + key-screen wireframes** for the premium portal and generation flow.

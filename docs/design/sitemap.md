# Visagely — Sitemap

Information architecture for the site: a **public marketing surface** (unauthenticated, SEO/trust)
and the **authenticated portal** with value actions front-and-center.

![Visagely sitemap](renders/sitemap.png)

> Source: [`sitemap.html`](sitemap.html) (rendered with headless Chrome).

## Diagram

```mermaid
graph TD
  ENTRY["visagely.com"]

  subgraph PUBLIC["Public site — unauthenticated"]
    HOME["Home / Landing"]
    HIW["How it works"]
    GAL["Sample gallery"]
    PRICE["Pricing — Tokens"]
    FAQ["FAQ"]
    LEGAL["Privacy & Legal"]
    LEGAL --> PP["Privacy Policy"]
    LEGAL --> TC["Terms & Conditions"]
    LEGAL --> AIDATA["AI & Data Use (Art. 50)"]
    LEGAL --> COOK["Cookie Policy"]
    AUTH["Sign up / Log in — 18+ gate + consent"]
  end

  subgraph PORTAL["Portal — authenticated"]
    DASH["Portal Home / Dashboard — free starter tokens + base LoRA"]
    TRAIN["Value 1 · Train a LoRA"]
    TRAIN --> TRAINFLOW["Upload → QC (fidelity/size + NSFW/underage) → 'it's me' → tier (tokens) → consent → start"]
    GEN["Value 2 · My Models → Generate"]
    GEN --> GENFLOW["Template/keywords/prompt → 4 previews → pick → upres (pay) → refine / generate similar → download"]
    LIB["Value 3 · Library — favorite / delete / download"]
    TOKENS["Utility · Buy Tokens — Stripe, EU VAT, non-expiring"]
    ACCT["Utility · Account & Settings"]
    ACCT --> DATACTRL["Data controls — export · delete model · delete all · withdraw consent"]
    ACCT --> NOTIF["Notifications — email / push"]
    PLEGAL["Utility · Privacy & Legal (shared)"]
  end

  ENTRY --> PUBLIC
  ENTRY --> PORTAL
  AUTH --> DASH
  DASH --> TRAIN
  DASH --> GEN
  DASH --> LIB
  TRAIN -. "on complete (notify)" .-> GEN
```

## Page tree

### Public site (unauthenticated)

- **Home / Landing** — hero, promise ("best real version of you"), social proof, primary CTA.
- **How it works** — Train → Generate → Download; verification-safe explainer.
- **Sample gallery** — before/after and curated example scenes.
- **Pricing — Tokens** — bundles, no subscription, tokens don't expire.
- **FAQ** — privacy, Face Check, realism, refunds.
- **Privacy & Legal** — Privacy Policy · Terms & Conditions · AI & Data Use (Art. 50 disclosure) ·
  Cookie Policy.
- **Sign up / Log in** — hard 18+ age gate, explicit consent capture, OAuth + email.

### Portal (authenticated)

- **Portal Home / Dashboard** — free starter tokens + base LoRA on first entry; value actions
  front-and-center.
- **Value 1 · Train a LoRA** — upload photos → QC (fidelity/size + NSFW/underage block) → "it's me"
  checkbox → choose tier (tokens) → consent → start.
- **Value 2 · My Models → Generate** — trained + in-progress models with ETA (email/push on
  completion) → generation: template / keywords / free prompt → 4 previews → pick favorite → upres
  (pay tokens) → refine / generate similar → download.
- **Value 3 · Library** — all images; favorite / delete / download.
- **Utility · Buy Tokens** — Stripe checkout, EU VAT, iDEAL/SEPA/cards, non-expiring.
- **Utility · Account & Settings** — profile; notifications (email/push); data controls (export,
  delete model, delete all data, withdraw consent).
- **Utility · Privacy & Legal** — shared with public policies + consent records.

## Post-MVP additions

Packs (curated template bundles) · Video support · Profile builder (app presets, slot ordering) ·
Coaching.

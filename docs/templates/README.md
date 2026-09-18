# Visagely Template Library

The template library is Visagely's core differentiator. A **template is not a photo** — it is a
reusable, rights-clean **scene recipe** that pairs:

1. one or more **black-and-white composition control maps** (pose / depth / edges / segmentation /
   luminance), and
2. a structured **JSON description** of the scene, colors, subject placement, clothing, emotion,
   and pose.

At generation time the recipe is combined with the user's **personal identity LoRA** and compiled
into a positive/negative prompt plus a ControlNet configuration. This is what lets Visagely produce
*interesting, controllable, high-fidelity* compositions instead of the repetitive output typical of
pure IP-Adapter/InstantID pipelines.

## Files

- `template.schema.json` — the JSON Schema (draft 2020-12) every template must validate against.
- `examples/golden-hour-beach.json` — full-body outdoor example (depth + openpose control).
- `examples/city-evening-restaurant.json` — seated medium portrait example (depth control).

## The three inputs at generation time

| Input | Source | Controls |
| --- | --- | --- |
| **Identity** | User's trained LoRA (`{trigger}` word) | Who the person is |
| **Structure** | Template `control[]` maps via ControlNet | Pose, placement, composition |
| **Semantics** | Template JSON compiled into the prompt | Scene, clothing, lighting, emotion, colors |

### Why multiple control maps

A single B&W image cannot cleanly encode pose *and* placement *and* lighting at once, because
those are different ControlNet signals:

- `openpose` → locks the **pose** (skeleton).
- `depth` → locks **placement** and 3D scene geometry.
- `canny` → locks **edges/architecture** (great for scenes; can fight identity if applied to the
  person).
- `segmentation` → locks **region layout** (subject here, background there).
- `luminance` → drives **tonal/lighting** blocking.

Templates may therefore carry a small **stack** of control maps (e.g. `depth` for composition +
`openpose` for pose), each with its own `strength` and `endPercent`.

### The `endPercent` release trick

ControlNet is applied only for the first part of denoising, then **released** so identity, skin,
and hair form naturally. Holding structure for the full run produces a "pencil-sketch / plastic"
look. Recommended range: `endPercent` ≈ **0.5–0.65**.

## Prompt compilation

`promptTemplate.positive` contains placeholders in braces that are substituted at generation time:

- `{trigger}` → the user's LoRA trigger word (identity).
- any editable field path, e.g. `{clothing.style}`, `{expression.label}`, `{clothing.colors}`.

Example (from `golden-hour-beach.json`):

```
candid full-body photo of {trigger}, {clothing.style} outfit, {pose.description},
on a sunlit sandy beach at golden hour, warm backlight, soft bokeh ocean horizon,
{expression.label}, natural skin texture, shot on 50mm f/2.0, photorealistic
```

With `{trigger} = "a1b2c3 man"`, `{clothing.style} = "smart casual"`,
`{expression.label} = "subtle_smile"`, this resolves to a concrete prompt while the `depth` +
`openpose` maps lock the composition and pose.

## Editable fields → UI controls

`editableFields` lists the JSON paths a user may override in the UI (dropdowns/sliders). This is
how the recipe becomes **flexible without forcing users to write prompts**: e.g. exposing
`clothing.style`, `expression.label`, `expression.intensity`, and `scene.timeOfDay` as controls.
Power users can still free-form prompt; everyone else adjusts structured knobs.

## Rights & safety

- `provenance.source` must be one of `ai_generated`, `regenerated_from_reference`, or
  `original_authored`. Prefer AI-generated / originally-authored compositions. If a reference
  inspired the composition, treat it as inspiration only — do not reproduce a recognizable
  copyrighted image.
- `safety.sfwOnly` is always `true`.
- `datingContext.verificationSafe` should stay `true`: compositions must preserve the user's real
  identity and body so outputs pass biometric Face Check and do not misrepresent the user.

## Validation

Validate any template against the schema with a JSON Schema validator, e.g. `ajv`:

```sh
npx ajv-cli validate -s docs/templates/template.schema.json \
  -d "docs/templates/examples/*.json" --spec=draft2020
```

## Authoring a new template (checklist)

1. Create/generate the B&W control map(s); upload to EU object storage; note `assetUri`(s).
2. Fill in `scene`, `palette`, `lighting`, `subject`, `pose`, `clothing`, `expression`, `camera`.
3. Write `promptTemplate.positive` / `.negative` with `{trigger}` and editable-field placeholders.
4. Set `generation` params for the target base model.
5. Choose `editableFields` to expose in the UI.
6. Set `provenance` and `safety`; keep `verificationSafe: true`.
7. Validate against the schema, then move `status` to `review` → `published`.

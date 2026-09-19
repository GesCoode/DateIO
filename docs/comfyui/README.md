# Visagely — ComfyUI pipeline (RTX 2070 + vast.ai)

This is the first working stack for the product: **per-user identity LoRA + template-driven
generation**. Hardware is split on purpose.

| Machine | GPU | Use it for | Do not use it for |
| --- | --- | --- | --- |
| Local | RTX 2070 **8 GB**, Turing, **32 GB RAM** | Dataset prep, GGUF FLUX generation, LoRA *inference*, ControlNet *preprocess* | Serious FLUX LoRA **training**, 1024² + ControlNet + LoRA together |
| vast.ai | **24 GB** (RTX 4090 / 3090 24 GB / A5000) | FLUX LoRA training, ControlNet generation, quality iteration | Leaving it running overnight empty (you still pay) |

The 2070 is Turing: **no native bfloat16**. Always use **fp16 / fp8 / GGUF**. Community reports
confirm FLUX LoRA *can* train on a 2070 at ~7.5 s/it, but it is overnight-slow and OOM-fragile.
Use it to learn the graph; rent 24 GB when you actually care about the weights.

**License reminder:** `FLUX.1 [dev]` is **non-commercial**. Fine for prototyping. Production later
needs a BFL license or `FLUX.1 [pro]` via API.

---

## 1. What we are building this week

A closed loop you can run end-to-end:

```
selfies  →  captions  →  identity LoRA  →  generate with trigger word
                                           →  (vast) ControlNet pose/depth from a template
                                           →  pick 4  →  upscale one
```

That maps to the product: Train → My Models → Generate → pay-on-upres.

---

## 2. Local ComfyUI — get FLUX generating tonight

### 2.1 Launch flags (Windows)

If you use the portable build, edit `run_nvidia_gpu.bat` (or add a shortcut) so ComfyUI starts
with low VRAM:

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --lowvram --preview-method auto
```

`--lowvram` is mandatory on 8 GB. Close Chrome hardware-accel / Discord overlay / anything else
on the GPU before queueing.

### 2.2 Custom nodes (ComfyUI Manager)

Install these, then restart:

| Node pack | Why |
| --- | --- |
| **ComfyUI-GGUF** (`city96`) | Run FLUX on 8 GB |
| **ComfyUI-Manager** | already have, hopefully |
| **comfyui_controlnet_aux** (`Fannovel16`) | OpenPose / Depth preprocessors for templates |
| **ComfyUI-FluxTrainer** (`kijai`) | Optional local trainer experiments |

### 2.3 Models — local 8 GB set

Download into the folders in [`models.md`](models.md). Minimum to generate:

- UNET GGUF: `flux1-dev-Q4_K_S.gguf` → `models/unet/`
- T5 GGUF (not fp16 — fp16 T5 alone is ~9 GB): `t5xxl_fp8_e4m3fn.safetensors` **or** a T5 GGUF → `models/clip/` / `models/text_encoders/`
- CLIP-L: `clip_l.safetensors` → `models/clip/`
- VAE: `ae.safetensors` → `models/vae/`

Accept the **FLUX.1 [dev] license** on Hugging Face first (`black-forest-labs/FLUX.1-dev`), then
download `ae.safetensors`.

### 2.4 First generation (no LoRA)

1. Drag [`workflows/local-2070-flux-gguf.json`](workflows/local-2070-flux-gguf.json) onto the
   ComfyUI canvas (or **Load**).
2. If a node is red, install the missing pack and reload.
3. Point the GGUF / CLIP / VAE loaders at the files you downloaded.
4. Queue **one** 768×1024 image, 20 steps, cfg **1**, FluxGuidance **3.5**.

If it OOMs: drop to `768×768`, or switch the UNET to `Q3_K_S` / `Q4_0`. If T5 is fp16, that is
almost always the cause — swap it.

### 2.5 First generation *with* a LoRA

After you have a `.safetensors` LoRA (from vast.ai, or a public FLUX character LoRA to test the
graph):

- Load [`workflows/local-2070-flux-gguf-lora.json`](workflows/local-2070-flux-gguf-lora.json)
- LoRA strength **0.8–1.0**
- Put the **trigger word first** in the prompt

GGUF + standard LoRA loader works in current ComfyUI-GGUF. IP-Adapter does **not** — we are not
using it.

---

## 3. Dataset — do this locally before you rent a GPU

Folder convention (also in `datasets/identity-v1/`):

```
datasets/identity-v1/
  images/
    001.jpg
    001.txt          ← caption, same stem
    002.jpg
    002.txt
    ...
  dataset.toml       ← kohya / FluxTrainer
```

**How many:** 15–25 curated photos. Quality beats volume.

**Shot mix (this is what makes faces hold):**

| Shot | Count | Why |
| --- | --- | --- |
| Extreme close-up (eyes/nose fill the frame) | 4–6 | Identity lock |
| Head & shoulders | 8–10 | Default dating lead |
| 3/4 / medium (chest-up) | 4–6 | Body + head relationship |
| Full body, uncropped feet | 3–5 | Stops “your face on someone else’s body” |

**Rules:**

- Only **you**, 18+, no sunglasses, no other faces, no heavy beauty filters
- Varied light (window, indoor warm, overcast outdoor) and expressions (neutral, slight smile)
- Same person across days is good; same shirt on every shot is bad
- Export **JPEG or PNG**, longest side **1024–2048**, faces in focus
- NSFW / nudes stay **out** (product policy + trainer collapse)

**Caption recipe** — natural language, trigger first, omit things you want the model to *vary*
(clothing, scene) when possible:

```
vsgly_id, a man with short dark wavy hair and a short beard, brown eyes, facing camera, close-up portrait, indoor window light
```

Use **one unique trigger** (`vsgly_id` or similar). Do not use `person` / `man` as the trigger.

A filled example caption set lives in [`datasets/identity-v1/README.md`](datasets/identity-v1/README.md).

---

## 4. vast.ai — train the LoRA (first paid session)

Budget: a 4090 is often ~$0.30–0.50/hr on-demand. A character LoRA is **30–90 minutes** of
training plus download time. First session should cost a few dollars if you destroy the instance
when done.

### 4.1 Rent

1. [vast.ai console](https://cloud.vast.ai/) → **Templates** → official **ComfyUI** *or* **FluxGym**.
2. GPU: **24 GB+** (RTX 4090, RTX 3090 24 GB, RTX A5000). Filter **On-Demand** for the first run
   (interruptible is cheaper but can kill a train).
3. Disk: **80–120 GB** is enough for FLUX fp8 + one LoRA train. 200 GB if you also want Union
   ControlNet + upscaler.
4. Open the instance portal → ComfyUI / Jupyter / FluxGym.

**EU note:** vast.ai hosts are worldwide. Fine for personal prototyping. Production later needs
**EU-region GPUs** for the privacy promise — do not bake “any host” into the product.

### 4.2 Train (FluxGym is the fastest path)

FluxGym = Kohya `sd-scripts` with a Gradio UI. Upload `datasets/identity-v1/images/`, set:

| Setting | Value |
| --- | --- |
| Base | FLUX.1-dev (fp8 is fine) |
| Repeat / epochs | ~15 images × 10–15 repeats, or **1500–2000 steps** |
| Resolution | 512 or 768 (1024 if 24 GB is comfortable) |
| Network dim / alpha | **16 / 16** to start; 32/16 if faces are still soft |
| LR | `1e-4` AdamW8bit, **cosine** scheduler |
| Batch | 1 |
| Trigger | `vsgly_id` |
| Precision | fp16 if the host GPU is Turing; bf16 on 30-series / 40-series |

Download the `.safetensors` the moment training finishes. Copy it to local
`ComfyUI/models/loras/`.

### 4.3 Alternative: ComfyUI-FluxTrainer on the same box

Use the settings in [`training/fluxtrainer-24gb.json`](training/fluxtrainer-24gb.json). Same
numbers as above; `blocks_to_swap` can stay **0** on 24 GB.

### 4.4 Generate with ControlNet (vast, not 2070)

On 24 GB, load
[`workflows/vast-flux-lora-union-controlnet.json`](workflows/vast-flux-lora-union-controlnet.json):

- Identity: your LoRA
- Structure: InstantX / Shakker **Union** ControlNet
  - mode **4 = pose** (OpenPose skeleton)
  - mode **2 = depth** (placement)
- Strength **0.55–0.7**, **end_percent ~0.55–0.65** (release so skin/hair form naturally)
- 1024×1024 or 768×1024, 24–28 steps, FluxGuidance 3.5

This is the product generation path: template control map + JSON-compiled prompt + LoRA.

ControlNet **plus** GGUF FLUX on 8 GB is optional/experimental — expect OOM. Keep that graph on
vast.ai.

---

## 5. Suggested order this weekend

1. **Tonight, local:** FLUX GGUF generates *anything* on the 2070.
2. **Tonight, local:** shoot / cull 15–25 photos, write captions.
3. **Next session, vast.ai:** train `vsgly_id` LoRA, download it, **destroy the instance**.
4. **Back local:** generate 4 previews with the LoRA (no ControlNet).
5. **Second vast session:** ControlNet pose/depth + LoRA, save 4 + 1 upscale. That is the MVP
   generate loop.

Do not start with video, packs, or IP-Adapter.

---

## 6. Quality bar (before you call a LoRA “good”)

Generate 8 seeds of a **close-up** and 8 of a **new scene the dataset never showed**.

- Face still reads as you on a new background → keep it
- Same shirt / same room leaking into every scene → captions were too specific or rank too high
- Plastic skin / melted ears → lower LoRA strength, or retrain with more close-ups and cosine LR
- Face Check test later: live selfie vs generated close-up should still be the same person

---

## 7. Files in this folder

| Path | What |
| --- | --- |
| [`models.md`](models.md) | Exact files + Hugging Face URLs |
| [`datasets/identity-v1/`](datasets/identity-v1/) | Dataset layout + caption rules |
| [`training/`](training/) | FluxTrainer / FluxGym settings |
| [`workflows/`](workflows/) | Importable ComfyUI API-format graphs |
| [`vastai/provision.sh`](vastai/provision.sh) | Optional first-boot downloads on a ComfyUI instance |

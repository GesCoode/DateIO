# Visagely — ComfyUI pipeline (RTX 2070 + vast.ai)

This is the first working stack for the product: **per-user identity LoRA + template-driven
generation**. Hardware is split on purpose.

| Machine | GPU | Use it for | Do not use it for |
| --- | --- | --- | --- |
| Local | RTX 2070 **8 GB**, Turing, **32 GB RAM** | Dataset prep, GGUF FLUX generation, LoRA *inference*, ControlNet *preprocess* | Serious FLUX LoRA **training**, 1024² + ControlNet + LoRA together |
| vast.ai | **RTX 6000 Ada 48 GB** (or 4090 24 GB) | FLUX LoRA training, ControlNet generation, fidelity + reference experiments | Leaving it running overnight empty (you still pay) |

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

Budget: a 4090 is often ~$0.30–0.50/hr on-demand; **RTX 6000 Ada 48 GB** listings in this range
are ~$0.60/hr. A FLUX identity LoRA is **~3–4.5 hours of training** plus ~20–40 min setup
(~$2.50–$3.50 if you destroy the instance when done). SDXL jobs from the old notes were faster;
do not use those time estimates.

**VRAM vs download speed:** pick VRAM (and GPU generation). A full FLUX stack is ~30–40 GB of
downloads. At ~500 Mbps that is ~10 minutes (~$0.10). At ~5 Gbps it is ~1 minute. Experimentation
hours dominate; one OOM or a 7× slower Turing card costs more than a slow download ever will.

### 4.1 Which GPU (from the current listings)

| Listing | Pick? | Why |
| --- | --- | --- |
| **RTX 6000 Ada · 48 GB · ~81 TFLOPS · ~$0.60/hr** | **Yes — default** | Ada (bf16), 48 GB so FLUX fp16 + LoRA train + Union ControlNet + 1024² without swapping. This is “experiment freely.” Downlink ~0.5 Gbps is fine. |
| Q RTX 8000 · 48 GB · ~12 TFLOPS · ~$0.27/hr | Budget backup only | Same 48 GB but **Turing** (no bf16, ~7× less compute). Cheap overnight jobs, not a playground. |
| CMP 170HX · 64 GB · ~14 TFLOPS | No | Mining SKU, weak PCIe (~6 GB/s), flaky CUDA/ML support. |
| GB10 · 119 GB unified · ARM Cortex | No | NVIDIA GB10 / DIGITS-class **ARM**. ComfyUI custom nodes and PyTorch wheels will fight you. |

If a **24 GB Ada 4090** appears cheaper than the 6000, it is enough for LoRA train + one ControlNet.
Prefer the **48 GB 6000 Ada** while you are still changing graphs every ten minutes.

### 4.2 Rent

1. [vast.ai console](https://cloud.vast.ai/) → **Templates** → official **ComfyUI** *or* **FluxGym**.
2. GPU: **RTX 6000 Ada 48 GB** (or 4090 24 GB). Filter **On-Demand** for the first run
   (interruptible is cheaper but can kill a train).
3. Disk: **80–120 GB** is enough for FLUX fp8 + one LoRA train. 200 GB if you also want Union
   ControlNet + upscaler.
4. Open the instance portal → ComfyUI / Jupyter / FluxGym.

Existing work on the laptop (`…\Desktop\Visagely\Laptop`) — zip the dataset (not the whole
OneDrive tree), upload to the instance. Do not train off a live OneDrive folder.

**EU note:** vast.ai hosts are worldwide. Fine for personal prototyping. Production later needs
**EU-region GPUs** for the privacy promise — do not bake “any host” into the product.

### 4.3 Train (Kohya)

Do **not** `apt upgrade` or install NVIDIA drivers; the vast template already has CUDA.

**FLUX identity LoRA** uses `kohya-ss/sd-scripts`:

- [`training/kohya-flux-identity.md`](training/kohya-flux-identity.md)
- [`training/prior-notes-audit.md`](training/prior-notes-audit.md)
- paste-ready: [`training/kohya-flux-48gb.sh`](training/kohya-flux-48gb.sh)

**Krea 2 identity LoRA** uses `kohya-ss/musubi-tuner` (not sd-scripts). Train on Raw, run on Turbo:

- [`training/kohya-krea2-raw.md`](training/kohya-krea2-raw.md)
- paste-ready: [`training/kohya-krea2-raw.sh`](training/kohya-krea2-raw.sh)

On a box that is already set up:

```bash
bash /workspace/krea2_train/start.sh
```

FLUX on a fresh box:

```bash
# after photos are in /workspace/flux_train/vsgly_id/  (photo_##.png + photo_##.txt)
bash docs/comfyui/training/kohya-flux-48gb.sh setup
bash docs/comfyui/training/kohya-flux-48gb.sh config   # the two TOML files
tmux new -s lora
bash docs/comfyui/training/kohya-flux-48gb.sh retrain
```

| Setting | Value |
| --- | --- |
| Script | `flux_train_network.py` (`networks.lora_flux`) |
| Base | FLUX.1-dev **bf16** (48 GB — no fp8, no block swap) |
| dim / alpha | **16 / 16** (not kohya’s example alpha=1) |
| Steps | **2000**, save / sample every **250** |
| LR | `1e-4` AdamW8bit, warmup 100, `flux_shift` |
| Batch / reso | 1 / **1024** buckets |
| TE | unet-only + cached T5/CLIP (do not train T5) |
| Trigger | `vsgly_id` |

Expect **5–8 s/it** and likeness around **step 500–750**; keep the **1000–1500** checkpoint more often than 2000. Download `.safetensors` before destroying the instance.

FluxGym is the same trainer with a UI if you would rather click than paste. Ostris AI-Toolkit is the fallback (that is the run that already hit likeness at 500).

### 4.4 Alternative: ComfyUI-FluxTrainer on the same box

Use the settings in [`training/fluxtrainer-24gb.json`](training/fluxtrainer-24gb.json). Same
numbers as above; `blocks_to_swap` can stay **0** on 24 GB.

### 4.5 Generate with ControlNet (vast, not 2070)

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

## 5. Phased plan (agreed)

This is the product order. Do not skip identity lock to chase story prompts.

1. **Identity LoRA** — cull the `Visagely\Laptop` set (plus new shots if needed) to 15–25
   photos, caption, train `vsgly_id` on vast. Download the `.safetensors` immediately.
2. **Fidelity workflows** — same person, new clothes/light/background. Close-up + unseen
   scene tests (section 6). Tune LoRA strength, Union ControlNet `end_percent`, guidance.
   Stay here until a stranger would still say it is you.
3. **Story / “special sauce”** — great date photos as *structure* (pose/depth/composition
   maps) plus the identity LoRA. The reference picture supplies the scene grammar; the LoRA
   supplies the face. This is not IP-Adapter FaceID.
4. **Narrow the stack** — keep only what survived: likely FLUX + identity LoRA + Union
   ControlNet (pose/depth) + JSON template. Drop InstantID / IP-Adapter unless a specific
   shot type still needs them.
5. **Try the 2070 again** — LoRA *inference* and dataset work belong on the laptop.
   Training + ControlNet + 1024² together probably stay rented. Re-test after the stack is
   frozen; if GGUF + LoRA (no CN) is good enough for previews, only rent for train/upres.

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
| [`WORKFLOW.md`](WORKFLOW.md) | Slow command checklist (this week’s order) |
| [`datasets/identity-v1/`](datasets/identity-v1/) | Dataset layout + caption rules |
| [`training/`](training/) | Kohya FLUX script + identity recipe; FluxTrainer JSON fallback |
| [`workflows/`](workflows/) | Importable ComfyUI API-format graphs |
| [`vastai/provision.sh`](vastai/provision.sh) | Optional first-boot downloads on a ComfyUI instance |
| [`vastai/krea2_server_init/`](vastai/krea2_server_init/) | Laptop script: SSH in, check GPU/disk, install musubi, download Krea 2 (does not train) |

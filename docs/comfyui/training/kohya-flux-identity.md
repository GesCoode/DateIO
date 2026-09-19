# FLUX identity LoRA — Kohya on RTX 6000 Ada 48 GB

Paste-ready trainer: [`kohya-flux-48gb.sh`](kohya-flux-48gb.sh).
This is **kohya-ss/sd-scripts**, not the old bmaltais GUI and not SDXL.

## Time and money (this GPU)

FLUX LoRA is slower than the SDXL jobs in the old notes. Plan for a **half-day session**, not 40 minutes.

| Phase | Wall clock on 6000 Ada | Cost at ~$0.60/hr |
| --- | --- | --- |
| Do **not** `apt upgrade` / install NVIDIA drivers | skip | you would waste 15–30 min |
| Clone sd-scripts + pip | 8–15 min | ~$0.10 |
| Download FLUX.1-dev + CLIP-L + T5 fp16 + AE (~33 GB) | ~8–12 min at ~0.5 Gbps | ~$0.10 |
| Cache latents + T5/CLIP | 2–5 min | — |
| **2000 steps**, batch 1, 1024, no block-swap | **~3–4.5 h** at 5–8 s/it | **~$1.80–$2.70** |
| Samples every 250 steps (3 prompts) | +5–10 min total | — |
| **Whole first session** | **~4–5.5 h** | **~$2.50–$3.50** |

Speed check: after step ~20 the log should read **about 5–8 s/it**. If you see 20+ s/it, something is offloading (block swap, fp8 on a 48 GB card you do not need, or T5 not cached). Stop and fix; do not let it crawl.

Comparable numbers: RTX 5090 Kohya FLUX ~2.9 s/it; A6000-class 16-bit ~8–9 s/it; 4090 often 3–5 s/it. The 6000 Ada sits in the A6000 band, with 48 GB so we skip swapping.

## Quality vs step (what to actually look at)

FLUX binds a face **early**. Your Ostris run already showed likeness around **500**. That is normal, not a miracle.

| Steps | What you should see | Action |
| --- | --- | --- |
| 250 | Trigger does *something*; face is a cousin | Ignore |
| **500–750** | “That’s me” on a close-up. Clothes may still stick | First candidate |
| **1000–1500** | Face holds on a **new** scene/outfit | Usual keepers |
| 2000 | Peak for 15–25 images | Compare vs 1250/1500 |
| 2500+ | Same shirt, same room, plastic skin | Overfit — throw away |

**Always keep every 250-step checkpoint.** The last file is often worse than 1250 or 1500.

After training, generate (ComfyUI, LoRA strength 0.8–1.0, FluxGuidance 3.5, cfg 1):

1. 8 seeds **close-up**, prompt close to the captions.
2. 8 seeds **unseen scene** (café / street / navy overshirt — none of that in the dataset captions).

Pass: a stranger still says it is you on the unseen scene. Fail: every image is the training hoodie. Recaption (drop clothing) and retrain; do not just raise rank.

## Settings (and why not the old ones)

| Knob | This run | Not this |
| --- | --- | --- |
| Script | `flux_train_network.py` | `sdxl_train_network.py` |
| Module | `networks.lora_flux` | `networks.lora`, `lycoris.kohya` |
| dim / alpha | **16 / 16** | kohya example `16 / 1` (16× weaker); LoKR 32; rank 4 miniature |
| LR / optimiser | **1e-4 AdamW8bit** | Prodigy 1.0, SDXL 5e-5, 1e-3 |
| Scheduler | `constant_with_warmup`, 100 steps | cosine-with-restarts is fine too; not required |
| Steps | **2000**, save every **250** | 700 (too short), 2500+ LoKR |
| Batch | **1** | 2–4 is faster per *image* on paper, worse on small face sets |
| Resolution | 1024, buckets on | 512 miniature; 768 only if you OOM (you will not on 48 GB) |
| Precision | **bf16**, no fp8 base, no block swap | `--fp8_base` / `blocks_to_swap` are 8–24 GB tricks |
| TE | **`--network_train_unet_only`** + cache TE outputs | Training T5; `text_encoder_lr=1.0` |
| Flux bits | `timestep_sampling=flux_shift`, `model_prediction_type=raw`, `guidance_scale=1.0` | `min_snr_gamma`, `noise_offset`, `multires_noise` |
| Captions | Natural language, trigger first, **no shuffle**, no dropout (incompatible with TE cache) | WD14 tags, `shuffle_caption` |
| Reg images | none | `--reg_data_dir` |

If close-ups are still soft at 1500–2000: **dim 32 / alpha 16**, more eye-level close-ups, same LR. Do not crank LR.

## Dataset (do this before `train`)

From `C:\Users\jeroe\OneDrive\Desktop\Visagely\Laptop`: zip **images + captions only**, upload, unzip to `/workspace/flux_train/images/`.

```
/workspace/flux_train/images/
  001.jpg
  001.txt
  002.jpg
  002.txt
  ...
```

15–25 photos. Mix: 4–6 extreme close-ups, 8–10 head-and-shoulders, 4–6 three-quarter, 3–5 full body with feet. Several outfits and lights. No sunglasses, no second face, no NSFW, no beauty filters.

Each `.txt` is one line:

```
vsgly_id, a man with short dark wavy hair and a short beard, brown eyes, looking at camera, head and shoulders, overcast outdoor light
```

Caption **stable identity** (hair, beard, eyes) and **this shot’s** framing/light. Leave clothing and place out if you want them to vary. Rewrite any old WD14 tag dumps.

20 images × 10 repeats × batch 1 → 200 steps/epoch → **2000 steps = 10 epochs**. That is the intended math. If you have 16 images, set `num_repeats = 12` in `dataset.toml` so you still land near 2000.

## Commands on the rented box

Hugging Face: accept [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev), then `huggingface-cli login` (or export `HF_TOKEN`).

```bash
# 0) GPU must be Ada / Ampere, ~48 GB, CUDA visible. Do not apt-upgrade.
nvidia-smi

# 1) Get the script from this repo (or scp the training/ folder)
# 2) Put photos in /workspace/flux_train/images/
# 3) Setup once (~20–40 min)
bash kohya-flux-48gb.sh setup

# 4) Train (~3–4.5 h). tmux/screen so an SSH drop does not kill it.
tmux new -s lora
bash kohya-flux-48gb.sh train
```

When a sample at 1000–1500 looks right you can Ctrl+C, copy the matching `.safetensors` off the box, and destroy the instance. Leaving it idle still bills.

## If Kohya fights you

Same knobs in **Ostris AI-Toolkit** (`python run.py config.yaml`): rank 16/16, lr 1e-4, 2000 steps, flux, quantize on, `train_text_encoder: false`. You already proved that path. Do not fall back to SDXL InstantID.

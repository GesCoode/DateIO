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

## Dataset (your layout)

Photos can live in `/workspace/flux_train/zdp/` as `photo_##.png` + `photo_##.txt` (same number).
The script auto-detects `zdp/`, `zpd/`, or `images/`. `photo_01.png` / `photo_01.txt` is a valid pair.

Open the first caption and use **that** trigger in `sample-prompts.txt` (`zpd person` from the old run, or `vsgly_id`). Do not mix triggers.

## Config files (this is what you edit)

Kohya does not use the old GUI JSON on this path. Two TOML files:

| File on the rented box | What it controls |
| --- | --- |
| **`/workspace/flux_train/kohya-flux.toml`** | Rank, alpha, LR, optimiser, steps, precision, Flux flags |
| **`/workspace/flux_train/dataset.toml`** | `image_dir`, `batch_size`, `num_repeats`, resolution, buckets |

Repo copies (source of truth before setup copies them onto the box):

- [`kohya-flux.toml`](kohya-flux.toml)
- [`dataset.toml`](dataset.toml)

```bash
bash kohya-flux-48gb.sh config    # prints both files
nano /workspace/flux_train/kohya-flux.toml
nano /workspace/flux_train/dataset.toml
```

## 120 GB VRAM

You will not OOM at rank 16 / 1024 / batch 2. Extra VRAM is **not** a reason to jump to dim 64 or batch 8 — that overfits a 15–40 image face set.

This profile spends the memory on **speed and stability**:

- full **AdamW** (not 8-bit)
- **`gradient_checkpointing = false`**
- **`full_bf16 = true`**, no fp8, no block swap
- **batch 2** in `dataset.toml`
- **1500 steps** (batch 2 sees each image about as often as 2000 × batch 1)

If you want maximum identity quality over speed, set `batch_size = 1` and `max_train_steps = 2000`.

Expect faster than the 48 GB estimate (often ~3–6 s/it). If it is 20+ s/it, something is still offloading.

## Dataset (do this before `train`)

From `C:\Users\jeroe\OneDrive\Desktop\Visagely\Laptop`: zip **images + captions only**, upload, unzip to `/workspace/flux_train/zdp/` (or `images/`).

```
/workspace/flux_train/zdp/
  photo_01.png
  photo_01.txt
  photo_02.png
  photo_02.txt
  ...
```

15–25 photos. Mix: 4–6 extreme close-ups, 8–10 head-and-shoulders, 4–6 three-quarter, 3–5 full body with feet. Several outfits and lights. No sunglasses, no second face, no NSFW, no beauty filters.

Each `.txt` is one line:

```
vsgly_id, a man with short dark wavy hair and a short beard, brown eyes, looking at camera, head and shoulders, overcast outdoor light
```

Caption **stable identity** (hair, beard, eyes) and **this shot’s** framing/light. Leave clothing and place out if you want them to vary. Rewrite any old WD14 tag dumps.

20 images × 10 repeats × batch 2 → 100 steps/epoch → **1500 steps ≈ 15 epochs**. Edit `num_repeats` / `max_train_steps` in the two TOML files if your `zdp` folder is much larger.

## Commands on the rented box

Hugging Face: accept [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev), then `huggingface-cli login` (or export `HF_TOKEN`).

```bash
# 0) GPU must be CUDA visible. 120 GB is plenty. Do not apt-upgrade.
nvidia-smi

# 1) Photos already in /workspace/flux_train/zdp/photo_##.png +.txt
# 2) Setup once if weights/venv are missing
bash kohya-flux-48gb.sh setup

# 3) Inspect / edit the two TOML files
bash kohya-flux-48gb.sh config
nano /workspace/flux_train/kohya-flux.toml
nano /workspace/flux_train/dataset.toml

# 4) From-scratch train. tmux so an SSH drop does not kill it.
tmux new -s lora
bash kohya-flux-48gb.sh retrain
```

`retrain` = `clean` + `train`. It deletes previous checkpoints, sample folders, and latent/text-encoder `.npz` caches. Photos and the FLUX base weights stay. There is no `--resume` and no `--network_weights`; step 0 is a new LoRA.

If setup already ran and you only want to wipe: `bash kohya-flux-48gb.sh clean`.

When a sample at 1000–1500 looks right you can Ctrl+C, copy the matching `.safetensors` off the box, and destroy the instance. Leaving it idle still bills.

## If Kohya fights you

Same knobs in **Ostris AI-Toolkit** (`python run.py config.yaml`): rank 16/16, lr 1e-4, 2000 steps, flux, quantize on, `train_text_encoder: false`. You already proved that path. Do not fall back to SDXL InstantID.

# Audit of the prior Visagely LoRA notes

What to keep from the old runbook, what to throw away, and why the Kohya
command in `kohya-flux-48gb.sh` looks different from the SDXL recipes.

## Keep (product, not trainer)

| Note | Status |
| --- | --- |
| Safe picture storage, 18+, explicit consent | Product law. Unchanged. |
| No NSFW, no impersonation, no catfishing | Product policy. Unchanged. |
| Trigger word + identity traits in captions | Keep. Use `vsgly_id`, not `ohwx_person` / `zpd person`. |
| ComfyUI for prototyping | Keep. |
| Depth / OpenPose ControlNet | **Later phase** (fidelity → story). Not part of LoRA training. |
| Optional upscaler + face pass | Later, pay-on-upres. Not identity. |
| The FLUX Kohya command (`lora_flux`, dim 16, 1e-4, 1500 steps, `flux_shift`) | Closest old recipe to current practice. |
| Ostris AI-Toolkit run: likeness by **step 500**, loss ~0.49 | Best result you already have. Match those knobs in Kohya. |

## Drop for this train

| Old idea | Why it is worse now |
| --- | --- |
| InstantID / FaceID as the identity path | You already flagged the body problem. InstantID is a face conditioner, not a person model. Dating photos need the whole figure. LoRA is the product. |
| SDXL + FaceDetailer / Adetailer | FaceDetailer hides a weak identity model on full-body shots. FLUX LoRAs hold faces at distance without it. Optional later as an upres pass, not the stack. |
| Face LoRA + Body LoRA + Style LoRA | Three adapters fight. One captioned identity LoRA; style lives in templates. |
| WD14 / BLIP auto-captions as the source of truth | Taggers bake shirt + room into the concept. Manual natural-language captions (LLM draft, then edit) win on FLUX. |
| Regularization images | Rarely used for FLUX character LoRAs; they dilute identity. |
| DoRA, LyCORIS LoKR, `algo=lokr` | Style/architecture adapters. Overfit clothing. Extra deps. |
| Prodigy with `learning_rate=1.0` **and** `unet_lr=1e-4` | Those two recipes contradict each other. Prodigy wants ~1.0; AdamW wants 1e-4. The “NEW” LoKR command mixed both and undertrained. |
| `min_snr_gamma`, `noise_offset`, `multires_noise_*` | SDXL / DDPM tricks. Not Flux-native (flow matching). |
| `shuffle_caption` on FLUX | FLUX wants full sentences, not shuffled SD 1.5 tags. |
| Kohya `network_alpha=1` with `dim=16` | Official example. **16× weaker** than the Ostris 16/16 run that already worked. Use **alpha = dim**. |
| Full DreamBooth of FLUX | Slow, overfits, not the product artifact. LoRA is. |
| `z_image_turbo`, Qwen NSFW checkpoints | Wrong base, and NSFW is policy-forbidden. Do not download onto the rented box. |
| `sudo apt upgrade` + `ubuntu-drivers autoinstall` + reboot | Vast templates already have CUDA. This burns time and can break the image. |
| Diffusers `train_dreambooth_lora_flux_miniature` rank 4 @ 512×768, 700 steps | Too small and too short for a shippable face. |
| The “Claire Hemmings…” paragraph as a **training** caption | Perfect as a *generation* scene recipe. As a training caption it locks café + jacket into the identity. |

## The bug in the two LoKR commands

1. First LoKR: Prodigy + `learning_rate=1.0` + **`text_encoder_lr=1.0`**. That is the Civitai SDXL style recipe. Training CLIP that hard makes the trigger sticky and kills prompt flexibility (every scene still looks like the dataset room).
2. “NEW” LoKR: still Prodigy, but `unet_lr=0.0001` and `text_encoder_lr=0.00005`. Prodigy then barely steps. That is why it felt like it needed 2500 steps and still wandered.

Do not port either to FLUX.

## What actually worked

The Ostris FLUX job (`my_first_flux_lora_v1`, trigger `zpd person`, batch 4, latent cache, samples every 250, likeness ~step 500) is the existence proof. Current (2026) consensus for a FLUX **identity** LoRA is the same shape:

- Base: **FLUX.1 [dev]** (not SDXL, not Schnell, not FLUX.2 for this first train)
- Trainer: **kohya-ss/sd-scripts** `flux_train_network.py` (this is Kohya; the bmaltais GUI is optional)
- Rank **16 / 16**, AdamW8bit, **1e-4**, ~**2000 steps**, **do not train T5**, cache latents + text-encoder outputs
- Natural-language captions, unique trigger first
- Pick a checkpoint from samples, not “the last step”

Ostris is the easier GUI if sd-scripts fights you. Same hyperparameters. You asked for Kohya, so the paste-ready path is `kohya-flux-48gb.sh`.

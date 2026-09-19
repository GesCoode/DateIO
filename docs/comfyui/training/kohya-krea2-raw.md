# Krea 2 Raw identity LoRA — musubi-tuner

This is **kohya-ss/musubi-tuner**, not `sd-scripts` / `flux_train_network.py`.
Train on **Krea 2 Raw**. Run the LoRA on **Turbo** in ComfyUI.

Paste-ready launcher: [`kohya-krea2-raw.sh`](kohya-krea2-raw.sh).

On the rented box, after setup:

```bash
bash /workspace/krea2_train/start.sh
```

That stops ComfyUI and launches training in tmux session `krea2-train`.
Watch with `tmux attach -t krea2-train`.

## Settings

| Knob | This run |
| --- | --- |
| Script | `krea2_train_network.py` |
| Module | `networks.lora_krea2` |
| dim / alpha | 32 / 32 |
| LR / optimiser | 1e-4 AdamW |
| Epochs | 8 × 6 repeats × 55 images ≈ 2640 steps |
| Batch | 1 |
| Resolution | 1024, buckets on |
| Flow | `timestep_sampling=krea2_shift` |
| Trigger | `vsgly_id` first in every caption |

On RTX PRO 6000 96 GB: no gradient checkpointing (speed path). If it OOMs, add `--gradient_checkpointing` and rerun.

## After training

Copy `vsgly_id_krea2_v1*.safetensors` to `ComfyUI/models/loras/`.
Load Turbo UNET + LoRA + Qwen3-VL (type `krea2`) + `qwen_image_vae`. Prompt starts with `vsgly_id`. Turbo: ~8 steps, CFG 1.

# Correct workflow — one page, in order

This replaces the old note dump (SDXL, InstantID, LoKR, Prodigy, `apt upgrade`,
z_image_turbo, NSFW). Do **not** paste those old commands.

**This week is only:** captions → Kohya FLUX identity LoRA (`vsgly_id`) → look
at samples. InstantID, ControlNet, ComfyUI generate, upscaler, product/legal
code — later.

Stop after each block. Do not start the next block until the current one
finished without errors.

Trigger: **`vsgly_id`**. Photo folder name `zdp` is fine.

---

## 0. What from the old notes still applies

| Old note | Now |
| --- | --- |
| Safe storage, 18+, consent, no NSFW, no impersonation, no catfishing | Product rules. Unchanged. Do not download NSFW checkpoints. |
| Kohya trainer | Yes — **`kohya-ss/sd-scripts`**, not the bmaltais GUI, not SDXL. |
| FLUX base | Yes. Not SDXL, not z_image_turbo. |
| ComfyUI | Later, for generating with the LoRA. Not needed to *train*. |
| Depth / OpenPose ControlNet | Later (fidelity → story). |
| InstantID / FaceDetailer / Adetailer | Not the identity path. Optional much later. |
| Face LoRA + Body LoRA + Style LoRA | One identity LoRA. |
| WD14 / BLIP auto-captions | Do not re-run. Edit the `.txt` you already have. |
| `sudo apt update/upgrade`, NVIDIA driver install, reboot | **Skip.** Vast templates already have CUDA. |
| LoKR + Prodigy, DoRA, min_snr, noise offset | Skip. Those are SDXL recipes. |
| Ostris run (likeness ~step 500, `zpd person`) | Proof FLUX works. Same knobs; trigger is now `vsgly_id`. |

2FA, Stripe, watermarking, age estimation, Figma — not this session.

---

## 1. On the rented box — confirm GPU, then wait

```bash
nvidia-smi
```

You want CUDA visible and a lot of VRAM. Then stop. Do not apt-upgrade.

---

## 2. Captions (can be laptop or the box)

Photos: `/workspace/flux_train/vsgly_id/photo_##.png` + `photo_##.txt`.

If captions still say `zdp` / `zdp person` / `zpd person`:

```bash
python3 change_zdp_to_vsgly.py /workspace/flux_train/zdp
head -n 1 /workspace/flux_train/zdp/photo_01.txt
```

Laptop copy of the same folder:

```powershell
python change_zdp_to_vsgly.py "C:\Users\jeroe\OneDrive\Desktop\Visagely\Laptop\TrainingSets\TrainingSix\zdp"
```

First line of `photo_01.txt` must start with `vsgly_id`. Then stop.

---

## 3. Install libraries (Hugging Face is a pip package — install it before login)

Every `pip` / `huggingface-cli` line below must run **after** `source /workspace/kohya_env/bin/activate`.
If that venv is not active, `huggingface-cli` will not exist.

```bash
# 3.1 venv
python3 -m venv /workspace/kohya_env
source /workspace/kohya_env/bin/activate
pip install -U pip wheel

# 3.2 PyTorch with CUDA (large)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# 3.3 Hugging Face CLI  ← this is the missing piece
pip install -U "huggingface_hub[cli]"
huggingface-cli --help

# 3.4 Kohya sd-scripts + its Python deps (also installs huggingface-hub, accelerate, transformers, …)
git clone --depth 1 --recurse-submodules https://github.com/kohya-ss/sd-scripts.git /workspace/sd-scripts
cd /workspace/sd-scripts
pip install -r requirements.txt
```

`requirements.txt` pulls in at least: `accelerate`, `transformers`, `diffusers`, `safetensors`, `bitsandbytes`, `toml`, `einops`, `opencv-python`, `sentencepiece`, `huggingface-hub`, `tensorboard`, `rich`, plus `-e .` (the kohya library itself).

Accept https://huggingface.co/black-forest-labs/FLUX.1-dev then:

```bash
source /workspace/kohya_env/bin/activate
huggingface-cli login
```

---

## 4. Download FLUX weights (only after 3.3 + login)

```bash
source /workspace/kohya_env/bin/activate
mkdir -p /workspace/models/flux
huggingface-cli download black-forest-labs/FLUX.1-dev flux1-dev.safetensors --local-dir /workspace/models/flux
huggingface-cli download black-forest-labs/FLUX.1-dev ae.safetensors --local-dir /workspace/models/flux
huggingface-cli download comfyanonymous/flux_text_encoders clip_l.safetensors --local-dir /workspace/models/flux
huggingface-cli download comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors --local-dir /workspace/models/flux
ls -lh /workspace/models/flux
```

`bash kohya-flux-48gb.sh setup` is the same sequence in one script. It still needs the venv active for later steps, and it will `pip install -U "huggingface_hub[cli]"` before any download. Do not start training until the four files are on disk.

Check before moving on:

```bash
source /workspace/kohya_env/bin/activate
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
ls -lh /workspace/models/flux
```

You should see CUDA `True` and those four weight files. Then stop.

Do **not** download z_image_turbo, Qwen NSFW, or InstantID for this train.

---

## 5. Look at the two config files — do not train yet

```bash
bash kohya-flux-48gb.sh config
# or
nano /workspace/flux_train/kohya-flux.toml
nano /workspace/flux_train/dataset.toml
```

| File | Meaning |
| --- | --- |
| `kohya-flux.toml` | rank 16/16, AdamW, 1e-4, 1500 steps, save every 250, Flux flags |
| `dataset.toml` | `image_dir = "/workspace/flux_train/vsgly_id"`, batch 2, 1024, repeats 10 |

`keep_tokens = 1` because `vsgly_id` is one token.

Then stop.

---

## 6. Train — only after steps 1–5 are done

Use tmux so an SSH drop does not kill it.

```bash
tmux new -s lora
source /workspace/kohya_env/bin/activate
bash kohya-flux-48gb.sh retrain
```

`retrain` = rewrite captions to `vsgly_id` + delete old LoRA caches + start at step 0.

What it actually launches (you do not need to type this if the script runs):

```bash
source /workspace/kohya_env/bin/activate
cd /workspace/sd-scripts
accelerate launch --mixed_precision bf16 --num_cpu_threads_per_process 2 \
  flux_train_network.py \
  --config_file=/workspace/flux_train/kohya-flux.toml \
  --dataset_config=/workspace/flux_train/dataset.toml
```

After ~20 steps the log should show a few seconds per iteration, not 20+.
Checkpoints: `/workspace/flux_train/output/` every 250 steps.
Keep **750 / 1000 / 1250** more often than the last file.

Copy the `.safetensors` off the box before you destroy the instance.

---

## 7. After training (not now)

- Load the LoRA in ComfyUI, strength 0.8–1.0, FluxGuidance 3.5, cfg 1
- 8 close-ups + 8 unseen scenes
- Then ControlNet pose/depth (story). Not InstantID.

---

## Commands from the old notes you should not run

- `sudo apt update && sudo apt upgrade`
- `ubuntu-drivers autoinstall` / reboot
- `git clone https://github.com/bmaltais/kohya_ss.git`
- anything with `sdxl_train_network.py`
- LyCORIS / LoKR / Prodigy / DoRA / `min_snr_gamma` / `noise_offset`
- InstantID install
- `aria2c` / `hf download` of z_image_turbo or Qwen NSFW
- `train_dreambooth_lora_flux_miniature.py` (rank 4, 512×768, 700 steps)

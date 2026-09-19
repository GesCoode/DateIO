#!/usr/bin/env bash
# FLUX.1 [dev] identity LoRA on a 24–48 GB Ada GPU (RTX 6000 Ada / 4090).
# This is kohya-ss/sd-scripts. Do NOT apt-upgrade or install NVIDIA drivers on vast.ai.
#
#   bash kohya-flux-48gb.sh setup    # venv, clone, weights (~20–40 min)
#   bash kohya-flux-48gb.sh clean    # wipe old LoRAs, samples, latent/TE caches
#   bash kohya-flux-48gb.sh train    # 2000 steps from step 0 (no resume)
#   bash kohya-flux-48gb.sh retrain  # clean + train
#
# Env overrides: ROOT, HF_TOKEN, TRIGGER, DIM, MAX_STEPS, OUTPUT_NAME
set -euo pipefail

ROOT="${ROOT:-/workspace}"
SD_SCRIPTS="${SD_SCRIPTS:-$ROOT/sd-scripts}"
VENV="${VENV:-$ROOT/kohya_env}"
MODELS="${MODELS:-$ROOT/models/flux}"
TRAIN="${TRAIN:-$ROOT/flux_train}"
IMAGES="${IMAGES:-$TRAIN/images}"
OUT="${OUT:-$TRAIN/output}"
TRIGGER="${TRIGGER:-vsgly_id}"
DIM="${DIM:-16}"
ALPHA="${ALPHA:-$DIM}"
MAX_STEPS="${MAX_STEPS:-2000}"
SAVE_EVERY="${SAVE_EVERY:-250}"
SAMPLE_EVERY="${SAMPLE_EVERY:-250}"
OUTPUT_NAME="${OUTPUT_NAME:-${TRIGGER}_flux_v1}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

need_gpu() {
  command -v nvidia-smi >/dev/null || { echo "nvidia-smi missing — wrong instance"; exit 1; }
  nvidia-smi
  python3 - <<'PY' || true
import json, subprocess, sys
try:
    import torch
    print("torch", torch.__version__, "cuda", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
except Exception as e:
    print("torch not in this python yet:", e)
PY
}

cmd_setup() {
  need_gpu
  mkdir -p "$MODELS" "$IMAGES" "$OUT" "$TRAIN"

  if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
  fi
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  pip install -U pip wheel

  if ! python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
  fi

  if [[ ! -d "$SD_SCRIPTS/.git" ]]; then
    git clone --depth 1 --recurse-submodules https://github.com/kohya-ss/sd-scripts.git "$SD_SCRIPTS"
  fi
  pip install -r "$SD_SCRIPTS/requirements.txt"
  pip install -U "huggingface_hub[cli]"

  if [[ -n "${HF_TOKEN:-}" ]]; then
    huggingface-cli login --token "$HF_TOKEN" --add-to-git-credential || true
  fi

  download() {
    local repo="$1" file="$2"
    if [[ -f "$MODELS/$file" ]]; then
      echo "have $file"
      return
    fi
    huggingface-cli download "$repo" "$file" --local-dir "$MODELS"
  }

  echo "==> FLUX.1-dev is gated. Accept the license on Hugging Face first."
  download black-forest-labs/FLUX.1-dev flux1-dev.safetensors
  download black-forest-labs/FLUX.1-dev ae.safetensors
  download comfyanonymous/flux_text_encoders clip_l.safetensors
  download comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors

  if [[ ! -f "$TRAIN/dataset.toml" ]]; then
    if [[ -f "$SCRIPT_DIR/../datasets/identity-v1/dataset.toml" ]]; then
      cp "$SCRIPT_DIR/../datasets/identity-v1/dataset.toml" "$TRAIN/dataset.toml"
    fi
  fi
  # Point image_dir at this box
  python3 - <<PY
from pathlib import Path
p = Path("$TRAIN/dataset.toml")
if p.exists():
    text = p.read_text()
    text = text.replace('image_dir = "./images"', 'image_dir = "$IMAGES"')
    p.write_text(text)
    print("dataset.toml image_dir -> $IMAGES")
PY

  if [[ ! -f "$TRAIN/sample-prompts.txt" && -f "$SCRIPT_DIR/sample-prompts.txt" ]]; then
    cp "$SCRIPT_DIR/sample-prompts.txt" "$TRAIN/sample-prompts.txt"
  fi

  echo "==> setup done. Put 15–25 jpg+txt pairs in $IMAGES then: $0 retrain"
}

cmd_clean() {
  echo "==> wiping previous LoRA runs (photos and FLUX base weights stay)"
  rm -rf "$OUT"
  mkdir -p "$OUT"
  # Old paths from the SDXL / first FLUX notes
  rm -rf /home/user/kohya_output /workspace/kohya_output
  rm -rf /home/user/dataset/.cache "$TRAIN/.cache" "$IMAGES/.cache"
  # kohya disk caches sit next to the images; they must go or a recaption is ignored
  if [[ -d "$IMAGES" ]]; then
    find "$IMAGES" -maxdepth 2 \( -name '*.npz' -o -name '*_te.safetensors' -o -name '*_te.npz' \) -delete
  fi
  if [[ -d /home/user/dataset ]]; then
    find /home/user/dataset -name '*.npz' -delete
    find /home/user/dataset -type d -name '.cache' -prune -exec rm -rf {} +
  fi
  echo "==> clean. Next: $0 train  (starts at step 0, no --resume, no old LoRA loaded)"
}

write_dataset_toml() {
  cat > "$TRAIN/dataset.toml" <<EOF
# kohya-ss/sd-scripts FLUX dataset
[general]
shuffle_caption = false
keep_tokens = 1
caption_extension = ".txt"

[[datasets]]
resolution = 1024
batch_size = 1
enable_bucket = true
bucket_no_upscale = true
min_bucket_reso = 640
max_bucket_reso = 1280
bucket_reso_steps = 64

  [[datasets.subsets]]
  image_dir = "$IMAGES"
  num_repeats = 10
EOF
}

cmd_train() {
  need_gpu
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"

  shopt -s nullglob nocaseglob
  local imgs=( "$IMAGES"/*.jpg "$IMAGES"/*.jpeg "$IMAGES"/*.png "$IMAGES"/*.webp )
  shopt -u nocaseglob
  local n="${#imgs[@]}"
  if [[ "$n" -lt 10 ]]; then
    echo "Need >=10 captioned images in $IMAGES (found $n). Zip the Laptop dataset and upload."
    exit 1
  fi
  local missing=0
  local img stem
  for img in "${imgs[@]}"; do
    stem="${img%.*}"
    if [[ ! -f "${stem}.txt" ]]; then
      echo "missing caption: ${stem}.txt"
      missing=1
    fi
  done
  if [[ "$missing" -eq 1 ]]; then
    echo "Every image needs a same-stem .txt caption starting with ${TRIGGER}"
    exit 1
  fi

  for f in flux1-dev.safetensors clip_l.safetensors t5xxl_fp16.safetensors ae.safetensors; do
    [[ -f "$MODELS/$f" ]] || { echo "missing $MODELS/$f — run: $0 setup"; exit 1; }
  done

  write_dataset_toml
  mkdir -p "$OUT"
  if [[ ! -f "$TRAIN/sample-prompts.txt" ]]; then
    cp "$SCRIPT_DIR/sample-prompts.txt" "$TRAIN/sample-prompts.txt"
  fi

  echo "==> FROM SCRATCH  $n images  dim=$DIM alpha=$ALPHA  steps=$MAX_STEPS  name=$OUTPUT_NAME"
  echo "    no --resume, no --network_weights, caches rebuilt"
  echo "    expect ~5–8 s/it on RTX 6000 Ada → ~3–4.5 h for 2000 steps"
  cd "$SD_SCRIPTS"

  accelerate launch --mixed_precision bf16 --num_cpu_threads_per_process 2 \
    flux_train_network.py \
    --pretrained_model_name_or_path="$MODELS/flux1-dev.safetensors" \
    --clip_l="$MODELS/clip_l.safetensors" \
    --t5xxl="$MODELS/t5xxl_fp16.safetensors" \
    --ae="$MODELS/ae.safetensors" \
    --dataset_config="$TRAIN/dataset.toml" \
    --output_dir="$OUT" \
    --output_name="$OUTPUT_NAME" \
    --logging_dir="$OUT/log" \
    --save_model_as=safetensors \
    --save_precision=bf16 \
    --network_module=networks.lora_flux \
    --network_dim="$DIM" \
    --network_alpha="$ALPHA" \
    --network_train_unet_only \
    --learning_rate=1e-4 \
    --optimizer_type=AdamW8bit \
    --lr_scheduler=constant_with_warmup \
    --lr_warmup_steps=100 \
    --max_train_steps="$MAX_STEPS" \
    --save_every_n_steps="$SAVE_EVERY" \
    --sample_every_n_steps="$SAMPLE_EVERY" \
    --sample_prompts="$TRAIN/sample-prompts.txt" \
    --mixed_precision=bf16 \
    --gradient_checkpointing \
    --sdpa \
    --highvram \
    --cache_latents \
    --cache_latents_to_disk \
    --cache_text_encoder_outputs \
    --cache_text_encoder_outputs_to_disk \
    --persistent_data_loader_workers \
    --max_data_loader_n_workers=2 \
    --seed=42 \
    --guidance_scale=1.0 \
    --timestep_sampling=flux_shift \
    --model_prediction_type=raw \
    --apply_t5_attn_mask \
    --max_grad_norm=1.0

  echo "==> checkpoints in $OUT"
  echo "    Copy the 1000/1250/1500-step files off the box before you destroy the instance."
}

cmd_retrain() {
  cmd_clean
  cmd_train
}

usage() {
  echo "usage: $0 setup|clean|train|retrain"
  exit 2
}

case "${1:-}" in
  setup) cmd_setup ;;
  clean) cmd_clean ;;
  train) cmd_train ;;
  retrain) cmd_retrain ;;
  *) usage ;;
esac

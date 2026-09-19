#!/usr/bin/env bash
# FLUX.1 [dev] identity LoRA (kohya-ss/sd-scripts).
# Do NOT apt-upgrade or install NVIDIA drivers on vast.ai.
#
#   bash kohya-flux-48gb.sh setup     # venv, clone, weights
#   bash kohya-flux-48gb.sh config    # print where to edit settings
#   bash kohya-flux-48gb.sh retag     # rewrite captions → vsgly_id
#   bash kohya-flux-48gb.sh clean     # wipe old LoRAs + latent caches
#   bash kohya-flux-48gb.sh train     # uses /workspace/flux_train/*.toml
#   bash kohya-flux-48gb.sh retrain   # clean + train
#
# Edit settings here (copied onto the box at setup):
#   /workspace/flux_train/kohya-flux.toml   rank, LR, steps, optimiser
#   /workspace/flux_train/dataset.toml      image folder, batch, repeats
set -euo pipefail

ROOT="${ROOT:-/workspace}"
SD_SCRIPTS="${SD_SCRIPTS:-$ROOT/sd-scripts}"
VENV="${VENV:-$ROOT/kohya_env}"
MODELS="${MODELS:-$ROOT/models/flux}"
TRAIN="${TRAIN:-$ROOT/flux_train}"
OUT="${OUT:-$TRAIN/output}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IMAGES="${IMAGES:-}"

detect_images() {
  if [[ -n "$IMAGES" ]]; then
    echo "==> dataset (IMAGES=): $IMAGES"
    return
  fi
  local d
  for d in "$TRAIN/zdp" "$TRAIN/zpd" "$TRAIN/images"; do
    [[ -d "$d" ]] || continue
    shopt -s nullglob nocaseglob
    local hits=( "$d"/*.png "$d"/*.jpg "$d"/*.jpeg "$d"/*.webp )
    shopt -u nocaseglob
    if [[ ${#hits[@]} -gt 0 ]]; then
      IMAGES="$d"
      echo "==> dataset: $IMAGES  (${#hits[@]} images)"
      return
    fi
  done
  IMAGES="$TRAIN/zdp"
  echo "==> no photos found yet; expecting $IMAGES/photo_##.png + .txt"
}

need_gpu() {
  command -v nvidia-smi >/dev/null || { echo "nvidia-smi missing — wrong instance"; exit 1; }
  nvidia-smi
  python3 - <<'PY' || true
try:
    import torch
    print("torch", torch.__version__, "cuda", torch.cuda.is_available(),
          torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
except Exception as e:
    print("torch not in this python yet:", e)
PY
}

install_configs() {
  mkdir -p "$TRAIN" "$OUT" "$MODELS"
  if [[ ! -f "$TRAIN/kohya-flux.toml" ]]; then
    cp "$SCRIPT_DIR/kohya-flux.toml" "$TRAIN/kohya-flux.toml"
  fi
  if [[ ! -f "$TRAIN/dataset.toml" ]]; then
    cp "$SCRIPT_DIR/dataset.toml" "$TRAIN/dataset.toml"
  fi
  if [[ ! -f "$TRAIN/sample-prompts.txt" && -f "$SCRIPT_DIR/sample-prompts.txt" ]]; then
    cp "$SCRIPT_DIR/sample-prompts.txt" "$TRAIN/sample-prompts.txt"
  fi
  python3 - <<PY
from pathlib import Path
root = Path("$ROOT")
train = Path("$TRAIN")
models = Path("$MODELS")
images = Path("$IMAGES")
out = Path("$OUT")

ds = train / "dataset.toml"
text = ds.read_text()
# keep other user edits; only force the image folder we detected
import re
text2, n = re.subn(r'image_dir\s*=\s*".*"', f'image_dir = "{images}"', text, count=1)
if n:
    ds.write_text(text2)
    print(f"dataset.toml image_dir -> {images}")

cfg = train / "kohya-flux.toml"
c = cfg.read_text()
repls = {
    "/workspace/models/flux": str(models),
    "/workspace/flux_train/dataset.toml": str(train / "dataset.toml"),
    "/workspace/flux_train/output/log": str(out / "log"),
    "/workspace/flux_train/output": str(out),
    "/workspace/flux_train/sample-prompts.txt": str(train / "sample-prompts.txt"),
}
# longer paths first
for old, new in sorted(repls.items(), key=lambda kv: len(kv[0]), reverse=True):
    c = c.replace(old, new)
cfg.write_text(c)
print("training config:", cfg)
print("dataset config: ", ds)
PY
}

cmd_config() {
  detect_images
  install_configs
  echo
  echo "Edit Kohya settings in these two files, then run: $0 train"
  echo "  $TRAIN/kohya-flux.toml    rank, LR, steps, optimiser, precision"
  echo "  $TRAIN/dataset.toml       image_dir, batch_size, num_repeats, resolution"
  echo
  echo "----- $TRAIN/kohya-flux.toml -----"
  cat "$TRAIN/kohya-flux.toml"
  echo
  echo "----- $TRAIN/dataset.toml -----"
  cat "$TRAIN/dataset.toml"
}

cmd_setup() {
  detect_images
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

  install_configs
  echo "==> setup done. Check captions, edit $TRAIN/kohya-flux.toml if you want, then: $0 retrain"
}

cmd_clean() {
  detect_images
  echo "==> wiping previous LoRA runs (photos, toml, and FLUX weights stay)"
  rm -rf "$OUT"
  mkdir -p "$OUT"
  rm -rf /home/user/kohya_output /workspace/kohya_output
  rm -rf /home/user/dataset/.cache "$TRAIN/.cache" "$IMAGES/.cache"
  if [[ -d "$IMAGES" ]]; then
    find "$IMAGES" -maxdepth 2 \( -name '*.npz' -o -name '*_te.safetensors' -o -name '*_te.npz' \) -delete
  fi
  if [[ -d /home/user/dataset ]]; then
    find /home/user/dataset -name '*.npz' -delete
    find /home/user/dataset -type d -name '.cache' -prune -exec rm -rf {} +
  fi
  echo "==> clean. Next: $0 train"
}

cmd_train() {
  detect_images
  need_gpu
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  install_configs

  shopt -s nullglob nocaseglob
  local imgs=( "$IMAGES"/*.jpg "$IMAGES"/*.jpeg "$IMAGES"/*.png "$IMAGES"/*.webp )
  shopt -u nocaseglob
  local n="${#imgs[@]}"
  if [[ "$n" -lt 10 ]]; then
    echo "Need >=10 captioned images in $IMAGES (found $n)."
    echo "Expected: $IMAGES/photo_##.png + photo_##.txt"
    exit 1
  fi
  local missing=0 img stem
  for img in "${imgs[@]}"; do
    stem="${img%.*}"
    if [[ ! -f "${stem}.txt" ]]; then
      echo "missing caption: ${stem}.txt"
      missing=1
    fi
  done
  if [[ "$missing" -eq 1 ]]; then
    echo "Every image needs a same-stem .txt caption."
    exit 1
  fi

  local first_txt="${imgs[0]%.*}.txt"
  echo "==> first caption ($(basename "$first_txt")):"
  head -n 1 "$first_txt"
  echo "    use that trigger in sample-prompts.txt"

  for f in flux1-dev.safetensors clip_l.safetensors t5xxl_fp16.safetensors ae.safetensors; do
    [[ -f "$MODELS/$f" ]] || { echo "missing $MODELS/$f — run: $0 setup"; exit 1; }
  done

  echo "==> FROM SCRATCH  $n images  config=$TRAIN/kohya-flux.toml"
  echo "    120 GB: no OOM at these settings. Watch s/it after step 20."
  cd "$SD_SCRIPTS"

  accelerate launch --mixed_precision bf16 --num_cpu_threads_per_process 2 \
    flux_train_network.py \
    --config_file="$TRAIN/kohya-flux.toml" \
    --dataset_config="$TRAIN/dataset.toml"

  echo "==> checkpoints in $OUT"
  echo "    Copy the 750/1000/1250-step files off the box before you destroy the instance."
}

cmd_retag() {
  detect_images
  python3 "$SCRIPT_DIR/retag-captions.py" "$IMAGES"
  echo "==> recache next: captions changed, so wipe .npz before train ($0 retrain)"
}

cmd_retrain() {
  cmd_retag
  cmd_clean
  cmd_train
}

usage() {
  echo "usage: $0 setup|config|retag|clean|train|retrain"
  exit 2
}

case "${1:-}" in
  setup) cmd_setup ;;
  config) cmd_config ;;
  retag) cmd_retag ;;
  clean) cmd_clean ;;
  train) cmd_train ;;
  retrain) cmd_retrain ;;
  *) usage ;;
esac

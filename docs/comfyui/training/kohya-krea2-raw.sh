#!/usr/bin/env bash
# Krea 2 Raw identity LoRA via kohya-ss/musubi-tuner (not sd-scripts).
# Train on Raw, run the LoRA on Turbo in ComfyUI.
# Do NOT apt-upgrade or install NVIDIA drivers on vast.ai.
#
#   bash kohya-krea2-raw.sh start     # stop ComfyUI + launch training in tmux
#   bash kohya-krea2-raw.sh attach    # watch the trainer
#   bash kohya-krea2-raw.sh cache     # re-cache if captions/images changed
#
set -euo pipefail

ROOT="${ROOT:-/workspace}"
VENV="${VENV:-$ROOT/musubi_env}"
MUSUBI="${MUSUBI:-$ROOT/musubi-tuner}"
TRAIN="${TRAIN:-$ROOT/krea2_train}"
OUT="${OUT:-$TRAIN/output}"
IMAGES="${IMAGES:-$ROOT/flux_train/vsgly_id}"
DIT="${DIT:-$ROOT/ComfyUI/models/diffusion_models/krea2_raw_bf16.safetensors}"
VAE="${VAE:-$ROOT/ComfyUI/models/vae/qwen_image_vae.safetensors}"
TE="${TE:-$ROOT/ComfyUI/models/text_encoders/qwen3vl_4b_bf16.safetensors}"
TURBO="${TURBO:-$ROOT/ComfyUI/models/diffusion_models/krea2_turbo_fp8_scaled.safetensors}"
SESSION="${SESSION:-krea2-train}"

need() {
  local f
  for f in "$DIT" "$VAE" "$TE" "$TRAIN/dataset.toml"; do
    [[ -s "$f" ]] || { echo "missing: $f"; exit 1; }
  done
}

activate() {
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  cd "$MUSUBI"
  export HF_HOME="${HF_HOME:-$ROOT/.hf_home}"
  export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
}

cache() {
  activate
  need
  python src/musubi_tuner/krea2_cache_latents.py \
    --dataset_config "$TRAIN/dataset.toml" \
    --vae "$VAE"
  python src/musubi_tuner/krea2_cache_text_encoder_outputs.py \
    --dataset_config "$TRAIN/dataset.toml" \
    --text_encoder "$TE" \
    --batch_size 1
}

train_cmd() {
  cat <<CMD
accelerate launch --num_cpu_threads_per_process 1 --mixed_precision bf16 \
  src/musubi_tuner/krea2_train_network.py \
  --dit "$DIT" \
  --vae "$VAE" \
  --text_encoder "$TE" \
  --turbo_dit "$TURBO" \
  --dataset_config "$TRAIN/dataset.toml" \
  --sdpa --mixed_precision bf16 \
  --timestep_sampling krea2_shift --weighting_scheme none \
  --optimizer_type adamw --learning_rate 1e-4 \
  --max_data_loader_n_workers 2 --persistent_data_loader_workers \
  --network_module networks.lora_krea2 --network_dim 32 --network_alpha 32 \
  --max_train_epochs 8 --save_every_n_epochs 1 --save_state \
  --sample_prompts "$TRAIN/sample-prompts.txt" \
  --sample_every_n_epochs 1 --sample_at_first \
  --seed 42 \
  --output_dir "$OUT" \
  --output_name vsgly_id_krea2_v1 \
  --logging_dir "$TRAIN/log" --log_with tensorboard
CMD
}

start() {
  need
  [[ -s "$TURBO" ]] || echo "warning: Turbo missing at $TURBO (samples will use Raw)"
  if command -v supervisorctl >/dev/null 2>&1; then
    echo "==> stopping ComfyUI so training can use the GPU"
    supervisorctl stop comfyui || true
  fi
  mkdir -p "$OUT" "$TRAIN/log"
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "tmux session $SESSION already exists. Attach with: tmux attach -t $SESSION"
    exit 1
  fi
  activate
  tmux new-session -d -s "$SESSION" -c "$MUSUBI"
  tmux send-keys -t "$SESSION" "source $VENV/bin/activate && cd $MUSUBI && export HF_HOME=${HF_HOME:-$ROOT/.hf_home} && export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True && $(train_cmd | tr '\n' ' ')" C-m
  echo "==> training started in tmux session $SESSION"
  echo "    tmux attach -t $SESSION"
  echo "    LoRAs land in $OUT"
}

case "${1:-start}" in
  start) start ;;
  cache) cache ;;
  attach) tmux attach -t "$SESSION" ;;
  cmd) train_cmd ;;
  *) echo "usage: $0 start|cache|attach|cmd"; exit 1 ;;
esac

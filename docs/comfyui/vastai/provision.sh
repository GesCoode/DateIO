#!/usr/bin/env bash
# Optional first-boot script for a vast.ai ComfyUI instance.
# Run from /workspace (or wherever ComfyUI lives). Requires huggingface-cli login
# if the FLUX.1-dev repo is gated.
set -euo pipefail

COMFY="${COMFY_DIR:-/workspace/ComfyUI}"
mkdir -p "$COMFY/models/"{unet,diffusion_models,clip,vae,loras,controlnet,upscale_models}

echo "==> custom nodes"
cd "$COMFY/custom_nodes"
[[ -d ComfyUI-GGUF ]] || git clone https://github.com/city96/ComfyUI-GGUF
[[ -d comfyui_controlnet_aux ]] || git clone https://github.com/Fannovel16/comfyui_controlnet_aux
[[ -d ComfyUI-FluxTrainer ]] || git clone https://github.com/kijai/ComfyUI-FluxTrainer

echo "==> download helper (huggingface-cli if available, else skip)"
if command -v huggingface-cli >/dev/null 2>&1; then
  huggingface-cli download comfyanonymous/flux_text_encoders clip_l.safetensors --local-dir "$COMFY/models/clip"
  huggingface-cli download comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors --local-dir "$COMFY/models/clip"
  echo "Download ae.safetensors from black-forest-labs/FLUX.1-dev into models/vae/"
  echo "Download flux1-dev-fp8.safetensors (Kijai/flux-fp8) into models/unet/ or models/diffusion_models/"
  echo "Download InstantX Union ControlNet into models/controlnet/"
else
  echo "huggingface-cli not found. Use the instance portal / wget from models.md"
fi

echo "Done. Restart ComfyUI, press R to reload models."

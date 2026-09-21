# Model files

Accept the FLUX.1 [dev] license first:
https://huggingface.co/black-forest-labs/FLUX.1-dev

Hugging Face CLI (once): `huggingface-cli login`

Paths are relative to your ComfyUI root.

## Local RTX 2070 (8 GB) — generation

| File | Put in | Source |
| --- | --- | --- |
| `flux1-dev-Q4_K_S.gguf` | `models/unet/` | [city96/FLUX.1-dev-gguf](https://huggingface.co/city96/FLUX.1-dev-gguf) — Q4_K_S is the 8 GB sweet spot. Fall back to `Q4_0` / `Q3_K_S` on OOM. |
| `t5xxl_fp8_e4m3fn.safetensors` | `models/clip/` | [comfyanonymous/flux_text_encoders](https://huggingface.co/comfyanonymous/flux_text_encoders) — **do not** use fp16 T5 on 8 GB. Optional: a T5 GGUF from [city96/t5-v1_1-xxl-encoder-gguf](https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf). |
| `clip_l.safetensors` | `models/clip/` | same `flux_text_encoders` repo |
| `ae.safetensors` | `models/vae/` | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) (`ae.safetensors`) |
| your LoRA `.safetensors` | `models/loras/` | trained on vast.ai |

Optional later (still local, may OOM with LoRA):

| File | Put in | Source |
| --- | --- | --- |
| OpenPose / Depth preprocessor weights | auto-downloaded by `comfyui_controlnet_aux` on first run | — |

## vast.ai 24 GB — training + ControlNet

Add the fp8 (or fp16) UNET so trainers are happy, plus Union ControlNet:

| File | Put in | Source |
| --- | --- | --- |
| `flux1-dev-fp8.safetensors` | `models/diffusion_models/` **or** `models/unet/` | [Kijai/flux-fp8](https://huggingface.co/Kijai/flux-fp8) or [XLabs-AI/flux-dev-fp8](https://huggingface.co/XLabs-AI/flux-dev-fp8) |
| `t5xxl_fp16.safetensors` or fp8 T5 | `models/clip/` | `comfyanonymous/flux_text_encoders` — fp16 T5 is OK on 24 GB |
| `clip_l.safetensors` | `models/clip/` | same |
| `ae.safetensors` | `models/vae/` | BFL |
| `flux1-dev-controlnet-union.safetensors` (or Union-Pro fp8) | `models/controlnet/` | [InstantX/FLUX.1-dev-Controlnet-Union](https://huggingface.co/InstantX/FLUX.1-dev-Controlnet-Union) or [Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro](https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro) |
| 4x upscaler (e.g. `4x-UltraSharp.pth`) | `models/upscale_models/` | any ESRGAN 4x you already use |

Union ControlNet modes we care about: **0 canny**, **2 depth**, **4 pose**.

## France RTX 3090 — Krea 2 Turbo generate

From [Comfy-Org/Krea-2](https://huggingface.co/Comfy-Org/Krea-2). Nested folder names match the Comfy missing-model dropdown.

| File | Put in | Source |
| --- | --- | --- |
| `krea2-turbo.safetensors` (bf16, 26.3 GB) | `models/diffusion_models/Krea-2/` | `diffusion_models/krea2_turbo_bf16.safetensors` |
| `qwen3vl_4b_bf16.safetensors` (8.3 GB) | `models/text_encoders/Krea-2/` | `text_encoders/qwen3vl_4b_bf16.safetensors` |
| `qwen_image_vae.safetensors` | `models/vae/QwenImage/` | `vae/qwen_image_vae.safetensors` (same file as flat `models/vae/`) |

CLIP type must be **`krea2`**. Official Turbo UNET does not need the turbo LoRA (that LoRA is for running RAW as Turbo).

## Disk budget

- Local 2070 kit (GGUF Q4 + encoders + VAE): ~**12–16 GB**
- vast.ai train + generate kit (fp8 UNET + T5 + Union CN): ~**30–40 GB**
- Do not download FLUX.2 / video models onto the 2070.

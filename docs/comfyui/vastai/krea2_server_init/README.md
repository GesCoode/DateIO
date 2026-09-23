# Krea 2 vast.ai server init

Run this from your laptop (PyCharm: `C:\Users\jeroe\PycharmProjects\Kre2ServerInit`). It SSHs into a fresh vast.ai box, checks GPU/disk, installs musubi-tuner, and downloads Krea 2 Raw + Turbo + Qwen3-VL + VAE.

It does **not** start training and does **not** cache latents. You copy `photo_##.png` + `photo_##.txt` into `/workspace/flux_train/vsgly_id/` yourself, then paste the commands it prints.

## Setup on Windows

```text
python -m pip install -r requirements.txt
```

Copy `krea2_server_init.py` into the PyCharm project. At the top of the file (or in `secrets.local.py` next to it):

```python
HF_TOKEN = "hf_..."
SSH_CONNECT = "ssh -p 46253 root@93.91.156.93 -L 8080:localhost:8080"
SSH_KEY_PATH = r"C:\Users\jeroe\.ssh\id_ed25519"
```

Add this machine's public key on the vast instance first. Do not commit real tokens.

## What it checks before downloading

- ARM / GB10 / CMP 170HX → stop
- VRAM under 48 GB → `maybe not enough VRAM` (you type `proceed` or `stop`)
- Tight `/workspace` disk → `possibly not enough disk space` (same prompt)

Do not `apt upgrade` or install NVIDIA drivers on the template.

## After it finishes

Upload the dataset, then run the printed **cache** block, then the printed **train** block in `tmux`.

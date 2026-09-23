#!/usr/bin/env python3
"""Prepare a vast.ai box for Krea 2 Raw LoRA training (musubi-tuner).

Fill in HF_TOKEN and SSH_CONNECT at the top (or put them in secrets.local.py).
This script does NOT start training and does NOT cache latents — you upload
photo_##.png + photo_##.txt yourself, then run the printed cache/train commands.

Do not apt-upgrade or install NVIDIA drivers on vast templates.
"""

from __future__ import annotations

import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# =============================================================================
# FILL THESE IN
# =============================================================================

# Hugging Face token (hf_...). Used only on the remote box for gated/large downloads.
HF_TOKEN = ""

# Paste the vast.ai SSH line, for example:
#   ssh -p 46253 root@93.91.156.93 -L 8080:localhost:8080
SSH_CONNECT = ""

# Optional private key. Leave empty to try the default keys under ~/.ssh
# (id_ed25519, id_rsa, vast_agent, id_ecdsa).
SSH_KEY_PATH = ""

# Optional override next to this file: secrets.local.py with the same names.
# That file is gitignored so tokens stay off the repo.
_SECRETS = Path(__file__).with_name("secrets.local.py")
if _SECRETS.is_file():
    _ns: dict = {}
    exec(_SECRETS.read_text(encoding="utf-8"), _ns)
    HF_TOKEN = str(_ns.get("HF_TOKEN", HF_TOKEN) or HF_TOKEN)
    SSH_CONNECT = str(_ns.get("SSH_CONNECT", SSH_CONNECT) or SSH_CONNECT)
    SSH_KEY_PATH = str(_ns.get("SSH_KEY_PATH", SSH_KEY_PATH) or SSH_KEY_PATH)

HF_TOKEN = (os.environ.get("HF_TOKEN") or HF_TOKEN).strip()
SSH_CONNECT = (os.environ.get("SSH_CONNECT") or SSH_CONNECT).strip()
SSH_KEY_PATH = (os.environ.get("SSH_KEY_PATH") or SSH_KEY_PATH).strip()

# =============================================================================
# Remote layout (vast ComfyUI template)
# =============================================================================

REMOTE_ROOT = "/workspace"
VENV = f"{REMOTE_ROOT}/musubi_env"
MUSUBI = f"{REMOTE_ROOT}/musubi-tuner"
TRAIN = f"{REMOTE_ROOT}/krea2_train"
IMAGES = f"{REMOTE_ROOT}/flux_train/vsgly_id"
MODELS = f"{REMOTE_ROOT}/ComfyUI/models"

RAW_DIT = f"{MODELS}/diffusion_models/krea2_raw_bf16.safetensors"
TURBO_DIT = f"{MODELS}/diffusion_models/krea2_turbo_fp8_scaled.safetensors"
TEXT_ENCODER = f"{MODELS}/text_encoders/qwen3vl_4b_bf16.safetensors"
VAE = f"{MODELS}/vae/qwen_image_vae.safetensors"

# musubi-tuner 0.3.5 requires this exact hub version. `pip install -U huggingface_hub`
# pulls 1.x and breaks transformers / accelerate.
HF_HUB_PIN = "0.34.3"

# Weights we download. min_bytes is a sanity floor (partial Jupyter uploads fail this).
DOWNLOADS = (
    ("Comfy-Org/Krea-2", "diffusion_models/krea2_raw_bf16.safetensors", RAW_DIT, 20 * 1024**3),
    ("Comfy-Org/Krea-2", "diffusion_models/krea2_turbo_fp8_scaled.safetensors", TURBO_DIT, 10 * 1024**3),
    ("Comfy-Org/Krea-2", "text_encoders/qwen3vl_4b_bf16.safetensors", TEXT_ENCODER, 7 * 1024**3),
    ("Comfy-Org/Krea-2", "vae/qwen_image_vae.safetensors", VAE, 200 * 1024**2),
)

# Raw + Turbo + Qwen3-VL + VAE + venv + musubi clone. Leave headroom for cache/output.
DISK_WARN_FREE_GB = 90
DISK_MIN_FREE_GB = 55
VRAM_OK_MB = 48 * 1024
VRAM_WARN_MB = 24 * 1024

DATASET_TOML = """\
[general]
resolution = [1024, 1024]
caption_extension = ".txt"
batch_size = 1
enable_bucket = true
bucket_no_upscale = true

[[datasets]]
image_directory = "/workspace/flux_train/vsgly_id"
cache_directory = "/workspace/krea2_train/cache"
num_repeats = 6
"""

SAMPLE_PROMPTS = """\
vsgly_id, a man with short dark wavy hair and a short beard, brown eyes, close-up portrait, window light, looking at camera, photorealistic --w 1024 --h 1024 --s 8 --l 1 --d 42
vsgly_id, a man with short dark wavy hair and a short beard, standing outdoors in a navy overshirt, golden hour, medium shot, photorealistic --w 1024 --h 1024 --s 8 --l 1 --d 43
vsgly_id, a man sitting at a cafe table, cinematic lighting, chest-up, photorealistic --w 1024 --h 1024 --s 8 --l 1 --d 44
vsgly_id, a man running on a beach wearing a swimsuit, cinematic lighting, chest-up, photorealistic --w 1024 --h 1024 --s 8 --l 1 --d 44
vsgly_id, a naked man with a big penis with two beautiful naked woman at his feet, cinematic lighting, chest-up, photorealistic --w 1024 --h 1024 --s 8 --l 1 --d 44
"""


# =============================================================================
# SSH helpers
# =============================================================================


@dataclass
class SshTarget:
    user: str
    host: str
    port: int = 22


def parse_ssh_connect(line: str) -> SshTarget:
    text = line.strip()
    if not text:
        raise SystemExit("SSH_CONNECT is empty. Paste the vast.ai ssh line at the top of this file.")
    if text.lower().startswith("ssh "):
        text = text[4:]
    port = 22
    m_port = re.search(r"(?:^|\s)-p\s+(\d+)", text)
    if m_port:
        port = int(m_port.group(1))
    m_userhost = re.search(r"(\w+)@([A-Za-z0-9._-]+)", text)
    if not m_userhost:
        raise SystemExit(f"Could not parse user@host from SSH_CONNECT:\n  {line}")
    return SshTarget(user=m_userhost.group(1), host=m_userhost.group(2), port=port)


def default_key_paths() -> list[Path]:
    if SSH_KEY_PATH:
        return [Path(SSH_KEY_PATH).expanduser()]
    home = Path.home() / ".ssh"
    names = ("id_ed25519", "id_rsa", "vast_agent", "id_ecdsa")
    return [home / n for n in names if (home / n).is_file()]


class Remote:
    def __init__(self, target: SshTarget):
        try:
            import paramiko
        except ImportError as exc:
            raise SystemExit(
                "paramiko is required. From this folder run:\n"
                "  python -m pip install -r requirements.txt"
            ) from exc

        self._paramiko = paramiko
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        keys = default_key_paths()
        last_err: Exception | None = None
        connected = False
        for key in keys or [None]:
            try:
                print(f"Connecting {target.user}@{target.host}:{target.port}"
                      + (f"  key={key}" if key else "  (agent / default keys)"))
                self.client.connect(
                    hostname=target.host,
                    port=target.port,
                    username=target.user,
                    key_filename=str(key) if key else None,
                    allow_agent=True,
                    look_for_keys=True,
                    timeout=20,
                    banner_timeout=20,
                    auth_timeout=20,
                )
                connected = True
                break
            except Exception as err:  # noqa: BLE001 — try the next key
                last_err = err
        if not connected:
            raise SystemExit(
                "SSH failed. Add your public key on the vast instance and set SSH_KEY_PATH.\n"
                f"Last error: {last_err}"
            )
        self.sftp = self.client.open_sftp()

    def close(self) -> None:
        try:
            self.sftp.close()
        except Exception:
            pass
        self.client.close()

    def run(self, command: str, *, check: bool = True, timeout: int = 3600) -> tuple[int, str, str]:
        print(f"\n$ {command if len(command) < 220 else command[:200] + ' ...'}")
        stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        stdin.close()
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        code = stdout.channel.recv_exit_status()
        if out.strip():
            print(out.rstrip())
        if err.strip():
            print(err.rstrip(), file=sys.stderr)
        if check and code != 0:
            raise SystemExit(f"Remote command failed (exit {code}):\n{command}")
        return code, out, err

    def bash(self, script: str, *, check: bool = True, timeout: int = 7200) -> tuple[int, str, str]:
        """Run a multi-line bash snippet on the box (login-less)."""
        wrapped = "bash -lc " + shlex_quote(script)
        return self.run(wrapped, check=check, timeout=timeout)

    def write_text(self, remote_path: str, text: str) -> None:
        parent = str(Path(remote_path).parent).replace("\\", "/")
        self.run(f"mkdir -p {shlex_quote(parent)}")
        with self.sftp.file(remote_path, "w") as fh:
            fh.write(text.encode("utf-8"))
        print(f"Wrote {remote_path}")

    def exists(self, remote_path: str) -> bool:
        try:
            self.sftp.stat(remote_path)
            return True
        except OSError:
            return False


def shlex_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


# =============================================================================
# Compatibility check
# =============================================================================


@dataclass
class Preflight:
    hard_stops: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    gpu_name: str = ""
    vram_mb: int = 0
    compute_cap: str = ""
    free_disk_gb: float = 0.0
    python: str = ""
    arch: str = ""


def collect_preflight(remote: Remote) -> Preflight:
    pf = Preflight()
    _, arch, _ = remote.run("uname -m", check=False)
    pf.arch = arch.strip()
    if pf.arch in {"aarch64", "arm64"}:
        pf.hard_stops.append(
            f"CPU arch is {pf.arch}. Skip GB10 / ARM boxes — PyTorch CUDA wheels will not work."
        )

    code, _, _ = remote.run("command -v nvidia-smi", check=False)
    if code != 0:
        pf.hard_stops.append("nvidia-smi is missing — this is not a CUDA GPU instance.")
        return pf

    _, gpu_csv, _ = remote.run(
        "nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv,noheader,nounits",
        check=False,
    )
    line = gpu_csv.strip().splitlines()[0] if gpu_csv.strip() else ""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 3:
        pf.gpu_name, vram_s, pf.compute_cap = parts[0], parts[1], parts[2]
        try:
            pf.vram_mb = int(float(vram_s))
        except ValueError:
            pf.vram_mb = 0
    else:
        pf.hard_stops.append(f"Could not parse nvidia-smi output: {gpu_csv!r}")

    name_l = pf.gpu_name.lower()
    if "gb10" in name_l:
        pf.hard_stops.append(f"GPU is {pf.gpu_name}. Skip NVIDIA GB10 (ARM).")
    if "cmp 170" in name_l or "170hx" in name_l:
        pf.hard_stops.append(f"GPU is {pf.gpu_name}. Skip CMP 170HX (mining SKU, flaky CUDA).")
    if pf.compute_cap.startswith("12.1"):
        pf.hard_stops.append(
            f"Compute capability {pf.compute_cap} (GB10-class). No usable PyTorch kernel image."
        )

    if pf.vram_mb and pf.vram_mb < VRAM_WARN_MB:
        pf.warnings.append(
            f"maybe not enough VRAM: {pf.gpu_name} has {pf.vram_mb / 1024:.1f} GB. "
            "This recipe trains Krea 2 Raw bf16 (rank 32, 1024). Want 48 GB+. "
            "Below 24 GB it will almost certainly OOM."
        )
    elif pf.vram_mb and pf.vram_mb < VRAM_OK_MB:
        pf.warnings.append(
            f"maybe not enough VRAM: {pf.gpu_name} has {pf.vram_mb / 1024:.1f} GB. "
            "The 48 GB+ recipe has no gradient checkpointing. On 24–47 GB you must add "
            "--gradient_checkpointing when you start training."
        )

    _, df_out, _ = remote.run("df -PB1 /workspace | tail -1", check=False)
    cols = df_out.split()
    if len(cols) >= 4:
        try:
            pf.free_disk_gb = int(cols[3]) / 1024**3
        except ValueError:
            pf.free_disk_gb = 0.0
    if pf.free_disk_gb and pf.free_disk_gb < DISK_MIN_FREE_GB:
        pf.warnings.append(
            f"possibly not enough disk space: {pf.free_disk_gb:.0f} GB free on /workspace. "
            f"Krea 2 Raw+Turbo+Qwen3-VL is ~47 GB plus venv, cache, and checkpoints. "
            f"Want {DISK_WARN_FREE_GB}+ GB free."
        )
    elif pf.free_disk_gb and pf.free_disk_gb < DISK_WARN_FREE_GB:
        pf.warnings.append(
            f"possibly not enough disk space: {pf.free_disk_gb:.0f} GB free on /workspace. "
            "Downloads will fit, but cache + 8 epoch checkpoints will get tight."
        )

    _, py, _ = remote.run("python3 --version", check=False)
    pf.python = py.strip()
    m_py = re.search(r"Python (\d+)\.(\d+)", pf.python)
    if m_py:
        major, minor = int(m_py.group(1)), int(m_py.group(2))
        if (major, minor) >= (3, 13) or (major, minor) < (3, 10):
            pf.warnings.append(
                f"{pf.python} — musubi-tuner wants Python 3.10–3.12."
            )

    return pf


def decide(pf: Preflight) -> None:
    print("\n========== compatibility ==========")
    print(f"arch        {pf.arch or '?'}")
    print(f"python      {pf.python or '?'}")
    print(f"gpu         {pf.gpu_name or '?'}")
    print(f"vram        {pf.vram_mb / 1024:.1f} GB" if pf.vram_mb else "vram        ?")
    print(f"compute     {pf.compute_cap or '?'}")
    print(f"disk free   {pf.free_disk_gb:.0f} GB" if pf.free_disk_gb else "disk free   ?")

    if pf.hard_stops:
        print("\nINCOMPATIBLE — stopping before any download:")
        for item in pf.hard_stops:
            print(f"  - {item}")
        raise SystemExit(1)

    if not pf.warnings:
        print("Looks compatible. Continuing setup.")
        return

    print("\nWarnings (setup has not started):")
    for item in pf.warnings:
        print(f"  - {item}")
    answer = input("\nType proceed or stop: ").strip().lower()
    if answer not in {"proceed", "p", "yes", "y"}:
        raise SystemExit("Stopped. Nothing was installed.")


# =============================================================================
# Setup
# =============================================================================


def write_remote_files(remote: Remote) -> None:
    remote.run(
        "mkdir -p "
        f"{IMAGES} "
        f"{TRAIN}/cache {TRAIN}/output {TRAIN}/log "
        f"{MODELS}/diffusion_models {MODELS}/text_encoders {MODELS}/vae {MODELS}/loras"
    )
    remote.write_text(f"{TRAIN}/dataset.toml", DATASET_TOML)
    remote.write_text(f"{TRAIN}/sample-prompts.txt", SAMPLE_PROMPTS)


def install_stack(remote: Remote) -> None:
    # Do not apt-upgrade. Vast already has CUDA.
    remote.bash(
        f"""
set -euo pipefail
python3 -m venv {VENV}
source {VENV}/bin/activate
pip install -U pip wheel
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(), 'CUDA not visible'; print(torch.__version__, torch.cuda.get_device_name(0))"
""",
        timeout=1800,
    )

    if not remote.exists(f"{MUSUBI}/.git"):
        remote.run(f"git clone --depth 1 https://github.com/kohya-ss/musubi-tuner.git {MUSUBI}")
    else:
        print(f"{MUSUBI} already cloned — leaving it.")

    remote.bash(
        f"""
set -euo pipefail
source {VENV}/bin/activate
cd {MUSUBI}
pip install -e .
pip install "huggingface_hub[cli]=={HF_HUB_PIN}" tensorboard
# requirements / -e . can pull a CPU or cu124 torch — put cu128 back
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch, huggingface_hub; print('torch', torch.__version__, torch.cuda.is_available()); print('hub', huggingface_hub.__version__)"
""",
        timeout=1800,
    )

    if HF_TOKEN:
        remote.bash(
            f"""
set -euo pipefail
source {VENV}/bin/activate
huggingface-cli login --token {shlex_quote(HF_TOKEN)} --add-to-git-credential
""",
            timeout=120,
        )
    else:
        print("HF_TOKEN is empty — downloads that need auth will fail.")


def download_weights(remote: Remote) -> None:
    for repo, repo_file, dest, min_bytes in DOWNLOADS:
        if remote.exists(dest):
            _, size_s, _ = remote.run(f"stat -c %s {shlex_quote(dest)}", check=False)
            try:
                size = int(size_s.strip() or "0")
            except ValueError:
                size = 0
            if size >= min_bytes:
                print(f"already have {dest} ({size / 1024**3:.1f} GB) — skip download")
                continue
            print(f"{dest} is too small ({size} bytes) — re-downloading")
            remote.run(f"rm -f {shlex_quote(dest)}")

        remote.bash(
            f"""
set -euo pipefail
source {VENV}/bin/activate
export HF_HOME={REMOTE_ROOT}/.hf_home
huggingface-cli download {shlex_quote(repo)} {shlex_quote(repo_file)} --local-dir {shlex_quote(MODELS)}
""",
            timeout=7200,
        )
        _, size_s, _ = remote.run(f"stat -c %s {shlex_quote(dest)}")
        size = int(size_s.strip())
        if size < min_bytes:
            raise SystemExit(f"{dest} is only {size} bytes — download looks truncated.")
        print(f"ok {dest} ({size / 1024**3:.2f} GB)")


def print_train_block() -> None:
    cache = f"""source {VENV}/bin/activate
cd {MUSUBI}
export HF_HOME={REMOTE_ROOT}/.hf_home
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

python src/musubi_tuner/krea2_cache_latents.py \\
  --dataset_config {TRAIN}/dataset.toml \\
  --vae {VAE}

python src/musubi_tuner/krea2_cache_text_encoder_outputs.py \\
  --dataset_config {TRAIN}/dataset.toml \\
  --text_encoder {TEXT_ENCODER} \\
  --batch_size 1"""

    train = f"""supervisorctl stop comfyui || true
tmux new -s krea2-train
source {VENV}/bin/activate
cd {MUSUBI}
export HF_HOME={REMOTE_ROOT}/.hf_home
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

accelerate launch --num_cpu_threads_per_process 1 --mixed_precision bf16 \\
  src/musubi_tuner/krea2_train_network.py \\
  --dit {RAW_DIT} \\
  --vae {VAE} \\
  --text_encoder {TEXT_ENCODER} \\
  --turbo_dit {TURBO_DIT} \\
  --dataset_config {TRAIN}/dataset.toml \\
  --sdpa --mixed_precision bf16 \\
  --timestep_sampling krea2_shift --weighting_scheme none \\
  --optimizer_type adamw --learning_rate 1e-4 \\
  --max_data_loader_n_workers 2 --persistent_data_loader_workers \\
  --network_module networks.lora_krea2 --network_dim 32 --network_alpha 32 \\
  --max_train_epochs 8 --save_every_n_epochs 1 --save_state \\
  --sample_prompts {TRAIN}/sample-prompts.txt \\
  --sample_every_n_epochs 1 --sample_at_first \\
  --seed 42 \\
  --output_dir {TRAIN}/output \\
  --output_name vsgly_id_krea2_v1 \\
  --logging_dir {TRAIN}/log --log_with tensorboard"""

    print("\n" + "=" * 72)
    print("SETUP DONE. Training was NOT started.")
    print(f"Upload photo_##.png + photo_##.txt into:\n  {IMAGES}")
    print("Each caption should start with: vsgly_id")
    print("=" * 72)
    print("\n--- 1) after photos are on the box, cache (required) ---\n")
    print(cache)
    print("\n--- 2) start training manually ---\n")
    print(train)
    print("\nDetach tmux with Ctrl-b then d. Reattach: tmux attach -t krea2-train")
    print("LoRAs land in /workspace/krea2_train/output/")
    print(
        "\nNote: in-training samples stay noise if --turbo_dit is the Comfy fp8_scaled "
        "file. That does not mean the LoRA failed — test checkpoints in ComfyUI Turbo."
    )


def main() -> int:
    if not SSH_CONNECT:
        print("Set SSH_CONNECT at the top of this file (the vast.ai ssh line).")
        return 2
    if not HF_TOKEN:
        print("HF_TOKEN is empty. Downloads from Hugging Face may fail. Continuing to preflight.")

    target = parse_ssh_connect(SSH_CONNECT)
    remote = Remote(target)
    try:
        pf = collect_preflight(remote)
        decide(pf)
        write_remote_files(remote)
        install_stack(remote)
        download_weights(remote)
        remote.run(
            "ls -lh "
            f"{RAW_DIT} {TURBO_DIT} {TEXT_ENCODER} {VAE} "
            f"{TRAIN}/dataset.toml {IMAGES}"
        )
        print_train_block()
        return 0
    finally:
        remote.close()


if __name__ == "__main__":
    # Unbuffered so PyCharm shows progress while downloads run.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    t0 = time.time()
    code = main()
    print(f"\nFinished in {time.time() - t0:.0f}s")
    raise SystemExit(code)

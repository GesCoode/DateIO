#!/usr/bin/env python3
"""Replace the reference person with the LoRA character.

Draft at ~0.6MP (empty latent, pose + scene refs). LaMa removes the old
person from the original photo. The new LoRA person is pasted onto that
cleaned kitchen. No blur-heal, no second sampler, no ghost.
"""
from __future__ import annotations

import json
from pathlib import Path

IDENTITY = (
    "vsgly_id, a man with short dark wavy hair and a short beard, "
    "masculine face and body, natural skin, matching the skeleton pose, "
    "full torso and hips visible, standing behind the counter, "
    "same camera angle, same lighting as the reference photograph, photorealistic"
)
ADJUST = ""
NEG = (
    "woman, female, long hair, feminine body, breasts, mixed gender, "
    "ghost, double exposure, overlay of two people, leftover original person, "
    "hard cutout, sticker, pasted, mask outline, halo, different lighting, "
    "cropped legs, missing hips, cut off at the waist, floating torso, "
    "white blob, melted marble"
)

CORE = {"cnr_id": "comfy-core", "ver": "0.37.0"}
OSTRIS = {
    "aux_id": "ostris/comfyui-krea2-ostris-edit",
    "ver": "7756566160c4a1b24bb1bd9f0ff3ced1a83d7547",
    "cnr_id": "comfyui-krea2-ostris-edit",
}
RMBG = {"Node name for S&R": "RMBG", "cnr_id": "comfyui-rmbg", "ver": "3.1.0"}
LAMA = {"Node name for S&R": "AILab_LamaRemover", "cnr_id": "comfyui-rmbg", "ver": "3.1.0"}
AUX = {
    "Node name for S&R": "DWPreprocessor",
    "cnr_id": "comfyui_controlnet_aux",
    "ver": "1.1.5",
}
KJ = {"Node name for S&R": "ColorToMask", "cnr_id": "comfyui-kjnodes"}
NOTE = (
    "1. Draft is ~0.6MP so you get a preview faster. Pose + identity generate "
    "the whole frame (empty latent).\n"
    "2. image1 = reference with the old person painted out (lighting/camera). "
    "image2 = DWPose on gray. Pose LoRA 0.9.\n"
    "3. BEN masks the person (not the island). LaMa removes the old person "
    "from the original kitchen. Then only the new BEN person is pasted on. "
    "No ghost, no leftover original person, no generated marble blob. "
    "No second sampler.\n"
    "4. Type extra directions in Your adjustments (e.g. make the shirt red).\n"
    "5. Final is a lanczos upscale of the married draft.\n"
    "CLIP type must be krea2."
)


def props(name: str, extra: dict | None = None) -> dict:
    p = {"Node name for S&R": name, **CORE}
    if extra:
        p.update(extra)
    return p


def out(name, typ, links, slot=0):
    return {"name": name, "type": typ, "slot_index": slot, "links": links}


def inp(name, typ, link, *, shape=None, widget=None):
    d = {"name": name, "type": typ, "link": link}
    if shape is not None:
        d["shape"] = shape
    if widget is not None:
        d["widget"] = {"name": widget}
    return d


def rmbg_widgets(blur: int = 8, offset: int = 0, *, model: str = "BEN") -> tuple[list, dict]:
    wv = [model, 1, 768, blur, offset, False, False, "Alpha", "#222222"]
    named = {
        "model": model,
        "sensitivity": 1,
        "process_res": 768,
        "mask_blur": blur,
        "mask_offset": offset,
        "invert_output": False,
        "refine_foreground": False,
        "background": "Alpha",
        "background_color": "#222222",
    }
    return wv, named


def ostris_in(clip_l, vae_l, img1, img2, prompt_l=None):
    rows = [inp("clip", "CLIP", clip_l)]
    if prompt_l is not None:
        rows.append(inp("prompt", "STRING", prompt_l, widget="prompt"))
    rows.extend(
        [
            inp("vae", "VAE", vae_l, shape=7),
            inp("image1", "IMAGE", img1, shape=7),
            inp("image2", "IMAGE", img2, shape=7),
            inp("image3", "IMAGE", None, shape=7),
        ]
    )
    return rows


def main() -> None:
    nodes: list[dict] = []

    def add(n: dict) -> None:
        nodes.append(n)

    add({
        "id": 1, "type": "UNETLoader", "pos": [-1400, 40], "size": [400, 82],
        "flags": {}, "order": 0, "mode": 0, "inputs": [],
        "outputs": [out("MODEL", "MODEL", [1])],
        "title": "UNET (Sick Ollie / Krea2)",
        "properties": props("UNETLoader"),
        "widgets_values": ["SICK_OLLIE_Krea2_BF16.safetensors", "default"],
        "widgets_values_named": {"unet_name": "SICK_OLLIE_Krea2_BF16.safetensors", "weight_dtype": "default"},
    })
    add({
        "id": 2, "type": "CLIPLoader", "pos": [-1400, 160], "size": [400, 106],
        "flags": {}, "order": 1, "mode": 0, "inputs": [],
        "outputs": [out("CLIP", "CLIP", [2, 3, 4])],
        "title": "CLIP (type must be krea2)",
        "properties": props("CLIPLoader"),
        "widgets_values": ["qwen3vl_4b_bf16.safetensors", "krea2", "default"],
        "widgets_values_named": {
            "clip_name": "qwen3vl_4b_bf16.safetensors",
            "type": "krea2",
            "device": "default",
        },
    })
    add({
        "id": 3, "type": "VAELoader", "pos": [-1400, 310], "size": [400, 58],
        "flags": {}, "order": 2, "mode": 0, "inputs": [],
        "outputs": [out("VAE", "VAE", [5, 6, 7])],
        "title": "VAE",
        "properties": props("VAELoader"),
        "widgets_values": ["krea2RealVae_v10.safetensors"],
        "widgets_values_named": {"vae_name": "krea2RealVae_v10.safetensors"},
    })
    add({
        "id": 4, "type": "Krea2OstrisEditModelPatch", "pos": [-940, 40], "size": [280, 72],
        "flags": {}, "order": 3, "mode": 0,
        "inputs": [inp("model", "MODEL", 1)],
        "outputs": [out("MODEL", "MODEL", [8])],
        "title": "Ostris model patch",
        "properties": {**OSTRIS, "Node name for S&R": "Krea2OstrisEditModelPatch"},
        "widgets_values": [False],
        "widgets_values_named": {"kv_cache": False},
    })
    add({
        "id": 5, "type": "LoraLoader", "pos": [-940, 150], "size": [300, 126],
        "flags": {}, "order": 4, "mode": 0,
        "inputs": [inp("model", "MODEL", 8), inp("clip", "CLIP", 2)],
        "outputs": [out("MODEL", "MODEL", [9], 0), out("CLIP", "CLIP", None, 1)],
        "title": "Identity LoRA 1.0",
        "properties": props("LoraLoader"),
        "widgets_values": ["KreAlpha2640.safetensors", 1.0, 1.0],
        "widgets_values_named": {
            "lora_name": "KreAlpha2640.safetensors",
            "strength_model": 1.0,
            "strength_clip": 1.0,
        },
    })
    add({
        "id": 6, "type": "LoraLoaderModelOnly", "pos": [-940, 320], "size": [300, 82],
        "flags": {}, "order": 5, "mode": 0,
        "inputs": [inp("model", "MODEL", 9)],
        "outputs": [out("MODEL", "MODEL", [10])],
        "title": "Pose LoRA 0.9",
        "properties": props("LoraLoaderModelOnly"),
        "widgets_values": ["krea2_turbo_openpose_controlnet.safetensors", 0.9],
        "widgets_values_named": {
            "lora_name": "krea2_turbo_openpose_controlnet.safetensors",
            "strength_model": 0.9,
        },
    })
    add({
        "id": 70, "type": "PrimitiveStringMultiline", "pos": [-940, 440], "size": [360, 160],
        "flags": {}, "order": 6, "mode": 0, "inputs": [],
        "outputs": [out("STRING", "STRING", [80])],
        "title": "Identity + camera + lighting",
        "properties": props("PrimitiveStringMultiline"),
        "widgets_values": [IDENTITY],
        "widgets_values_named": {"value": IDENTITY},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 71, "type": "PrimitiveStringMultiline", "pos": [-940, 630], "size": [360, 120],
        "flags": {}, "order": 7, "mode": 0, "inputs": [],
        "outputs": [out("STRING", "STRING", [81])],
        "title": "Your adjustments (e.g. make the shirt red)",
        "properties": props("PrimitiveStringMultiline"),
        "widgets_values": [ADJUST],
        "widgets_values_named": {"value": ADJUST},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 72, "type": "StringConcatenate", "pos": [-540, 520], "size": [300, 130],
        "flags": {}, "order": 8, "mode": 0,
        "inputs": [
            inp("string_a", "STRING", 80, widget="string_a"),
            inp("string_b", "STRING", 81, widget="string_b"),
        ],
        "outputs": [out("STRING", "STRING", [130])],
        "title": "Join prompts",
        "properties": props("StringConcatenate"),
        "widgets_values": ["", "", ", "],
        "widgets_values_named": {"string_a": "", "string_b": "", "delimiter": ", "},
    })
    add({
        "id": 7, "type": "LoadImage", "pos": [-1400, 460], "size": [400, 360],
        "flags": {}, "order": 9, "mode": 0, "inputs": [],
        "outputs": [out("IMAGE", "IMAGE", [11], 0), out("MASK", "MASK", None, 1)],
        "title": "Scene photo",
        "properties": props("LoadImage"),
        "widgets_values": ["ExampleReferenceImage.png", "image"],
        "widgets_values_named": {"image": "ExampleReferenceImage.png", "upload": "image"},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 28, "type": "Note", "pos": [1680, 860], "size": [460, 280],
        "flags": {}, "order": 10, "mode": 0, "inputs": [], "outputs": [],
        "properties": {"Node name for S&R": "Note"},
        "widgets_values": [NOTE],
        "widgets_values_named": {"text": NOTE},
        "color": "#432",
        "bgcolor": "#653",
    })
    add({
        "id": 10, "type": "ImageScaleToTotalPixels", "pos": [-1400, 860], "size": [320, 106],
        "flags": {}, "order": 11, "mode": 0,
        "inputs": [inp("image", "IMAGE", 11)],
        "outputs": [out("IMAGE", "IMAGE", [14, 40, 71, 82, 132])],
        "title": "Draft size ~0.6MP (fast preview)",
        "properties": props("ImageScaleToTotalPixels"),
        "widgets_values": ["lanczos", 0.6, 1],
        "widgets_values_named": {"upscale_method": "lanczos", "megapixels": 0.6, "resolution_steps": 1},
    })
    add({
        "id": 11, "type": "GetImageSize", "pos": [-1040, 860], "size": [230, 82],
        "flags": {}, "order": 12, "mode": 0,
        "inputs": [inp("image", "IMAGE", 14)],
        "outputs": [
            out("width", "INT", [19, 90, 133], 0),
            out("height", "INT", [22, 91, 134], 1),
            out("batch_size", "INT", None, 2),
        ],
        "title": "Draft size",
        "properties": props("GetImageSize"),
    })
    add({
        "id": 12, "type": "EmptyLatentImage", "pos": [-780, 860], "size": [270, 106],
        "flags": {}, "order": 13, "mode": 0,
        "inputs": [
            inp("width", "INT", 90, widget="width"),
            inp("height", "INT", 91, widget="height"),
        ],
        "outputs": [out("LATENT", "LATENT", [70])],
        "title": "Empty latent (full generate, not a hole)",
        "properties": props("EmptyLatentImage"),
        "widgets_values": [1024, 1024, 1],
        "widgets_values_named": {"width": 1024, "height": 1024, "batch_size": 1},
    })

    wv, named = rmbg_widgets(2, 0, model="BEN")
    add({
        "id": 40, "type": "RMBG", "pos": [-1400, 1020], "size": [300, 292],
        "flags": {}, "order": 14, "mode": 0,
        "inputs": [inp("image", "IMAGE", 71)],
        "outputs": [
            out("IMAGE", "IMAGE", None, 0),
            out("MASK", "MASK", [64, 136], 1),
            out("MASK_IMAGE", "IMAGE", None, 2),
        ],
        "title": "Old person mask (RMBG)",
        "properties": RMBG,
        "widgets_values": wv,
        "widgets_values_named": named,
        "color": "#222e40",
        "bgcolor": "#364254",
    })
    add({
        "id": 41, "type": "GrowMask", "pos": [-1060, 1020], "size": [240, 82],
        "flags": {}, "order": 15, "mode": 0,
        "inputs": [inp("mask", "MASK", 64)],
        "outputs": [out("MASK", "MASK", [65])],
        "title": "Grow 20 — hide old person in image1",
        "properties": props("GrowMask"),
        "widgets_values": [20, True],
        "widgets_values_named": {"expand": 20, "tapered_corners": True},
    })
    add({
        "id": 42, "type": "GrowMask", "pos": [-1060, 1140], "size": [240, 82],
        "flags": {}, "order": 16, "mode": 0,
        "inputs": [inp("mask", "MASK", 136)],
        "outputs": [out("MASK", "MASK", [66])],
        "title": "Grow 6 — old person (LaMa hole)",
        "properties": props("GrowMask"),
        "widgets_values": [6, True],
        "widgets_values_named": {"expand": 6, "tapered_corners": True},
    })
    add({
        "id": 44, "type": "EmptyImage", "pos": [-800, 1020], "size": [250, 130],
        "flags": {}, "order": 18, "mode": 0,
        "inputs": [
            inp("width", "INT", 133, widget="width"),
            inp("height", "INT", 134, widget="height"),
        ],
        "outputs": [out("IMAGE", "IMAGE", [83])],
        "title": "Gray fill",
        "properties": props("EmptyImage"),
        "widgets_values": [512, 512, 1, 10526880],
        "widgets_values_named": {"width": 512, "height": 512, "batch_size": 1, "color": 10526880},
    })
    add({
        "id": 45, "type": "ImageCompositeMasked", "pos": [-520, 1020], "size": [300, 146],
        "flags": {}, "order": 19, "mode": 0,
        "inputs": [
            inp("destination", "IMAGE", 82),
            inp("source", "IMAGE", 83),
            inp("mask", "MASK", 65, shape=7),
        ],
        "outputs": [out("IMAGE", "IMAGE", [15, 16, 84])],
        "title": "image1 — scene, old person painted out",
        "properties": props("ImageCompositeMasked"),
        "widgets_values": [0, 0, False],
        "widgets_values_named": {"x": 0, "y": 0, "resize_source": False},
    })
    add({
        "id": 46, "type": "PreviewImage", "pos": [-200, 1020], "size": [220, 220],
        "flags": {}, "order": 20, "mode": 0,
        "inputs": [inp("images", "IMAGE", 84)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "image1 (lighting / camera)",
        "properties": props("PreviewImage"),
    })

    add({
        "id": 30, "type": "DWPreprocessor", "pos": [-1400, 1360], "size": [300, 222],
        "flags": {}, "order": 21, "mode": 0,
        "inputs": [inp("image", "IMAGE", 40)],
        "outputs": [
            out("IMAGE", "IMAGE", [41, 42, 43, 44], 0),
            out("POSE_KEYPOINT", "POSE_KEYPOINT", None, 1),
        ],
        "title": "DWPose from draft",
        "properties": AUX,
        "widgets_values": [
            "enable", "enable", "enable", 768,
            "yolox_l.onnx", "dw-ll_ucoco_studio_384_bs5.torchscript.pt", "disable",
        ],
        "widgets_values_named": {
            "detect_hand": "enable",
            "detect_body": "enable",
            "detect_face": "enable",
            "resolution": 768,
            "bbox_detector": "yolox_l.onnx",
            "pose_estimator": "dw-ll_ucoco_384_bs5.torchscript.pt",
            "scale_stick_for_xinsr_cn": "disable",
        },
        "color": "#322",
        "bgcolor": "#533",
    })
    # Fix pose estimator filename - I typo'd studio. Use the real name.
    nodes[-1]["widgets_values"][5] = "dw-ll_ucoco_384_bs5.torchscript.pt"

    add({
        "id": 31, "type": "PreviewImage", "pos": [-1060, 1360], "size": [200, 200],
        "flags": {}, "order": 22, "mode": 0,
        "inputs": [inp("images", "IMAGE", 41)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Raw DWPose",
        "properties": props("PreviewImage"),
    })
    add({
        "id": 32, "type": "GetImageSize", "pos": [-1400, 1620], "size": [230, 82],
        "flags": {}, "order": 23, "mode": 0,
        "inputs": [inp("image", "IMAGE", 42)],
        "outputs": [
            out("width", "INT", [45], 0),
            out("height", "INT", [46], 1),
            out("batch_size", "INT", None, 2),
        ],
        "title": "Pose map size",
        "properties": props("GetImageSize"),
    })
    add({
        "id": 33, "type": "EmptyImage", "pos": [-1140, 1620], "size": [250, 130],
        "flags": {}, "order": 24, "mode": 0,
        "inputs": [
            inp("width", "INT", 45, widget="width"),
            inp("height", "INT", 46, widget="height"),
        ],
        "outputs": [out("IMAGE", "IMAGE", [47])],
        "title": "Light-gray canvas",
        "properties": props("EmptyImage"),
        "widgets_values": [512, 512, 1, 10526880],
        "widgets_values_named": {"width": 512, "height": 512, "batch_size": 1, "color": 10526880},
    })
    add({
        "id": 34, "type": "ColorToMask", "pos": [-860, 1620], "size": [260, 178],
        "flags": {}, "order": 25, "mode": 0,
        "inputs": [inp("images", "IMAGE", 43)],
        "outputs": [out("MASK", "MASK", [48])],
        "title": "Near-black pose background",
        "properties": KJ,
        "widgets_values": [False, 0, 0, 0, 48, 16],
        "widgets_values_named": {
            "invert": False, "red": 0, "green": 0, "blue": 0, "threshold": 48, "per_batch": 16,
        },
    })
    add({
        "id": 36, "type": "GrowMask", "pos": [-580, 1620], "size": [240, 82],
        "flags": {}, "order": 26, "mode": 0,
        "inputs": [inp("mask", "MASK", 48)],
        "outputs": [out("MASK", "MASK", [49])],
        "title": "Grow black fill",
        "properties": props("GrowMask"),
        "widgets_values": [2, True],
        "widgets_values_named": {"expand": 2, "tapered_corners": True},
    })
    add({
        "id": 35, "type": "ImageCompositeMasked", "pos": [-320, 1620], "size": [300, 146],
        "flags": {}, "order": 27, "mode": 0,
        "inputs": [
            inp("destination", "IMAGE", 44),
            inp("source", "IMAGE", 47),
            inp("mask", "MASK", 49, shape=7),
        ],
        "outputs": [out("IMAGE", "IMAGE", [12])],
        "title": "Replace black bg with gray",
        "properties": props("ImageCompositeMasked"),
        "widgets_values": [0, 0, True],
        "widgets_values_named": {"x": 0, "y": 0, "resize_source": True},
    })
    add({
        "id": 13, "type": "ImageScale", "pos": [0, 1620], "size": [280, 150],
        "flags": {}, "order": 28, "mode": 0,
        "inputs": [
            inp("image", "IMAGE", 12),
            inp("width", "INT", 19, widget="width"),
            inp("height", "INT", 22, widget="height"),
        ],
        "outputs": [out("IMAGE", "IMAGE", [25, 26, 27])],
        "title": "Pose to draft size (no crop)",
        "properties": props("ImageScale"),
        "widgets_values": ["lanczos", 1024, 1024, "disabled"],
        "widgets_values_named": {
            "upscale_method": "lanczos", "width": 1024, "height": 1024, "crop": "disabled",
        },
    })
    add({
        "id": 14, "type": "PreviewImage", "pos": [300, 1620], "size": [220, 220],
        "flags": {}, "order": 29, "mode": 0,
        "inputs": [inp("images", "IMAGE", 25)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Pose ref (image2)",
        "properties": props("PreviewImage"),
    })

    add({
        "id": 15, "type": "TextEncodeKrea2OstrisEdit", "pos": [-200, 40], "size": [420, 200],
        "flags": {}, "order": 30, "mode": 0,
        "inputs": ostris_in(3, 5, 15, 26, 130),
        "outputs": [out("CONDITIONING", "CONDITIONING", [30])],
        "title": "Positive draft (image1=scene, image2=pose)",
        "properties": {**OSTRIS, "Node name for S&R": "TextEncodeKrea2OstrisEdit"},
        "widgets_values": [""],
        "widgets_values_named": {"prompt": ""},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 16, "type": "TextEncodeKrea2OstrisEdit", "pos": [-200, 280], "size": [420, 140],
        "flags": {}, "order": 31, "mode": 0,
        "inputs": ostris_in(4, 6, 16, 27),
        "outputs": [out("CONDITIONING", "CONDITIONING", [31])],
        "title": "Negative draft",
        "properties": {**OSTRIS, "Node name for S&R": "TextEncodeKrea2OstrisEdit"},
        "widgets_values": [NEG],
        "widgets_values_named": {"prompt": NEG},
    })
    add({
        "id": 17, "type": "FluxKontextMultiReferenceLatentMethod", "pos": [260, 40], "size": [340, 58],
        "flags": {}, "order": 32, "mode": 0,
        "inputs": [inp("conditioning", "CONDITIONING", 30)],
        "outputs": [out("CONDITIONING", "CONDITIONING", [32])],
        "title": "Positive refs",
        "properties": props("FluxKontextMultiReferenceLatentMethod"),
        "widgets_values": ["index_timestep_zero"],
        "widgets_values_named": {"reference_latents_method": "index_timestep_zero"},
    })
    add({
        "id": 18, "type": "FluxKontextMultiReferenceLatentMethod", "pos": [260, 140], "size": [340, 58],
        "flags": {}, "order": 33, "mode": 0,
        "inputs": [inp("conditioning", "CONDITIONING", 31)],
        "outputs": [out("CONDITIONING", "CONDITIONING", [33])],
        "title": "Negative refs",
        "properties": props("FluxKontextMultiReferenceLatentMethod"),
        "widgets_values": ["index_timestep_zero"],
        "widgets_values_named": {"reference_latents_method": "index_timestep_zero"},
    })
    add({
        "id": 19, "type": "KSampler", "pos": [640, 40], "size": [320, 262],
        "flags": {}, "order": 34, "mode": 0,
        "inputs": [
            inp("model", "MODEL", 10),
            inp("positive", "CONDITIONING", 32),
            inp("negative", "CONDITIONING", 33),
            inp("latent_image", "LATENT", 70),
        ],
        "outputs": [out("LATENT", "LATENT", [34])],
        "title": "Draft 8 steps",
        "properties": props("KSampler"),
        "widgets_values": [42, "randomize", 8, 1, "euler", "simple", 1],
        "widgets_values_named": {
            "seed": 42, "control_after_generate": "randomize",
            "steps": 8, "cfg": 1, "sampler_name": "euler",
            "scheduler": "simple", "denoise": 1,
        },
    })
    add({
        "id": 20, "type": "VAEDecode", "pos": [1000, 40], "size": [210, 46],
        "flags": {}, "order": 35, "mode": 0,
        "inputs": [inp("samples", "LATENT", 34), inp("vae", "VAE", 7)],
        "outputs": [out("IMAGE", "IMAGE", [35, 85, 135])],
        "title": "Decode draft",
        "properties": props("VAEDecode"),
    })
    add({
        "id": 21, "type": "PreviewImage", "pos": [1240, 40], "size": [320, 400],
        "flags": {}, "order": 36, "mode": 0,
        "inputs": [inp("images", "IMAGE", 35)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Draft generate (check pose here)",
        "properties": props("PreviewImage"),
        "color": "#322",
        "bgcolor": "#533",
    })

    wv2, named2 = rmbg_widgets(2, 0, model="BEN")
    named2["process_res"] = 1024
    wv2[2] = 1024
    add({
        "id": 50, "type": "RMBG", "pos": [640, 360], "size": [300, 292],
        "flags": {}, "order": 37, "mode": 0,
        "inputs": [inp("image", "IMAGE", 85)],
        "outputs": [
            out("IMAGE", "IMAGE", None, 0),
            out("MASK", "MASK", [86], 1),
            out("MASK_IMAGE", "IMAGE", None, 2),
        ],
        "title": "NEW person cutout (from generate)",
        "properties": RMBG,
        "widgets_values": wv2,
        "widgets_values_named": named2,
        "color": "#222e40",
        "bgcolor": "#364254",
    })
    add({
        "id": 51, "type": "GrowMask", "pos": [960, 360], "size": [240, 82],
        "flags": {}, "order": 38, "mode": 0,
        "inputs": [inp("mask", "MASK", 86)],
        "outputs": [out("MASK", "MASK", [87, 140])],
        "title": "Grow 2 — new person paste",
        "properties": props("GrowMask"),
        "widgets_values": [2, True],
        "widgets_values_named": {"expand": 2, "tapered_corners": True},
    })
    add({
        "id": 52, "type": "FeatherMask", "pos": [960, 470], "size": [250, 154],
        "flags": {}, "order": 39, "mode": 0,
        "inputs": [inp("mask", "MASK", 87)],
        "outputs": [out("MASK", "MASK", [88])],
        "title": "Feather new person",
        "properties": props("FeatherMask"),
        "widgets_values": [8, 8, 8, 8],
        "widgets_values_named": {"left": 8, "top": 8, "right": 8, "bottom": 8},
    })
    add({
        "id": 53, "type": "MaskComposite", "pos": [1220, 360], "size": [280, 154],
        "flags": {}, "order": 40, "mode": 0,
        "inputs": [
            inp("destination", "MASK", 66),
            inp("source", "MASK", 140),
        ],
        "outputs": [out("MASK", "MASK", [89])],
        "title": "Leftover hole (old minus new)",
        "properties": props("MaskComposite"),
        "widgets_values": [0, 0, "subtract"],
        "widgets_values_named": {"x": 0, "y": 0, "operation": "subtract"},
    })
    add({
        "id": 56, "type": "MaskToImage", "pos": [1520, 360], "size": [180, 26],
        "flags": {"collapsed": True}, "order": 41, "mode": 0,
        "inputs": [inp("mask", "MASK", 89)],
        "outputs": [out("IMAGE", "IMAGE", [93])],
        "title": "Leftover to image",
        "properties": props("MaskToImage"),
    })
    add({
        "id": 47, "type": "PreviewImage", "pos": [1520, 400], "size": [200, 200],
        "flags": {}, "order": 42, "mode": 0,
        "inputs": [inp("images", "IMAGE", 93)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Leftover hole (LaMa fills this)",
        "properties": props("PreviewImage"),
    })
    add({
        "id": 76, "type": "AILab_LamaRemover", "pos": [640, 680], "size": [300, 106],
        "flags": {}, "order": 43, "mode": 0,
        "inputs": [
            inp("images", "IMAGE", 132),
            inp("masks", "MASK", 66),
        ],
        "outputs": [out("images", "IMAGE", [146, 147])],
        "title": "LaMa — remove old person from kitchen",
        "properties": LAMA,
        "widgets_values": [200, 8],
        "widgets_values_named": {"removal_strength": 200, "edge_smoothness": 8},
        "color": "#222e40",
        "bgcolor": "#364254",
    })
    add({
        "id": 77, "type": "PreviewImage", "pos": [960, 680], "size": [260, 260],
        "flags": {}, "order": 44, "mode": 0,
        "inputs": [inp("images", "IMAGE", 147)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Kitchen after LaMa (no old person)",
        "properties": props("PreviewImage"),
    })
    add({
        "id": 55, "type": "ImageCompositeMasked", "pos": [1240, 680], "size": [320, 146],
        "flags": {}, "order": 45, "mode": 0,
        "inputs": [
            inp("destination", "IMAGE", 146),
            inp("source", "IMAGE", 135),
            inp("mask", "MASK", 88, shape=7),
        ],
        "outputs": [out("IMAGE", "IMAGE", [94, 95])],
        "title": "Paste new person onto LaMa kitchen",
        "properties": props("ImageCompositeMasked"),
        "widgets_values": [0, 0, False],
        "widgets_values_named": {"x": 0, "y": 0, "resize_source": False},
    })
    add({
        "id": 22, "type": "PreviewImage", "pos": [1580, 40], "size": [360, 400],
        "flags": {}, "order": 45, "mode": 0,
        "inputs": [inp("images", "IMAGE", 94)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Married draft",
        "properties": props("PreviewImage"),
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 60, "type": "ImageScaleToTotalPixels", "pos": [980, 680], "size": [320, 106],
        "flags": {}, "order": 46, "mode": 0,
        "inputs": [inp("image", "IMAGE", 95)],
        "outputs": [out("IMAGE", "IMAGE", [96, 97])],
        "title": "Upscale married ~1.8MP",
        "properties": props("ImageScaleToTotalPixels"),
        "widgets_values": ["lanczos", 1.8, 1],
        "widgets_values_named": {"upscale_method": "lanczos", "megapixels": 1.8, "resolution_steps": 1},
    })
    add({
        "id": 24, "type": "PreviewImage", "pos": [1320, 680], "size": [400, 520],
        "flags": {}, "order": 47, "mode": 0,
        "inputs": [inp("images", "IMAGE", 96)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Final",
        "properties": props("PreviewImage"),
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 23, "type": "SaveImage", "pos": [1320, 1220], "size": [400, 58],
        "flags": {}, "order": 48, "mode": 0,
        "inputs": [inp("images", "IMAGE", 97)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Save final",
        "properties": props("SaveImage"),
        "widgets_values": ["krea2_edited_frame"],
        "widgets_values_named": {"filename_prefix": "krea2_edited_frame"},
    })

    producers: dict[int, tuple[int, int, str]] = {}
    for n in nodes:
        for slot, o in enumerate(n.get("outputs") or []):
            for lid in o.get("links") or []:
                producers[lid] = (n["id"], slot, o["type"])

    links = []
    for n in nodes:
        for slot, i in enumerate(n.get("inputs") or []):
            lid = i.get("link")
            if lid is None:
                continue
            if lid not in producers:
                raise SystemExit(f"missing producer for link {lid} -> node {n['id']} {i['name']}")
            src, src_slot, typ = producers[lid]
            if typ != i["type"]:
                raise SystemExit(f"type mismatch link {lid}: {typ} vs {i['type']}")
            links.append([lid, src, src_slot, n["id"], slot, typ])

    extra_prod = set(producers) - {row[0] for row in links}
    if extra_prod:
        raise SystemExit(f"unused link ids: {sorted(extra_prod)}")

    graph = {
        "id": "krea2-edited-frame",
        "revision": 0,
        "last_node_id": 77,
        "last_link_id": 147,
        "nodes": nodes,
        "links": links,
        "groups": [
            {"id": 1, "title": "Models + prompts", "bounding": [-1440, 0, 1240, 430], "color": "#3f789e", "flags": {}},
            {"id": 2, "title": "Draft photo, hide old person, pose", "bounding": [-1440, 430, 2000, 1480], "color": "#322", "flags": {}},
            {"id": 3, "title": "Draft generate (empty latent)", "bounding": [-240, 0, 1860, 680], "color": "#3f789e", "flags": {}},
            {"id": 4, "title": "LaMa hole fill + paste new person + upscale", "bounding": [600, 660, 1160, 640], "color": "#3f789e", "flags": {}},
        ],
        "config": {},
        "extra": {
            "ds": {"scale": 0.42, "offset": [1480, 80]},
            "frontendVersion": "1.52.7",
            "visagely": {
                "title": "Replace person: LaMa kitchen + paste LoRA person",
                "notes": "Empty latent draft. BEN person masks. LaMa removes the old person. Paste only the new person onto the cleaned kitchen.",
            },
        },
        "version": 0.4,
        "floatingLinks": [],
        "definitions": {},
    }

    text = json.dumps(graph, indent=2) + "\n"
    out_dir = Path("/workspace/docs/comfyui/workflows")
    for name in (
        "replace-character-baked.json",
        "Inpaint.json",
        "InpaintV6.json",
        "inpaint-replace-character-krea2.json",
        "Edited_Frame.json",
    ):
        (out_dir / name).write_text(text)
    print(f"wrote {len(nodes)} nodes, {len(links)} links")


if __name__ == "__main__":
    main()

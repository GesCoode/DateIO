#!/usr/bin/env python3
"""Build the baked kitchen/pose/mask Krea2 character-replace graph."""
from __future__ import annotations

import json
from pathlib import Path

PROMPT = (
    "vsgly_id, a man with short dark wavy hair and a short beard, "
    "white long-sleeve shirt, denim shorts, standing in a bright white kitchen, photorealistic"
)

CORE = {"cnr_id": "comfy-core", "ver": "0.37.0"}
OSTRIS = {
    "aux_id": "ostris/comfyui-krea2-ostris-edit",
    "ver": "7756566160c4a1b24bb1bd9f0ff3ced1a83d7547",
    "cnr_id": "comfyui-krea2-ostris-edit",
}


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


def named_from_widgets(mapping: dict) -> dict:
    return mapping


def main() -> None:
    nodes: list[dict] = []

    def add(n: dict) -> None:
        nodes.append(n)

    add({
        "id": 1, "type": "UNETLoader", "pos": [-1180, 40], "size": [400, 82],
        "flags": {}, "order": 0, "mode": 0, "inputs": [],
        "outputs": [out("MODEL", "MODEL", [1])],
        "title": "UNET (Sick Ollie / Krea2)",
        "properties": props("UNETLoader"),
        "widgets_values": ["SICK_OLLIE_Krea2_BF16.safetensors", "default"],
        "widgets_values_named": {"unet_name": "SICK_OLLIE_Krea2_BF16.safetensors", "weight_dtype": "default"},
    })
    add({
        "id": 2, "type": "CLIPLoader", "pos": [-1180, 160], "size": [400, 106],
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
        "id": 3, "type": "VAELoader", "pos": [-1180, 310], "size": [400, 58],
        "flags": {}, "order": 2, "mode": 0, "inputs": [],
        "outputs": [out("VAE", "VAE", [5, 6, 7])],
        "title": "VAE (qwen_image or krea2RealVae_v10)",
        "properties": props("VAELoader"),
        "widgets_values": ["qwen_image_vae.safetensors"],
        "widgets_values_named": {"vae_name": "qwen_image_vae.safetensors"},
    })
    add({
        "id": 4, "type": "Krea2OstrisEditModelPatch", "pos": [-720, 40], "size": [280, 72],
        "flags": {}, "order": 3, "mode": 0,
        "inputs": [inp("model", "MODEL", 1)],
        "outputs": [out("MODEL", "MODEL", [8])],
        "title": "Ostris model patch",
        "properties": {**OSTRIS, "Node name for S&R": "Krea2OstrisEditModelPatch"},
        "widgets_values": [False],
        "widgets_values_named": {"kv_cache": False},
    })
    add({
        "id": 5, "type": "LoraLoader", "pos": [-720, 150], "size": [300, 126],
        "flags": {}, "order": 4, "mode": 0,
        "inputs": [inp("model", "MODEL", 8), inp("clip", "CLIP", 2)],
        "outputs": [out("MODEL", "MODEL", [9], 0), out("CLIP", "CLIP", None, 1)],
        "title": "Identity LoRA",
        "properties": props("LoraLoader"),
        "widgets_values": ["KreAlpha2640.safetensors", 0.9, 1.0],
        "widgets_values_named": {
            "lora_name": "KreAlpha2640.safetensors",
            "strength_model": 0.9,
            "strength_clip": 1.0,
        },
    })
    add({
        "id": 6, "type": "LoraLoaderModelOnly", "pos": [-720, 320], "size": [300, 82],
        "flags": {}, "order": 5, "mode": 0,
        "inputs": [inp("model", "MODEL", 9)],
        "outputs": [out("MODEL", "MODEL", [10])],
        "title": "Pose LoRA 0.45 (photo wins lean)",
        "properties": props("LoraLoaderModelOnly"),
        "widgets_values": ["krea2_turbo_openpose_controlnet.safetensors", 0.45],
        "widgets_values_named": {
            "lora_name": "krea2_turbo_openpose_controlnet.safetensors",
            "strength_model": 0.45,
        },
    })

    add({
        "id": 7, "type": "LoadImage", "pos": [-1180, 460], "size": [400, 360],
        "flags": {}, "order": 6, "mode": 0, "inputs": [],
        "outputs": [out("IMAGE", "IMAGE", [11], 0), out("MASK", "MASK", None, 1)],
        "title": "1. Kitchen (baked background)",
        "properties": props("LoadImage"),
        "widgets_values": ["ExampleReferenceImage.png", "image"],
        "widgets_values_named": {"image": "ExampleReferenceImage.png", "upload": "image"},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 8, "type": "LoadImage", "pos": [-760, 460], "size": [400, 360],
        "flags": {}, "order": 7, "mode": 0, "inputs": [],
        "outputs": [out("IMAGE", "IMAGE", [12], 0), out("MASK", "MASK", None, 1)],
        "title": "2. Pose map (gray bg, baked)",
        "properties": props("LoadImage"),
        "widgets_values": ["ExampleReferenceImage.png", "image"],
        "widgets_values_named": {"image": "ExampleReferenceImage.png", "upload": "image"},
        "color": "#322",
        "bgcolor": "#533",
    })
    add({
        "id": 9, "type": "LoadImage", "pos": [-340, 460], "size": [400, 360],
        "flags": {}, "order": 8, "mode": 0, "inputs": [],
        "outputs": [out("IMAGE", "IMAGE", [13], 0), out("MASK", "MASK", None, 1)],
        "title": "3. Person mask (white=person)",
        "properties": props("LoadImage"),
        "widgets_values": ["ExampleReferenceImage.png", "image"],
        "widgets_values_named": {"image": "ExampleReferenceImage.png", "upload": "image"},
        "color": "#432",
        "bgcolor": "#653",
    })

    add({
        "id": 28, "type": "Note", "pos": [80, 460], "size": [420, 360],
        "flags": {}, "order": 9, "mode": 0, "inputs": [], "outputs": [],
        "properties": {"Node name for S&R": "Note"},
        "widgets_values": [
            "Baked inputs — no SAM3 / RMBG / Lama / DWPose.\n\n"
            "1 Kitchen: the photo to keep.\n"
            "2 Pose: OpenPose/DWPose PNG. Use a MID-GRAY background, not black "
            "(black pose bg speckles the shirt).\n"
            "3 Mask: white person, black kitchen. Photoshop is fine. Does not need to be perfect.\n\n"
            "CLIP type MUST be krea2 (ComfyUI >= 0.26).\n"
            "Pose is the pose map + pose LoRA. Do not describe pose in the prompt.\n"
            "Skip the composite Save if you will cut in Photoshop — use Edited frame."
        ],
        "widgets_values_named": {
            "text": (
                "Baked inputs — no SAM3 / RMBG / Lama / DWPose.\n\n"
                "1 Kitchen: the photo to keep.\n"
                "2 Pose: OpenPose/DWPose PNG. Use a MID-GRAY background, not black "
                "(black pose bg speckles the shirt).\n"
                "3 Mask: white person, black kitchen. Photoshop is fine. Does not need to be perfect.\n\n"
                "CLIP type MUST be krea2 (ComfyUI >= 0.26).\n"
                "Pose is the pose map + pose LoRA. Do not describe pose in the prompt.\n"
                "Skip the composite Save if you will cut in Photoshop — use Edited frame."
            )
        },
        "color": "#432",
        "bgcolor": "#653",
    })

    add({
        "id": 10, "type": "ImageScaleToTotalPixels", "pos": [-1180, 860], "size": [320, 106],
        "flags": {}, "order": 10, "mode": 0,
        "inputs": [inp("image", "IMAGE", 11)],
        "outputs": [out("IMAGE", "IMAGE", [14, 15, 16, 17])],
        "title": "Scale kitchen ~1.5MP",
        "properties": props("ImageScaleToTotalPixels"),
        "widgets_values": ["lanczos", 1.5, 1],
        "widgets_values_named": {"upscale_method": "lanczos", "megapixels": 1.5, "resolution_steps": 1},
    })
    add({
        "id": 11, "type": "GetImageSize", "pos": [-820, 860], "size": [230, 82],
        "flags": {}, "order": 11, "mode": 0,
        "inputs": [inp("image", "IMAGE", 14)],
        "outputs": [
            out("width", "INT", [18, 19, 20], 0),
            out("height", "INT", [21, 22, 23], 1),
            out("batch_size", "INT", None, 2),
        ],
        "title": "Kitchen size",
        "properties": props("GetImageSize"),
    })
    add({
        "id": 12, "type": "EmptyLatentImage", "pos": [-560, 860], "size": [270, 106],
        "flags": {}, "order": 12, "mode": 0,
        "inputs": [
            inp("width", "INT", 18, widget="width"),
            inp("height", "INT", 21, widget="height"),
        ],
        "outputs": [out("LATENT", "LATENT", [24])],
        "title": "Latent at kitchen size",
        "properties": props("EmptyLatentImage"),
        "widgets_values": [1024, 1024, 1],
        "widgets_values_named": {"width": 1024, "height": 1024, "batch_size": 1},
    })
    add({
        "id": 13, "type": "ImageScale", "pos": [-760, 1000], "size": [280, 150],
        "flags": {}, "order": 13, "mode": 0,
        "inputs": [
            inp("image", "IMAGE", 12),
            inp("width", "INT", 19, widget="width"),
            inp("height", "INT", 22, widget="height"),
        ],
        "outputs": [out("IMAGE", "IMAGE", [25, 26, 27])],
        "title": "Pose to kitchen size (no crop)",
        "properties": props("ImageScale"),
        "widgets_values": ["lanczos", 1024, 1024, "disabled"],
        "widgets_values_named": {
            "upscale_method": "lanczos",
            "width": 1024,
            "height": 1024,
            "crop": "disabled",
        },
    })
    add({
        "id": 14, "type": "PreviewImage", "pos": [-440, 1000], "size": [240, 240],
        "flags": {}, "order": 14, "mode": 0,
        "inputs": [inp("images", "IMAGE", 25)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Pose ref (image2)",
        "properties": props("PreviewImage"),
    })
    add({
        "id": 23, "type": "ImageScale", "pos": [-340, 1000], "size": [280, 150],
        "flags": {}, "order": 15, "mode": 0,
        "inputs": [
            inp("image", "IMAGE", 13),
            inp("width", "INT", 20, widget="width"),
            inp("height", "INT", 23, widget="height"),
        ],
        "outputs": [out("IMAGE", "IMAGE", [28])],
        "title": "Mask to kitchen size",
        "properties": props("ImageScale"),
        "widgets_values": ["lanczos", 1024, 1024, "disabled"],
        "widgets_values_named": {
            "upscale_method": "lanczos",
            "width": 1024,
            "height": 1024,
            "crop": "disabled",
        },
    })
    add({
        "id": 24, "type": "ImageToMask", "pos": [-20, 1000], "size": [210, 58],
        "flags": {}, "order": 16, "mode": 0,
        "inputs": [inp("image", "IMAGE", 28)],
        "outputs": [out("MASK", "MASK", [29])],
        "title": "White = person",
        "properties": props("ImageToMask"),
        "widgets_values": ["red"],
        "widgets_values_named": {"channel": "red"},
    })

    def ostris(clip_l, vae_l, img1, img2):
        return [
            inp("clip", "CLIP", clip_l),
            inp("vae", "VAE", vae_l, shape=7),
            inp("image1", "IMAGE", img1, shape=7),
            inp("image2", "IMAGE", img2, shape=7),
            inp("image3", "IMAGE", None, shape=7),
        ]

    add({
        "id": 15, "type": "TextEncodeKrea2OstrisEdit", "pos": [-380, 40], "size": [420, 200],
        "flags": {}, "order": 17, "mode": 0,
        "inputs": ostris(3, 5, 15, 26),
        "outputs": [out("CONDITIONING", "CONDITIONING", [30])],
        "title": "Positive (image1=kitchen, image2=pose)",
        "properties": {**OSTRIS, "Node name for S&R": "TextEncodeKrea2OstrisEdit"},
        "widgets_values": [PROMPT],
        "widgets_values_named": {"prompt": PROMPT},
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 16, "type": "TextEncodeKrea2OstrisEdit", "pos": [-380, 280], "size": [420, 140],
        "flags": {}, "order": 18, "mode": 0,
        "inputs": ostris(4, 6, 16, 27),
        "outputs": [out("CONDITIONING", "CONDITIONING", [31])],
        "title": "Negative (empty)",
        "properties": {**OSTRIS, "Node name for S&R": "TextEncodeKrea2OstrisEdit"},
        "widgets_values": [""],
        "widgets_values_named": {"prompt": ""},
    })
    add({
        "id": 17, "type": "FluxKontextMultiReferenceLatentMethod", "pos": [80, 40], "size": [340, 58],
        "flags": {}, "order": 19, "mode": 0,
        "inputs": [inp("conditioning", "CONDITIONING", 30)],
        "outputs": [out("CONDITIONING", "CONDITIONING", [32])],
        "title": "Positive refs",
        "properties": props("FluxKontextMultiReferenceLatentMethod"),
        "widgets_values": ["index_timestep_zero"],
        "widgets_values_named": {"reference_latents_method": "index_timestep_zero"},
    })
    add({
        "id": 18, "type": "FluxKontextMultiReferenceLatentMethod", "pos": [80, 140], "size": [340, 58],
        "flags": {}, "order": 20, "mode": 0,
        "inputs": [inp("conditioning", "CONDITIONING", 31)],
        "outputs": [out("CONDITIONING", "CONDITIONING", [33])],
        "title": "Negative refs",
        "properties": props("FluxKontextMultiReferenceLatentMethod"),
        "widgets_values": ["index_timestep_zero"],
        "widgets_values_named": {"reference_latents_method": "index_timestep_zero"},
    })
    add({
        "id": 19, "type": "KSampler", "pos": [460, 40], "size": [320, 262],
        "flags": {}, "order": 21, "mode": 0,
        "inputs": [
            inp("model", "MODEL", 10),
            inp("positive", "CONDITIONING", 32),
            inp("negative", "CONDITIONING", 33),
            inp("latent_image", "LATENT", 24),
        ],
        "outputs": [out("LATENT", "LATENT", [34])],
        "title": "KSampler (edit kitchen)",
        "properties": props("KSampler"),
        "widgets_values": [42, "randomize", 10, 1, "euler", "simple", 1],
        "widgets_values_named": {
            "seed": 42,
            "control_after_generate": "randomize",
            "steps": 10,
            "cfg": 1,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1,
        },
    })
    add({
        "id": 20, "type": "VAEDecode", "pos": [820, 40], "size": [210, 46],
        "flags": {}, "order": 22, "mode": 0,
        "inputs": [inp("samples", "LATENT", 34), inp("vae", "VAE", 7)],
        "outputs": [out("IMAGE", "IMAGE", [35, 36, 37])],
        "title": "VAE Decode",
        "properties": props("VAEDecode"),
    })
    add({
        "id": 21, "type": "PreviewImage", "pos": [1060, 40], "size": [360, 520],
        "flags": {}, "order": 23, "mode": 0,
        "inputs": [inp("images", "IMAGE", 35)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Edited frame (use this if compositing in PS)",
        "properties": props("PreviewImage"),
        "color": "#232",
        "bgcolor": "#353",
    })
    add({
        "id": 22, "type": "SaveImage", "pos": [1060, 580], "size": [360, 58],
        "flags": {}, "order": 24, "mode": 0,
        "inputs": [inp("images", "IMAGE", 36)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Save edited frame",
        "properties": props("SaveImage"),
        "widgets_values": ["krea2_edited_frame"],
        "widgets_values_named": {"filename_prefix": "krea2_edited_frame"},
    })

    add({
        "id": 25, "type": "ImageCompositeMasked", "pos": [220, 1000], "size": [300, 146],
        "flags": {}, "order": 25, "mode": 0,
        "inputs": [
            inp("destination", "IMAGE", 17),
            inp("source", "IMAGE", 37),
            inp("mask", "MASK", 29, shape=7),
        ],
        "outputs": [out("IMAGE", "IMAGE", [38, 39])],
        "title": "Optional: paste on baked kitchen",
        "properties": props("ImageCompositeMasked"),
        "widgets_values": [0, 0, False],
        "widgets_values_named": {"x": 0, "y": 0, "resize_source": False},
    })
    add({
        "id": 26, "type": "PreviewImage", "pos": [560, 1000], "size": [300, 360],
        "flags": {}, "order": 26, "mode": 0,
        "inputs": [inp("images", "IMAGE", 38)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Composite (mask not critical)",
        "properties": props("PreviewImage"),
    })
    add({
        "id": 27, "type": "SaveImage", "pos": [560, 1380], "size": [300, 58],
        "flags": {}, "order": 27, "mode": 0,
        "inputs": [inp("images", "IMAGE", 39)],
        "outputs": [out("IMAGE", "IMAGE", None)],
        "title": "Save composite",
        "properties": props("SaveImage"),
        "widgets_values": ["krea2_pose_composite"],
        "widgets_values_named": {"filename_prefix": "krea2_pose_composite"},
    })

    by_id = {n["id"]: n for n in nodes}
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

    used = {row[0] for row in links}
    extra_prod = set(producers) - used
    if extra_prod:
        raise SystemExit(f"unused link ids: {sorted(extra_prod)}")

    graph = {
        "id": "krea2-replace-character-baked",
        "revision": 0,
        "last_node_id": 28,
        "last_link_id": 39,
        "nodes": nodes,
        "links": links,
        "groups": [
            {"id": 1, "title": "Models", "bounding": [-1220, 0, 820, 430], "color": "#3f789e", "flags": {}},
            {"id": 2, "title": "Baked kitchen / pose / mask", "bounding": [-1220, 430, 1760, 400], "color": "#8A5530", "flags": {}},
            {"id": 3, "title": "Edit (Ostris image1=kitchen, image2=pose)", "bounding": [-420, 0, 1860, 430], "color": "#3f789e", "flags": {}},
            {"id": 4, "title": "Optional Photoshop-style composite", "bounding": [-380, 960, 1280, 500], "color": "#2B6B4A", "flags": {}},
        ],
        "config": {},
        "extra": {
            "ds": {"scale": 0.55, "offset": [1280, 40]},
            "frontendVersion": "1.52.7",
            "visagely": {
                "title": "Replace character — baked kitchen, pose, mask",
                "notes": (
                    "No SAM3/RMBG/Lama/DWPose. Ostris image1=kitchen, image2=gray pose. "
                    "Identity LoRA 0.9, pose LoRA 0.45, CLIP type krea2, euler/simple/cfg 1/10 steps."
                ),
            },
        },
        "version": 0.4,
        "floatingLinks": [],
        "definitions": {},
    }

    text = json.dumps(graph, indent=2) + "\n"
    out_dir = Path("/workspace/docs/comfyui/workflows")
    (out_dir / "replace-character-baked.json").write_text(text)
    (out_dir / "Inpaint.json").write_text(text)
    (out_dir / "inpaint-replace-character-krea2.json").write_text(text)
    print(f"wrote {len(nodes)} nodes, {len(links)} links")


if __name__ == "__main__":
    main()

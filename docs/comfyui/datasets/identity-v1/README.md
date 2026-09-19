# identity-v1 dataset

Put **your** photos in `images/`. Do not commit real selfies to git — `images/` is gitignored
except for the caption template.

## Layout

```
identity-v1/
  README.md          ← this file
  dataset.toml       ← kohya / FluxTrainer
  captions.example.txt
  images/
    001.jpg
    001.txt
    ...
```

## Shot list (15–25 images)

Tick these off while shooting. Natural light > ring light. Neutral / slight smile. 18+ only.

- [ ] 4–6 extreme close-ups (eyes and nose fill most of the frame, several angles)
- [ ] 8–10 head-and-shoulders
- [ ] 4–6 chest-up / three-quarter
- [ ] 3–5 full body, feet in frame
- [ ] At least 3 lighting situations
- [ ] At least 3 outfits
- [ ] No sunglasses, no second person, no heavy filters, no NSFW

## Caption rules

Filename: `003.jpg` + `003.txt` (same stem). One line, trigger **first**:

```
vsgly_id, a man with short dark wavy hair and a short beard, brown eyes, looking at camera, head and shoulders, overcast outdoor light
```

- Name **stable identity traits** (hair, beard, eye colour, age-range look).
- Name **this photo’s** framing and light.
- **Do not** lock clothing/scene if you want those to vary at generation time.
- Never caption other people.

Change `vsgly_id` in `dataset.toml` if you pick a different trigger — keep it unique.

## Training pointer

On the rented box, put jpg+txt into `/workspace/flux_train/images/` and run
[`../../training/kohya-flux-48gb.sh`](../../training/kohya-flux-48gb.sh). FluxGym / FluxTrainer can
still load this folder; use the same 16/16, 1e-4, 2000-step numbers.

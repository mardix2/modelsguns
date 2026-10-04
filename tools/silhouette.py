"""Extract side silhouettes from reference photos (run once, needs the photos).

    python3 tools/silhouette.py /path/to/photos

Writes tools/silhouettes/<gun>.png: a black/white mask in a normalised frame
(muzzle pointing left, bore horizontal), and <gun>_mat.png: the same frame
with the furniture (wood / polymer, found by colour) marked 255.  Only the silhouette is kept; the
photos themselves are not stored in the repository.
"""

import json
import os
import sys

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "silhouettes")

# photo, crop box, grabcut rect (inside crop), flip (muzzle right in photo),
# rotation (deg, to level the bore), threshold-mask fallback
GUNS = {
    "deagle": dict(photo="1.webp", crop=(0, 0, 1024, 548), rect=(8, 15, 1005, 530)),
    "ak47": dict(photo="2.webp", crop=(0, 60, 1280, 400), rect=(15, 25, 1240, 330), threshold=30,
                 furniture="wood"),
    "mp5": dict(photo="5.png", crop=(0, 0, 600, 272), rect=(15, 20, 585, 250), flip=True),
    "m870": dict(photo="6.webp", crop=(0, 330, 2000, 1000), rect=(0, 50, 1960, 500), level=(60, 760),
                 furniture="wood"),
    "awm": dict(photo="7.png", crop=(0, 0, 1177, 330), alpha=True, furniture="green"),
}


def largest(m):
    lab, n = ndi.label(m)
    if not n:
        return m
    sizes = ndi.sum(m, lab, range(1, n + 1))
    return lab == (np.argmax(sizes) + 1)


def grabcut(rgb, rect):
    mask = np.zeros(rgb.shape[:2], np.uint8)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(np.ascontiguousarray(rgb[..., ::-1]), mask, rect, bgd, fgd, 8, cv2.GC_INIT_WITH_RECT)
    return (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)


def threshold(rgb, thr):
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]).astype(np.float32)
    bg = np.median(border, axis=0)
    return np.sqrt(((rgb.astype(np.float32) - bg) ** 2).sum(-1)) > thr


def furniture(rgb, kind):
    """Wood (orange-brown) or olive/green polymer pixels, cleaned up."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    if kind == "wood":
        f = (h <= 22) & (s > 90) & (v > 45)
    else:
        f = (h >= 20) & (h <= 60) & (s > 45) & (v > 50)
    f = ndi.binary_closing(f, iterations=4)
    f = ndi.binary_opening(f, iterations=2)
    f = ndi.binary_fill_holes(f) | f
    lab, n = ndi.label(f)
    if n:
        sizes = ndi.sum(f, lab, range(1, n + 1))
        keep = [i + 1 for i, sz in enumerate(sizes) if sz > f.size * 0.004]
        f = np.isin(lab, keep)
    return f


def transform(m, rot, flip):
    if rot:
        h, w = m.shape
        r = cv2.getRotationMatrix2D((w / 2, h / 2), rot, 1.0)
        m = cv2.warpAffine(m.astype(np.uint8) * 255, r, (w, h), flags=cv2.INTER_LINEAR) > 127
    if flip:
        m = m[:, ::-1]
    return m


def main(photo_dir):
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for name, c in GUNS.items():
        im = np.array(Image.open(os.path.join(photo_dir, c["photo"])).convert("RGBA"))
        x0, y0, x1, y1 = c["crop"]
        im = im[y0:y1, x0:x1]
        rgb = np.ascontiguousarray(im[..., :3])
        if c.get("alpha"):
            m = im[..., 3] > 100
        elif c.get("threshold"):
            m = threshold(rgb, c["threshold"])
            m = ndi.binary_closing(m, iterations=3) | (grabcut(rgb, c["rect"]) & (np.arange(m.shape[1]) < 330)[None, :])
        else:
            m = grabcut(rgb, c["rect"])
        m = ndi.binary_opening(m, iterations=1)
        m = largest(m)
        # fill small holes (specks, markings) but keep real openings
        holes = ndi.binary_fill_holes(m) & ~m
        lab, n = ndi.label(holes)
        if n:
            sizes = ndi.sum(holes, lab, range(1, n + 1))
            for i, sz in enumerate(sizes):
                if sz < m.sum() * 0.004:
                    m |= lab == (i + 1)
        if c.get("level"):
            # level the bore: fit the top edge of the barrel and rotate it flat
            xa, xb = c["level"]
            xs = np.arange(xa, xb, 5)
            ys = np.array([np.argmax(m[:, x]) for x in xs])
            slope = np.polyfit(xs, ys, 1)[0]
            ang = np.degrees(np.arctan(slope))
            h, w = m.shape
            rot = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
            m = cv2.warpAffine(m.astype(np.uint8) * 255, rot, (w, h), flags=cv2.INTER_LINEAR) > 127
            c["applied_rotation"] = float(ang)
            print("  levelled by", round(float(ang), 2), "deg")
        if c.get("flip"):
            m = m[:, ::-1]
        if c.get("furniture"):
            f = transform(furniture(rgb, c["furniture"]), c.get("applied_rotation", 0.0), c.get("flip"))
            Image.fromarray((f * 255).astype(np.uint8)).save(os.path.join(OUT, name + "_mat.png"))
        Image.fromarray((m * 255).astype(np.uint8)).save(os.path.join(OUT, name + ".png"))
        meta[name] = {"photo": c["photo"], "crop": c["crop"], "flip": bool(c.get("flip")),
                      "rotation": c.get("applied_rotation", 0.0)}
        print(name, m.shape, round(float(m.mean()), 3))
    with open(os.path.join(OUT, "sources.json"), "w") as fh:
        json.dump(meta, fh, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])

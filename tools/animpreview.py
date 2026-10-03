"""Render animation previews (GIF) by sampling the authored keyframes."""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bbgen  # noqa: E402

EASE = {
    None: lambda t: t, "linear": lambda t: t, "step": lambda t: 0.0,
    "easeOutQuad": lambda t: 1 - (1 - t) ** 2, "easeInQuad": lambda t: t * t,
    "easeOutCubic": lambda t: 1 - (1 - t) ** 3, "easeInCubic": lambda t: t ** 3,
    "easeInOutSine": lambda t: -(math.cos(math.pi * t) - 1) / 2,
    "easeOutBack": lambda t: 1 + 2.70158 * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2,
    "easeOutBounce": lambda t: 1 - (1 - t) ** 2,
}


def sample(keys, t):
    ks = sorted(keys.items())
    vals = [(k, v[0] if isinstance(v, tuple) else v, v[1] if isinstance(v, tuple) else None) for k, v in ks]
    if t <= vals[0][0]:
        return vals[0][1]
    for (t0, v0, _), (t1, v1, e1) in zip(vals, vals[1:]):
        if t0 <= t <= t1:
            f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
            f = EASE.get(e1, lambda x: x)(f)
            return [a + (b - a) * f for a, b in zip(v0, v1)]
    return vals[-1][1]


def pose_at(model, spec, t):
    pose = {}
    for bone, chans in spec["bones"].items():
        pos = sample(chans["position"], t) if "position" in chans else [0, 0, 0]
        rot = sample(chans["rotation"], t) if "rotation" in chans else [0, 0, 0]
        pose[bone] = (pos, rot)
    return pose


def posed_model(model, pose):
    """Copy of the model with every cube transformed by its bone + root."""
    import copy
    pm = copy.copy(model)
    pm.cubes = []
    for c in model.cubes:
        c2 = copy.copy(c)
        for bone, pivot in ((c.group, model.group_pivot(c.group)), ("root", model.root_pivot)):
            if bone not in pose:
                continue
            pos, rot = pose[bone]
            rm = bbgen.euler_matrix(rot)
            cm = bbgen.euler_matrix(c2.rot[1]) if c2.rot else [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            oc = c2.rot[2] if c2.rot else [(c2.frm[i] + c2.to[i]) / 2 for i in range(3)]
            r = bbgen.mat_mul3(rm, cm)
            moved = bbgen.mat_vec(rm, [oc[i] - pivot[i] for i in range(3)])
            t = [moved[i] + pivot[i] - oc[i] + pos[i] for i in range(3)]
            c2.frm = [c2.frm[i] + t[i] for i in range(3)]
            c2.to = [c2.to[i] + t[i] for i in range(3)]
            c2.rot = ("e", bbgen.matrix_euler(r), [oc[i] + t[i] for i in range(3)])
        pm.cubes.append(c2)
    return pm


def gif(model, spec, path, yaw=-130, pitch=18, fps=20, size=(480, 320), bounds=None, slow=1.0):
    from PIL import Image
    n = max(2, int(spec["length"] * fps * slow) + 1)
    frames = []
    for i in range(n):
        t = spec["length"] * i / (n - 1)
        pm = posed_model(model, pose_at(model, spec, t))
        if bounds:
            pm.bounds = lambda b=bounds: b
        frames.append(bbgen.render(pm, yaw, pitch, size[0], size[1], ss=1).convert("P", palette=Image.ADAPTIVE))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)


def main():
    import importlib
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "previews", "anim")
    os.makedirs(out, exist_ok=True)
    names = sys.argv[1:] or ["mk18", "glock17"]
    for name in names:
        mod = importlib.import_module(name)
        m = mod.build()
        shift = m.center_yz()
        m.root_pivot = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
        m.build_texture()
        lo, hi = m.bounds()
        pad = 7
        bounds = ([lo[0] - pad, lo[1] - pad * 1.6, lo[2] - pad], [hi[0] + pad, hi[1] + pad * 0.4, hi[2] + pad])
        for anim, spec in mod.ANIMATIONS.items():
            if isinstance(spec, tuple):
                spec = {"length": spec[0], "bones": spec[1]}
            gif(m, spec, os.path.join(out, "%s_%s.gif" % (name, anim)), bounds=bounds)
            print(name, anim)


if __name__ == "__main__":
    main()

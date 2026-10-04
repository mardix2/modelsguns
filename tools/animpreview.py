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


def to_view(model, display):
    """Copy of a (posed) model moved into first-person view space (1/16
    block, eye at the origin): item point p -> 16 * (0.56, -0.52, -0.72) + t
    + s * (p - 8) for the right hand with zero display rotation; shifted by
    8 for render().  Cubes behind the near plane are dropped."""
    import copy
    fp = display["firstperson_righthand"]
    t, s = fp["translation"], fp["scale"][0]
    base = [16 * 0.56 + t[0], 16 * -0.52 + t[1], 16 * -0.72 + t[2]]

    def tr(p):
        return [8 + base[i] + s * (p[i] - 8) for i in range(3)]

    vm = copy.copy(model)
    vm.cubes = []
    for c in model.cubes:
        c2 = copy.copy(c)
        c2.frm, c2.to = tr(c.frm), tr(c.to)
        if c.rot:
            c2.rot = ("e", c.rot[1], tr(c.rot[2]))
        if (c2.frm[2] + c2.to[2]) / 2 - 8 > -0.8:
            continue
        vm.cubes.append(c2)
    return vm


def frame_png(model, display, pose, size=(480, 320), yaw=14, pitch=8, half_w=13.0):
    """First-person frame seen slightly from the left of the eye (a straight
    orthographic view down the barrel shows nothing); the red cross marks
    the screen centre."""
    from PIL import ImageDraw
    vm = to_view(posed_model(model, pose), display)
    hh = half_w * size[1] / size[0]
    vm.bounds = lambda: ([8 - half_w, 8 - hh, 8], [8 + half_w, 8 + hh, 8])
    im = bbgen.render(vm, yaw, pitch, size[0], size[1], ss=1)
    d = ImageDraw.Draw(im)
    cx, cy = size[0] // 2, size[1] // 2
    d.line([(cx - 5, cy), (cx + 5, cy)], fill=(230, 40, 40))
    d.line([(cx, cy - 5), (cx, cy + 5)], fill=(230, 40, 40))
    return im


def gif(model, display, spec, path, fps=16):
    from PIL import Image
    n = max(2, int(spec["length"] * fps) + 1)
    frames = []
    for i in range(n):
        t = spec["length"] * i / (n - 1)
        frames.append(frame_png(model, display, pose_at(model, spec, t)).convert("P", palette=Image.ADAPTIVE))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)


def main():
    import importlib

    import build
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "previews", "anim")
    os.makedirs(out, exist_ok=True)
    args = sys.argv[1:] or build.GUN_MODULES
    only = [a.split(":")[1] for a in args if ":" in a]
    names = [a.split(":")[0] for a in args]
    for name in dict.fromkeys(names):
        mod = importlib.import_module(name)
        m, display, _, anim_set = build.prepare(mod)
        for anim, spec in anim_set.items():
            if only and anim not in only:
                continue
            gif(m, display, spec, os.path.join(out, "%s_%s.gif" % (m.name, anim)))
            print(name, anim)


if __name__ == "__main__":
    main()

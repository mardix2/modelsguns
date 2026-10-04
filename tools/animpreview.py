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
        chain, b = [], c.group
        while b and b != "root":
            chain.append((b, model.group_pivot(b)))
            b = getattr(model, "parents", {}).get(b)
        for bone, pivot in chain + [("root", model.root_pivot)]:
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


FP_BASE = (0.56, -0.52, -0.72)     # vanilla right-hand item offset (blocks)


def _clip_near(poly, near):
    """Sutherland-Hodgman clip of [(x, y, z, u, v)] against z <= -near."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ina, inb = a[2] <= -near, b[2] <= -near
        if ina:
            out.append(a)
        if ina != inb:
            t = (-near - a[2]) / (b[2] - a[2])
            out.append(tuple(a[j] + (b[j] - a[j]) * t for j in range(5)))
    return out


def render_fp(model, display, size=(480, 270), fov=70.0, near=0.05, bg=(150, 176, 206), cross=True):
    """Perspective first-person render, as Minecraft draws a held item: item
    point p -> FP_BASE + t / 16 + s / 16 * (p - 8) (blocks, eye at the
    origin looking down -Z), vertical field of view `fov`."""
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = size
    fp = display["firstperson_righthand"]
    tr_, sc = fp["translation"], fp["scale"][0]
    base = [FP_BASE[i] + tr_[i] / 16 for i in range(3)]
    rr = [math.radians(v) for v in fp["rotation"]]
    Rx = [[1, 0, 0], [0, math.cos(rr[0]), -math.sin(rr[0])], [0, math.sin(rr[0]), math.cos(rr[0])]]
    Ry = [[math.cos(rr[1]), 0, math.sin(rr[1])], [0, 1, 0], [-math.sin(rr[1]), 0, math.cos(rr[1])]]
    Rz = [[math.cos(rr[2]), -math.sin(rr[2]), 0], [math.sin(rr[2]), math.cos(rr[2]), 0], [0, 0, 1]]
    R = bbgen.mat_mul3(bbgen.mat_mul3(Rx, Ry), Rz)
    f = (H / 2) / math.tan(math.radians(fov / 2))
    light = (0.35, 0.85, 0.4)
    ln = math.sqrt(sum(v * v for v in light))
    light = [v / ln for v in light]
    tex = np.asarray(model.texture.convert("RGBA")).astype(np.float32)
    col = np.zeros((H, W, 3), np.float32)
    col[:] = bg
    zbuf = np.zeros((H, W), np.float32)          # stores 1/w, larger = closer

    def view(p):
        q = bbgen.mat_vec(R, [p[i] - 8 for i in range(3)])
        return [base[i] + sc / 16 * q[i] for i in range(3)]

    for c in model.cubes:
        for face in bbgen.FACES:
            if face not in c.uv:
                continue
            tl, tr, bl = (bbgen.rotate(p, c.rot) for p in bbgen.face_corners(c, face))
            br = tuple(tr[i] + bl[i] - tl[i] for i in range(3))
            e1 = [tr[i] - tl[i] for i in range(3)]
            e2 = [bl[i] - tl[i] for i in range(3)]
            nrm = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
            nl = math.sqrt(sum(v * v for v in nrm)) or 1
            nrm = [-v / nl for v in nrm]
            vtl = view(tl)
            if sum(nrm[i] * -vtl[i] for i in range(3)) <= 0:
                continue
            u0, v0, u1, v1 = c.uv[face]
            poly = [tuple(view(tl)) + (u0, v0), tuple(view(tr)) + (u1, v0),
                    tuple(view(br)) + (u1, v1), tuple(view(bl)) + (u0, v1)]
            poly = _clip_near(poly, near)
            if len(poly) < 3:
                continue
            shade = 0.55 + 0.45 * max(0.0, sum(nrm[i] * light[i] for i in range(3)))
            umin, umax = min(u0, u1), max(u0, u1) - 1
            vmin, vmax = min(v0, v1), max(v0, v1) - 1
            pts = [(W / 2 + f * x / -z, H / 2 - f * y / -z, 1.0 / -z, u, v) for x, y, z, u, v in poly]
            for k in range(1, len(pts) - 1):
                A, B, C = pts[0], pts[k], pts[k + 1]
                det = (B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])
                if abs(det) < 1e-9:
                    continue
                x0 = max(0, int(min(A[0], B[0], C[0])))
                x1 = min(W, int(max(A[0], B[0], C[0])) + 2)
                y0 = max(0, int(min(A[1], B[1], C[1])))
                y1 = min(H, int(max(A[1], B[1], C[1])) + 2)
                if x1 <= x0 or y1 <= y0:
                    continue
                gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
                l1 = ((gx - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (gy - A[1])) / det
                l2 = ((B[0] - A[0]) * (gy - A[1]) - (gx - A[0]) * (B[1] - A[1])) / det
                l0 = 1 - l1 - l2
                m_ = (l0 >= 0) & (l1 >= 0) & (l2 >= 0)
                if not m_.any():
                    continue
                iw = l0 * A[2] + l1 * B[2] + l2 * C[2]
                uu = (l0 * A[3] * A[2] + l1 * B[3] * B[2] + l2 * C[3] * C[2]) / iw
                vv = (l0 * A[4] * A[2] + l1 * B[4] * B[2] + l2 * C[4] * C[2]) / iw
                tu = np.clip(np.floor(uu).astype(int), umin, umax)
                tv = np.clip(np.floor(vv).astype(int), vmin, vmax)
                texel = tex[tv, tu]
                zb = zbuf[y0:y1, x0:x1]
                m_ &= (texel[..., 3] > 127) & (iw > zb)
                zb[m_] = iw[m_]
                cb = col[y0:y1, x0:x1]
                cb[m_] = texel[..., :3][m_] * shade
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB")
    if cross:
        d = ImageDraw.Draw(im)
        d.line([(W // 2 - 5, H // 2), (W // 2 + 5, H // 2)], fill=(255, 255, 255))
        d.line([(W // 2, H // 2 - 5), (W // 2, H // 2 + 5)], fill=(255, 255, 255))
    return im


def frame_png(model, display, pose, size=(480, 270)):
    return render_fp(posed_model(model, pose), display, size)


def gif(model, display, spec, path, fps=12):
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

"""Build every gun: Blockbench projects, resource pack and preview renders.

    python3 tools/build.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arms  # noqa: E402
import bbgen  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "modelsguns"


# --- rotation maths (Minecraft applies display rotation as Rx * Ry * Rz) ------

def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def rx(d):
    c, s = math.cos(math.radians(d)), math.sin(math.radians(d))
    return [[1, 0, 0], [0, c, -s], [0, s, c]]


def ry(d):
    c, s = math.cos(math.radians(d)), math.sin(math.radians(d))
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


def rz(d):
    c, s = math.cos(math.radians(d)), math.sin(math.radians(d))
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def clean(v):
    v = round(v, 2)
    return 0.0 if v == 0 else v


def euler_xyz(r):
    b = math.asin(max(-1.0, min(1.0, r[0][2])))
    a = math.atan2(-r[1][2], r[2][2])
    c = math.atan2(-r[0][1], r[0][0])
    out = [clean(math.degrees(v)) for v in (a, b, c)]
    back = mat_mul(mat_mul(rx(out[0]), ry(out[1])), rz(out[2]))
    assert all(abs(back[i][j] - r[i][j]) < 1e-3 for i in range(3) for j in range(3))
    return out


def apply(r, v):
    return [sum(r[i][k] * v[k] for k in range(3)) for i in range(3)]


def transform(rot_matrix, scale, point, target=(0, 0, 0)):
    """Display entry that maps model `point` onto `target` (in 1/16 block)."""
    rel = [p - 8 for p in point]
    moved = apply(rot_matrix, [v * scale for v in rel])
    t = [max(-80, min(80, clean(target[i] - moved[i]))) for i in range(3)]
    return {"rotation": euler_xyz(rot_matrix), "translation": t, "scale": [round(scale, 3)] * 3}


FP_BASE = (0.56, -0.52, -0.72)   # vanilla first-person right-hand item offset (blocks)


def display_for(model, grip, hand_scale, fp_scale, gui_scale, gui_tilt, fp_pos, fp_rot=(0, 0, 0)):
    lo, hi = model.bounds()
    centre = [(a + b) / 2 for a, b in zip(lo, hi)]
    # third person: item +y = forward, +z = up  ->  model -Z forward, +Y up
    tp = transform(rx(90), hand_scale, grip, (0, 1.5, -1.0))
    # first person: view -Z is forward, same as the model
    # first person: the grip lands on fp_pos (view space, blocks: right, up,
    # forward negative); view -Z is forward, same as the model
    fp_m = mat_mul(mat_mul(rx(fp_rot[0]), ry(fp_rot[1])), rz(fp_rot[2]))
    fp = transform(fp_m, fp_scale, grip, [(fp_pos[i] - FP_BASE[i]) * 16 for i in range(3)])
    # inventory: right side towards the viewer, muzzle to the right, tilted up
    gui_rot = mat_mul(rz(gui_tilt), ry(-90))
    gui = transform(gui_rot, gui_scale, centre)
    fixed = transform(ry(90), gui_scale * 1.25, centre)
    ground = transform(rz(0), hand_scale * 0.75, centre, (0, 2, 0))
    head = transform(ry(-90), 0.6, centre, (0, 10, 0))
    return {
        "thirdperson_righthand": tp,
        "thirdperson_lefthand": tp,
        "firstperson_righthand": fp,
        "firstperson_lefthand": fp,
        "gui": gui,
        "ground": ground,
        "fixed": fixed,
        "head": head,
    }


def animation_json(name, anims):
    """Animations are authored in model (Java) space; Bedrock mirrors X, so
    X positions and X/Y rotations flip sign (GeckoLib flips them back)."""
    out = {}
    for anim, spec in anims.items():
        if isinstance(spec, tuple):          # legacy (length, bones)
            spec = {"length": spec[0], "loop": False, "bones": spec[1]}
        bb = {}
        for bone, chans in spec["bones"].items():
            bb[bone] = {}
            for chan, keys in chans.items():
                conv = {}
                for t, v in sorted(keys.items()):
                    ease = None
                    if isinstance(v, tuple):
                        v, ease = v
                    if chan == "position":
                        v = [-v[0], v[1], v[2]]
                    else:
                        v = [-v[0], -v[1], v[2]]
                    v = [clean(x) for x in v]
                    conv["%g" % t] = {"vector": v, "easing": ease} if ease else v
                bb[bone][chan] = conv
        entry = {"animation_length": spec["length"]}
        if spec.get("loop"):
            entry["loop"] = True
        entry["bones"] = bb
        out["animation.%s.%s" % (name, anim)] = entry
    return {"format_version": "1.8.0", "animations": out}


def sight_line(cubes):
    """Highest point over the rear 60 % of the gun: (y, z) of the sight line."""
    zs = [z for c in cubes for z in (c.frm[2], c.to[2])]
    z0, z1 = min(zs), max(zs)
    rear = [c for c in cubes if (c.frm[2] + c.to[2]) / 2 > z0 + (z1 - z0) * 0.4 and not c.rot]
    top = max(rear, key=lambda c: c.to[1])
    return top.to[1], (top.frm[2] + top.to[2]) / 2


def ads_offset(display, cubes, pivot, dist=0.42, above=0.0, eye_behind_grip=None):
    """Root pose (position px, rotation deg) putting the sight line on the
    screen centre.

    First person, right hand: an item point p ends up at
    FP_BASE + t / 16 + s / 16 * R (p - 8) in view space (blocks).  The root
    rotation undoes the display rotation R (so the bore is parallel to the
    view axis) and the position moves the sight line onto x = y = 0.  Depth:
    pistols put the rear sight `dist` blocks in front of the eye; long guns
    put the eye `eye_behind_grip` blocks behind the grip, over the comb of
    the stock, as with a real cheek weld."""
    fp = display["firstperson_righthand"]
    t, s = fp["translation"], fp["scale"][0]
    r = fp["rotation"]
    R = mat_mul(mat_mul(rx(r[0]), ry(r[1]), ), rz(r[2]))
    Rt = [[R[j][i] for j in range(3)] for i in range(3)]
    ys, zs = sight_line(cubes)
    if eye_behind_grip is not None:
        zs, dist = pivot[2], eye_behind_grip
    ps = [8, ys - 0.1 + above, zs]
    target = [0.0, 0.0, -dist]
    # base + t/16 + s/16 * [(ps - pivot) + R (pivot - 8 + dp)] = target
    w = [(target[i] - FP_BASE[i] - t[i] / 16) * 16 / s - (ps[i] - pivot[i]) for i in range(3)]
    q = apply(Rt, w)
    dp = [q[i] - (pivot[i] - 8) for i in range(3)]
    rot = euler_xyz(Rt)
    return [round(v, 3) for v in dp], [round(v, 3) for v in rot]


def group_box(m, group, name_prefix=None):
    cs = [c for c in m.cubes if c.group == group and (not name_prefix or c.name.startswith(name_prefix))]
    if not cs:
        return None
    lo = [min(c.frm[i] for c in cs) for i in range(3)]
    hi = [max(c.to[i] for c in cs) for i in range(3)]
    return lo, hi


def full_animations(mod, m, display, palms, gun_cubes, shift=(0, 0, 0)):
    """The gun's own animations + aiming / dry fire / walk, with the arms
    following the parts the hands work."""
    import copy

    import anims
    c = dict(mod.ANIM)
    pistol = getattr(mod, "ARMS", {}).get("left", {}).get("kind") == "support"
    # guns without iron sights (bare rail) are aimed over the rail, as if
    # through an optic at the usual height
    above = c.get("aim_above_mm", 0.0) / mod.U
    pos, rot = ads_offset(display, gun_cubes or m.cubes, m.root_pivot, 0.52, above,
                          None if pistol else c.get("eye_behind_grip", 0.24))
    c["ads"] = {"pos": pos, "rot": rot}
    out = copy.deepcopy(mod.ANIMATIONS)
    for k, v in anims.standard_extras(c).items():
        out.setdefault(k, v)
    if not palms:
        return out
    hands = c.get("hands", {"left_arm": [("magazine", None, None)]})
    # optional resting places other than the grip / forend for some animations
    # (e.g. the shotgun's loading port while shells go in)
    k = bbgen.MM(None, mod.U)
    spots = {n: [a_ + b_ for a_, b_ in zip(k.P(*p_), shift)] for n, p_ in c.get("hand_points", {}).items()}
    for name, spec in out.items():
        for arm in hands:
            rs = c.get("hand_rest", {}).get(arm, {}).get(name, (None, None))
            rest = [[spots[r][i] - palms[arm][i] for i in range(3)] if r else [0, 0, 0] for r in rs]
            parts = hands[arm]
            segs = []
            for bone, prefix, only in parts:
                if only and name not in only:
                    continue
                if bone not in m.groups:
                    continue
                if bone == c.get("mag", "magazine"):
                    lo, hi = group_box(m, bone)
                    base = [c_ for c_ in m.cubes if c_.group == bone and c_.frm[1] < lo[1] + 1.0]
                    zc = sum((c_.frm[2] + c_.to[2]) / 2 for c_ in base) / len(base)
                    point = [8, lo[1] - 6 / mod.U, zc]                        # hold it by the base
                else:
                    lo, hi = group_box(m, bone, prefix)
                    point = [(a_ + b_) / 2 for a_, b_ in zip(lo, hi)]
                ride = bone == "pump"
                delta = [0, 0, 0] if ride else [point[i] - palms[arm][i] for i in range(3)]
                for win in bone_windows(spec, bone):
                    segs.append((win, bone, point, delta, ride))
            if segs or any(r for r in rs):
                arm_track(spec, arm, segs, lambda b: bone_chain(m, b), rest=rest,
                          job_rot=c.get("arm_job_rot", {}).get(arm))
    return out


def bone_chain(m, bone):
    out = []
    while bone and bone != "root":
        out.append((bone, m.group_pivot(bone)))
        bone = m.parents.get(bone)
    return out


def bone_windows(spec, bone, merge=0.16):
    """Time intervals in which a bone moves (between keys that differ)."""
    import animpreview
    chans = spec["bones"].get(bone, {})
    times = sorted({t for ch in chans.values() for t in ch})
    out = []
    for ta, tb in zip(times, times[1:]):
        va = [animpreview.sample(ch, ta) for ch in chans.values()]
        vb = [animpreview.sample(ch, tb) for ch in chans.values()]
        if any(abs(x - y) > 1e-4 for a_, b_ in zip(va, vb) for x, y in zip(a_, b_)):
            if out and ta - out[-1][1] < merge:
                out[-1][1] = tb
            else:
                out.append([ta, tb])
    return [tuple(w) for w in out]


def point_offset(spec, chain, point, t):
    """How far `point` has moved at time t (model px); chain = [(bone, pivot)]
    from the bone up through its parents."""
    import animpreview
    p = list(point)
    for bone, pivot in chain:
        chans = spec["bones"].get(bone, {})
        pos = animpreview.sample(chans["position"], t) if "position" in chans else [0, 0, 0]
        rot = animpreview.sample(chans["rotation"], t) if "rotation" in chans else [0, 0, 0]
        q = bbgen.mat_vec(bbgen.euler_matrix(rot), [p[i] - pivot[i] for i in range(3)])
        p = [q[i] + pivot[i] + pos[i] for i in range(3)]
    return [p[i] - point[i] for i in range(3)]


def arm_track(spec, arm, segs, pivot_of, reach=0.2, back=0.28, rate=20, rest=([0, 0, 0], [0, 0, 0]),
              job_rot=None):
    """Position keys for an arm doing the jobs in `segs` one after another:
    reach the part, move with it (sampled), go back to its resting place
    (rest[0] at the start, rest[1] from the first job on / at the end)."""
    r0, r1 = rest
    keys = [(0.0, r0, None)]
    L = spec["length"]
    segs = sorted(segs, key=lambda s: s[0][0])
    for i, ((t0, t1), bone, point, delta, ride) in enumerate(segs):
        chain = pivot_of(bone)
        start = max(keys[-1][0], t0 - (0 if ride and keys[-1][1] == [0, 0, 0] else reach))
        if start > keys[-1][0] + 0.02 and keys[-1][1] in (r0, r1):
            keys.append((start, keys[-1][1], None))
        n = max(1, int((t1 - t0) * rate))
        for j in range(n + 1):
            t = t0 + (t1 - t0) * j / n
            if t <= keys[-1][0] + 1e-4:
                continue
            off = point_offset(spec, chain, point, t)
            keys.append((t, [delta[q] + off[q] for q in range(3)], "easeInOutSine" if j == 0 else None))
        nxt = segs[i + 1][0][0] - reach if i + 1 < len(segs) else L + 1
        end = min(L, t1 + (0 if ride else back))
        if end > keys[-1][0] + 1e-4 and end <= nxt:
            keys.append((end, r1, "easeInOutSine"))
    if not segs:      # only moves between resting places
        keys.append((L * 0.8, r1, "easeInOutSine"))
    elif keys[-1][0] < L - 1e-4 and keys[-1][1] != r1:
        keys.append((L, r1, "easeInOutSine"))
    if job_rot:
        # the arm turns (about its hand end) while it works away from rest
        rot = spec["bones"].setdefault(arm, {}).setdefault("rotation", {})
        rot.clear()
        rot[0.0] = [0, 0, 0]
        away = False
        for t, v, e in keys:
            out = any(abs(x) > 1e-6 for x in v)
            if out != away:
                rot[round(t, 4)] = (list(job_rot) if out else [0, 0, 0], "easeInOutSine")
                away = out
    ch = spec["bones"].setdefault(arm, {}).setdefault("position", {})
    ch.clear()
    for t, v, e in keys:
        t = round(t, 4)
        ch[t] = ([round(x, 4) for x in v], e) if e else [round(x, 4) for x in v]


GUN_MODULES = ["mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm", "m1911", "m9a4", "p320", "mk23", "rhino"]


def prepare(mod):
    """Build a gun: model (centred, with arms), display transforms, the
    gun-only cube list and the full animation set."""
    m = mod.build()
    shift = m.center_yz()
    grip = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
    m.root_pivot = grip
    dp = mod.DISPLAY
    pistol = getattr(mod, "ARMS", {}).get("left", {}).get("kind") == "support"
    fp_pos = dp.get("fp_pos", (0.22, -0.25, -0.42) if pistol else (0.26, -0.31, -0.50))
    fp_rot = dp.get("fp_rot", (0, 8, 0) if pistol else (0, 10, 0))
    display = display_for(m, grip, dp["hand"], dp["fp"], dp["gui"], dp["tilt"], fp_pos, fp_rot)
    gun_cubes = None
    palms = {}
    if hasattr(mod, "ARMS"):
        # first-person arms (added after the display transforms so they do
        # not change the gun's framing in hand / GUI)
        gun_cubes = list(m.cubes)
        n0 = len(m.cubes)
        piv, palms = arms.add(m, bbgen.MM(m, mod.U), mod.ARMS, mod.DISPLAY["fp"])
        for c in m.cubes[n0:]:
            c.shift(shift)
        m.pivots.update({g: [a + b for a, b in zip(p, shift)] for g, p in piv.items()})
        palms = {g: [a + b for a, b in zip(p, shift)] for g, p in palms.items()}
    m.build_texture()
    return m, display, gun_cubes, full_animations(mod, m, display, palms, gun_cubes, shift)


def fp_preview(m, display, anim_set):
    from PIL import Image

    import animpreview
    out = Image.new("RGB", (960, 270))
    for i, name in enumerate(("idle", "aim")):
        pose = animpreview.pose_at(m, anim_set[name], 0.0)
        out.paste(animpreview.frame_png(m, display, pose), (480 * i, 0))
    return out


def main():
    import importlib
    only = sys.argv[1:]
    gl = os.path.join(ROOT, "geckolib/assets", NS)
    dirs = {
        # GeckoLib 5 (Minecraft 26.x) layout
        "gl_geo": os.path.join(gl, "geckolib/models/item"),
        "gl_anim": os.path.join(gl, "geckolib/animations/item"),
        "gl_tex": os.path.join(gl, "textures/item"),
        "gl_mdl": os.path.join(gl, "models/item"),
        "gl_items": os.path.join(gl, "items"),
        "bb": os.path.join(ROOT, "blockbench"), "pv": os.path.join(ROOT, "previews"),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    for modname in GUN_MODULES:
        if only and modname not in only:
            continue
        mod = importlib.import_module(modname)
        m, display, gun_cubes, anim_set = prepare(mod)
        n = m.name
        vanilla = m.java_legal()

        # GeckoLib 5: geometry, animations, texture, base model (display), item definition
        bbgen.save_json(m.geo_json(), os.path.join(dirs["gl_geo"], n + ".geo.json"))
        bbgen.save_json(animation_json(n, anim_set),
                        os.path.join(dirs["gl_anim"], n + ".animation.json"))
        m.texture.save(os.path.join(dirs["gl_tex"], n + ".png"))
        bbgen.save_json({"textures": {"particle": "%s:item/%s" % (NS, n)}, "gui_light": "front",
                         "display": display}, os.path.join(dirs["gl_mdl"], n + ".json"))
        bbgen.save_json({"model": {"type": "minecraft:special", "base": "%s:item/%s" % (NS, n),
                                   "model": {"type": "geckolib:geckolib"}}},
                        os.path.join(dirs["gl_items"], n + ".json"))

        rel = "../geckolib/assets/%s/textures/item/%s.png" % (NS, n)
        bbgen.save_json(m.bbmodel(display, rel, "java_block" if vanilla else "bedrock"),
                        os.path.join(dirs["bb"], n + ".bbmodel"))

        all_cubes = m.cubes
        if gun_cubes is not None:
            # first person with the arms: hip (idle) and aimed
            fp_preview(m, display, anim_set).save(os.path.join(dirs["pv"], "%s_fp.png" % n))
            m.cubes = gun_cubes
        views = {"right": (-90, 0), "left": (90, 0), "iso_right": (-130, 22), "iso_left": (50, 22)}
        for vname, (yaw, pitch) in views.items():
            bbgen.render(m, yaw, pitch).save(os.path.join(dirs["pv"], "%s_%s.png" % (n, vname)))
        m.cubes = all_cubes
        print("%-8s cubes=%3d texture=%dx%d vanilla=%s bones=%s" % (
            n, len(m.cubes), m.size, m.size, vanilla, ",".join(m.groups)))


def contact_sheet():
    """previews/all_guns.png: every gun from the left, trimmed, in a grid."""
    from PIL import Image, ImageChops, ImageDraw
    pv = os.path.join(ROOT, "previews")
    tiles = []
    for n in GUN_MODULES:
        path = os.path.join(pv, "%s_left.png" % n)
        if not os.path.exists(path):
            continue
        im = Image.open(path).convert("RGB")
        bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
        box = ImageChops.difference(im, bg).getbbox()
        im = im.crop(box) if box else im
        im.thumbnail((560, 260))
        tiles.append((n, im))
    cols, tw, th = 2, 600, 300
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (236, 238, 242))
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x + (tw - im.width) // 2, y + 24 + (th - 24 - im.height) // 2))
        d.text((x + 12, y + 8), n, fill=(40, 40, 40))
    sheet.save(os.path.join(pv, "all_guns.png"))


if __name__ == "__main__":
    main()
    if not sys.argv[1:]:
        contact_sheet()

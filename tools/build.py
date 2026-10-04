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


def display_for(model, grip, hand_scale, fp_scale, gui_scale, gui_tilt, fp_push):
    lo, hi = model.bounds()
    centre = [(a + b) / 2 for a, b in zip(lo, hi)]
    # third person: item +y = forward, +z = up  ->  model -Z forward, +Y up
    tp = transform(rx(90), hand_scale, grip, (0, 1.5, -1.0))
    # first person: view -Z is forward, same as the model
    fp = transform(rz(0), fp_scale, grip, (0, -1.0, fp_push))
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


def ads_offset(display, cubes):
    """Root offset (model px) putting the sight line on the screen centre.

    First person, right hand: an item point p ends up at
    (0.56, -0.52, -0.72) + t / 16 + s / 16 * (p - 8) in view space (blocks),
    with the display rotation at zero."""
    fp = display["firstperson_righthand"]
    t, s = fp["translation"], fp["scale"][0]
    ys, zs = sight_line(cubes)
    dx = -(0.56 + t[0] / 16) * 16 / s
    dy = (0.52 - t[1] / 16) * 16 / s - (ys - 8) + 0.1
    dz = max(0.0, (-0.32 + 0.72 - t[2] / 16) * 16 / s - (zs - 8))
    return [round(dx, 3), round(dy, 3), round(dz, 3)]


def group_box(m, group, name_prefix=None):
    cs = [c for c in m.cubes if c.group == group and (not name_prefix or c.name.startswith(name_prefix))]
    if not cs:
        return None
    lo = [min(c.frm[i] for c in cs) for i in range(3)]
    hi = [max(c.to[i] for c in cs) for i in range(3)]
    return lo, hi


def full_animations(mod, m, display, palms, gun_cubes):
    """The gun's own animations + aiming / dry fire / walk, with the arms
    following the parts the hands work."""
    import copy

    import anims
    c = dict(mod.ANIM)
    c["ads"] = {"pos": ads_offset(display, gun_cubes or m.cubes)}
    out = copy.deepcopy(mod.ANIMATIONS)
    for k, v in anims.standard_extras(c).items():
        out.setdefault(k, v)
    if not palms:
        return out
    U = mod.U
    groups = set(m.groups)
    lp, rp = palms["left_arm"], palms["right_arm"]
    mag = c.get("mag", "magazine")
    mag_target = None
    if mag in groups:
        lo, hi = group_box(m, mag)
        bottom = [c_ for c_ in m.cubes if c_.group == mag and c_.frm[1] < lo[1] + 0.6]
        zc = sum((c_.frm[2] + c_.to[2]) / 2 for c_ in bottom) / len(bottom)
        mag_target = [8 - lp[0], lo[1] - 8 / U - lp[1], zc - lp[2]]
    charge = c.get("charging", (None,))[0]
    for name, spec in out.items():
        bones = spec["bones"]
        moved = lambda b: any(any(abs(x) > 1e-6 for x in (v[0] if isinstance(v, tuple) else v))  # noqa: E731
                              for v in bones.get(b, {}).get("position", {}).values())
        if mag_target and moved(mag):
            anims.follow(spec, "left_arm", mag, mag_target)
        elif charge and moved(charge):
            box = group_box(m, charge)
            if box:
                ctr = [(a + b) / 2 for a, b in zip(*box)]
                tgt = [ctr[0] - lp[0], ctr[1] - lp[1], ctr[2] - lp[2]]
                anims.follow(spec, "left_arm", charge, tgt)
        if "pump" in groups and moved("pump"):
            if "shell" in groups and moved("shell"):
                box = group_box(m, "shell")
                ctr = [(a + b) / 2 for a, b in zip(*box)]
                anims.follow(spec, "left_arm", "shell", [ctr[0] - lp[0], box[0][1] - lp[1], ctr[2] - lp[2]])
            else:
                anims.ride(spec, "left_arm", "pump")
        elif "shell" in groups and moved("shell"):
            box = group_box(m, "shell")
            ctr = [(a + b) / 2 for a, b in zip(*box)]
            anims.follow(spec, "left_arm", "shell", [ctr[0] - lp[0], box[0][1] - lp[1], ctr[2] - lp[2]])
        if "bolt" in groups and moved("bolt") and group_box(m, "bolt", "bolt_knob") and not c.get("action"):
            lo, hi = group_box(m, "bolt", "bolt_knob")
            ctr = [(a + b) / 2 for a, b in zip(lo, hi)]
            anims.follow(spec, "right_arm", "bolt", [ctr[0] - rp[0], ctr[1] - rp[1], ctr[2] - rp[2]],
                         reach=0.15, back=0.2)
    return out


GUN_MODULES = ["mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm"]


def prepare(mod):
    """Build a gun: model (centred, with arms), display transforms, the
    gun-only cube list and the full animation set."""
    m = mod.build()
    shift = m.center_yz()
    grip = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
    m.root_pivot = grip
    dp = mod.DISPLAY
    display = display_for(m, grip, dp["hand"], dp["fp"], dp["gui"], dp["tilt"], dp["push"])
    gun_cubes = None
    palms = {}
    if hasattr(mod, "ARMS"):
        # first-person arms (added after the display transforms so they do
        # not change the gun's framing in hand / GUI)
        gun_cubes = list(m.cubes)
        n0 = len(m.cubes)
        piv, palms = arms.add(m, bbgen.MM(m, mod.U), mod.ARMS)
        for c in m.cubes[n0:]:
            c.shift(shift)
        m.pivots.update({g: [a + b for a, b in zip(p, shift)] for g, p in piv.items()})
        palms = {g: [a + b for a, b in zip(p, shift)] for g, p in palms.items()}
    m.build_texture()
    return m, display, gun_cubes, full_animations(mod, m, display, palms, gun_cubes)


def fp_preview(m, display, anim_set):
    from PIL import Image

    import animpreview
    out = Image.new("RGB", (960, 320))
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

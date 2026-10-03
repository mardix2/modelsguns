"""Build every gun: Blockbench projects, resource pack and preview renders.

    python3 tools/build.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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


GUN_MODULES = ["mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm"]


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
        m = mod.build()
        shift = m.center_yz()
        grip = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
        m.root_pivot = grip
        m.build_texture()
        dp = mod.DISPLAY
        display = display_for(m, grip, dp["hand"], dp["fp"], dp["gui"], dp["tilt"], dp["push"])
        n = m.name
        vanilla = m.java_legal()

        # GeckoLib 5: geometry, animations, texture, base model (display), item definition
        bbgen.save_json(m.geo_json(), os.path.join(dirs["gl_geo"], n + ".geo.json"))
        bbgen.save_json(animation_json(n, mod.ANIMATIONS),
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

        views = {"right": (-90, 0), "left": (90, 0), "iso_right": (-130, 22), "iso_left": (50, 22)}
        for vname, (yaw, pitch) in views.items():
            bbgen.render(m, yaw, pitch).save(os.path.join(dirs["pv"], "%s_%s.png" % (n, vname)))
        print("%-8s cubes=%3d texture=%dx%d vanilla=%s bones=%s" % (
            n, len(m.cubes), m.size, m.size, vanilla, ",".join(m.groups)))


if __name__ == "__main__":
    main()

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
    """Animations are written in model (Java) space; Bedrock mirrors X, so
    X positions and X/Y rotations flip sign."""
    out = {}
    for anim, (length, bones) in anims.items():
        bb = {}
        for bone, chans in bones.items():
            bb[bone] = {}
            for chan, keys in chans.items():
                conv = {}
                for t, v in sorted(keys.items()):
                    if chan == "position":
                        v = [-v[0], v[1], v[2]]
                    else:
                        v = [-v[0], -v[1], v[2]]
                    conv["%g" % t] = [clean(x) for x in v]
                bb[bone][chan] = conv
        out["animation.%s.%s" % (name, anim)] = {"animation_length": length, "bones": bb}
    return {"format_version": "1.8.0", "animations": out}


GUN_MODULES = ["mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm"]


def main():
    import importlib
    only = sys.argv[1:]
    rp = os.path.join(ROOT, "resourcepack/assets", NS)
    gl = os.path.join(ROOT, "geckolib/assets", NS)
    dirs = {
        "tex": os.path.join(rp, "textures/item"), "mdl": os.path.join(rp, "models/item"),
        "items": os.path.join(rp, "items"),
        "gl_geo": os.path.join(gl, "geo/item"), "gl_tex": os.path.join(gl, "textures/item"),
        "gl_anim": os.path.join(gl, "animations/item"), "gl_mdl": os.path.join(gl, "models/item"),
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
        m.check_java_limits()
        grip = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
        m.build_texture()
        dp = mod.DISPLAY
        display = display_for(m, grip, dp["hand"], dp["fp"], dp["gui"], dp["tilt"], dp["push"])
        n = m.name

        # vanilla item model (resource pack, 1.21.4+ item definition)
        m.texture.save(os.path.join(dirs["tex"], n + ".png"))
        bbgen.save_json(m.java_json(NS, display), os.path.join(dirs["mdl"], n + ".json"))
        bbgen.save_json({"model": {"type": "minecraft:model", "model": "%s:item/%s" % (NS, n)}},
                        os.path.join(dirs["items"], n + ".json"))
        # GeckoLib: geometry, texture, animations, item display json
        bbgen.save_json(m.geo_json(), os.path.join(dirs["gl_geo"], n + ".geo.json"))
        m.texture.save(os.path.join(dirs["gl_tex"], n + ".png"))
        bbgen.save_json(animation_json(n, mod.ANIMATIONS),
                        os.path.join(dirs["gl_anim"], n + ".animation.json"))
        bbgen.save_json({"parent": "builtin/entity", "gui_light": "front", "display": display},
                        os.path.join(dirs["gl_mdl"], n + ".json"))
        # Blockbench project
        rel = "../resourcepack/assets/%s/textures/item/%s.png" % (NS, n)
        bbgen.save_json(m.bbmodel(display, rel), os.path.join(dirs["bb"], n + ".bbmodel"))

        views = {"right": (-90, 0), "left": (90, 0), "iso_right": (-130, 22), "iso_left": (50, 22)}
        for vname, (yaw, pitch) in views.items():
            bbgen.render(m, yaw, pitch).save(os.path.join(dirs["pv"], "%s_%s.png" % (n, vname)))
        print("%-8s cubes=%3d texture=%dx%d bones=%s" % (n, len(m.cubes), m.size, m.size,
                                                        ",".join(m.groups)))


if __name__ == "__main__":
    main()

"""Build every gun: Blockbench projects, resource pack and preview renders.

    python3 tools/build.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bbgen  # noqa: E402
import glock17  # noqa: E402
import mk18  # noqa: E402

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


GUNS = [
    # module, hand scale, first person scale, gui scale, gui tilt, fp push (z)
    (mk18, 0.4, 0.42, 0.34, 30, -2.0),
    (glock17, 0.28, 0.32, 0.52, 0, 0.0),
]


def main():
    tex_dir = os.path.join(ROOT, "resourcepack/assets", NS, "textures/item")
    mdl_dir = os.path.join(ROOT, "resourcepack/assets", NS, "models/item")
    bb_dir = os.path.join(ROOT, "blockbench")
    pv_dir = os.path.join(ROOT, "previews")
    for d in (tex_dir, mdl_dir, bb_dir, pv_dir):
        os.makedirs(d, exist_ok=True)

    for mod, hs, fs, gs, tilt, push in GUNS:
        m = mod.build()
        shift = m.center_yz()
        m.check_java_limits()
        grip = [a + b for a, b in zip(mod.GRIP_POINT, shift)]
        m.build_texture()
        display = display_for(m, grip, hs, fs, gs, tilt, push)

        png = os.path.join(tex_dir, m.name + ".png")
        m.texture.save(png)
        bbgen.save_json(m.java_json(NS, display), os.path.join(mdl_dir, m.name + ".json"))
        rel = "../resourcepack/assets/%s/textures/item/%s.png" % (NS, m.name)
        bbgen.save_json(m.bbmodel(display, rel), os.path.join(bb_dir, m.name + ".bbmodel"))

        views = {"right": (-90, 0), "left": (90, 0), "iso_right": (-130, 22), "iso_left": (50, 22)}
        for vname, (yaw, pitch) in views.items():
            bbgen.render(m, yaw, pitch).save(os.path.join(pv_dir, "%s_%s.png" % (m.name, vname)))
        print("%-8s cubes=%3d texture=%dx%d shift=%s" % (m.name, len(m.cubes), m.size, m.size, shift))


if __name__ == "__main__":
    main()

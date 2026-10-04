"""First-person arms: gloved hands and sleeves holding the gun.

Built in real millimetres (so every gun gets same-size hands) into two bones,
`right_arm` and `left_arm`, children of `root`.  The mod hides both bones
outside first person (see geckolib/example GunRenderer).

Spec per gun (all in the gun's mm space: z back, y up, x right):

    ARMS = {
        "grip": ((z_top, y_top), (z_bottom, y_bottom)),   # pistol grip centre line
        "grip_w": 15, "grip_d": 16,    # half width, half depth of the grip
        "trigger": (z, y),             # where the index finger rests
        "left": {"kind": "forend", "z": .., "y_top": .., "y_bot": .., "w": ..}
              or {"kind": "support"}   # pistols: left hand wraps the right
        "right_dir": (pitch, yaw), "left_dir": (pitch, yaw),   # optional
    }
"""

import math

from bbgen import Material

MATS = {
    "glove": Material((44, 45, 47), 4),
    "glove_light": Material((70, 71, 73), 4),
    "glove_palm": Material((58, 54, 48), 5),
    "sleeve": Material((104, 108, 82), 6),
    "sleeve_dark": Material((80, 84, 62), 5),
    "cuff": Material((36, 36, 38), 3),
}

FINGER = 18.0     # finger thickness (mm)


def _seg(k, name, p0, p1, x0, x1, th, mat, g, bev=2.0):
    """Box from p0 to p1 (z, y) between x0 and x1, th thick, rounded."""
    (z0, y0), (z1, y1) = p0, p1
    L = math.hypot(z1 - z0, y1 - y0)
    ang = math.degrees(math.atan2(-(y1 - y0), z1 - z0))
    with k.frame("x", ang, 0, y0, z0):
        k.bv(name, x0, y0 - th / 2, z0 - th * 0.15, x1, y0 + th / 2, z0 + L + th * 0.15, bev, mat, g)


def _forearm(k, name, wrist, w, h, pitch, yaw, g):
    """Glove cuff + sleeve going back from the wrist (x, y, z)."""
    x, y, z = wrist
    with k.frame("y", yaw, x, y, z):
        with k.frame("x", pitch, x, y, z):
            k.bv(name + "_wrist", x - w * 0.42, y - h * 0.42, z - 10, x + w * 0.42, y + h * 0.42, z + 40, 6,
                 "glove", g)
            k.bv(name + "_cuff", x - w * 0.5, y - h * 0.5, z + 40, x + w * 0.5, y + h * 0.5, z + 70, 6,
                 "cuff", g)
            k.bv(name + "_sleeve", x - w * 0.56, y - h * 0.56, z + 66, x + w * 0.56, y + h * 0.56, z + 330, 9,
                 "sleeve", g, "wood")
            k.bv(name + "_sleeve_end", x - w * 0.6, y - h * 0.6, z + 330, x + w * 0.6, y + h * 0.6, z + 520, 10,
                 "sleeve_dark", g)


def right_hand(k, spec, g="right_arm"):
    (tz, ty), (bz, by) = spec["grip"]
    hw, d = spec["grip_w"], spec["grip_d"]
    rake = math.degrees(math.atan2(bz - tz, ty - by))     # bottom swept back = positive
    top = ty - 4
    with k.frame("x", -rake, 0, ty, tz):
        zf, zb = tz - d, tz + d                          # front / back strap in the grip frame
        # palm on the right side and the heel wrapping the back strap
        k.bv("rh_palm", hw - 1, top - 92, zf + 6, hw + 20, top + 4, zb + 14, 6, "glove", g)
        k.bv("rh_heel", -hw * 0.4, top - 92, zb - 2, hw + 16, top - 8, zb + 20, 7, "glove", g)
        k.bv("rh_web", -hw - 4, top - 8, zb - 6, hw + 14, top + 10, zb + 16, 5, "glove", g)
        # middle, ring and little finger wrapped round the front strap
        for i in range(3):
            y1 = top - 18 - i * 21
            y0 = y1 - (FINGER - (2 if i == 2 else 0))
            k.bv("rh_finger%d_front" % i, -hw - 3, y0, zf - FINGER, hw + 12, y1, zf + 1, 4, "glove", g)
            k.bv("rh_finger%d_tip" % i, -hw - FINGER + 2, y0 + 0.5, zf - FINGER + 2, -hw + 1, y1 - 0.5,
                 zf + d * 0.9, 4, "glove", g)
            k.b("rh_knuckle%d" % i, hw + 12, y0 + 3, zf - 6, hw + 13, y1 - 3, zf + 4, "glove_light", g)
        # thumb along the left side, pointing forward
        k.bv("rh_thumb_base", -hw - 17, top - 18, zf + 8, -hw + 1, top + 2, zb + 10, 5, "glove", g)
        k.bv("rh_thumb", -hw - 16, top - 14, zf - 22, -hw, top + 2, zf + 12, 5, "glove", g)
        wrist = (hw * 0.4, top - 70, zb + 18)
    # index finger on the trigger (gun space)
    trz, tr_y = spec["trigger"]
    kz, ky = tz - d * 0.6, ty - 6
    kz, ky = _rot_zy(kz, ky, tz, ty, -rake)
    _seg(k, "rh_index_a", (kz, ky), (trz + 10, tr_y + 2), hw + 2, hw + 18, FINGER - 2, "glove", g)
    k.bv("rh_index_tip", -4, tr_y - 8, trz - 14, hw + 16, tr_y + 9, trz + 12, 4, "glove", g)
    # forearm: back, down and slightly right
    wx, wy, wz = wrist
    wz2, wy2 = _rot_zy(wz, wy, tz, ty, -rake)
    pitch, yaw = spec.get("right_dir", (28, 14))
    _forearm(k, "rh_arm", (wx, wy2, wz2), 74, 66, pitch, yaw, g)
    return (wx, wy2, wz2)


def left_hand(k, spec, g="left_arm"):
    lf = spec["left"]
    if lf["kind"] == "support":
        return _support_hand(k, spec, g)
    z, yt, yb, w = lf["z"], lf["y_top"], lf["y_bot"], lf["w"]
    h = yt - yb
    # palm cupped under the forend, heel on the near (left) side
    k.bv("lh_palm", -w - 14, yb - 20, z - 46, w * 0.5, yb + 1, z + 46, 7, "glove_palm", g)
    k.bv("lh_heel", -w - 18, yb - 16, z - 30, -w + 1, yb + h * 0.45, z + 52, 6, "glove", g)
    # four fingers up the far (right) side
    for i in range(4):
        z0 = z - 46 + i * 23
        k.bv("lh_finger%d" % i, w * 0.3, yb - 18, z0, w + 4, yb - 2, z0 + FINGER, 4, "glove", g)
        k.bv("lh_finger%d_up" % i, w - 1, yb - 14, z0 + 1, w + FINGER - 2, yb + h * (0.7 - 0.06 * abs(i - 1.5)),
             z0 + FINGER - 1, 4, "glove", g)
    # thumb on the near side, pointing forward
    k.bv("lh_thumb", -w - 16, yb + h * 0.25, z - 70, -w + 1, yb + h * 0.25 + 17, z - 10, 5, "glove", g)
    k.bv("lh_thumb_base", -w - 18, yb + h * 0.1, z - 20, -w + 1, yb + h * 0.4, z + 20, 5, "glove", g)
    wrist = (-w * 0.6, yb - 24, z + 46)
    pitch, yaw = spec.get("left_dir", (34, -34))
    _forearm(k, "lh_arm", wrist, 70, 62, pitch, yaw, g)
    return wrist


def _support_hand(k, spec, g):
    """Pistol: the left hand wraps the right hand's fingers."""
    (tz, ty), (bz, by) = spec["grip"]
    hw, d = spec["grip_w"], spec["grip_d"]
    rake = math.degrees(math.atan2(bz - tz, ty - by))
    top = ty - 4
    with k.frame("x", -rake, 0, ty, tz):
        zf, zb = tz - d, tz + d
        k.bv("lh_palm", -hw - 40, top - 92, zf - 10, -hw - 16, top - 6, zb + 8, 6, "glove", g)
        for i in range(4):
            y1 = top - 14 - i * 20
            k.bv("lh_finger%d" % i, -hw - 20, y1 - FINGER, zf - FINGER * 2 - 2, hw + 16, y1, zf - FINGER + 2, 4,
                 "glove", g)
        k.bv("lh_thumb", -hw - 34, top - 6, zf - 30, -hw - 16, top + 10, zf + 26, 5, "glove", g)
        wrist = (-hw - 30, top - 66, zb + 8)
    wx, wy, wz = wrist
    wz2, wy2 = _rot_zy(wz, wy, tz, ty, -rake)
    pitch, yaw = spec.get("left_dir", (26, -24))
    _forearm(k, "lh_arm", (wx, wy2, wz2), 70, 62, pitch, yaw, g)
    return (wx, wy2, wz2)


def _rot_zy(z, y, oz, oy, deg):
    """Rotate (z, y) about (oz, oy) by a frame('x', deg) rotation."""
    a = math.radians(deg)
    dy, dz = y - oy, z - oz
    return oz + dy * math.sin(a) + dz * math.cos(a), oy + dy * math.cos(a) - dz * math.sin(a)


def add(m, k, spec):
    """Add both arms to model m (MM helper k); returns bone pivots (model units)."""
    for name, mat in MATS.items():
        m.materials.setdefault(name, mat)
    rw = right_hand(k, spec)
    lw = left_hand(k, spec)
    (tz, ty), _ = spec["grip"]
    lf = spec["left"]
    if lf["kind"] == "forend":
        lpalm = (-lf["w"] * 0.3, lf["y_bot"] - 10, lf["z"])
    else:
        lpalm = (-spec["grip_w"] - 28, ty - 50, tz)
    rpalm = (spec["grip_w"] + 10, ty - 40, tz)
    m.dynamic |= {"right_arm", "left_arm"}
    # about one texel per 2.5 mm, whatever the gun's scale
    m.group_density.update({"right_arm": 0.4 * k.u, "left_arm": 0.4 * k.u})
    palms = {"right_arm": k.P(*rpalm), "left_arm": k.P(*lpalm)}
    return {"right_arm": k.P(*rw), "left_arm": k.P(*lw)}, palms

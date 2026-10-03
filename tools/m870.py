"""Remington 870 Wingmaster (12 ga), 18.5" barrel, walnut furniture.

Scale: 1 model unit ~= 22 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((48, 49, 54), 5),         # blued steel
    "steel_dark": Material((30, 30, 33), 4),
    "steel_light": Material((96, 97, 102), 6),
    "wood": Material((112, 62, 32), 5),          # walnut
    "wood_s": Material((112, 62, 32), 5, edge=False),
    "wood_dark": Material((78, 42, 22), 5),
    "rubber": Material((26, 26, 26), 5),
    "white": Material((214, 214, 206), 3, edge=False),
    "brass": Material((190, 152, 70), 6),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def lerp(pts, z):
    for (z0, v0), (z1, v1) in zip(pts, pts[1:]):
        if z0 <= z <= z1:
            return v0 + (v1 - v0) * (z - z0) / (z1 - z0)
    return pts[-1][1] if z > pts[-1][0] else pts[0][1]


def build():
    m = Model("m870", MATERIALS, density=8)
    B = m.box
    cx, cy = 8.0, 10.0
    my = 8.95  # magazine tube axis

    # ======================================================================
    # barrel, bead, magazine tube
    # ======================================================================
    g = "barrel"
    m.cyl_z("barrel", cx, cy, -15.0, 7.0, 0.44, "steel", g)
    m.cyl_z("muzzle_ring", cx, cy, -15.05, -14.75, 0.47, "steel", g)
    B("muzzle_bore", 7.7, 9.7, -15.1, 8.3, 10.3, -15.05, "bore", g)
    m.cyl_z("bead", cx, 10.55, -14.75, -14.55, 0.11, "brass", g)
    m.bevel("barrel_ring", 7.42, my - 0.6, -9.0, 8.58, 10.5, -8.45, 0.2, "steel", g)
    m.cyl_z("barrel_extension", cx, cy, 6.6, 7.05, 0.6, "steel", g)
    m.cyl_z("mag_tube", cx, my, -8.6, 6.9, 0.48, "steel", g)
    m.cyl_z("mag_cap", cx, my, -9.6, -8.6, 0.56, "steel", g, "knurl")
    B("mag_cap_stud", 7.85, my - 0.85, -9.35, 8.15, my - 0.5, -9.0, "steel_light", g)

    # ======================================================================
    # pump forend with grooves and action bars
    # ======================================================================
    g = "pump"
    m.bevel("forend", 6.9, 7.65, -5.0, 9.1, 10.0, 2.0, 0.45, "wood", g, "wood")
    for k in range(7):
        z = -4.3 + k * 0.9
        B("forend_groove_l_%d" % k, 6.88, 8.0, z, 6.9, 9.7, z + 0.28, "wood_dark", g)
        B("forend_groove_r_%d" % k, 9.1, 8.0, z, 9.12, 9.7, z + 0.28, "wood_dark", g)
        B("forend_groove_b_%d" % k, 7.4, 7.63, z, 8.6, 7.65, z + 0.28, "wood_dark", g)
    m.cyl_z("forend_nut", cx, my, -5.25, -5.0, 0.5, "steel", g)
    for side, (a, b) in (("l", (7.08, 7.2)), ("r", (8.8, 8.92))):
        B("action_bar_" + side, a, 8.55, 1.9, b, 8.85, 8.6, "steel_light", g)

    # ======================================================================
    # receiver
    # ======================================================================
    g = "receiver"
    m.bevel("receiver", 7.0, 7.4, 7.0, 9.0, 11.0, 16.6, 0.4, "steel", g,
            text={"west": "MODEL 870", "east": "12 GA"})
    B("receiver_groove_l", 6.98, 10.3, 7.3, 7.0, 10.4, 16.3, "steel_dark", g)
    B("receiver_groove_r", 9.0, 10.3, 7.3, 9.02, 10.4, 16.3, "steel_dark", g)
    B("ejection_port", 9.0, 9.25, 8.4, 9.02, 10.6, 11.7, "bore", g)
    B("bolt", 8.95, 9.55, 10.2, 9.0, 10.35, 11.65, "steel_light", g)
    B("loading_port", 7.4, 7.38, 7.5, 8.6, 7.4, 11.8, "bore", g)
    B("shell_lifter", 7.5, 7.36, 7.6, 8.5, 7.38, 11.0, "steel_light", g)
    for side, (a, b) in (("l", (6.94, 7.0)), ("r", (9.0, 9.06))):
        m.pin_x("pin_front_" + side, (a + b) / 2, 7.95, 11.8, 0.13, a, b, "steel_light", g)
        m.pin_x("pin_rear_" + side, (a + b) / 2, 7.95, 15.4, 0.13, a, b, "steel_light", g)
    # trigger plate + guard
    m.bevel("trigger_plate", 7.15, 6.9, 10.6, 8.85, 7.45, 16.3, 0.12, "steel_dark", g)
    B("tg_front", 7.62, 6.4, 11.0, 8.38, 6.95, 11.35, "steel_dark", g)
    m.bevel("tg_bottom", 7.6, 6.05, 11.3, 8.4, 6.45, 14.4, 0.1, "steel_dark", g)
    m.edge("tg_corner_f", "x", 7.62, 8.38, 6.05, 11.0, -1, -1, 0.35, "steel_dark", g)
    B("tg_rear", 7.62, 6.05, 14.3, 8.38, 6.95, 14.65, "steel_dark", g)
    B("action_release", 7.55, 6.55, 10.4, 7.75, 6.92, 11.0, "steel_dark", g)
    m.cyl_x("safety", 7.05, 8.95, 7.15, 15.0, 0.16, "steel_dark", g)
    B("safety_ring", 8.9, 7.0, 14.85, 8.97, 7.3, 15.15, "red", g)

    g = "trigger"
    B("trigger_top", 7.88, 6.9, 12.35, 8.12, 7.45, 12.65, "steel_light", g)
    B("trigger_low", 7.88, 6.25, 12.35, 8.12, 6.95, 12.65, "steel_light", g,
      rot=("x", 22.5, (8, 6.92, 12.5)))

    # ======================================================================
    # semi-pistol-grip walnut stock built from slices
    # ======================================================================
    g = "stock"
    top_pts = [(16.6, 10.85), (20.0, 10.45), (29.2, 10.05)]
    bot_pts = [(16.6, 7.4), (18.2, 6.55), (19.4, 6.15), (20.6, 6.3), (29.2, 3.85)]
    wid_pts = [(16.6, 0.78), (19.0, 0.72), (29.2, 0.98)]
    z, i = 16.6, 0
    while z < 29.19:
        z2 = min(29.2, z + 0.8)
        zm = (z + z2) / 2
        top, bot, hw = lerp(top_pts, zm), lerp(bot_pts, zm), lerp(wid_pts, zm)
        m.bevel("stock_slice_%02d" % i, 8 - hw, bot, z, 8 + hw, top, z2 + (0.02 if z2 < 29.2 else 0),
                min(0.32, hw * 0.4), "wood_s", g, "wood")
        z, i = z2, i + 1
    B("stock_spacer", 7.0, 3.75, 29.2, 9.0, 10.15, 29.3, "white", g)
    m.bevel("recoil_pad", 7.0, 3.7, 29.3, 9.0, 10.2, 30.1, 0.25, "rubber", g, "ribs")
    B("sling_stud", 7.85, 4.6, 26.6, 8.15, 4.75, 27.0, "steel_light", g,
      rot=("x", 22.5, (8, 4.7, 26.8)))

    m.regroup({}, pivots={"trigger": (8, 7.4, 12.5), "pump": (8, my, -1.5)})
    m.dynamic = {"pump", "trigger"}
    return m


MATERIALS["red"] = Material((170, 34, 30), 3, edge=False)

GRIP_POINT = (8.0, 6.6, 18.4)

DISPLAY = {"hand": 0.4, "fp": 0.42, "gui": 0.33, "tilt": 30, "push": -2.5}

ANIMATIONS = {
    "shoot": (0.75, {
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.03: [12, 0, 0], 0.15: [0, 0, 0]}},
        "pump": {"position": {0.2: [0, 0, 0], 0.4: [0, 0, 4.4], 0.45: [0, 0, 4.4], 0.65: [0, 0, 0]}},
    }),
    "pump": (0.5, {
        "pump": {"position": {0.0: [0, 0, 0], 0.2: [0, 0, 4.4], 0.25: [0, 0, 4.4], 0.45: [0, 0, 0]}},
    }),
}

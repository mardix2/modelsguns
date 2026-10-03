"""Remington 870 Wingmaster (12 ga): 18.5" vent-rib barrel, grooved walnut
forend, semi-pistol-grip walnut stock with checkering, recoil pad.

Real proportions: ~1000 mm overall, 470 mm barrel.
Scale: 1 unit ~= 16 mm.  Muzzle points north (-Z), bore axis x=8, y=10.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((46, 47, 53), 3),          # deep blued steel
    "steel_dark": Material((30, 30, 34), 3),
    "steel_light": Material((102, 103, 110), 4),
    "alloy": Material((40, 40, 43), 3),           # trigger plate
    "wood": Material((116, 62, 30), 4),           # walnut
    "wood_s": Material((116, 62, 30), 4, edge=False),
    "wood_dark": Material((76, 38, 18), 4),
    "rubber": Material((26, 26, 26), 4),
    "white": Material((222, 222, 214), 2, edge=False),
    "red": Material((176, 34, 30), 2, edge=False),
    "brass": Material((196, 160, 80), 5),
    "hull": Material((150, 36, 30), 4),
    "bore": Material((6, 6, 6), 1, edge=False),
}

CX, CY = 8.0, 10.0
MY = 8.6       # magazine tube axis


def build():
    m = Model("m870", MATERIALS, density=7)
    B = m.box

    # ======================================================================
    # barrel with ventilated rib and bead
    # ======================================================================
    g = "barrel"
    m.cyl_z("barrel", CX, CY, -30.0, 0.6, 0.63, "steel", g)
    m.cyl_z("muzzle_crown", CX, CY, -30.06, -30.0, 0.5, "steel_dark", g)
    m.cyl_z("muzzle_bore", CX, CY, -30.1, -30.06, 0.42, "bore", g)
    m.cyl_z("barrel_chamber", CX, CY, -2.0, 0.6, 0.72, "steel", g)
    # vent rib: flat rib on little posts
    m.bevel("rib", 7.72, 10.95, -29.8, 8.28, 11.12, -0.4, 0.06, "steel", g, "serration")
    z, i = -29.6, 0
    while z < -0.8:
        B("rib_post_%02d" % i, 7.82, 10.5, z, 8.18, 10.98, z + 0.45, "steel", g)
        z, i = z + 1.55, i + 1
    m.cyl_z("bead", CX, 11.25, -29.75, -29.45, 0.14, "white", g)
    B("bead_base", 7.9, 11.1, -29.8, 8.1, 11.2, -29.4, "steel", g)
    # barrel band clamping onto the magazine tube
    m.bevel("barrel_band", 7.25, MY - 0.85, -22.2, 8.75, 10.75, -21.4, 0.35, "steel", g)
    m.pin_x("barrel_band_screw", 8.78, 9.3, -21.8, 0.16, 8.72, 8.84, "steel_light", g)

    g = "magazine"
    m.cyl_z("mag_tube", CX, MY, -21.6, 0.2, 0.72, "steel", g)
    m.cyl_z("mag_cap", CX, MY, -23.4, -21.6, 0.84, "steel", g, "knurl")
    m.cyl_z("mag_cap_face", CX, MY, -23.5, -23.4, 0.6, "steel_dark", g)
    m.bevel("mag_cap_stud", 7.8, MY - 1.25, -22.9, 8.2, MY - 0.78, -22.3, 0.06, "steel_light", g)
    B("mag_cap_stud_hole", 7.78, MY - 1.15, -22.75, 8.22, MY - 0.95, -22.45, "bore", g)

    # ======================================================================
    # grooved walnut forend (pump) with action bars
    # ======================================================================
    g = "pump"
    m.bevel("forend", 6.55, 7.0, -12.5, 9.45, 10.15, 1.4, 0.85, "wood", g, "wood")
    m.bevel("forend_nose", 6.75, 7.25, -12.9, 9.25, 9.95, -12.4, 0.75, "wood", g, "wood")
    for k in range(10):
        z = -11.6 + k * 1.15
        B("forend_groove_l_%d" % k, 6.53, 7.7, z, 6.55, 9.5, z + 0.42, "wood_dark", g)
        B("forend_groove_r_%d" % k, 9.45, 7.7, z, 9.47, 9.5, z + 0.42, "wood_dark", g)
        B("forend_groove_b_%d" % k, 7.4, 6.98, z, 8.6, 7.0, z + 0.42, "wood_dark", g)
    m.cyl_z("forend_tube_nut", CX, MY, -13.1, -12.85, 0.55, "steel", g)
    B("forend_nut_slot", 7.9, MY - 0.55, -13.12, 8.1, MY + 0.55, -13.08, "bore", g)
    for side, (a, b) in (("l", (6.9, 7.08)), ("r", (8.92, 9.1))):
        m.bevel("action_bar_" + side, a, 7.65, 1.2, b, 8.05, 8.2, 0.04, "steel_light", g, axis="x")

    # ======================================================================
    # receiver
    # ======================================================================
    g = "receiver"
    m.bevel("receiver", 7.05, 7.35, 0.0, 8.95, 11.25, 13.0, 0.55, "steel", g,
            text={"west": "REMINGTON", "east": "MODEL 870"})
    B("rcv_top_flat", 7.55, 11.2, 0.4, 8.45, 11.3, 12.6, "steel", g, "serration")
    m.bevel("rcv_front_ring", 6.95, 7.45, -0.2, 9.05, 11.15, 0.3, 0.6, "steel", g)
    for side, (a, b) in (("l", (7.02, 7.05)), ("r", (8.95, 8.98))):
        B("rcv_line_" + side, a, 10.35, 0.6, b, 10.45, 12.4, "steel_dark", g)
    # ejection port with the bolt visible
    B("ejection_port", 8.95, 8.95, 1.6, 8.97, 10.85, 6.4, "bore", g)
    m.bevel("bolt", 8.6, 9.35, 4.7, 8.96, 10.6, 6.35, 0.06, "steel_light", g, axis="x")
    B("bolt_extractor", 8.95, 9.6, 4.75, 8.99, 10.3, 5.0, "steel_dark", g)
    # loading port underneath, shell lifter, follower
    B("loading_port", 7.4, 7.33, 0.6, 8.6, 7.35, 6.6, "bore", g)
    B("shell_lifter", 7.5, 7.31, 1.0, 8.5, 7.33, 5.8, "steel_light", g)
    # pins (trigger plate)
    for side, (a, b) in (("l", (6.98, 7.06)), ("r", (8.94, 9.02))):
        m.pin_x("pin_front_" + side, (a + b) / 2, 8.0, 5.6, 0.16, a, b, "steel_light", g)
        m.pin_x("pin_rear_" + side, (a + b) / 2, 8.0, 11.9, 0.16, a, b, "steel_light", g)
    # trigger plate + guard (alloy)
    m.bevel("trigger_plate", 7.2, 6.85, 5.0, 8.8, 7.45, 12.6, 0.18, "alloy", g)
    m.bevel("tg_front", 7.5, 6.0, 6.55, 8.5, 6.95, 7.0, 0.1, "alloy", g, axis="y")
    m.bevel("tg_bottom", 7.5, 5.55, 6.9, 8.5, 6.05, 10.3, 0.14, "alloy", g)
    m.edge("tg_corner_f", "x", 7.52, 8.48, 5.55, 6.55, -1, -1, 0.5, "alloy", g)
    m.bevel("tg_rear", 7.5, 5.55, 10.1, 8.5, 6.95, 10.55, 0.1, "alloy", g, axis="y")
    m.edge("tg_corner_b", "x", 7.52, 8.48, 5.55, 10.55, -1, 1, 0.45, "alloy", g)
    # action (slide) release lever, left, in front of the guard
    with m.frame(("x", 15, (7.3, 6.9, 6.2))):
        m.bevel("slide_release", 7.15, 6.3, 5.6, 7.45, 6.95, 6.6, 0.06, "alloy", g, "knurl", axis="x")
    # cross-bolt safety behind the guard with red ring on the left
    m.cyl_x("safety", 7.0, 9.0, 7.15, 10.95, 0.24, "alloy", g)
    m.cyl_x("safety_ring", 6.95, 7.02, 7.15, 10.95, 0.26, "red", g)

    g = "trigger"
    m.bevel("trigger_top", 7.72, 6.6, 8.2, 8.28, 7.0, 8.65, 0.06, "steel_light", g, axis="y")
    with m.frame(("x", 16, (8, 6.65, 8.42))):
        m.bevel("trigger_mid", 7.72, 5.95, 8.2, 8.28, 6.7, 8.65, 0.06, "steel_light", g, axis="y")
    with m.frame(("x", 40, (8, 6.0, 8.25))):
        m.bevel("trigger_tip", 7.72, 5.7, 8.05, 8.28, 6.05, 8.45, 0.06, "steel_light", g, axis="y")

    # ======================================================================
    # semi-pistol-grip walnut stock from overlapping slabs
    # ======================================================================
    g = "stock"
    m.bevel("stock_tang", 7.35, 7.6, 12.8, 8.65, 11.0, 13.4, 0.35, "steel", g)
    with m.frame(("x", 1.6, (8, 11.0, 13.0))):
        m.bevel("stock_comb", 7.1, 8.3, 13.0, 8.9, 11.0, 33.2, 0.6, "wood_s", g, "wood", edges="top")
    with m.frame(("x", 7.0, (8, 9.6, 13.0))):
        B("stock_mid", 7.11, 6.4, 13.0, 8.89, 10.3, 33.4, "wood_s", g, "wood")
    with m.frame(("x", 17.5, (8, 6.5, 17.3))):
        m.bevel("stock_belly", 7.12, 6.5, 17.3, 8.88, 9.2, 33.35, 0.6, "wood_s", g, "wood", edges="bottom")
    # semi pistol grip: wrist dips down, then the belly takes over
    with m.frame(("x", 27, (8, 7.4, 13.1))):
        m.bevel("stock_wrist_low", 7.2, 7.4, 13.1, 8.8, 9.4, 18.2, 0.6, "wood_s", g, "wood")
    # checkering panels on the wrist
    with m.frame(("x", 14, (8, 8.8, 14.0))):
        for side, (a, b) in (("l", (7.08, 7.1)), ("r", (8.9, 8.92))):
            B("checkering_" + side, a, 7.7, 14.0, b, 9.9, 17.6, "wood_dark", g, "checker")
    # recoil pad with white line spacer, sling stud
    with m.frame(("x", 3.0, (8, 6.5, 33.6))):
        B("pad_spacer", 7.12, 2.55, 33.55, 8.88, 10.6, 33.72, "white", g)
        m.bevel("recoil_pad", 7.08, 2.5, 33.72, 8.92, 10.65, 34.65, 0.35, "rubber", g, "ribs")
        for k, y in enumerate((3.2, 9.9)):
            m.pin_x("pad_screw_%d" % k, 8.0, y, 34.66, 0.13, 7.9, 8.1, "steel_light", g,
                    rot=("y", 90, (8.0, y, 34.66)))
    with m.frame(("x", 17.5, (8, 6.5, 17.3))):
        m.bevel("sling_stud", 7.8, 6.15, 29.6, 8.2, 6.5, 30.2, 0.06, "steel_light", g)
        B("sling_stud_hole", 7.78, 6.25, 29.75, 8.22, 6.4, 30.05, "bore", g)

    # ======================================================================
    # spare shell held on the lifter (for the loading animation)
    # ======================================================================
    g = "shell"
    m.cyl_z("shell_hull", CX, 8.0, 1.1, 5.1, 0.42, "hull", g)
    m.cyl_z("shell_brass", CX, 8.0, 5.1, 5.9, 0.44, "brass", g)

    m.regroup({}, pivots={"trigger": (8, 7.0, 8.42), "pump": (8, MY, -5.5), "shell": (8, 8.0, 3.5)})
    m.dynamic = {"pump", "trigger", "shell"}
    return m


GRIP_POINT = (8.0, 6.8, 15.8)

DISPLAY = {"hand": 0.3, "fp": 0.32, "gui": 0.22, "tilt": 30, "push": -3.5}

ANIMATIONS = {
    "shoot": (0.75, {
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.03: [-12, 0, 0], 0.15: [0, 0, 0]}},
        "pump": {"position": {0.2: [0, 0, 0], 0.4: [0, 0, 5.8], 0.45: [0, 0, 5.8], 0.65: [0, 0, 0]}},
    }),
    "pump": (0.5, {
        "pump": {"position": {0.0: [0, 0, 0], 0.2: [0, 0, 5.8], 0.25: [0, 0, 5.8], 0.45: [0, 0, 0]}},
    }),
    # push a shell up into the loading port and forward into the tube
    "reload": (0.7, {
        "shell": {"position": {0.0: [0, -5, 0], 0.3: [0, -0.4, 0], 0.55: [0, 1.6, -4.5],
                               0.56: [0, -5, 0], 0.7: [0, -5, 0]}},
    }),
}

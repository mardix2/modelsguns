"""Accuracy International AWM (.338 Lapua Magnum), olive drab folding
thumbhole stock, fluted barrel, muzzle brake.  No optic: only the integral
Picatinny rail it would sit on.

Real proportions: 1230 mm overall, 686 mm barrel.
Scale: 1 unit ~= 20 mm.  Muzzle points north (-Z), bore axis x=8, y=10.
"""

import anims
from bbgen import Material, Model

MATERIALS = {
    "steel": Material((44, 45, 50), 3),
    "steel_dark": Material((28, 28, 31), 3),
    "steel_light": Material((100, 101, 107), 4),
    "od": Material((88, 96, 62), 4),              # olive drab stock
    "od_dark": Material((66, 72, 46), 4),
    "alu": Material((54, 56, 50), 3),             # chassis
    "rubber": Material((26, 26, 26), 4),
    "brass": Material((184, 148, 70), 5),
    "red": Material((176, 34, 30), 2, edge=False),
    "white": Material((222, 222, 214), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

CX, CY = 8.0, 10.0


def build():
    m = Model("awm", MATERIALS, density=7)
    B = m.box

    # ======================================================================
    # muzzle brake (two rows of ports) and fluted barrel
    # ======================================================================
    g = "barrel"
    m.cyl_z("brake_core", CX, CY, -31.0, -28.6, 0.6, "steel_dark", g)
    m.ring_z("brake_ports_a", CX, CY, -30.6, -29.95, 0.78, 0.18, 0.5, "steel", g)
    m.ring_z("brake_ports_b", CX, CY, -29.65, -29.0, 0.78, 0.18, 0.5, "steel", g)
    for k, (z0, z1) in enumerate(((-31.05, -30.6), (-29.95, -29.65), (-29.0, -28.6))):
        m.cyl_z("brake_ring_%d" % k, CX, CY, z0, z1, 0.78, "steel", g)
    m.cyl_z("muzzle_bore", CX, CY, -31.1, -31.05, 0.22, "bore", g)
    m.cyl_z("barrel_front", CX, CY, -28.6, -14.0, 0.6, "steel", g)
    m.cyl_z("barrel_rear", CX, CY, -14.0, 0.2, 0.7, "steel", g)
    m.cyl_z("barrel_taper", CX, CY, -14.3, -13.7, 0.66, "steel", g)
    for k, ang in enumerate((0, 60, 120, 180, 240, 300)):
        with m.frame(("z", ang, (CX, CY, -10))):
            B("flute_f_%d" % k, 7.88, 10.55, -27.4, 8.12, 10.62, -15.0, "steel_dark", g)
            B("flute_r_%d" % k, 7.86, 10.66, -13.0, 8.14, 10.72, -2.0, "steel_dark", g)

    # ======================================================================
    # action with integral rail, ejection port
    # ======================================================================
    g = "action"
    m.cyl_z("action_body", CX, 10.15, 0.0, 11.2, 0.9, "steel", g)
    m.bevel("action_flat", 7.2, 9.05, 0.0, 8.8, 10.2, 11.2, 0.15, "steel", g,
            text={"west": "AWM .338 LAPUA MAG"})
    m.bevel("recoil_lug", 7.25, 8.5, 0.2, 8.75, 9.1, 1.0, 0.1, "steel", g)
    m.rail_z("rail", 7.3, 8.7, 11.42, -1.0, 11.0, "steel", g, period=0.5, tooth=0.3, h=0.2, neck=0.25)
    B("rail_numbers", 7.29, 11.1, -0.8, 7.31, 11.25, 10.8, "white", g)
    B("ejection_port", 8.88, 9.85, 4.4, 8.91, 10.85, 7.6, "bore", g)
    m.cyl_z("bolt_body_seen", CX, 10.25, 4.5, 7.5, 0.72, "steel_light", g)
    for side, (a, b) in (("l", (7.15, 7.22)), ("r", (8.78, 8.85))):
        m.pin_x("action_screw_f_" + side, (a + b) / 2, 9.4, 1.6, 0.15, a, b, "steel_light", g)
        m.pin_x("action_screw_b_" + side, (a + b) / 2, 9.4, 10.4, 0.15, a, b, "steel_light", g)

    g = "bolt"
    m.cyl_z("bolt_shroud", CX, 10.25, 11.2, 12.7, 0.68, "steel_dark", g)
    m.cyl_z("bolt_shroud_cap", CX, 10.25, 12.7, 12.9, 0.5, "steel_dark", g)
    B("cocking_indicator", 7.9, 10.95, 12.2, 8.1, 11.1, 12.9, "red", g)
    with m.frame(("z", -12, (8.75, 10.3, 10.6))):
        m.cyl_x("bolt_handle", 8.6, 10.6, 10.3, 10.6, 0.2, "steel_light", g)
        m.cyl_x("bolt_knob", 10.5, 11.6, 10.3, 10.6, 0.55, "steel_dark", g, "knurl")
        m.cyl_x("bolt_knob_cap", 11.6, 11.75, 10.3, 10.6, 0.4, "steel_dark", g)
    # three-position safety (right, rear)
    with m.frame(("x", -20, (8.9, 9.6, 11.6))):
        m.bevel("safety_lever", 8.85, 9.45, 11.0, 9.1, 9.8, 12.4, 0.05, "steel_dark", g, "knurl", axis="x")

    # ======================================================================
    # chassis + olive drab forend
    # ======================================================================
    g = "stock"
    m.bevel("forend", 6.8, 7.4, -10.2, 9.2, 9.75, 3.2, 0.55, "od", g)
    m.bevel("forend_nose", 6.95, 7.6, -10.6, 9.05, 9.55, -10.1, 0.5, "od", g)
    m.bevel("channel_wall_l", 6.85, 9.6, -10.0, 7.25, 10.25, 3.0, 0.15, "od", g, edges="top")
    m.bevel("channel_wall_r", 8.75, 9.6, -10.0, 9.15, 10.25, 3.0, 0.15, "od", g, edges="top")
    for k in range(4):
        z = -8.8 + k * 2.4
        m.cyl_x("vent_l_%d" % k, 6.78, 6.82, 8.6, z, 0.42, "od_dark", g)
        m.cyl_x("vent_r_%d" % k, 9.18, 9.22, 8.6, z, 0.42, "od_dark", g)
    m.bevel("bipod_stud", 7.75, 6.95, -9.4, 8.25, 7.45, -8.6, 0.08, "steel_light", g)
    B("bipod_stud_hole", 7.73, 7.05, -9.15, 8.27, 7.3, -8.85, "bore", g)
    # chassis mid section around the action / magazine well
    m.bevel("chassis_mid", 6.9, 6.7, 3.0, 9.1, 9.3, 11.6, 0.35, "alu", g)
    for side, (a, b) in (("l", (6.84, 6.9)), ("r", (9.1, 9.16))):
        m.bevel("side_panel_" + side, a, 7.0, -9.4, b, 9.3, 2.6, 0.12, "od_dark", g, "stipple", axis="x")
        for k, z in enumerate((-8.0, -3.4, 1.4, 4.4, 10.4)):
            m.pin_x("panel_screw_%s_%d" % (side, k), (a + b) / 2, 8.15, z, 0.14,
                    a - 0.04 if side == "l" else a, b if side == "l" else b + 0.04, "steel_light", g)
    # trigger guard and magazine release lever
    m.bevel("tg_front", 7.55, 5.85, 7.3, 8.45, 6.75, 7.75, 0.1, "alu", g, axis="y")
    m.bevel("tg_bottom", 7.55, 5.45, 7.6, 8.45, 5.9, 11.6, 0.12, "alu", g)
    m.edge("tg_corner", "x", 7.57, 8.43, 5.45, 7.3, -1, -1, 0.5, "alu", g)
    with m.frame(("x", 20, (8, 6.6, 6.9))):
        m.bevel("mag_release", 7.55, 5.9, 6.75, 8.45, 6.7, 7.2, 0.08, "steel_dark", g, "knurl")

    g = "trigger"
    m.bevel("trigger_top", 7.72, 6.3, 9.1, 8.28, 6.7, 9.5, 0.06, "steel_light", g, axis="y")
    with m.frame(("x", 16, (8, 6.35, 9.3))):
        m.bevel("trigger_mid", 7.72, 5.75, 9.1, 8.28, 6.4, 9.5, 0.06, "steel_light", g, axis="y")
    with m.frame(("x", 40, (8, 5.8, 9.15))):
        m.bevel("trigger_tip", 7.72, 5.5, 8.95, 8.28, 5.85, 9.35, 0.06, "steel_light", g, axis="y")

    # ======================================================================
    # thumbhole butt (folding), adjustable cheek piece, monopod
    # ======================================================================
    g = "butt"
    with m.frame(("x", -16, (8, 7.0, 12.6))):
        m.bevel("grip", 7.05, 2.7, 11.5, 8.95, 7.2, 13.7, 0.45, "od", g, "stipple", axis="y")
        m.bevel("grip_cap", 7.1, 2.45, 11.55, 8.9, 2.75, 13.65, 0.2, "od_dark", g, axis="y")
    m.bevel("grip_heel", 7.15, 2.8, 12.6, 8.85, 4.2, 18.2, 0.4, "od", g)
    m.bevel("bridge", 7.15, 9.0, 11.4, 8.85, 10.45, 17.8, 0.45, "od", g, edges="top")
    m.bevel("thumbhole_post", 7.15, 3.8, 16.4, 8.85, 9.4, 18.0, 0.4, "od", g)
    # folding hinge
    for k, y in enumerate((5.0, 7.0, 9.0)):
        m.cyl_z("hinge_knuckle_%d" % k, 9.0, y, 17.6, 18.5, 0.32, "steel_dark", g)
    m.bevel("butt_body", 7.1, 3.1, 18.0, 8.9, 10.45, 30.2, 0.45, "od", g)
    for side, (a, b) in (("l", (7.08, 7.1)), ("r", (8.9, 8.92))):
        B("butt_recess_" + side, a, 4.4, 19.6, b, 9.0, 28.6, "od_dark", g)
    # adjustable cheek piece on two posts with a locking knob
    m.bevel("cheek_piece", 7.2, 10.95, 19.0, 8.8, 12.0, 28.8, 0.4, "od", g, edges="top")
    for k, z in enumerate((20.4, 27.2)):
        m.cyl_z("cheek_post_%d" % k, CX, 10.7, z, z + 0.6, 0.25, "steel_light", g)
    m.cyl_x("cheek_knob", 6.45, 7.1, 9.8, 20.7, 0.42, "steel_dark", g, "knurl")
    # spacers and butt pad
    B("butt_spacer_a", 7.15, 3.2, 30.2, 8.85, 10.4, 30.45, "steel_dark", g)
    B("butt_spacer_b", 7.15, 3.2, 30.45, 8.85, 10.4, 30.7, "od_dark", g)
    m.bevel("butt_pad", 7.05, 3.0, 30.7, 8.95, 10.6, 31.6, 0.35, "rubber", g, "ribs")
    # monopod
    m.bevel("monopod_housing", 7.6, 2.6, 26.6, 8.4, 3.2, 28.2, 0.15, "steel_dark", g)
    m.cyl_x("monopod_wheel", 7.45, 8.55, 2.4, 27.4, 0.5, "steel_dark", g, "knurl")
    m.bevel("monopod_leg", 7.8, 1.0, 27.15, 8.2, 2.6, 27.65, 0.08, "steel_light", g, axis="y")
    m.bevel("monopod_foot", 7.55, 0.7, 26.9, 8.45, 1.05, 27.9, 0.12, "rubber", g, axis="y")
    # QD sling cups
    m.pin_x("qd_cup_front_l", 6.8, 8.6, -6.0, 0.36, 6.7, 6.86, "steel_dark", g)
    m.pin_x("qd_cup_butt_l", 7.0, 4.6, 26.4, 0.36, 6.9, 7.12, "steel_dark", g)

    # ======================================================================
    # 5 round magazine
    # ======================================================================
    g = "magazine"
    m.bevel("mag_body", 7.32, 6.2, 3.6, 8.68, 9.2, 6.8, 0.15, "steel_dark", g, axis="y")
    for k in range(3):
        y = 6.6 + k * 0.8
        B("mag_rib_l_%d" % k, 7.28, y, 3.8, 7.32, y + 0.3, 6.6, "steel_dark", g)
        B("mag_rib_r_%d" % k, 8.68, y, 3.8, 8.72, y + 0.3, 6.6, "steel_dark", g)
    B("mag_round", 7.55, 9.2, 3.8, 8.45, 9.6, 6.6, "brass", g)
    m.cyl_z("mag_round_tip", CX, 9.4, 3.3, 3.8, 0.25, "brass", g)
    m.bevel("mag_floor", 7.25, 5.95, 3.5, 8.75, 6.25, 6.95, 0.1, "steel", g, axis="y")

    m.regroup({}, pivots={"trigger": (8, 6.7, 9.3), "bolt": (8, 10.25, 10.6),
                          "magazine": (8, 8.0, 5.2)})
    m.dynamic = {"bolt", "trigger", "magazine"}
    return m


GRIP_POINT = (8.0, 4.8, 13.2)

DISPLAY = {"hand": 0.3, "fp": 0.32, "gui": 0.22, "tilt": 30, "push": -4.0}

ANIM = {
    "trigger": True, "trigger_angle": 10,
    "mag_dir": [0, -1, 0], "mag_far": 14, "mag_gap": 0.45, "press_check": False,
    "recoil": 3.4, "recoil_time": 0.45, "shot_time": 0.5,
    "reload_time": 2.0, "reload_empty_time": 3.1,
    "reload_tilt": [4, 10, -22], "reload_lift": [-1.0, 1.0, -1.5],
}


def _bolt(a, t0):
    """Lift, pull, push, lock."""
    a.rot("bolt", t0, anims.ZERO)
    a.rot("bolt", t0 + 0.15, [0, 0, 62], "easeOutQuad")
    a.pos("bolt", t0 + 0.15, anims.ZERO)
    a.pos("bolt", t0 + 0.38, [0, 0, 6.0], "easeOutQuad")
    a.pos("bolt", t0 + 0.48, [0, 0, 6.0])
    a.pos("bolt", t0 + 0.7, anims.ZERO, "easeInQuad")
    a.rot("bolt", t0 + 0.7, [0, 0, 62])
    a.rot("bolt", t0 + 0.82, anims.ZERO, "easeInQuad")
    a.track("root", "rotation", [(t0, anims.ZERO), (t0 + 0.15, [2, 3, -8], "easeInOutSine"),
                                 (t0 + 0.7, [1, 3, -8], "easeInOutSine"), (t0 + 0.95, anims.ZERO, "easeInOutSine")])


def _bolt_only(c):
    a = anims.Anim(1.0)
    _bolt(a, 0.0)
    return a


def _reload_empty(c):
    a = anims.reload(dict(c, reload_time=2.0))
    a.length = c["reload_empty_time"]
    _bolt(a, 2.0)
    return a


ANIMATIONS = anims.build(ANIM, {"bolt": _bolt_only, "reload_empty": _reload_empty})

"""Accuracy International AWM (.338 Lapua Magnum): green thumbhole stock,
round action with integral rail, long barrel with muzzle brake, butt pad and
monopod.  No optic.

Outlines are traced from a side photo (tools/silhouettes/awm*.png, 0.893 px
per mm); widths come from real dimensions.  1 model unit = 20 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "steel": Material((48, 50, 54), 3),
    "steel_dark": Material((30, 31, 34), 3),
    "steel_light": Material((112, 114, 120), 4),
    "green": Material((96, 116, 62), 6),
    "green_dark": Material((72, 88, 46), 4),
    "rubber": Material((28, 28, 29), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((222, 222, 214), 2, edge=False),
    "red": Material((176, 34, 30), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 20.0
S = Silhouette("awm", 0.893, 32, 96)
Z, Y = S.zmm, S.ymm


def build():
    m = Model("awm", MATERIALS, density=7)
    k = MM(m, U)

    # ======================================================================
    # barrel: brake with two port rows, hex collar, taper, fluted barrel
    # ======================================================================
    g = "barrel"
    rings = ((32, 40, 12.5), (40, 47, 10.5), (47, 55, 12.5), (55, 62, 10.5), (62, 70, 12.5))
    for i, (a, b, r) in enumerate(rings):
        k.cyl("brake_%d" % i, 0, Z(a), Z(b), r, "steel_dark" if r < 12 else "steel", g)
    k.cyl("muzzle_bore", 0, Z(31.5), Z(32), 5.5, "bore", g)
    k.cyl("brake_collar", 0, Z(70), Z(76), 11.5, "steel", g)
    k.cyl("barrel_nut", 0, Z(76), Z(97), 15.5, "steel", g, "knurl")
    k.cyl("barrel_taper", 0, Z(97), Z(120), 11.5, "steel", g)
    k.cyl("barrel", 0, Z(120), Z(470), 9.8, "steel", g)
    k.cyl("barrel_rear", 0, Z(470), Z(605), 11.2, "steel", g)
    for i, ang in enumerate((0, 60, 120, 180, 240, 300)):
        with k.frame("z", ang, 0, 0, Z(300)):
            k.b("flute_%d" % i, -1.8, 9.4, Z(135), 1.8, 10.0, Z(455), "steel_dark", g)

    # ======================================================================
    # action: traced side outline, round body, integral rail, bolt
    # ======================================================================
    g = "action"
    act = S.rings([(586, 84), (842, 84), (842, 126), (586, 126)], src="metal")
    k.prof("action", act, -17, 17, "steel", g, step=8, bevel=7)
    k.cyl("action_round", -6, Z(600), Z(790), 17.5, "steel", g)
    rail_lo, rail_hi = Y(86), Y(79)
    k.b("rail_base", -10.5, rail_lo, Z(593), 10.5, rail_lo + 3, Z(800), "steel", g)
    m.teeth_z("rail_t", "up", k.X(-10.5), k.X(10.5), k.Y(rail_lo + 3), (rail_hi - rail_lo - 3) / U,
              k.Z(Z(595)), k.Z(Z(800)), "steel", g, period=10 / U, tooth=5.2 / U)
    k.b("rail_numbers", -10.6, rail_lo + 0.5, Z(600), -10.5, rail_lo + 2.5, Z(795), "white", g)
    k.b("action_mark", -17.2, Y(108), Z(640), -17, Y(98), Z(760), "steel", g,
        text={"west": "AWM .338 LAPUA"})
    k.b("ejection_port", 17, Y(104), Z(690), 17.3, Y(92), Z(760), "bore", g)
    for side, (a0, a1) in (("l", (-17.6, -17)), ("r", (17, 17.6))):
        k.pin("action_screw_f_" + side, (a0 + a1) / 2, Y(112), Z(615), 2.6, a0, a1, "steel_light", g)
        k.pin("action_screw_r_" + side, (a0 + a1) / 2, Y(112), Z(780), 2.6, a0, a1, "steel_light", g)

    g = "bolt"
    by = Y(100)
    k.cyl("bolt_body", by, Z(700), Z(758), 10.5, "steel_light", g, x=4)
    k.cyl("bolt_shroud", by, Z(836), Z(858), 13.5, "steel_dark", g)
    k.cyl("bolt_shroud_cap", by, Z(858), Z(864), 10, "steel_dark", g)
    k.b("cocking_indicator", -2, by + 9, Z(855), 2, by + 13, Z(866), "red", g)
    with k.frame("z", -25, 17, by, Z(826)):
        k.cylx("bolt_handle", 14, 58, by, Z(826), 4, "steel_light", g)
        k.cylx("bolt_knob", 50, 74, by, Z(826), 10, "steel_dark", g, "knurl")
    # three-position safety (right, rear)
    with k.frame("x", -20, 17, Y(108), Z(845)):
        k.bv("safety_lever", 16.5, Y(112), Z(832), 20, Y(104), Z(858), 1, "steel_dark", g, "knurl", axis="x")

    # ======================================================================
    # stock: traced green outline (forend, centre section, thumbhole butt)
    # ======================================================================
    g = "stock"
    # outline measured on the photo (px), thumbhole as an ellipse
    stock = [S.poly([(447, 107), (776, 107), (784, 112), (836, 113), (1066, 113), (1069, 116), (1069, 216),
                     (1064, 219), (1050, 219), (1046, 201), (1040, 196), (968, 196), (956, 204),
                     (940, 214), (920, 220), (885, 228), (862, 233), (846, 233), (841, 228), (834, 196),
                     (828, 168), (824, 154), (790, 152), (782, 170), (752, 170), (745, 159), (735, 155),
                     (726, 160), (722, 167), (676, 164), (660, 159), (640, 151), (620, 149), (452, 148),
                     (444, 143), (441, 135), (441, 117)]),
             S.poly([(892 + 25 * math.cos(a * math.pi / 8), 170 + 22 * math.sin(a * math.pi / 8))
                     for a in range(16)])]
    k.prof("stock", stock, -25, 25, "green", g, step=10, bevel=6)
    # barrel channel walls and the long vent slot
    k.b("channel", -14, Y(104), Z(452), 14, Y(102), Z(600), "green_dark", g)
    for side, x0 in (("l", -25.4), ("r", 25)):
        k.b("vent_slot_" + side, x0, Y(122), Z(462), x0 + 0.4, Y(117), Z(600), "green_dark", g)
    # screws (traced positions)
    for i, (sx, sy, w) in enumerate(((480, 140, 25), (575, 140, 25), (690, 152, 25), (783, 153, 25),
                                     (862, 133, 25), (1017, 135, 25), (1048, 188, 25), (860, 222, 25))):
        for side, s in (("l", -1), ("r", 1)):
            k.pin("screw_%d_%s" % (i, side), s * (w + 0.3), Y(sy), Z(sx), 3.4,
                  s * w - 0.2 if s > 0 else -w - 0.8, w + 0.8 if s > 0 else -w + 0.2, "steel_light", g)
    # front sling loop and QD cup
    k.cylx("sling_loop", -27, 27, Y(128), Z(458), 4.2, "steel_dark", g)
    k.cylx("qd_cup", -29, 29, Y(126), Z(1068), 6.5, "steel_dark", g)

    # trigger guard and magazine release (traced)
    guard = [S.poly([(786, 150), (783, 165), (788, 178), (800, 186), (818, 187), (832, 180), (837, 168),
                     (834, 150)]),
             S.poly([(796, 153), (794, 166), (800, 176), (812, 179), (824, 175), (828, 165), (825, 153)])]
    k.prof("trigger_guard", guard, -7, 7, "steel_dark", g, step=3, t=4, bevel=1.6)

    g = "trigger"
    tx, ty = Z(806), Y(152)
    k.bv("trigger_top", -3, ty - 6, tx - 3, 3, ty + 2, tx + 3, 0.6, "steel_light", g, axis="y")
    with k.frame("x", 18, 0, ty - 6, tx):
        k.bv("trigger_mid", -3, ty - 16, tx - 3, 3, ty - 5, tx + 3, 0.6, "steel_light", g, axis="y")
    with k.frame("x", 42, 0, ty - 15, tx - 1):
        k.bv("trigger_tip", -3, ty - 22, tx - 4, 3, ty - 14, tx + 2, 0.6, "steel_light", g, axis="y")

    # ======================================================================
    # butt pad, spacers, monopod (traced)
    # ======================================================================
    g = "stock"
    pad = S.rings([(1060, 92), (1140, 92), (1140, 240), (1060, 240)], src="metal")
    k.prof("butt_pad", pad, -29, 29, "rubber", g, "ribs", step=8, bevel=6)
    mono = S.rings([(995, 196), (1058, 196), (1058, 236), (995, 236)], src="metal")
    k.prof("monopod", mono, -10, 10, "steel_dark", g, "knurl", step=3, bevel=2)

    # ======================================================================
    # 5 round magazine (traced bottom)
    # ======================================================================
    g = "magazine"
    mag = S.rings([(674, 150), (776, 150), (776, 194), (674, 194)], src="metal")
    k.prof("mag_floor", mag, -18, 18, "steel_dark", g, step=4, bevel=2)
    k.bv("mag_body", -16, Y(162), Z(690), 16, Y(105), Z(765), 1.2, "steel_dark", g)
    k.b("mag_round", -6, Y(105), Z(694), 6, Y(98), Z(762), "brass", g)

    m.regroup({}, pivots={"trigger": k.P(0, ty, tx), "bolt": k.P(0, by, Z(826)),
                          "magazine": k.P(0, Y(150), Z(725))})
    m.dynamic = {"bolt", "trigger", "magazine"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(185), Z(880))


ARMS = {
    "grip": ((Z(848), Y(150)), (Z(857), Y(228))), "grip_w": 25, "grip_d": 17,
    "trigger": (Z(806), Y(166)),
    "left": {"kind": "forend", "z": Z(540), "y_top": Y(107), "y_bot": Y(148), "w": 25},
}

DISPLAY = {"hand": 0.3, "fp": 0.32, "gui": 0.22, "tilt": 30, "push": -4.0}

ANIM = {
    "hands": {"left_arm": [("magazine", None, None)], "right_arm": [("bolt", "bolt_knob", None)]},
    "aim_above_mm": 42,
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
    a.pos("bolt", t0 + 0.38, [0, 0, 5.0], "easeOutQuad")
    a.pos("bolt", t0 + 0.48, [0, 0, 5.0])
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

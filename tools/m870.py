"""Remington 870 Express Magnum (12 ga): vent-rib barrel, magazine tube,
checkered walnut forend (pump), receiver, checkered semi-pistol-grip stock
with recoil pad.

Outlines are measured on a side photo (2.1 px per mm, muzzle at x=-24,
bore at y=98; the forend and stock come from the traced wood mask);
widths from real dimensions.  1 model unit = 16 mm.
"""

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "steel": Material((70, 72, 78), 3),
    "steel_dark": Material((40, 41, 45), 3),
    "steel_light": Material((128, 130, 136), 4),
    "wood": Material((176, 102, 46), 5),
    "wood_dark": Material((120, 66, 28), 4),
    "rubber": Material((40, 40, 42), 4),
    "white": Material((224, 224, 216), 2, edge=False),
    "red": Material((176, 34, 30), 2, edge=False),
    "brass": Material((196, 160, 80), 5),
    "hull": Material((150, 36, 30), 4),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 16.0
S = Silhouette("m870", 2.1, -24, 98)
Z, Y, P = S.zmm, S.ymm, S.poly
MY = Y(161)   # magazine tube axis


def build():
    m = Model("m870", MATERIALS, density=7)
    k = MM(m, U)

    # ======================================================================
    # barrel with ventilated rib and bead, barrel band
    # ======================================================================
    g = "barrel"
    k.cyl("barrel", 0, Z(-24), Z(845), 9.3, "steel", g)
    k.cyl("muzzle_bore", 0, Z(-24.6), Z(-24), 7.6, "bore", g)
    k.bv("rib", -4, Y(73), Z(-22), 4, Y(67), Z(838), 0.6, "steel", g, "serration")
    x, i = -10, 0
    while x < 820:
        k.b("rib_post_%02d" % i, -2.4, Y(80), Z(x), 2.4, Y(72), Z(x + 22), "steel", g)
        x, i = x + 92, i + 1
    k.cyl("bead", Y(64), Z(-20), Z(-14), 1.6, "white", g)
    band = P([(238, 108), (281, 108), (281, 140), (238, 140)])
    k.prof("barrel_band", band, -9, 9, "steel", g, step=8, bevel=2)
    k.pin("band_screw", 9.5, Y(126), Z(259), 2.6, 9, 10.5, "steel_light", g)

    g = "magazine"
    k.cyl("mag_tube", MY, Z(262), Z(845), 12, "steel", g)
    k.cyl("mag_cap", MY, Z(205), Z(262), 15.5, "steel", g, "knurl")
    k.cyl("mag_cap_face", MY, Z(200), Z(205), 11, "steel_dark", g)
    k.cyl("mag_cap_ring", MY, Z(248), Z(262), 16, "steel_dark", g)

    # ======================================================================
    # checkered wooden forend (pump) with action bars
    # ======================================================================
    g = "pump"
    fe = P([(281, 109), (291, 101), (754, 101), (762, 109), (762, 205), (752, 213), (293, 213), (281, 202)])
    k.prof("forend", fe, -24, 24, "wood", g, "wood", step=12, bevel=7)
    panel = P([(410, 150), (560, 141), (720, 150), (655, 166), (720, 183), (560, 194), (410, 186),
               (470, 168)])
    for side, (a, b) in (("l", (-24.4, -23.6)), ("r", (23.6, 24.4))):
        k.prof("forend_checker_" + side, panel, a, b, "wood_dark", g, "checker", step=12, t=4, bevel=0.1)
    k.cyl("forend_nut", MY, Z(762), Z(778), 10, "steel", g)
    for side, (a0, a1) in (("l", (-13, -11)), ("r", (11, 13))):
        k.bv("action_bar_" + side, a0, Y(150), Z(760), a1, Y(140), Z(990), 0.4, "steel_light", g, axis="x")

    # ======================================================================
    # receiver, trigger plate and guard
    # ======================================================================
    g = "receiver"
    rcv = P([(838, 74), (1135, 79), (1197, 90), (1238, 102), (1219, 184), (838, 182)])
    k.prof("receiver", rcv, -17, 17, "steel", g, step=12, bevel=4)
    k.b("rcv_mark_l", -17.3, Y(160), Z(870), -17, Y(145), Z(1080), "steel", g,
        text={"west": "REMINGTON 870 EXPRESS MAGNUM"})
    for side, (a0, a1) in (("l", (-17.6, -17)), ("r", (17, 17.6))):
        k.pin("pin_front_" + side, (a0 + a1) / 2, Y(152), Z(1097), 2.6, a0, a1, "steel_light", g)
        k.pin("pin_rear_" + side, (a0 + a1) / 2, Y(152), Z(1200), 2.6, a0, a1, "steel_light", g)
    k.b("ejection_port", 17, Y(140), Z(880), 17.3, Y(100), Z(1010), "bore", g)
    k.bv("bolt", 14, Y(132), Z(935), 17.2, Y(108), Z(990), 0.6, "steel_light", g, axis="x")
    k.b("loading_port", -11, Y(182.6), Z(880), 11, Y(181.8), Z(1040), "bore", g)
    k.b("shell_lifter", -9, Y(182.3), Z(890), 9, Y(181.5), Z(1030), "steel_light", g)
    tp = P([(1000, 181), (1222, 181), (1222, 192), (1060, 192), (1000, 186)])
    k.prof("trigger_plate", tp, -13, 13, "steel_dark", g, step=8, t=3, bevel=1)
    guard = P([(1066, 190), (1084, 190), (1122, 214), (1150, 224), (1196, 226), (1206, 212), (1206, 190),
               (1222, 190), (1220, 230), (1210, 243), (1160, 241), (1110, 228), (1080, 204)])
    k.prof("trigger_guard", guard, -6, 6, "steel_dark", g, step=6, t=3, bevel=1.2)
    k.prof("action_release", P([(1062, 190), (1098, 190), (1092, 198), (1070, 198)]), -14, -6,
           "steel_dark", g, step=6, t=3, bevel=0.6)
    k.cylx("safety", -16, 16, Y(193), Z(1210), 3.8, "steel_light", g)
    k.cylx("safety_ring", -16.6, -16, Y(193), Z(1210), 4.2, "red", g)

    g = "trigger"
    k.prof("trigger", P([(1185, 192), (1195, 192), (1203, 214), (1201, 234), (1195, 232), (1192, 212)]),
           -3.5, 3.5, "steel_light", g, step=6, t=3, bevel=0.6)

    # ======================================================================
    # semi-pistol-grip stock with checkering, recoil pad
    # ======================================================================
    g = "stock"
    stock = P([(1238, 102), (1316, 128), (1389, 146), (1453, 151), (1544, 155), (1680, 169), (1857, 187),
               (1857, 415), (1725, 360), (1589, 315), (1480, 278), (1453, 278), (1407, 302), (1380, 302),
               (1362, 278), (1316, 219), (1271, 196), (1222, 192), (1219, 184)])
    k.prof("stock", stock, -21, 21, "wood", g, "wood", step=14, bevel=8)
    chk = P([(1262, 130), (1330, 140), (1420, 190), (1453, 240), (1380, 225), (1290, 170)])
    for side, (a, b) in (("l", (-21.4, -20.6)), ("r", (20.6, 21.4))):
        k.prof("grip_checker_" + side, chk, a, b, "wood_dark", g, "checker", step=12, t=4, bevel=0.1)
    k.prof("grip_cap", P([(1372, 300), (1410, 300), (1408, 310), (1380, 310)]), -15, 15, "steel_dark", g,
           step=6, t=3, bevel=1)
    k.prof("pad_spacer", P([(1855, 188), (1861, 189), (1861, 415), (1855, 413)]), -21.5, 21.5, "white", g,
           step=4, t=2, bevel=0.5)
    pad = P([(1861, 189), (1905, 195), (1935, 424), (1925, 437), (1861, 415)])
    k.prof("recoil_pad", pad, -22, 22, "rubber", g, "ribs", step=8, bevel=5)

    # ======================================================================
    # spare shell (loading animation), at the loading port
    # ======================================================================
    g = "shell"
    k.cyl("shell_hull", Y(160), Z(905), Z(1028), 10.3, "hull", g)
    k.cyl("shell_brass", Y(160), Z(1028), Z(1052), 10.8, "brass", g)

    m.regroup({}, pivots={"trigger": k.P(0, Y(192), Z(1190)), "pump": k.P(0, MY, Z(520)),
                          "shell": k.P(0, Y(160), Z(980))})
    m.dynamic = {"pump", "trigger", "shell"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(250), Z(1360))


ARMS = {
    "grip": ((Z(1322), Y(175)), (Z(1395), Y(280))), "grip_w": 21, "grip_d": 19,
    "trigger": (Z(1197), Y(215)),
    "left": {"kind": "forend", "z": Z(520), "y_top": Y(101), "y_bot": Y(213), "w": 24},
}

DISPLAY = {"hand": 0.3, "fp": 0.32, "gui": 0.22, "tilt": 30, "push": -3.5}

PUMP = 95 / U

ANIM = {
    "trigger": True, "trigger_angle": 12, "mag": None,
    "recoil": 3.0, "recoil_time": 0.4, "shot_time": 0.45,
}


def _pump(a, t0):
    a.pos("pump", t0, anims.ZERO)
    a.pos("pump", t0 + 0.16, [0, 0, PUMP], "easeOutQuad")
    a.pos("pump", t0 + 0.22, [0, 0, PUMP])
    a.pos("pump", t0 + 0.38, anims.ZERO, "easeInQuad")
    a.track("root", "position", [(t0, anims.ZERO), (t0 + 0.16, [0, -0.3, 0.6], "easeOutQuad"),
                                 (t0 + 0.38, anims.ZERO, "easeInOutSine")])


def _shoot(c):
    a = anims.shoot(c)
    a.length = 0.95
    _pump(a, 0.45)
    return a


def _pump_only(c):
    a = anims.Anim(0.42)
    _pump(a, 0.0)
    return a


def _insert(a, t0):
    """One shell pushed up into the loading port and forward into the tube."""
    a.pos("shell", t0, [0, -6, 2])
    a.pos("shell", t0 + 0.2, [0, -1.0, 0], "easeOutCubic")
    a.pos("shell", t0 + 0.32, [0, 0.3, -3.0], "easeInQuad")
    a.pos("shell", t0 + 0.33, [0, -6, 2], "step")


def _reload(c):
    """Loop this once per shell."""
    a = anims.Anim(0.55)
    a.track("root", "rotation", [(0, [4, 10, -40]), (0.55, [4, 10, -40])])
    a.track("root", "position", [(0, [-1, 1.5, -2]), (0.55, [-1, 1.5, -2])])
    _insert(a, 0.1)
    return a


def _reload_start(c):
    a = anims.Anim(0.35)
    a.track("root", "rotation", [(0, anims.ZERO), (0.35, [4, 10, -40], "easeInOutSine")])
    a.track("root", "position", [(0, anims.ZERO), (0.35, [-1, 1.5, -2], "easeInOutSine")])
    return a


def _reload_end(c):
    a = anims.Anim(0.85)
    a.track("root", "rotation", [(0, [4, 10, -40]), (0.35, anims.ZERO, "easeInOutSine")])
    a.track("root", "position", [(0, [-1, 1.5, -2]), (0.35, anims.ZERO, "easeInOutSine")])
    _pump(a, 0.4)
    return a


def _inspect(c):
    a = anims.inspect(c)
    a.pos("pump", 2.0, anims.ZERO)
    a.pos("pump", 2.2, [0, 0, 2.0], "easeInOutSine")
    a.pos("pump", 2.45, [0, 0, 2.0])
    a.pos("pump", 2.6, anims.ZERO, "easeInOutSine")
    return a


ANIMATIONS = anims.build(ANIM, {"shoot": _shoot, "pump": _pump_only, "reload": _reload,
                                "reload_start": _reload_start, "reload_end": _reload_end,
                                "inspect": _inspect})

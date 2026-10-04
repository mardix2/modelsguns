"""H&K MP5 (as in the reference photo: fixed A2 stock): slim handguard,
cocking tube, tri-lug muzzle, hooded front sight, drum rear sight, polymer
trigger group and stock, curved 30 rd magazine.

Outlines are measured on a side photo (tools/silhouettes/mp5.png, 0.81 px
per mm, muzzle at x=25, bore at y=81); widths from real dimensions.
1 model unit = 11 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "steel": Material((64, 66, 72), 3),
    "steel_dark": Material((34, 35, 39), 3),
    "steel_light": Material((104, 106, 112), 4),
    "polymer": Material((52, 53, 57), 4),
    "polymer_dark": Material((32, 33, 35), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((222, 222, 214), 2, edge=False),
    "red": Material((176, 34, 30), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 11.0
S = Silhouette("mp5", 0.81, 25, 81)
Z, Y, P = S.zmm, S.ymm, S.poly
TY = Y(58)    # cocking tube axis


def build():
    m = Model("mp5a5", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # barrel with tri-lug, hooded front sight, cocking tube
    # ======================================================================
    g = "barrel"
    k.cyl("barrel", 0, Z(25), Z(70), 7.4, "steel", g)
    k.cyl("muzzle_bore", 0, Z(24.6), Z(25), 4.2, "bore", g)
    for i in range(3):
        with k.frame("z", i * 120, 0, 0, Z(35)):
            k.b("tri_lug_%d" % i, -2.4, 6.5, Z(28), 2.4, 9.5, Z(42), "steel", g)
    k.cyl("barrel_collar", 0, Z(42), Z(46), 8.6, "steel", g)
    fs = P([(53, 87), (53, 30), (58, 27), (63, 27), (67, 30), (67, 87)])
    k.prof("front_sight", fs, -8, 8, "steel", g, step=8, bevel=1.5)
    k.b("fs_hood_hole", -8.2, Y(48), Z(55), 8.2, Y(35), Z(65), "bore", g)
    k.cyl("fs_post", Y(40), Z(58), Z(62), 1.0, "steel_dark", g)
    k.cyl("cocking_tube", TY, Z(62), Z(205), 9.5, "steel", g)
    k.cyl("cocking_tube_cap", TY, Z(58), Z(62), 8, "steel_dark", g)
    k.pin("fs_pin", 0, Y(70), Z(60), 2.2, -8.6, 8.6, "steel_light", g)

    # ======================================================================
    # handguard and receiver (traced)
    # ======================================================================
    g = "handguard"
    hg = S.rings([(67, 78), (203, 78), (203, 130), (67, 130)])
    k.prof("handguard", hg, -20, 20, "polymer", g, "ribs_z", step=10, bevel=5)

    g = "receiver"
    rcv = S.rings([(196, 50), (360, 50), (360, 106), (196, 106)])
    k.prof("receiver", rcv, -15, 15, "steel", g, step=10, bevel=2.5)
    k.cyl("rcv_tube", TY, Z(203), Z(360), 9.5, "steel", g)
    k.prof("rear_sight", P([(322, 52), (324, 40), (334, 35), (346, 38), (350, 52)]), -11, 11, "steel", g,
           step=8, bevel=1.5)
    k.cylx("rear_drum", -9, 9, Y(42), Z(336), 8, "steel_dark", g, "knurl")
    for side, x in (("l", -15.3), ("r", 15)):
        k.b("rcv_slot_" + side, x, Y(85), Z(228), x + 0.3, Y(77), Z(345), "steel_dark", g)
        k.b("rcv_rib_" + side, x, Y(66), Z(203), x + 0.3, Y(64), Z(355), "steel_dark", g)
        k.pin("rcv_pin_a_" + side, x + 0.15, Y(100), Z(212), 2.2, x - 0.3 if side == "l" else x,
              x + 0.3 if side == "l" else x + 0.6, "steel_light", g)
        k.pin("rcv_pin_b_" + side, x + 0.15, Y(100), Z(355), 2.2, x - 0.3 if side == "l" else x,
              x + 0.3 if side == "l" else x + 0.6, "steel_light", g)
    k.b("ejection_port", 15, Y(78), Z(232), 15.3, Y(62), Z(268), "bore", g)
    k.b("bolt_face", 13, Y(76), Z(234), 15.1, Y(64), Z(266), "steel_light", g)

    g = "cocking_handle"
    k.bv("cocking_handle", -26, TY - 3, Z(118), -9, TY + 3, Z(126), 1, "steel", g, axis="x")
    k.cylx("cocking_knob", -32, -24, TY, Z(122), 5, "polymer", g)
    k.b("cocking_slot", -9.8, TY - 2, Z(118), -9.4, TY + 2, Z(200), "bore", "receiver")

    # ======================================================================
    # trigger group, grip, stock (traced polymer)
    # ======================================================================
    g = "lower"
    low = P([(236, 104), (360, 104), (357, 112), (345, 128), (372, 187), (337, 207), (313, 140),
             (310, 137), (240, 137), (236, 130)])
    k.prof("trigger_housing", low, -14, 14, "polymer", g, step=10, bevel=3)
    guard = P([(258, 136), (266, 136), (268, 154), (276, 158), (302, 158), (308, 150), (310, 136),
               (314, 136), (312, 156), (304, 164), (272, 164), (262, 158)])
    k.prof("trigger_guard", guard, -5, 5, "polymer", g, step=6, t=3, bevel=1)
    k.b("mag_well", -14, Y(140), Z(203), 14, Y(100), Z(240), "steel", g)
    k.prof("mag_catch", P([(240, 100), (252, 100), (252, 128), (246, 132), (240, 128)]), -15.4, 15.4,
           "steel_dark", g, step=6, t=3, bevel=0.8)
    k.pin("mag_release", -14.6, Y(110), Z(246), 4, -15.6, -14, "steel_dark", g)
    for side, x in (("l", -14.3), ("r", 14)):
        k.pin("housing_pin_" + side, x + 0.15, Y(115), Z(345), 2.2, x - 0.3 if side == "l" else x,
              x + 0.3 if side == "l" else x + 0.6, "steel_light", g)
    # selector (left side) with its red/white markings
    k.b("sel_mark_s", -14.4, Y(104), Z(290), -14.2, Y(100), Z(296), "white", g)
    k.b("sel_mark_f", -14.4, Y(104), Z(270), -14.2, Y(100), Z(276), "red", g)

    g = "selector"
    k.pin("selector_hub", -15, Y(110), Z(302), 3.6, -16, -14, "steel_dark", g)
    k.bv("selector_lever", -16.2, Y(112), Z(280), -14.8, Y(107), Z(304), 0.3, "steel_dark", g, axis="x")

    g = "trigger"
    k.prof("trigger", P([(287, 133), (294, 133), (299, 145), (298, 155), (293, 153), (290, 143)]), -3, 3,
           "steel", g, step=4, t=2, bevel=0.5)

    g = "stock"
    stock = P([(357, 50), (383, 50), (403, 63), (427, 77), (460, 80), (567, 81), (575, 83), (577, 90),
               (577, 163), (568, 168), (507, 150), (447, 130), (403, 112), (370, 110), (357, 106)])
    k.prof("stock", stock, -18, 18, "polymer", g, step=12, bevel=5)
    k.b("butt_cap", -18.2, Y(166), Z(571), 18.2, Y(84), Z(577.5), "polymer_dark", g)
    for i, (sx, sy) in enumerate(((478, 108), (527, 113))):
        k.cylx("stock_pin_%d" % i, -18.5, 18.5, Y(sy), Z(sx), 3.6, "steel_dark", g)

    # ======================================================================
    # magazine (curved, measured)
    # ======================================================================
    g = "magazine"
    mag = P([(212, 104), (233, 104), (233, 120), (223, 163), (207, 207), (193, 240), (190, 242),
             (173, 231), (176, 222), (187, 200), (200, 160), (212, 120)])
    k.prof("mag", mag, -11, 11, "steel", g, step=8, bevel=2)
    pts = [(222, 122), (212, 162), (198, 202), (186, 228)]
    for side, x in (("l", -11.4), ("r", 11)):
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            zc, yc = Z((x0 + x1) / 2), Y((y0 + y1) / 2)
            ang = -math.degrees(math.atan2(x1 - x0, y1 - y0))
            L = math.hypot(x1 - x0, y1 - y0) / S.ppm / 2
            with k.frame("x", ang, 0, yc, zc):
                k.b("mag_rib_%s_%d" % (side, i), x, yc - L, zc - 1.8, x + 0.4, yc + L, zc + 1.8, "steel_light", g)
    k.prof("mag_floor", P([(171, 229), (178, 226), (194, 238), (192, 246), (185, 247)]), -12, 12,
           "steel_dark", g, step=6, t=3, bevel=1)
    k.b("mag_round", -4, Y(106), Z(213), 4, Y(100), Z(232), "brass", g)

    m.regroup({}, pivots={"magazine": k.P(0, Y(110), Z(222)), "trigger": k.P(0, Y(133), Z(290)),
                          "cocking_handle": k.P(-16, TY, Z(122)), "selector": k.P(-15, Y(110), Z(302))})
    m.dynamic = {"magazine", "trigger", "cocking_handle", "selector"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(170), Z(345))


ARMS = {
    "grip": ((Z(330), Y(136)), (Z(355), Y(200))), "grip_w": 14, "grip_d": 19,
    "trigger": (Z(293), Y(148)),
    "left": {"kind": "forend", "z": Z(135), "y_top": Y(60), "y_bot": Y(108), "w": 20},
}

DISPLAY = {"hand": 0.32, "fp": 0.34, "gui": 0.28, "tilt": 25, "push": -1.5}

ANIM = {
    "trigger": True, "trigger_angle": 12,
    "selector": ("selector", [-40, 0, 0]),
    "charging": ("cocking_handle", 120 / U), "charging_moves_action": False,
    "mag_dir": [0, -1, -0.12], "mag_far": 22, "mag_gap": 0.5,
    "recoil": 0.45, "recoil_time": 0.09, "shot_time": 0.08,
    "reload_time": 2.0, "reload_empty_time": 3.0,
    "reload_tilt": [6, 12, -24], "reload_lift": [-1.0, 1.0, -1.5],
}


def _reload_empty(c):
    """The HK slap: handle locked back first, magazine swapped, then slapped home."""
    t = 120 / U
    a = anims.Anim(c["reload_empty_time"])
    a.pos("cocking_handle", 0.0, anims.ZERO)
    a.pos("cocking_handle", 0.25, [0, 0, t], "easeInOutSine")
    a.pos("cocking_handle", 0.33, [0, 0.4, t], "easeOutQuad")
    seat = anims._mag_swap(a, c, 0.55)
    tt = seat + 0.45
    a.pos("cocking_handle", tt, [0, 0.4, t])
    a.pos("cocking_handle", tt + 0.05, [0, 0, t - 0.2], "easeOutQuad")
    a.pos("cocking_handle", tt + 0.12, anims.ZERO, "easeInCubic")
    anims._tilt(a, c, 0.4, tt + 0.2, c["reload_empty_time"])
    return a


ANIMATIONS = anims.build(ANIM, {"reload_empty": _reload_empty})

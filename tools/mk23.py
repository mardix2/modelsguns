"""HK Mk23 Mod 0 (.45 ACP), the big SOCOM pistol: black slide with a deep
top chamfer and slanted rear serrations, threaded barrel standing out of the
nose, round knurled hammer, FDE polymer frame with an accessory groove,
stippled grip, slide stop, decocking lever and safety with a red dot on the
left, paddle magazine release behind the guard.

Outlines are measured on a side photo (left side; 2.79 px per mm, muzzle
at x=11, bore at y=65); widths from real dimensions (slide 27 mm, 39 mm
over the controls).  1 model unit = 7 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "slide": Material((40, 44, 54), 4),
    "slide_dark": Material((20, 22, 28), 3),
    "slide_light": Material((70, 76, 90), 4),
    "fde": Material((178, 140, 96), 5),
    "fde_dark": Material((160, 124, 84), 5),
    "black": Material((32, 33, 37), 3),
    "barrel": Material((50, 52, 58), 4),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "red": Material((214, 40, 40), 2, edge=False),
    "text": Material((40, 44, 54), 4, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
S = Silhouette("mk23", 2.79, 11, 65)
Z, Y, P = S.zmm, S.ymm, S.poly
SW, FW, GW = 13.5, 13.0, 15.6     # half widths: slide, frame, grip
RAKE = 19.0


def circle(cx, cy, r, n=10):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def build():
    m = Model("mk23", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide
    # ======================================================================
    g = "slide"
    slide = P([(43, 36), (46, 32), (630, 32), (634, 36), (657, 100), (657, 105), (43, 105)])
    k.prof("slide", slide, -SW, SW, "slide", g, step=14, bevel=4)
    for side, x in (("l", -SW - 0.2), ("r", SW)):
        xo = -SW - 0.15 if side == "l" else SW
        k.b("side_step_" + side, xo, Y(83), Z(46), xo + 0.15, Y(80), Z(640), "slide_dark", g)
        for i in range(10):
            zc = Z(500 + i * 14.2)
            with k.frame("x", -11, 0, Y(75), zc):
                k.b("serr_%s_%d" % (side, i), x, Y(100), zc - 0.9, x + 0.2, Y(50), zc + 0.9, "slide_dark", g)
    k.b("slide_mark", -SW - 0.15, Y(75), Z(70), -SW, Y(50), Z(330), "text", g,
        text={"west": "HK MARK 23  Cal .45 Auto"})
    k.b("ejection_port", SW - 0.9, Y(66), Z(300), SW + 0.05, Y(33), Z(400), "slide_dark", g)
    k.b("port_chamber", SW - 0.5, Y(62), Z(306), SW + 0.1, Y(34), Z(394), "barrel", g)
    k.prof("front_sight", P([(58, 33), (60, 20), (64, 14), (82, 13), (85, 18), (85, 33)]), -2, 2, "slide_dark",
           g, step=6, t=2, bevel=0.4)
    k.b("front_dot", -1, Y(22), Z(57.8), 1, Y(17), Z(58.2), "white", g)
    k.prof("rear_sight", P([(562, 33), (564, 25), (580, 22), (582, 12), (605, 11), (607, 22), (626, 24),
                            (629, 33)]), -8, 8, "slide_dark", g, step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.6, Y(20), Z(578), 1.6, Y(10), Z(609), "bore", g)
    for side, xx in (("l", -6), ("r", 5)):
        k.b("rear_dot_" + side, xx, Y(19), Z(607.2), xx + 1, Y(15), Z(607.6), "white", g)

    # ======================================================================
    # barrel: threaded muzzle in front of the nose
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_thread", Y(65), Z(12), Z(44), 7.2, "barrel", g, "knurl")
    k.cyl("barrel_crown", Y(65), Z(11.4), Z(12), 6.6, "slide_light", g)
    k.cyl("muzzle_bore", Y(65), Z(11.2), Z(11.4), 5.8, "bore", g)
    k.cyl("barrel_body", Y(65), Z(44), Z(400), 8.4, "barrel", g)

    # ======================================================================
    # frame: dust cover with the accessory groove, guard, stippled grip
    # ======================================================================
    g = "frame"
    frame = P([(46, 105), (668, 105), (672, 120), (689, 131), (666, 152), (617, 170), (606, 183), (607, 198),
               (615, 209), (624, 240), (639, 266), (640, 278), (647, 289), (650, 315), (655, 321), (654, 333),
               (670, 384), (668, 392), (497, 392), (494, 388), (493, 364), (461, 266), (461, 257), (448, 243),
               (405, 250), (344, 250), (294, 245), (270, 237), (256, 227), (256, 219), (265, 203), (265, 173),
               (253, 156), (242, 152), (112, 154), (54, 148), (40, 129), (45, 122), (40, 115), (42, 112)])
    hole = P([(297, 172), (309, 161), (383, 158), (440, 158), (452, 175), (452, 205), (440, 222), (392, 226),
              (345, 227), (318, 224), (299, 208)])
    k.prof("frame", [frame, hole], -FW, FW, "fde", g, step=14, bevel=2.4)
    grip = P([(470, 232), (480, 200), (500, 175), (530, 160), (604, 160), (607, 198), (615, 209), (624, 240),
              (639, 266), (647, 289), (650, 315), (655, 321), (654, 333), (670, 384), (668, 392), (497, 392),
              (494, 388), (493, 364), (475, 300), (466, 265)])
    k.prof("grip", grip, -GW, GW, "fde_dark", g, "stipple", step=14, bevel=2.4)
    for side, x in (("l", -FW - 0.15), ("r", FW)):
        k.prof("groove_" + side, P([(50, 115), (226, 115), (231, 120), (231, 125), (226, 130), (50, 130)]),
               x, x + 0.15, "fde_dark", g, step=10, t=2, bevel=0.05)
        k.b("groove_low_" + side, x, Y(147), Z(103), x + 0.15, Y(143), Z(177), "fde_dark", g)
        k.b("hk_logo_" + side, (x - 2.6) if side == "l" else x + 2.6, Y(364), Z(560),
            (x - 2.45) if side == "l" else x + 2.75, Y(348), Z(600), "fde", g,
            text={"west" if side == "l" else "east": "HK"})
    # decocking lever, safety with the red dot (left), paddle release, pin
    k.prof("decocker", P([(509, 111), (548, 122), (582, 139), (579, 153), (568, 154), (509, 128)]), -FW - 2.4,
           -FW, "black", g, step=8, t=2, bevel=0.5)
    k.prof("decocker_hub", circle(512, 118, 7), -FW - 2.8, -FW, "black", g, step=6, t=2, bevel=0.4)
    k.prof("safety", P([(586, 125), (600, 116), (640, 119), (648, 126), (648, 139), (640, 144), (587, 143)]),
           -FW - 2.4, -FW, "black", g, "knurl", step=8, t=2, bevel=0.5)
    k.prof("safety_hub", circle(605, 114, 6), -FW - 2.8, -FW, "black", g, step=6, t=2, bevel=0.4)
    k.b("safety_red", -FW - 2.65, Y(118), Z(589), -FW - 2.4, Y(110), Z(597), "red", g)
    k.prof("mag_paddle", P([(432, 222), (452, 218), (464, 226), (462, 238), (440, 238)]), -FW - 0.6, FW + 0.6, "black", g,
           step=6, t=2, bevel=0.6)
    for side, (a, b) in (("l", (-FW - 0.6, -FW)), ("r", (FW, FW + 0.6))):
        k.pin("pin_a_" + side, (a + b) / 2, Y(209), Z(457), 1.4, a, b, "black", g)
        k.pin("pin_b_" + side, (a + b) / 2, Y(152), Z(640), 1.4, a, b, "black", g)

    g = "slide_stop"
    k.prof("slide_stop", P([(350, 110), (486, 108), (488, 128), (470, 134), (360, 136), (347, 128)]), -FW - 1.8,
           -FW, "black", g, step=8, t=2, bevel=0.5)
    k.prof("slide_stop_hub", circle(364, 119, 7), -FW - 2.4, -FW, "black", g, step=6, t=2, bevel=0.4)

    g = "trigger"
    trig = P([(397, 146), (426, 146), (431, 170), (434, 195), (428, 212), (412, 222), (406, 218), (418, 205),
              (420, 190), (414, 172), (403, 158)])
    k.prof("trigger", trig, -3.6, 3.6, "black", g, step=6, t=2, bevel=0.5)

    g = "hammer"
    k.prof("hammer", circle(677, 114, 15, 12), -4.5, 4.5, "black", g, "knurl", step=6, t=3, bevel=0.8)
    k.prof("hammer_stem", P([(652, 104), (668, 104), (670, 128), (652, 128)]), -3.5, 3.5, "black", g, step=6,
           t=2, bevel=0.5)

    g = "magazine"
    mz, my = Z(540), Y(300)
    with k.frame("x", -RAKE, 0, my, mz):
        k.b("mag_body", -11.5, Y(392), mz - 16, 11.5, Y(160), mz + 16, "black", g)
        k.b("mag_round", -5.5, Y(160), mz - 15, 5.5, Y(145), mz + 13, "brass", g)
    k.prof("mag_base", P([(498, 396), (510, 387), (636, 386), (652, 392), (658, 404), (654, 413), (500, 413)]),
           -FW - 0.4, FW + 0.4, "black", g, step=10, bevel=1.6)

    m.regroup({}, pivots={"trigger": k.P(0, Y(147), Z(412)), "magazine": k.P(0, my, mz),
                          "slide": k.P(0, Y(65), Z(350)), "barrel": k.P(0, Y(65), Z(200)),
                          "slide_stop": k.P(-13.5, Y(119), Z(364)), "hammer": k.P(0, Y(125), Z(662))})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(290), Z(560))

ARMS = {
    "grip": ((Z(545), Y(180)), (Z(590), Y(380))), "trigger": (Z(418), Y(195)),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.25, "fp": 0.32, "gui": 0.43, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 30 / U, "locks_back": True, "hammer": 32,
    "followers": {"barrel": {"pos": [0, -0.2, 1.2], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.946, 0.326], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 2.0, "recoil_time": 0.28, "shot_time": 0.3, "cycle_back": 0.04, "cycle_fwd": 0.09,
    "reload_time": 1.7, "reload_empty_time": 2.1,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

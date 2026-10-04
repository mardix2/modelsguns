"""SIG Sauer P320 AXG: black stainless slide with angled front and rear
cuts, optic cover plate, dovetail sights, black alloy frame with an
accessory rail, beavertail and stippled front strap, checkered red wood
grip panels, knurled round magazine release, striker fired.

Outlines are measured on a side photo (left side; 4.76 px per mm, muzzle at
x=89, bore at y=148); widths from real dimensions (slide 25.4 mm, 35 mm
over the grips).  1 model unit = 7 mm.
"""

import math

import cv2
import numpy as np

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "slide": Material((44, 45, 49), 4),
    "slide_dark": Material((22, 23, 25), 3),
    "slide_light": Material((86, 88, 94), 4),
    "frame": Material((36, 36, 39), 4),
    "frame_dark": Material((20, 20, 22), 3),
    "wood": Material((150, 50, 34), 6),
    "wood_dark": Material((118, 38, 28), 5),
    "barrel": Material((96, 98, 104), 4),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "text": Material((44, 45, 49), 4, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
S = Silhouette("p320", 4.76, 89, 148)
Z, Y, P = S.zmm, S.ymm, S.poly
SW, FW, GW = 12.7, 11.4, 2.6     # half widths: slide, frame; grip panel thickness
RAKE = 14.0


def circle(cx, cy, r, n=10):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def inset(pts, d, eps=2.0):
    """outline (px) shrunk by d px"""
    m = np.zeros((800, 1100), np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
    m = cv2.erode(m, np.ones((2 * d + 1, 2 * d + 1), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    a = cv2.approxPolyDP(max(cs, key=cv2.contourArea), eps, True)[:, 0, :]
    return P([(float(x), float(y)) for x, y in a])


def cuts(k, name, side, xs, y0, y1, slant, w, mat, g):
    """slanted grooves on a slide side: tops lean forward by `slant` deg"""
    x = -SW - 0.2 if side == "l" else SW
    yc = (Y(y0) + Y(y1)) / 2
    for i, px in enumerate(xs):
        zc = Z(px)
        with k.frame("x", slant, 0, yc, zc):
            k.b("%s_%s_%d" % (name, side, i), x, Y(y1), zc - w / 2, x + 0.2, Y(y0), zc + w / 2, mat, g)


def build():
    m = Model("p320", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: deep top chamfers, angled cuts front and rear, optic plate
    # ======================================================================
    g = "slide"
    slide = P([(91, 96), (97, 89), (106, 86), (840, 86), (846, 95), (852, 130), (860, 188), (860, 194),
               (96, 194), (91, 189)])
    k.prof("slide", slide, -SW, SW, "slide", g, step=14, bevel=4)
    for side in ("l", "r"):
        cuts(k, "serr_f", side, [178 + 22 * i for i in range(7)], 142, 186, -15, 2.6, "slide_dark", g)
        cuts(k, "serr_r", side, [652 + 22 * i for i in range(8)], 120, 186, -15, 2.6, "slide_dark", g)
        x = -SW - 0.15 if side == "l" else SW
        k.b("chamfer_line_" + side, x, Y(142), Z(96), x + 0.15, Y(140), Z(852), "slide_dark", g)
        k.b("plate_line_" + side, x, Y(107), Z(561), x + 0.15, Y(105), Z(782), "slide_dark", g)
    k.b("slide_mark", -SW - 0.15, Y(124), Z(153), -SW, Y(100), Z(296), "text", g,
        text={"west": "SIG SAUER P320"})
    k.b("ejection_port", SW - 0.9, Y(130), Z(382), SW + 0.05, Y(87), Z(522), "slide_dark", g)
    k.b("port_chamber", SW - 0.5, Y(126), Z(388), SW + 0.1, Y(88), Z(516), "barrel", g)
    k.b("port_top", -6, Y(98), Z(382), SW - 1.4, Y(86) + 0.06, Z(522), "barrel", g)
    k.prof("front_sight", P([(102, 87), (106, 77), (112, 73), (150, 70), (155, 73), (155, 87)]), -1.7, 1.7,
           "slide_dark", g, step=6, t=2, bevel=0.4)
    k.b("front_dot", -0.9, Y(78), Z(101.8), 0.9, Y(73), Z(102.4), "white", g)
    k.prof("rear_sight", P([(778, 87), (780, 70), (788, 64), (820, 64), (824, 70), (824, 87)]), -6, 6,
           "slide_dark", g, step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.4, Y(76), Z(776), 1.4, Y(63), Z(826), "bore", g)

    # ======================================================================
    # barrel: crown in the slide nose, hood in the port
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_crown", Y(148), Z(90.4), Z(92), 7.0, "barrel", g)
    k.cyl("muzzle_bore", Y(148), Z(90.2), Z(90.4), 4.6, "bore", g)
    k.cyl("barrel_body", Y(148), Z(92), Z(560), 7.0, "barrel", g)

    # ======================================================================
    # frame: rail dust cover, squared guard, beavertail, grip
    # ======================================================================
    g = "frame"
    trig = [(512, 288), (547, 288), (538, 300), (537, 337), (533, 363), (523, 383), (507, 395), (487, 397),
            (484, 392), (500, 385), (516, 372), (522, 352), (522, 305)]
    frame = S.rings([(80, 193), (960, 193), (960, 681), (80, 681)], eps=3.0, smooth=2.5, min_edge=6, cut=[trig])
    frame = [r for r in frame if len(r) > 5]       # drop slivers left by the trigger cut
    k.prof("frame", frame, -FW, FW, "frame", g, step=14, bevel=2)
    # stippled front strap and checkered red wood panels
    panel = [(615, 221), (830, 221), (838, 232), (838, 262), (826, 282), (818, 305), (818, 340), (840, 400),
             (866, 500), (882, 560), (892, 610), (895, 673), (708, 675), (703, 580), (697, 535), (680, 455),
             (662, 425), (655, 400), (642, 355), (625, 300), (612, 250)]
    strap = P([(640, 432), (662, 428), (680, 455), (697, 535), (703, 580), (708, 675), (690, 677), (672, 612),
               (660, 520), (648, 470)])
    checker = inset([(628, 296), (818, 296)] + panel[6:19], 12)
    for side, (a, b) in (("l", (-FW - GW, -FW)), ("r", (FW, FW + GW))):
        o = a if side == "l" else b
        k.prof("strap_" + side, strap, -FW - 0.2 if side == "l" else FW, -FW if side == "l" else FW + 0.2,
               "frame_dark", g, "stipple", step=10, t=2, bevel=0.1)
        k.prof("grip_" + side, P(panel), a, b, "wood", g, step=12, bevel=1.2)
        k.prof("checker_" + side, checker, o - 0.15 if side == "l" else o - 0.3, o + 0.3 if side == "l" else o + 0.15,
               "wood_dark", g, "checker", step=10, t=2, bevel=0.1)
        for j, (cx, cy) in enumerate(((740, 360), (813, 627))):
            k.pin("grip_screw_%s_%d" % (side, j), o, Y(cy), Z(cx), 1.9, o - 0.5 if side == "l" else o - 0.2,
                  o + 0.2 if side == "l" else o + 0.5, "frame_dark", g)
    # takedown lever, magazine release (left), pins
    k.prof("takedown", P([(403, 200), (530, 200), (532, 205), (528, 228), (470, 230), (462, 245), (445, 254),
                          (430, 250), (418, 232), (405, 215)]), -FW - 1.4, -FW, "frame_dark", g, step=8, t=2,
           bevel=0.5)
    for i in range(4):
        yy = 205 + i * 5.5
        k.b("takedown_rib_%d" % i, -FW - 1.6, Y(yy + 2), Z(458), -FW - 1.4, Y(yy), Z(526), "slide_light", g)
    k.prof("mag_release", circle(643, 393, 18), -FW - 1.8, -FW, "frame_dark", g, "knurl", step=6, t=2, bevel=0.5)
    for side, (a, b) in (("l", (-FW - 0.6, -FW)), ("r", (FW, FW + 0.6))):
        k.pin("module_pin_" + side, (a + b) / 2, Y(230), Z(568), 1.4, a, b, "slide_light", g)

    g = "slide_stop"
    k.prof("slide_stop", P([(655, 190), (714, 190), (716, 204), (710, 218), (662, 218), (655, 205)]), -FW - 1.6,
           -FW, "frame_dark", g, step=8, t=2, bevel=0.5)
    for i in range(3):
        yy = 196 + i * 6
        k.b("stop_rib_%d" % i, -FW - 1.8, Y(yy + 2.4), Z(660), -FW - 1.6, Y(yy), Z(710), "slide_light", g)

    g = "trigger"
    k.prof("trigger", P(trig), -3.4, 3.4, "frame_dark", g, step=6, t=2, bevel=0.5)

    g = "magazine"
    mz, my = Z(735), Y(500)
    with k.frame("x", -RAKE, 0, my, mz):
        k.b("mag_body", -10.5, Y(680), mz - 14, 10.5, Y(320), mz + 14, "slide", g)
        k.b("mag_round", -4.5, Y(320), mz - 13, 4.5, Y(300), mz + 11, "brass", g)
    k.prof("mag_base", P([(687, 681), (872, 681), (874, 700), (866, 712), (700, 714), (690, 705)]), -FW - 0.6,
           FW + 0.6, "frame", g, step=10, bevel=1.6)

    m.regroup({}, pivots={"trigger": k.P(0, Y(292), Z(530)), "magazine": k.P(0, my, mz),
                          "slide": k.P(0, Y(148), Z(450)), "barrel": k.P(0, Y(148), Z(300)),
                          "slide_stop": k.P(-12, Y(204), Z(662))})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(480), Z(770))

ARMS = {
    "grip": ((Z(745), Y(310)), (Z(800), Y(660))), "trigger": (Z(523), Y(330)),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.28, "fp": 0.37, "gui": 0.5, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 25 / U, "locks_back": True,
    "followers": {"barrel": {"pos": [0, -0.15, 1.1], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.970, 0.242], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 1.6, "recoil_time": 0.24, "shot_time": 0.25, "cycle_back": 0.035, "cycle_fwd": 0.08,
    "reload_time": 1.6, "reload_empty_time": 2.0,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

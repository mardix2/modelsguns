"""Beretta M9A4 (9x19), all FDE: open-top slide showing the barrel, slanted
front and rear serrations, optic cover plate, ambidextrous decocking levers
on the slide (red dot when ready), spur hammer with a loop, threaded
barrel, dust cover with a rail, Vertec straight backstrap with a beavertail,
checkered grip panels with the Beretta medallion, black controls.

Outlines are measured on a side photo (right side, mirrored and levelled;
2.63 px per mm along the gun, 2.85 px per mm vertically, thread tip at x=36,
bore at y=172); widths from real dimensions (slide 26 mm, 38 mm over the
levers).  1 model unit = 7 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "fde": Material((190, 150, 106), 5),
    "fde_dark": Material((150, 118, 84), 4),
    "fde_light": Material((206, 170, 128), 5),
    "barrel": Material((150, 126, 98), 4),
    "black": Material((32, 32, 35), 3),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "red": Material((220, 40, 36), 2, edge=False),
    "text": Material((190, 150, 106), 4, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


class Sil(Silhouette):
    """photo with different horizontal and vertical scales"""

    def __init__(self, gun, ppm_x, ppm_y, muzzle_x, bore_y):
        super().__init__(gun, ppm_x, muzzle_x, bore_y)
        self.ppm_y = float(ppm_y)

    def mm(self, X, Y):
        return ((X - self.mx) / self.ppm, (self.by - Y) / self.ppm_y)

    def ymm(self, Y):
        return (self.by - Y) / self.ppm_y


U = 7.0
S = Sil("m9a4", 2.63, 2.85, 36, 172)
Z, Y, P = S.zmm, S.ymm, S.poly
SW, FW = 13.0, 11.0
RAKE = 14.0


def circle(cx, cy, r, n=10):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def cuts(k, name, side, xs, y0, y1, slant, w, mat, g):
    """slanted grooves on a slide side: tops lean forward by `slant` deg"""
    x = -SW - 0.2 if side == "l" else SW
    yc = (Y(y0) + Y(y1)) / 2
    for i, px in enumerate(xs):
        zc = Z(px)
        with k.frame("x", slant, 0, yc, zc):
            k.b("%s_%s_%d" % (name, side, i), x, Y(y1), zc - w / 2, x + 0.2, Y(y0), zc + w / 2, mat, g)


def build():
    m = Model("m9a4", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: nose ring, low walls along the open top, full rear section
    # ======================================================================
    g = "slide"
    k.prof("slide_nose", P([(83, 150), (87, 146), (112, 146), (118, 152), (118, 219), (83, 219)]), -SW, SW,
           "fde", g, step=12, bevel=2.4)
    k.prof("slide_walls", P([(118, 180), (385, 180), (385, 219), (118, 219)]), -SW, SW, "fde", g, step=14,
           bevel=1.6)
    k.prof("slide_rear", P([(385, 151), (390, 146), (560, 146), (578, 156), (602, 191), (611, 218), (611, 220),
                            (385, 220)]), -SW, SW, "fde", g, step=14, bevel=2.6)
    for side in ("l", "r"):
        cuts(k, "serr_f", side, [138 + 9.5 * i for i in range(11)], 183, 217, -13, 1.6, "fde_dark", g)
        cuts(k, "serr_r", side, [402 + 9.5 * i for i in range(12)], 183, 217, -13, 1.6, "fde_dark", g)
        x = -SW - 0.15 if side == "l" else SW
        k.b("plate_line_" + side, x, Y(156), Z(388), x + 0.15, Y(154), Z(522), "fde_dark", g)
    k.b("port", SW - 0.9, Y(179), Z(386), SW + 0.05, Y(155), Z(488), "black", g)
    k.b("port_chamber", SW - 0.5, Y(176), Z(392), SW + 0.1, Y(158), Z(482), "barrel", g)
    for i, (a, b) in enumerate(((402, 443), (464, 488))):
        k.b("plate_slot_%d" % i, -4, Y(153), Z(a), 4, Y(146) + 0.05, Z(b), "black", g)
    k.prof("front_sight", P([(85, 147), (87, 133), (92, 130), (114, 130), (116, 147)]), -1.8, 1.8, "black", g,
           step=6, t=2, bevel=0.4)
    k.b("front_dot", -0.9, Y(140), Z(84.6), 0.9, Y(135), Z(85.2), "white", g)
    k.prof("rear_sight", P([(528, 147), (530, 133), (536, 130), (557, 130), (559, 135), (559, 147)]), -6.5, 6.5,
           "black", g, step=6, t=2, bevel=0.5)
    k.b("rear_notch", -1.4, Y(142), Z(526), 1.4, Y(129), Z(561), "bore", g)
    for side, xx in (("l", -5), ("r", 4)):
        k.b("rear_dot_" + side, xx, Y(139), Z(559.2), xx + 1, Y(135), Z(559.6), "white", g)
    # ambidextrous decocking levers with the hub, red "fire" dot
    for side, (a, b) in (("l", (-SW - 2.2, -SW)), ("r", (SW, SW + 2.2))):
        k.prof("decocker_" + side, P([(512, 172), (540, 165), (550, 158), (566, 160), (571, 170), (566, 181),
                                      (552, 184), (515, 184)]), a, b, "black", g, step=8, t=2, bevel=0.5)
        k.prof("decocker_hub_" + side, circle(555, 169, 11), a - 0.4 if side == "l" else a, b if side == "l"
               else b + 0.4, "black", g, step=6, t=2, bevel=0.4)
        x = -SW - 0.15 if side == "l" else SW
        k.b("fire_dot_" + side, x, Y(208), Z(543), x + 0.15, Y(200), Z(551), "red", g)
        k.pin("fpb_" + side, x + (0.1 if side == "l" else 0.05), Y(155), Z(510), 1.4, x, x + 0.15, "black", g)

    # ======================================================================
    # barrel: threaded muzzle, visible along the open top
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_thread", Y(172), Z(37), Z(71), 7.2, "barrel", g, "knurl")
    k.cyl("barrel_crown", Y(172), Z(36.4), Z(37), 6.4, "fde_dark", g)
    k.cyl("muzzle_bore", Y(172), Z(36.2), Z(36.4), 4.6, "bore", g)
    k.cyl("barrel_body", Y(172), Z(71), Z(400), 7.6, "fde", g)
    k.bv("chamber_block", -7.8, Y(180), Z(385), 7.8, Y(152), Z(490), 1.2, "barrel", g)

    # ======================================================================
    # frame: rail dust cover, squared guard, beavertail, grip panels
    # ======================================================================
    g = "frame"
    trig = [(378, 262), (400, 262), (402, 290), (398, 312), (386, 330), (370, 342), (354, 346), (353, 340),
            (370, 328), (380, 312), (384, 292)]
    frame = S.rings([(70, 220), (700, 220), (700, 560), (612, 560), (612, 522), (70, 522)], eps=2.4, smooth=2,
                    min_edge=5, cut=[trig])
    frame = [r for r in frame if len(r) > 5]
    k.prof("frame", frame, -FW, FW, "fde", g, step=14, bevel=2)
    for side, x in (("l", -FW - 0.15), ("r", FW)):
        k.b("frame_mark_" + side, x, Y(240), Z(118), x + 0.15, Y(224), Z(240), "text", g,
            text={"west" if side == "l" else "east": "PIETRO BERETTA\nM9A4 9MM"})
    panel = [(443, 226), (602, 224), (611, 245), (612, 262), (620, 330), (630, 420), (642, 500), (643, 517),
             (515, 520), (505, 431), (487, 354), (470, 280), (452, 240)]
    for side, (a, b) in (("l", (-FW - 2.4, -FW)), ("r", (FW, FW + 2.4))):
        o = a if side == "l" else b
        k.prof("grip_" + side, P(panel), a, b, "fde_light", g, "checker", step=12, bevel=1)
        k.prof("medallion_" + side, circle(555, 385, 21, 12), o - 0.2 if side == "l" else o - 0.3,
               o + 0.3 if side == "l" else o + 0.2, "fde", g, step=8, t=2, bevel=0.2)
        for j, (cx, cy) in enumerate(((528, 299), (574, 470))):
            k.pin("grip_screw_%s_%d" % (side, j), o, Y(cy), Z(cx), 2.4, o - 0.5 if side == "l" else o - 0.2,
                  o + 0.2 if side == "l" else o + 0.5, "black", g)
    # takedown lever and button, magazine release, pins
    for side, (a, b) in (("l", (-FW - 1.6, -FW)), ("r", (FW, FW + 1.6))):
        k.prof("takedown_" + side, circle(318, 229, 11), a, b, "black", g, step=6, t=2, bevel=0.4)
        k.pin("trigger_pin_" + side, (a + b) / 2, Y(262), Z(392), 1.4, a + 0.8 if side == "l" else a,
              b if side == "l" else b - 0.8, "black", g)
    k.prof("takedown_button", P([(292, 252), (312, 249), (320, 254), (318, 262), (296, 263), (289, 258)]), FW,
           FW + 0.8, "black", g, step=6, t=2, bevel=0.3)
    k.prof("mag_release", circle(468, 340, 15), -FW - 1.8, FW + 1.8, "black", g, step=6, t=3, bevel=0.6)

    g = "slide_stop"
    k.prof("slide_stop", P([(373, 236), (390, 226), (433, 224), (433, 240), (410, 244), (395, 253), (378, 252)]),
           -FW - 1.6, -FW, "black", g, step=8, t=2, bevel=0.5)

    g = "trigger"
    k.prof("trigger", P(trig), -3.5, 3.5, "black", g, step=6, t=2, bevel=0.5)

    g = "hammer"
    ham = P([(578, 170), (588, 154), (604, 148), (617, 153), (621, 165), (612, 178), (600, 190), (584, 190)])
    k.prof("hammer", ham, -4, 4, "black", g, step=6, t=3, bevel=0.6)
    k.cylx("hammer_ring", -4.1, 4.1, Y(163), Z(606), 1.4, "fde_dark", g)

    g = "magazine"
    mz, my = Z(540), Y(400)
    with k.frame("x", -RAKE, 0, my, mz):
        k.b("mag_body", -10, Y(522), mz - 15, 10, Y(262), mz + 15, "black", g)
        k.b("mag_round", -4.5, Y(262), mz - 14, 4.5, Y(245), mz + 12, "brass", g)
    k.prof("mag_base", P([(496, 522), (612, 522), (618, 530), (615, 542), (500, 542), (494, 535)]), -FW - 0.4,
           FW + 0.4, "black", g, step=10, bevel=1.4)

    m.regroup({}, pivots={"trigger": k.P(0, Y(268), Z(390)), "magazine": k.P(0, my, mz),
                          "slide": k.P(0, Y(172), Z(350)), "barrel": k.P(0, Y(172), Z(200)),
                          "slide_stop": k.P(-12, Y(238), Z(400)), "hammer": k.P(0, Y(185), Z(590))})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(390), Z(540))

ARMS = {
    "grip": ((Z(530), Y(270)), (Z(575), Y(515))), "trigger": (Z(380), Y(300)),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.27, "fp": 0.35, "gui": 0.48, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 28 / U, "locks_back": True, "hammer": 34,
    # the falling locking block: the barrel only moves straight back a little
    "followers": {"barrel": {"pos": [0, 0, 1.2]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.970, 0.242], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 1.7, "recoil_time": 0.25, "shot_time": 0.26, "cycle_back": 0.035, "cycle_fwd": 0.08,
    "reload_time": 1.6, "reload_empty_time": 2.0,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

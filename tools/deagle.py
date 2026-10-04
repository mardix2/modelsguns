"""Desert Eagle Mark XIX (.50 AE): polished stainless, black serration
panels, ambidextrous safety, G10 grips.

Outlines are measured on a side photo (3.64 px per mm, muzzle at x=21, bore
at y=100); widths from real dimensions (slide 32 mm).  1 model unit = 7 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "ss": Material((196, 199, 205), 3),
    "ss_dark": Material((140, 143, 150), 3),
    "ss_deep": Material((92, 94, 100), 3),
    "black": Material((30, 30, 33), 3),
    "g10": Material((92, 90, 72), 5),
    "g10_dark": Material((62, 60, 48), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((236, 236, 228), 2, edge=False),
    "red": Material((184, 34, 30), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
S = Silhouette("deagle", 3.64, 21, 100)
Z, Y, P = S.zmm, S.ymm, S.poly


def circle(cx, cy, r, n=12):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def build():
    m = Model("deagle", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # fixed barrel: big flat-sided block, ventilated top rib, front sight
    # ======================================================================
    g = "barrel"
    barrel = P([(21, 60), (585, 60), (585, 187), (70, 187), (45, 181), (29, 166), (22, 142)])
    k.prof("barrel", barrel, -15, 15, "ss", g, "brushed", step=14, bevel=3)
    k.edge("barrel_top_l", "z", Z(22), Z(585), -15, Y(60), -1, 1, 6, "ss", g)
    k.edge("barrel_top_r", "z", Z(22), Z(585), 15, Y(60), 1, 1, 6, "ss", g)
    k.b("barrel_mark_l", -15.2, Y(160), Z(250), -15, Y(140), Z(470), "ss", g,
        text={"west": "DESERT EAGLE PISTOL"})
    k.b("barrel_mark_r", 15, Y(160), Z(40), 15.2, Y(140), Z(110), "ss", g, text={"east": "50AE"})
    for side, x in (("l", -15.3), ("r", 15)):
        k.b("barrel_groove_" + side, x, Y(186), Z(125), x + 0.3, Y(112), Z(127), "ss_deep", g)
        k.b("barrel_flat_" + side, x, Y(122), Z(127), x + 0.3, Y(112), Z(300), "ss_deep", g)
    k.cyl("muzzle_crown", 0, Z(20.6), Z(21.3), 9.5, "ss_dark", g)
    k.cyl("muzzle_bore", 0, Z(20.4), Z(20.6), 6.4, "bore", g)
    # ventilated rib: rail with windows
    k.bv("rib", -5, Y(60), Z(23), 5, Y(52), Z(585), 0.8, "ss", g, "brushed")
    for i, x in enumerate((135, 172, 210, 248, 288, 325, 362, 402, 440, 478, 516, 552)):
        k.b("rib_slot_%02d" % i, -5.2, Y(59), Z(x - 8), 5.2, Y(54.5), Z(x + 8), "ss_deep", g)
    k.prof("front_sight", P([(45, 53), (50, 32), (62, 25), (86, 34), (90, 53)]), -3, 3, "black", g,
           step=8, bevel=0.8)

    # ======================================================================
    # slide: black serration panel with slanted ridges, safety, rear sight
    # ======================================================================
    g = "slide"
    slide = P([(585, 44), (800, 44), (845, 48), (868, 68), (888, 105), (900, 150), (905, 186), (585, 186)])
    k.prof("slide", slide, -16, 16, "ss", g, "brushed", step=14, bevel=3)
    k.edge("slide_top_l", "z", Z(585), Z(850), -16, Y(44), -1, 1, 5, "ss", g)
    k.edge("slide_top_r", "z", Z(585), Z(850), 16, Y(44), 1, 1, 5, "ss", g)
    panel = P([(602, 80), (730, 80), (760, 128), (880, 128), (885, 184), (632, 184)])
    for side, (a, b) in (("l", (-16.4, -16)), ("r", (16, 16.4))):
        k.prof("serr_panel_" + side, panel, a, b, "black", g, step=12, t=3, bevel=0.1)
        for i in range(13):
            x0 = 612 + i * 20
            top = 82 if x0 < 735 else 130
            with k.frame("x", 16, 0, Y(184), Z(x0 + 30)):
                k.b("serr_ridge_%s_%02d" % (side, i), a - 0.25 if side == "l" else b - 0.15, Y(184),
                    Z(x0 + 30) - 0.7, a + 0.15 if side == "l" else b + 0.25, Y(top + 3), Z(x0 + 30) + 0.7,
                    "ss", g)
    k.b("ejection_port", 16, Y(100), Z(600), 16.2, Y(60), Z(700), "bore", g)
    k.cyl("bolt_face", Y(80), Z(612), Z(690), 6.2, "ss_dark", g, x=12)
    k.prof("rear_sight", P([(800, 46), (804, 30), (840, 27), (846, 46)]), -8, 8, "black", g, step=8, bevel=1)
    k.b("rear_notch", -2, Y(40), Z(803), 2, Y(26), Z(843), "bore", g)
    k.b("rear_dot_l", -6, Y(38), Z(846), -4, Y(34), Z(846.6), "white", g)
    k.b("rear_dot_r", 4, Y(38), Z(846), 6, Y(34), Z(846.6), "white", g)
    # ambidextrous safety: hub and lever with red dot
    for side, (a, b) in (("l", (-18.5, -16)), ("r", (16, 18.5))):
        lever = P([(740, 72), (800, 66), (836, 76), (842, 104), (818, 124), (790, 116), (746, 94)])
        k.prof("safety_" + side, lever, a, b, "black", g, step=8, t=3, bevel=0.6)
        hub = circle(822, 93, 13, 10)
        k.prof("safety_hub_" + side, hub, a - 0.6 if side == "l" else b - 0.2,
               a + 0.2 if side == "l" else b + 0.6, "black", g, step=6, t=3, bevel=0.6)
        k.b("safety_red_" + side, a - 0.1 if side == "l" else b, Y(124), Z(772), a if side == "l" else b + 0.1,
            Y(116), Z(780), "red", g)

    # ======================================================================
    # frame: dust cover, trigger guard, grip frame, beavertail
    # ======================================================================
    g = "frame"
    frame = [P([(70, 186), (585, 186), (905, 186), (960, 192), (1003, 205), (1005, 214), (985, 220),
                (940, 214), (897, 217), (875, 232), (864, 265), (868, 300), (891, 361), (922, 436),
                (940, 500), (948, 566), (714, 566), (697, 442), (685, 386), (666, 361), (660, 341),
                (640, 342), (510, 342), (495, 337), (487, 322), (485, 230), (470, 213), (440, 202),
                (100, 200), (75, 196)]),
             P([(507, 233), (660, 233), (660, 327), (515, 327), (507, 318)])]
    k.prof("frame", frame, -14, 14, "ss", g, "brushed", step=14, bevel=3)
    k.b("frame_line_l", -14.3, Y(201), Z(100), -14, Y(199), Z(480), "ss_deep", g)
    k.b("frame_line_r", 14, Y(201), Z(100), 14.3, Y(199), Z(480), "ss_deep", g)
    # barrel release (two discs, left), slide stop, magazine release, pins
    for i, (cx, cy) in enumerate(((495, 201), (497, 231))):
        k.prof("barrel_release_%d" % i, circle(cx, cy, 12, 10), -15.6, -14, "black", g, step=6, t=3,
               bevel=0.5)
    k.prof("slide_stop", P([(612, 202), (760, 202), (764, 214), (760, 221), (612, 221)]),
           -15.6, -14, "black", g, step=10, t=3, bevel=0.5)
    k.prof("slide_stop_pad", circle(624, 211, 13, 10), -16.6, -14, "black", g, "knurl", step=6, t=3,
           bevel=0.6)
    k.prof("mag_release", circle(653, 312, 12, 10), -15.4, -14, "black", g, step=6, t=3, bevel=0.6)
    for side, (a, b) in (("l", (-14.6, -14)), ("r", (14, 14.6))):
        k.pin("pin_a_" + side, (a + b) / 2, Y(207), Z(800), 1.6, a, b, "ss_dark", g)
        k.pin("pin_b_" + side, (a + b) / 2, Y(207), Z(880), 1.6, a, b, "ss_dark", g)

    g = "grip"
    panel = P([(682, 238), (702, 207), (828, 210), (860, 290), (890, 360), (924, 455), (936, 560),
               (720, 560), (702, 440), (690, 380)])
    for side, (a, b) in (("l", (-17.5, -14.2)), ("r", (14.2, 17.5))):
        k.prof("grip_" + side, panel, a, b, "g10", g, "stipple", step=12, bevel=1.4)
        for i, x in enumerate((700, 712, 724)):
            k.b("grip_groove_%s_%d" % (side, i), a - 0.1 if side == "l" else b - 0.2, Y(540), Z(x + 6),
                a + 0.2 if side == "l" else b + 0.1, Y(250), Z(x + 8), "g10_dark", g)
        k.pin("grip_screw_" + side, a if side == "l" else b, Y(392), Z(800), 3, a - 0.4 if side == "l" else b - 0.2,
              a + 0.2 if side == "l" else b + 0.4, "ss_dark", g)

    g = "trigger"
    trig = P([(600, 233), (626, 233), (645, 258), (651, 298), (642, 324), (632, 324), (630, 296),
              (618, 263), (602, 246)])
    k.prof("trigger", trig, -4, 4, "black", g, step=6, t=3, bevel=0.8)

    g = "hammer"
    ham = P([(885, 82), (900, 76), (928, 78), (946, 90), (942, 108), (928, 128), (906, 134), (890, 120)])
    k.prof("hammer", ham, -5, 5, "black", g, "knurl", step=8, t=4, bevel=1)
    for i in range(5):
        x = 902 + i * 8
        k.b("hammer_tooth_%d" % i, -5, Y(78), Z(x), 5, Y(73), Z(x + 4), "black", g)

    g = "magazine"
    k.bv("mag_body", -11, Y(560), Z(760), 11, Y(230), Z(880), 1.5, "ss_deep", g)
    k.b("mag_round", -6.5, Y(240), Z(770), 6.5, Y(222), Z(870), "brass", g)
    base = P([(712, 566), (952, 566), (956, 580), (716, 582)])
    k.prof("mag_base", base, -16, 16, "ss", g, "brushed", step=12, bevel=2)

    m.regroup({}, pivots={"trigger": k.P(0, Y(240), Z(613)), "hammer": k.P(0, Y(125), Z(900)),
                          "magazine": k.P(0, Y(400), Z(820)), "slide": k.P(0, Y(100), Z(745))})
    m.dynamic = {"slide", "trigger", "hammer", "magazine"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(400), Z(810))


ARMS = {
    "grip": ((Z(777), Y(240)), (Z(831), Y(520))), "grip_w": 17.5, "grip_d": 25,
    "trigger": (Z(640), Y(300)),
    "left": {"kind": "support"}, "right_dir": (14, 8), "left_dir": (16, -20),
}

DISPLAY = {"hand": 0.24, "fp": 0.31, "gui": 0.4, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 40 / U, "locks_back": True, "hammer": 35,
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.956, 0.292], "mag_far": 24, "mag_gap": 0.45,
    "recoil": 2.8, "recoil_time": 0.34, "shot_time": 0.36, "cycle_back": 0.045, "cycle_fwd": 0.1,
    "reload_time": 1.8, "reload_empty_time": 2.2,
    "reload_tilt": [12, 18, -30], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

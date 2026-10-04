"""Colt M1911A1 (.45 ACP): blued steel, barrel bushing and recoil spring
plug, rear slide serrations, spur hammer, grip safety, thumb safety, arched
mainspring housing, checkered walnut grips with double diamonds.

Designed in mm from the real dimensions (216 mm long, 127 mm barrel,
135 mm high, slide 23 mm wide, 18 deg grip).  1 model unit = 7 mm.
Muzzle at z=0 pointing -Z, bore at y=0.
"""

import math

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "blue": Material((46, 48, 56), 4),
    "blue_dark": Material((28, 29, 34), 3),
    "blue_light": Material((92, 95, 106), 4),
    "wood": Material((112, 56, 26), 5),
    "wood_dark": Material((74, 36, 16), 4),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "text": Material((46, 48, 56), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
TOP, SB = 12.0, -13.0       # slide top / bottom (mm from the bore)
RAKE = 18.0


def circle(cx, cy, r, n=10):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def build():
    m = Model("m1911", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: plain sides, rear serrations, fixed GI sights
    # ======================================================================
    g = "slide"
    slide = [(1, -9), (1, 9), (3, TOP), (208, TOP), (210, 9), (210, SB), (1, SB)]
    k.prof("slide", slide, -11.7, 11.7, "blue", g, step=12, bevel=2.2)
    for side, x in (("l", -11.9), ("r", 11.7)):
        for i in range(11):
            z = 180 + i * 2.6
            k.b("serr_%s_%02d" % (side, i), x, SB + 2, z, x + 0.2, TOP - 2, z + 1.2, "blue_dark", g)
    k.b("slide_mark", -11.85, -4, 60, -11.7, 3, 150, "text", g, text={"west": "COLT M1911 A1 US ARMY"})
    k.b("ejection_port", 9, 1, 92, 11.9, TOP + 0.1, 130, "bore", g)
    k.b("extractor", 11.7, 3, 130, 12.2, 7, 160, "blue_dark", g)
    k.bv("front_sight", -1.4, TOP - 0.4, 8, 1.4, TOP + 5, 13, 0.4, "blue_dark", g, axis="y")
    k.prof("rear_sight", [(194, TOP), (196, TOP + 4.5), (206, TOP + 4.5), (207, TOP)], -6, 6, "blue_dark", g,
           step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.3, TOP + 2, 195.5, 1.3, TOP + 4.6, 206.5, "bore", g)
    k.b("slide_stop_notch", -11.9, SB, 120, -11.7, SB + 4, 132, "blue_dark", g)

    # ======================================================================
    # barrel: bushing, crown, hood in the ejection port
    # ======================================================================
    g = "barrel"
    k.cyl("bushing", 0, -1.2, 1.5, 9.6, "blue", g)
    k.cyl("barrel_crown", 0, -1.6, 0, 7.4, "blue_light", g)
    k.cyl("muzzle_bore", 0, -1.8, -1.6, 5.8, "bore", g)
    k.cyl("barrel_body", 0, 0, 128, 7.4, "blue_light", g)
    k.b("hood_top", 1, TOP - 0.6, 94, 11.4, TOP + 0.08, 128, "blue_light", g)

    # ======================================================================
    # frame: short dust cover, round trigger guard, grip, grip safety
    # ======================================================================
    g = "frame"
    k.cyl("spring_plug", -19, -1.2, 9, 5.6, "blue", g)
    frame = [(9, SB), (205, SB), (215, -16), (214, -21), (204, -23), (191, -28), (185, -38),
             (188, -60), (194, -85), (196, -103), (194, -110), (137, -110), (133, -100), (125, -75),
             (116, -50), (110, -36), (106, -32), (103, -36), (102, -46), (96, -51), (72, -51), (65, -47),
             (63, -36), (64, -26), (12, -25), (9, -21)]
    hole = [(70, -26), (102, -26), (102, -30), (99, -33), (98, -44), (94, -47), (73, -47), (68, -42), (68, -32)]
    k.prof("frame", [frame, hole], -11, 11, "blue", g, step=10, bevel=2)
    k.b("frame_mark", -11.15, -22, 20, -11, -16, 55, "text", g, text={"west": "US"})
    # mainspring housing (arched, finely checkered) and lanyard loop
    k.prof("mainspring_housing", [(185, -60), (188, -60), (194, -85), (196, -103), (194, -108), (189, -108),
                                  (190, -85), (186, -64)], -9.5, 9.5, "blue_dark", g, "checker", step=6, t=3, bevel=0.8)
    k.cylx("lanyard_loop", -3, 3, -106, 192, 3, "blue_dark", g)
    # grip safety tang
    k.prof("grip_safety", [(198, -16), (214, -17), (215, -21), (204, -23), (192, -28), (186, -36), (184, -30)],
           -9.8, 9.8, "blue_light", g, step=6, t=3, bevel=1)
    # walnut grips: checkered with smooth diamonds around the screws
    grip = [(119, -37), (181, -37), (185, -58), (190, -84), (191, -100), (139, -102), (131, -80), (124, -58)]
    for side, (a, b) in (("l", (-13.2, -11)), ("r", (11, 13.2))):
        k.prof("grip_" + side, grip, a, b, "wood", g, "checker", step=10, t=4, bevel=1)
        o = a - 0.05 if side == "l" else b - 0.15
        for j, (sz, sy) in enumerate(((150, -45), (163, -93))):
            dia = [(sz - 8, sy), (sz, sy + 6), (sz + 8, sy), (sz, sy - 6)]
            k.prof("diamond_%s_%d" % (side, j), dia, o, o + 0.2, "wood_dark", g, step=6, t=2, bevel=0.1)
            k.pin("grip_screw_%s_%d" % (side, j), o + (0 if side == "l" else 0.2), sy, sz, 2.6,
                  o - 0.5 if side == "l" else o, o if side == "l" else o + 0.7, "blue_light", g)
    # thumb safety (left), magazine catch, pins
    k.prof("thumb_safety", [(178, -16), (196, -16), (198, -22), (186, -24), (176, -21)], -13, -11, "blue", g,
           step=6, t=2, bevel=0.5)
    k.prof("safety_paddle", [(168, -15), (180, -15), (180, -19), (168, -19)], -14.5, -11, "blue", g, "knurl",
           step=6, t=2, bevel=0.5)
    k.pin("mag_catch", -11.6, -32, 114, 3.4, -12.6, -11, "blue_dark", g)
    for side, (a, b) in (("l", (-11.6, -11)), ("r", (11, 11.6))):
        k.pin("sear_pin_" + side, (a + b) / 2, -19, 186, 1.6, a, b, "blue_light", g)
        k.pin("hammer_pin_" + side, (a + b) / 2, -13.5, 200, 1.6, a, b, "blue_light", g)

    g = "slide_stop"
    k.prof("slide_stop", [(112, -14), (140, -14), (145, -13.5), (152, -13.5), (152, -17), (146, -20), (112, -21)],
           -13, -11, "blue", g, "knurl", step=6, t=2, bevel=0.5)
    k.pin("slide_stop_pin", -12, -18.5, 114, 2.6, -13.4, -11, "blue_light", g)

    g = "trigger"
    k.prof("trigger_bow", [(85, -26), (92, -26), (92, -40), (89, -42), (85, -40)], -4, 4, "blue_light", g,
           "serration", step=4, t=2, bevel=0.5)

    g = "hammer"
    ham = [(201, -16), (207, -18), (210, -8), (215, -2), (221, 1), (220, 5), (212, 4), (205, 0), (201, -7)]
    k.prof("hammer", ham, -4, 4, "blue", g, "knurl", step=6, t=3, bevel=0.6)

    # ======================================================================
    # magazine: tube in the grip, steel base
    # ======================================================================
    g = "magazine"
    with k.frame("x", -RAKE, 0, -65, 160):
        k.b("mag_body", -10, -111, 138, 10, -30, 178, "blue_dark", g)
        k.b("mag_round", -5, -30, 141, 5, -24, 172, "brass", g)
    k.prof("mag_base", [(137, -110), (194, -110), (194, -114), (138, -114)], -10.5, 10.5, "blue_dark", g,
           step=8, t=3, bevel=1)

    m.regroup({}, pivots={"trigger": k.P(0, -34, 89), "magazine": k.P(0, -65, 160),
                          "slide": k.P(0, 0, 100), "barrel": k.P(0, 0, 60),
                          "slide_stop": k.P(-12, -18.5, 114), "hammer": k.P(0, -13.5, 200)})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, -68, 158)

ARMS = {
    "grip": ((143, -32), (165, -106)), "trigger": (89, -34),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.27, "fp": 0.35, "gui": 0.48, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 26 / U, "locks_back": True, "hammer": 32,
    "followers": {"barrel": {"pos": [0, -0.2, 1.0], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [8, 0, 0]},
    "trigger_slide": 3 / U,
    "mag_dir": [0, -0.951, 0.309], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 2.0, "recoil_time": 0.28, "shot_time": 0.3, "cycle_back": 0.04, "cycle_fwd": 0.09,
    "reload_time": 1.7, "reload_empty_time": 2.1,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

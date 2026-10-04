"""Beretta M9A4 (9x19): open-top slide showing the barrel, slide-mounted
ambidextrous safety/decocker levers, exposed hammer, takedown lever, Vertec
straight backstrap, dust cover with accessory rail, squared trigger guard.

Designed in mm from the real dimensions (217 mm long, 125 mm barrel,
140 mm high, 38 mm wide).  1 model unit = 7 mm.  Muzzle at z=0 (-Z),
bore at y=0.
"""

import math

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "slide": Material((40, 41, 45), 4),
    "slide_dark": Material((24, 25, 28), 3),
    "frame": Material((44, 45, 48), 4),
    "barrel": Material((112, 114, 120), 5),
    "steel": Material((80, 82, 88), 4),
    "grip": Material((36, 36, 38), 5),
    "grip_dark": Material((24, 24, 26), 4),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "text": Material((40, 41, 45), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
TOP, SB = 12.5, -13.0
WALL = 3.5          # top of the slide walls along the open section (barrel shows above)
RAKE = 15.0


def build():
    m = Model("m9a4", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: nose ring, open-top walls, full rear section
    # ======================================================================
    g = "slide"
    nose = [(6, -6), (8, 9), (32, 9), (32, SB), (6, SB)]
    k.prof("slide_nose", nose, -12.5, 12.5, "slide", g, step=10, bevel=2.4)
    wall = [(32, SB), (32, WALL), (118, WALL), (122, TOP), (118, SB)]
    for side, (a, b) in (("l", (-12.5, -7.6)), ("r", (7.6, 12.5))):
        k.prof("slide_wall_" + side, wall, a, b, "slide", g, step=12, t=4, bevel=1.6)
    k.b("slide_floor", -7.6, SB, 32, 7.6, -8, 118, "slide_dark", g)
    rear = [(118, SB), (118, WALL), (124, TOP), (215, TOP), (217, 9), (217, SB)]
    k.prof("slide_rear", rear, -12.5, 12.5, "slide", g, step=12, bevel=2.4)
    for side, x in (("l", -12.7), ("r", 12.5)):
        for i in range(9):
            z = 184 + i * 3.4
            k.b("serr_%s_%d" % (side, i), x, SB + 2.5, z, x + 0.2, TOP - 3, z + 1.6, "slide_dark", g)
    k.b("slide_mark", -12.65, -5, 40, -12.5, 2, 112, "text", g, text={"west": "P.BERETTA M9A4"})
    k.b("ejection_port", 9, 2, 100, 12.7, WALL + 0.1, 128, "bore", g)
    k.bv("front_sight", -1.6, 8.5, 12, 1.6, 15.5, 20, 0.4, "slide_dark", g, axis="y")
    k.b("front_dot", -0.8, 12.5, 11.9, 0.8, 14, 12, "white", g)
    k.prof("rear_sight", [(198, TOP), (200, TOP + 5), (211, TOP + 5), (212, TOP)], -7, 7, "slide_dark", g,
           step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.4, TOP + 2.5, 199.5, 1.4, TOP + 5.1, 211.5, "bore", g)
    # ambidextrous safety / decocker levers on the slide
    for side, (a, b) in (("l", (-14.5, -12.5)), ("r", (12.5, 14.5))):
        k.prof("safety_" + side, [(186, 5), (204, 3), (208, 7), (206, 11), (190, 11)], a, b, "slide_dark", g,
               "knurl", step=6, t=2, bevel=0.5)
        k.pin("safety_hub_" + side, a if side == "l" else b, 7, 200, 3, a - 0.4 if side == "l" else b - 0.2,
              a + 0.2 if side == "l" else b + 0.4, "steel", g)

    # ======================================================================
    # barrel: protrudes past the nose, visible along the open top
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_body", 0, -5, 120, 7.2, "barrel", g)
    k.cyl("barrel_crown", 0, -5.4, -5, 6.2, "steel", g)
    k.cyl("muzzle_bore", 0, -5.6, -5.4, 4.6, "bore", g)
    k.bv("chamber_block", -7.4, -6, 100, 7.4, WALL - 0.2, 128, 1.2, "barrel", g)

    # ======================================================================
    # frame: rail dust cover, squared guard, straight backstrap, grips
    # ======================================================================
    g = "frame"
    frame = [(16, SB), (206, SB), (213, -16), (211, -22), (197, -26), (187, -34), (186, -60), (190, -90),
             (193, -108), (192, -114), (132, -114), (129, -104), (124, -80), (118, -56), (112, -40), (105, -35),
             (100, -38), (97, -48), (92, -52), (58, -52), (53, -49), (52, -40), (50, -29), (20, -27), (16, -23)]
    hole = [(58, -28), (97, -28), (97, -31), (94, -34), (93, -46), (90, -48), (60, -48), (57, -45)]
    k.prof("frame", [frame, hole], -11, 11, "frame", g, step=10, bevel=2)
    for side, (a, b) in (("l", (-11.4, -10.2)), ("r", (10.2, 11.4))):
        k.b("rail_groove_" + side, a if side == "l" else b - 0.2, -25.5, 20, a + 0.2 if side == "l" else b, -23.5,
            50, "slide_dark", g)
    for i in range(2):
        k.b("rail_slot_%d" % i, -9, -27.2, 26 + i * 12, 9, -26.9, 32 + i * 12, "slide_dark", g)
    k.b("guard_hook", -4, -53, 52, 4, -50, 56, "frame", g)
    grip = [(119, -40), (182, -40), (182, -60), (186, -90), (189, -106), (134, -108), (128, -86), (122, -60)]
    for side, (a, b) in (("l", (-13, -11)), ("r", (11, 13))):
        k.prof("grip_" + side, grip, a, b, "grip", g, "stipple", step=10, t=4, bevel=1)
        o = a if side == "l" else b
        for j, (sz, sy) in enumerate(((152, -48), (164, -98))):
            k.pin("grip_screw_%s_%d" % (side, j), o, sy, sz, 2.4, o - 0.5 if side == "l" else o - 0.2,
                  o + 0.2 if side == "l" else o + 0.5, "steel", g)
        k.b("logo_" + side, o - 0.1, -76, 138, o + 0.1, -68, 172, "text", g,
            text={"west" if side == "l" else "east": "BERETTA"})
    # takedown lever (left), magazine release, pins
    k.prof("takedown", [(64, -15), (78, -15), (80, -21), (64, -21)], -12.6, -11, "slide_dark", g, step=6, t=2,
           bevel=0.5)
    k.pin("mag_release", -11.4, -34, 110, 3.4, -12.6, -11, "slide_dark", g)
    for side, (a, b) in (("l", (-11.6, -11)), ("r", (11, 11.6))):
        k.pin("trigger_pin_" + side, (a + b) / 2, -20, 98, 1.4, a, b, "steel", g)
        k.pin("hammer_pin_" + side, (a + b) / 2, -16, 198, 1.6, a, b, "steel", g)

    g = "slide_stop"
    k.prof("slide_stop", [(108, -14), (136, -14), (140, -16), (136, -19), (108, -19)], -12.8, -11, "slide_dark",
           g, "knurl", step=6, t=2, bevel=0.5)

    g = "trigger"
    trig = [(74, -28), (80, -28), (83, -34), (83, -42), (79, -46), (75, -46), (77, -41), (77, -34)]
    k.prof("trigger", trig, -3.5, 3.5, "slide_dark", g, step=4, t=2, bevel=0.5)

    g = "hammer"
    ham = [(198, -18), (205, -19), (208, -8), (213, -2), (219, 2), (216, 7), (208, 4), (201, -2), (198, -9)]
    k.prof("hammer", ham, -4, 4, "slide_dark", g, "knurl", step=6, t=3, bevel=0.6)
    k.cylx("hammer_ring", -4.2, 4.2, 2, 213, 3, "bore", g)

    g = "magazine"
    with k.frame("x", -RAKE, 0, -66, 160):
        k.b("mag_body", -10, -115, 136, 10, -30, 172, "steel", g)
        k.b("mag_round", -4.5, -30, 141, 4.5, -24, 170, "brass", g)
    k.prof("mag_base", [(131, -114), (192, -114), (193, -119), (133, -120)], -12, 12, "frame", g, step=8, t=3,
           bevel=1)

    m.regroup({}, pivots={"trigger": k.P(0, -30, 78), "magazine": k.P(0, -66, 160),
                          "slide": k.P(0, 0, 110), "barrel": k.P(0, 0, 60),
                          "slide_stop": k.P(-12, -16, 110), "hammer": k.P(0, -16, 198)})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, -68, 155)

ARMS = {
    "grip": ((146, -34), (162, -108)), "trigger": (80, -36),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.27, "fp": 0.35, "gui": 0.48, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 28 / U, "locks_back": True, "hammer": 34,
    # the falling locking block: the barrel only moves straight back a little
    "followers": {"barrel": {"pos": [0, 0, 1.2]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.966, 0.259], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 1.7, "recoil_time": 0.25, "shot_time": 0.26, "cycle_back": 0.035, "cycle_fwd": 0.08,
    "reload_time": 1.6, "reload_empty_time": 2.0,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

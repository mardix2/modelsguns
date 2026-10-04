"""SIG Sauer P320 (M17 style, 9x19): black slide with front and rear
serrations and a deep top chamfer, coyote polymer grip module with rail and
textured grip, striker fired (no hammer), takedown lever, flared magwell.

Designed in mm from the real dimensions (203 mm long, 120 mm barrel,
140 mm high, 35 mm wide).  1 model unit = 7 mm.  Muzzle at z=0 (-Z),
bore at y=0.
"""

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "slide": Material((34, 35, 38), 4),
    "slide_dark": Material((20, 21, 23), 3),
    "coyote": Material((150, 126, 92), 6),
    "coyote_dark": Material((112, 92, 66), 5),
    "barrel": Material((110, 104, 92), 5),
    "steel": Material((76, 78, 84), 4),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "green": Material((90, 220, 120), 2, edge=False),
    "text": Material((34, 35, 38), 3, edge=False),
    "text_c": Material((150, 126, 92), 4, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
TOP, SB = 13.0, -13.5
RAKE = 18.0


def build():
    m = Model("p320", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: bevelled nose, deep top chamfers, serrations front and rear
    # ======================================================================
    g = "slide"
    slide = [(0, 3), (6, TOP), (193, TOP), (197, 9), (197, SB), (2, SB), (0, -8)]
    k.prof("slide", slide, -12.5, 12.5, "slide", g, step=12, bevel=4.2)
    for side, x in (("l", -12.7), ("r", 12.5)):
        for i in range(5):
            z = 10 + i * 4.4
            k.b("serr_f_%s_%d" % (side, i), x, SB + 3, z, x + 0.2, TOP - 4.5, z + 2, "slide_dark", g)
        for i in range(8):
            z = 158 + i * 4.4
            k.b("serr_r_%s_%d" % (side, i), x, SB + 3, z, x + 0.2, TOP - 4.5, z + 2, "slide_dark", g)
    k.b("slide_mark", -12.65, -6, 60, -12.5, 0, 140, "text", g, text={"west": "SIG SAUER P320"})
    k.b("ejection_port", 9, 1.5, 70, 12.7, TOP + 0.1, 118, "bore", g)
    k.b("extractor", 12.5, 2, 118, 13, 6, 136, "slide_dark", g)
    k.cyl("nose_ring", 0, -0.5, 0.2, 8.4, "slide_dark", g)
    k.bv("front_sight", -1.8, TOP - 0.5, 6, 1.8, TOP + 5, 13, 0.4, "slide_dark", g, axis="y")
    k.b("front_dot", -0.9, TOP + 2.5, 5.9, 0.9, TOP + 4, 6, "green", g)
    k.prof("rear_sight", [(178, TOP), (180, TOP + 5.5), (192, TOP + 6), (193, TOP)], -7.5, 7.5, "slide_dark", g,
           step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.5, TOP + 2.5, 179.5, 1.5, TOP + 6.2, 192.5, "bore", g)
    for side, xx in (("l", -5), ("r", 4)):
        k.b("rear_dot_" + side, xx, TOP + 3, 193, xx + 1, TOP + 4.2, 193.1, "green", g)
    k.bv("rear_plate", -8, SB + 3, 197, 8, TOP - 4, 198.2, 1, "slide_dark", g)

    # ======================================================================
    # barrel: crown in the nose, hood in the ejection port
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_crown", 0, -0.7, 2, 7, "barrel", g)
    k.cyl("muzzle_bore", 0, -0.9, -0.7, 4.6, "bore", g)
    k.cyl("barrel_body", 0, 2, 118, 7, "barrel", g)
    k.b("hood_top", 1, TOP - 0.6, 72, 12.6, TOP + 0.08, 116, "barrel", g)

    # ======================================================================
    # grip module: rail, squared guard with undercut, textured grip, magwell
    # ======================================================================
    g = "frame"
    frame = [(8, SB), (188, SB), (197, -16), (196, -22), (185, -27), (177, -33), (178, -48), (184, -72),
             (190, -96), (194, -108), (194, -113), (130, -113), (126, -102), (118, -80), (110, -58), (104, -40),
             (101, -34), (97, -37), (97, -48), (92, -52), (58, -52), (52, -49), (51, -40), (50, -27), (12, -27),
             (8, -23)]
    hole = [(57, -28), (97, -28), (97, -31), (94, -34), (93, -46), (90, -48), (59, -48), (56, -45)]
    k.prof("frame", [frame, hole], -11.5, 11.5, "coyote", g, step=10, bevel=2.2)
    for side, (a, b) in (("l", (-11.9, -10.6)), ("r", (10.6, 11.9))):
        k.b("rail_groove_" + side, a if side == "l" else b - 0.2, -25, 14, a + 0.2 if side == "l" else b, -23,
            48, "coyote_dark", g)
    for i in range(3):
        k.b("rail_slot_%d" % i, -9.5, -27.2, 16 + i * 10, 9.5, -26.9, 21 + i * 10, "coyote_dark", g)
    texture = [(110, -40), (172, -40), (178, -62), (184, -86), (188, -102), (132, -104), (124, -84), (116, -60)]
    for side, (a, b) in (("l", (-11.8, -11.5)), ("r", (11.5, 11.8))):
        k.prof("grip_texture_" + side, texture, a, b, "coyote_dark", g, "stipple", step=10, t=2, bevel=0.1)
        k.b("sig_logo_" + side, a - 0.05 if side == "l" else b - 0.2, -50, 136, a + 0.2 if side == "l" else b + 0.05,
            -44, 162, "text_c", g, text={"west" if side == "l" else "east": "SIG"})
    k.prof("magwell", [(126, -104), (195, -101), (196, -111), (129, -114)], -12.5, 12.5, "coyote", g, step=8,
           t=3, bevel=1)
    k.prof("takedown", [(68, -15), (84, -15), (86, -21), (68, -21)], -13, -11.5, "slide_dark", g, step=6, t=2,
           bevel=0.5)
    k.pin("mag_release", -11.8, -38, 108, 3.6, -13, -11.5, "slide_dark", g)
    for side, (a, b) in (("l", (-12.1, -11.5)), ("r", (11.5, 12.1))):
        k.pin("module_pin_" + side, (a + b) / 2, -20, 96, 1.4, a, b, "steel", g)

    g = "slide_stop"
    k.prof("slide_stop", [(102, -14), (128, -14), (132, -16), (128, -20), (102, -20)], -13.2, -11.5,
           "slide_dark", g, "knurl", step=6, t=2, bevel=0.5)

    g = "trigger"
    trig = [(73, -28), (79, -28), (82, -34), (82, -42), (79, -46), (75, -46), (76, -41), (76, -34)]
    k.prof("trigger", trig, -3.2, 3.2, "slide_dark", g, step=4, t=2, bevel=0.5)

    g = "magazine"
    with k.frame("x", -RAKE, 0, -66, 160):
        k.b("mag_body", -11, -114, 134, 11, -30, 176, "steel", g)
        k.b("mag_round", -4.5, -30, 137, 4.5, -24, 168, "brass", g)
    k.prof("mag_base", [(130, -113), (195, -110), (196, -118), (191, -121), (133, -122), (129, -118)], -12.5,
           12.5, "slide_dark", g, step=8, bevel=2)

    m.regroup({}, pivots={"trigger": k.P(0, -28, 77), "magazine": k.P(0, -66, 160),
                          "slide": k.P(0, 0, 100), "barrel": k.P(0, 0, 50), "slide_stop": k.P(-12, -17, 104)})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop"}
    return m


GRIP_POINT = MM(None, U).P(0, -66, 152)

ARMS = {
    "grip": ((139, -32), (163, -106)), "trigger": (79, -36),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.28, "fp": 0.37, "gui": 0.5, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 25 / U, "locks_back": True,
    "followers": {"barrel": {"pos": [0, -0.15, 1.1], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.951, 0.309], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 1.6, "recoil_time": 0.24, "shot_time": 0.25, "cycle_back": 0.035, "cycle_fwd": 0.08,
    "reload_time": 1.6, "reload_empty_time": 2.0,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

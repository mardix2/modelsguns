"""HK Mk23 Mod 0 (.45 ACP), the big SOCOM pistol: angular slide with a
sloped nose and rear serrations, threaded barrel with O-ring standing out of
the slide, exposed hammer, frame with accessory grooves, decocker and
safety on the left, ambidextrous paddle magazine release behind the guard.

Designed in mm from the real dimensions (245 mm long, 149 mm barrel,
150 mm high, 39 mm wide).  1 model unit = 7 mm.  Muzzle at z=0 (-Z),
bore at y=0.
"""

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "slide": Material((40, 41, 44), 4),
    "slide_dark": Material((24, 25, 27), 3),
    "frame": Material((36, 36, 38), 5),
    "frame_dark": Material((24, 24, 26), 4),
    "barrel": Material((70, 72, 78), 4),
    "steel": Material((90, 92, 98), 4),
    "rubber": Material((140, 40, 34), 4, edge=False),
    "brass": Material((178, 142, 66), 5),
    "white": Material((226, 226, 218), 2, edge=False),
    "text": Material((40, 41, 44), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
TOP, SB = 14.0, -14.0
RAKE = 16.0
Z0 = 14.0           # front face of the slide (the threaded barrel sticks out in front)


def build():
    m = Model("mk23", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide
    # ======================================================================
    g = "slide"
    slide = [(Z0, -4), (Z0 + 14, TOP), (232, TOP), (236, 10), (236, SB), (Z0 + 2, SB), (Z0, -10)]
    k.prof("slide", slide, -13.5, 13.5, "slide", g, step=12, bevel=3.6)
    for side, x in (("l", -13.7), ("r", 13.5)):
        for i in range(9):
            z = 196 + i * 3.8
            k.b("serr_%s_%d" % (side, i), x, SB + 3, z, x + 0.2, TOP - 3.5, z + 1.8, "slide_dark", g)
    k.b("slide_mark", -13.65, -6, 70, -13.5, 2, 170, "text", g, text={"west": "MK23 USSOCOM"})
    k.b("ejection_port", 10, 2, 110, 13.7, TOP - 0.5, 160, "bore", g)
    k.b("extractor", 13.5, 3, 160, 14, 7, 178, "slide_dark", g)
    k.bv("front_sight", -1.8, TOP - 0.5, Z0 + 16, 1.8, TOP + 5.5, Z0 + 24, 0.4, "slide_dark", g, axis="y")
    k.b("front_dot", -0.9, TOP + 2.5, Z0 + 15.9, 0.9, TOP + 4, Z0 + 16, "white", g)
    k.prof("rear_sight", [(214, TOP), (216, TOP + 6), (229, TOP + 6), (230, TOP)], -8, 8, "slide_dark", g,
           step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.5, TOP + 3, 215.5, 1.5, TOP + 6.1, 229.5, "bore", g)
    for side, xx in (("l", -5.5), ("r", 4.5)):
        k.b("rear_dot_" + side, xx, TOP + 3.5, 230, xx + 1, TOP + 4.7, 230.1, "white", g)

    # ======================================================================
    # barrel: threaded muzzle with an O-ring, hood in the port
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_thread", 0, 0, Z0 - 2, 7.6, "barrel", g, "knurl")
    k.cyl("barrel_oring", 0, Z0 - 2, Z0, 8.6, "rubber", g)
    k.cyl("barrel_crown", 0, -0.4, 0, 6.6, "steel", g)
    k.cyl("muzzle_bore", 0, -0.6, -0.4, 5.8, "bore", g)
    k.cyl("barrel_body", 0, Z0, 158, 8.4, "barrel", g)
    k.b("hood_top", 1, TOP - 0.6, 112, 13.6, TOP + 0.08, 158, "barrel", g)

    # ======================================================================
    # frame
    # ======================================================================
    g = "frame"
    frame = [(Z0 + 6, SB), (224, SB), (230, -18), (228, -24), (214, -28), (206, -36), (207, -60), (211, -90),
             (214, -114), (213, -121), (142, -121), (138, -108), (130, -84), (122, -60), (116, -42), (111, -38),
             (107, -41), (107, -54), (101, -58), (64, -58), (57, -54), (55, -42), (54, -31), (Z0 + 10, -31),
             (Z0 + 6, -26)]
    hole = [(62, -32), (107, -32), (107, -35), (104, -38), (103, -51), (99, -54), (65, -54), (61, -50)]
    k.prof("frame", [frame, hole], -12.5, 12.5, "frame", g, step=10, bevel=2.4)
    for side, (a, b) in (("l", (-12.8, -12.5)), ("r", (12.5, 12.8))):
        k.b("utl_groove_" + side, a, -27, Z0 + 12, b, -24, 58, "frame_dark", g)
        k.b("frame_line_" + side, a, -17, Z0 + 12, b, -16, 200, "frame_dark", g)
    grip = [(120, -44), (200, -44), (203, -62), (207, -90), (209, -110), (144, -112), (136, -88), (127, -64)]
    for side, (a, b) in (("l", (-12.8, -12.5)), ("r", (12.5, 12.8))):
        k.prof("grip_texture_" + side, grip, a, b, "frame_dark", g, "stipple", step=10, t=2, bevel=0.1)
        k.b("hk_logo_" + side, a - 0.05 if side == "l" else b - 0.2, -58, 150, a + 0.2 if side == "l" else b + 0.05,
            -50, 176, "text", g, text={"west" if side == "l" else "east": "HK"})
    # decocking lever and safety (left), paddle magazine release, pins
    k.prof("decocker", [(150, -18), (166, -18), (170, -26), (152, -27)], -14, -12.5, "frame_dark", g, step=6,
           t=2, bevel=0.5)
    k.prof("safety", [(182, -16), (200, -16), (202, -22), (184, -24)], -14, -12.5, "frame_dark", g, "knurl",
           step=6, t=2, bevel=0.5)
    k.prof("mag_paddle", [(104, -56), (114, -54), (118, -60), (108, -62)], -9, 9, "frame_dark", g, step=6, t=2,
           bevel=0.6)
    for side, (a, b) in (("l", (-13.1, -12.5)), ("r", (12.5, 13.1))):
        k.pin("pin_a_" + side, (a + b) / 2, -21, 104, 1.6, a, b, "steel", g)
        k.pin("pin_b_" + side, (a + b) / 2, -20, 218, 1.6, a, b, "steel", g)

    g = "slide_stop"
    k.prof("slide_stop", [(118, -15), (146, -15), (150, -18), (146, -21), (118, -21)], -14, -12.5, "frame_dark",
           g, "knurl", step=6, t=2, bevel=0.5)

    g = "trigger"
    trig = [(82, -33), (89, -33), (92, -40), (92, -49), (88, -53), (84, -53), (86, -47), (86, -40)]
    k.prof("trigger", trig, -3.5, 3.5, "frame_dark", g, step=4, t=2, bevel=0.5)

    g = "hammer"
    ham = [(222, -20), (230, -21), (233, -10), (238, -3), (243, 2), (240, 7), (232, 4), (225, -3), (222, -11)]
    k.prof("hammer", ham, -4.5, 4.5, "slide_dark", g, "knurl", step=6, t=3, bevel=0.6)

    g = "magazine"
    with k.frame("x", -RAKE, 0, -72, 176):
        k.b("mag_body", -11, -122, 150, 11, -32, 196, "steel", g)
        k.b("mag_round", -5, -32, 153, 5, -25, 190, "brass", g)
    k.prof("mag_base", [(142, -121), (213, -121), (214, -126), (144, -127)], -13, 13, "frame", g, step=8, t=3,
           bevel=1)

    m.regroup({}, pivots={"trigger": k.P(0, -33, 86), "magazine": k.P(0, -72, 176),
                          "slide": k.P(0, 0, 120), "barrel": k.P(0, 0, 70),
                          "slide_stop": k.P(-13, -18, 120), "hammer": k.P(0, -16, 224)})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, -74, 174)

ARMS = {
    "grip": ((160, -38), (178, -114)), "trigger": (88, -42),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.25, "fp": 0.32, "gui": 0.43, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 30 / U, "locks_back": True, "hammer": 32,
    "followers": {"barrel": {"pos": [0, -0.2, 1.2], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.961, 0.276], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 2.0, "recoil_time": 0.28, "shot_time": 0.3, "cycle_back": 0.04, "cycle_fwd": 0.09,
    "reload_time": 1.7, "reload_empty_time": 2.1,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

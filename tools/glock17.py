"""Glock 17 Gen 5 (9x19): nDLC slide with front and rear serrations and a
bevelled nose, polymer frame with one-slot rail, square trigger guard with
undercut, 22 deg grip without finger grooves, RTF stippling, flared
magwell with the front cut-out, ambidextrous slide stop, factory sights.

Designed in mm from the real dimensions (202 mm long, 186 mm slide, 139 mm
high, 25.5 mm slide width) and the reference photo.  1 model unit = 7 mm.
Muzzle at z=0 pointing -Z, bore at y=0.
"""

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "slide": Material((54, 55, 59), 4),
    "slide_dark": Material((30, 31, 34), 3),
    "slide_text": Material((54, 55, 59), 4, edge=False),
    "frame_text": Material((44, 44, 43), 4, edge=False),
    "frame": Material((44, 44, 43), 5),
    "frame_dark": Material((30, 30, 30), 4),
    "steel": Material((78, 79, 84), 5),
    "barrel": Material((96, 96, 100), 5),
    "steel_dark": Material((22, 22, 24), 3),
    "white": Material((232, 232, 224), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
    "brass": Material((178, 142, 66), 5),
}

U = 7.0
TOP = 13.5          # slide top (mm above the bore)
SB = -14.0          # slide bottom
RAKE = 22.0         # grip angle


def build():
    m = Model("glock17", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: bevelled nose, front + rear serrations, sights, ejection port
    # ======================================================================
    g = "slide"
    slide = [(0, 7), (5, TOP), (183, TOP), (186, 10.5), (186, SB + 1), (184, SB), (4, SB), (0, -10)]
    k.prof("slide", slide, -12.75, 12.75, "slide", g, step=12, bevel=2.6)
    for side, x in (("l", -12.95), ("r", 12.75)):
        for i in range(6):                                   # front serrations
            z = 7 + i * 4.6
            k.b("serr_f_%s_%d" % (side, i), x, SB + 2.5, z, x + 0.2, TOP - 2.5, z + 2.0, "slide_dark", g)
        for i in range(8):                                   # rear serrations
            z = 146 + i * 4.6
            k.b("serr_r_%s_%d" % (side, i), x, SB + 2.5, z, x + 0.2, TOP - 2.5, z + 2.0, "slide_dark", g)
    k.b("slide_mark", -12.85, -2, 70, -12.7, 6, 135, "slide_text", g, text={"west": "GLOCK 17 GEN5"})
    k.b("slide_mark_b", -12.85, -10, 95, -12.7, -4, 130, "slide_text", g, text={"west": "AUSTRIA 9X19"})
    # muzzle: slide nose ring and barrel crown
    k.cyl("nose_ring", 0, -0.5, 0.2, 8.2, "slide_dark", g)
    # ejection port (right) and extractor
    k.b("ejection_port", 9, 1, 62, 12.95, TOP + 0.1, 112, "bore", g)
    k.b("extractor", 12.75, 2.5, 112, 13.3, 6.5, 128, "steel", g)
    k.b("extractor_ind", 13.3, 3.5, 114, 13.5, 5.5, 120, "steel_dark", g)
    # rear plate
    k.bv("rear_plate", -9, SB + 3, 186, 9, TOP - 3, 187.4, 1.2, "frame_dark", g)
    # sights
    k.bv("front_sight", -2, TOP - 0.5, 7, 2, TOP + 5.5, 13, 0.6, "steel_dark", g)
    k.b("front_sight_dot", -1, TOP + 2, 6.9, 1, TOP + 4, 7, "white", g)
    rs = [(166, TOP), (168, TOP + 5.5), (183, TOP + 6.5), (184, TOP)]
    for side, (a, b) in (("l", (-7, -2.2)), ("r", (2.2, 7))):
        k.prof("rear_sight_" + side, rs, a, b, "steel_dark", g, step=6, t=2.5, bevel=0.6)
        k.b("rear_dot_" + side, a + 1.4 if side == "l" else b - 3.4, TOP + 3, 184, a + 3.4 if side == "l" else b - 1.4,
            TOP + 5, 184.1, "white", g)
    k.b("rear_sight_base", -7, TOP - 0.4, 168, 7, TOP + 2, 183, "steel_dark", g)

    # ======================================================================
    # barrel: crown in the nose, hood in the ejection port
    # ======================================================================
    g = "barrel"
    k.cyl("barrel_crown", 0, -0.7, 2, 6.9, "barrel", g)
    k.cyl("muzzle_bore", 0, -0.9, -0.7, 4.6, "bore", g)
    k.cyl("barrel_body", 0, 2, 110, 6.9, "barrel", g)
    k.bv("barrel_hood", -8.6, 2.5, 62, 8.6, TOP - 0.2, 112, 1.4, "barrel", g)
    k.b("chamber_mark", 8.55, 5, 70, 8.7, 10, 100, "barrel", g)
    k.b("hood_top", 1, TOP - 0.6, 64, 12.6, TOP + 0.08, 110, "barrel", g)     # seen through the port

    # ======================================================================
    # frame: dust cover with one-slot rail, trigger guard, grip, magwell
    # ======================================================================
    g = "frame"
    frame = [(8, SB), (184, SB), (191, -18), (190, -23), (180, -27), (171, -31), (168, -38),
             (171, -55), (178, -75), (186, -95), (193, -106), (194, -110),
             (132, -113), (128, -103), (120, -82), (112, -61), (105, -43), (103, -36),
             (99, -33), (95, -36), (95, -48), (90, -52), (56, -52), (51, -49), (49, -42),
             (50, -27), (12, -27), (8, -24)]
    guard_hole = [(57, -27), (96, -27), (96, -30), (93, -33), (93, -45), (89, -47), (58, -47), (55, -44)]
    k.prof("frame", [frame, guard_hole], -12, 12, "frame", g, step=10, bevel=2.4)
    # one-slot accessory rail under the dust cover
    for side, (a, b) in (("l", (-11.6, -10.4)), ("r", (10.4, 11.6))):
        k.b("rail_groove_" + side, a if side == "l" else b - 0.2, -24.5, 12, a + 0.2 if side == "l" else b, -22.5,
            48, "frame_dark", g)
    k.b("rail_slot", -10, -27.2, 30, 10, -26.9, 36, "frame_dark", g)
    # guard front texture, frame markings
    k.b("guard_front_l", -12.2, -46, 49.6, -12, -30, 51, "frame_dark", g)
    k.b("frame_mark_l", -12.1, -25, 54, -11.95, -19, 90, "frame_text", g, text={"west": "GEN5"})
    # grip: RTF stippling panel and the magwell front cut-out
    grip_panel = [(108, -39), (165, -39), (169, -56), (176, -75), (183, -95), (186, -102), (133, -105),
                  (125, -86), (117, -64), (110, -46)]
    for side, (a, b) in (("l", (-12.25, -12)), ("r", (12, 12.25))):
        k.prof("grip_stipple_" + side, grip_panel, a, b, "frame_dark", g, "stipple", step=10, t=2, bevel=0.1)
        k.b("logo_" + side, a - 0.05 if side == "l" else b - 0.2, -52, 136, a + 0.2 if side == "l" else b + 0.05, -45,
            164, "frame_text", g, text={"west" if side == "l" else "east": "GLOCK"})
    k.prof("magwell_flare", [(129, -104), (195, -101), (196, -111), (132, -114)], -13, 13, "frame", g,
           step=8, t=3, bevel=1)
    k.b("magwell_cut", -6, -113.4, 129, 6, -101, 133.5, "bore", g)
    k.b("lanyard_slot", -5, -109, 188, 5, -103, 195.4, "frame_dark", g)
    # pins and controls
    for side, (a, b) in (("l", (-12.6, -12)), ("r", (12, 12.6))):
        k.pin("trigger_pin_" + side, (a + b) / 2, -20, 103, 1.2, a, b, "steel", g)
        k.pin("block_pin_" + side, (a + b) / 2, -18, 72, 1.2, a, b, "steel", g)
        k.pin("housing_pin_" + side, (a + b) / 2, -21, 170, 1.2, a, b, "steel", g)
        k.bv("takedown_" + side, a - 0.6 if side == "l" else b - 0.2, -21, 82, a + 0.2 if side == "l" else b + 0.6,
             -16.5, 92, 0.3, "steel_dark", g, axis="x")

    g = "slide_stop"
    for side, (a, b) in (("l", (-13.6, -12)), ("r", (12, 13.6))):
        k.bv("slide_stop_" + side, a, -19.5, 104, b, -15.5, 128, 0.4, "steel_dark", g, "knurl", axis="x")

    g = "mag_catch"
    k.bv("catch_mag", -13.4, -40, 100, 13.4, -33, 108, 0.6, "frame_dark", g, "knurl", axis="x")

    g = "trigger"
    trig = [(73, -27), (79, -27), (81, -32), (81, -40), (78, -44), (75, -44), (76, -38), (75, -31)]
    k.prof("trigger_shoe", trig, -3, 3, "frame_dark", g, step=4, t=2, bevel=0.5)
    k.b("trigger_safety", -0.8, -40, 77.5, 0.8, -29, 79.2, "steel_dark", g)

    # ======================================================================
    # magazine: body in the grip, base plate
    # ======================================================================
    g = "magazine"
    with k.frame("x", -RAKE, 0, -65, 152):
        k.b("mag_body", -11, -114, 131, 11, -30, 170, "steel_dark", g)
        k.b("mag_round", -4.5, -30, 134, 4.5, -25, 162, "brass", g)
    base = [(132, -113), (195, -110), (196, -118), (191, -121), (135, -123), (131, -119)]
    k.prof("mag_base", base, -12.5, 12.5, "frame", g, step=8, bevel=2)

    m.regroup({}, pivots={"trigger": k.P(0, -27, 77), "magazine": k.P(0, -65, 152),
                          "slide": k.P(0, 0, 100), "barrel": k.P(0, 0, 50),
                          "slide_stop": k.P(-12.8, -17.5, 106), "mag_catch": k.P(0, -36, 104)})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "mag_catch"}
    return m


GRIP_POINT = MM(None, U).P(0, -65, 150)

ARMS = {
    "grip": ((137, -32), (162, -106)), "trigger": (79, -36),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.28, "fp": 0.37, "gui": 0.52, "tilt": 0}

ANIM = {
    "action": "slide", "travel": 24 / U, "locks_back": True,
    # barrel unlocks: moves back with the slide and its breech drops
    "followers": {"barrel": {"pos": [0, -0.15, 1.1], "rot": [-4, 0, 0]}},
    "stop": {"bone": "slide_stop", "rot": [7, 0, 0]},
    "release": ("mag_catch", [0.25, 0, 0]),
    "trigger": True, "trigger_angle": 16,
    "mag_dir": [0, -0.927, 0.375], "mag_far": 18, "mag_gap": 0.4,
    "recoil": 1.6, "recoil_time": 0.24, "shot_time": 0.25, "cycle_back": 0.035, "cycle_fwd": 0.08,
    "reload_time": 1.6, "reload_empty_time": 2.0,
    "reload_tilt": [10, 18, -32], "reload_lift": [-1.5, 1.5, -1.5],
}

ANIMATIONS = anims.build(ANIM)

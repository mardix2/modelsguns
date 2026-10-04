"""Chiappa Rhino 60DS (.357 Magnum, 6"): the revolver that fires from the
bottom chamber - low barrel under a long slab-sided shroud with a vented top
rib, hexagonal six-shot cylinder above the bore, cocking lever at the back,
cylinder release lever, low grip.

Designed in mm from the real dimensions (about 265 mm long, 152 mm barrel,
140 mm high, 38 mm wide).  1 model unit = 7 mm.  Muzzle at z=0 (-Z), bore
(the bottom chamber) at y=0.

Bones: the crane (yoke) swings out to the left about its pin; the cylinder
is its child and turns 60 deg per shot about its own axis; the rounds are
the cylinder's child and get ejected / loaded.
"""

import math

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "steel": Material((40, 41, 45), 4),
    "steel_dark": Material((24, 25, 28), 3),
    "steel_light": Material((96, 98, 106), 4),
    "alloy": Material((50, 51, 55), 4),
    "wood": Material((70, 40, 22), 5),
    "wood_dark": Material((44, 24, 12), 4),
    "brass": Material((184, 148, 70), 5),
    "lead": Material((120, 110, 100), 4),
    "red": Material((220, 40, 30), 2, edge=False),
    "green": Material((90, 220, 120), 2, edge=False),
    "text": Material((40, 41, 45), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
CY = 12.5            # cylinder axis above the bore
CZ0, CZ1 = 150.0, 196.0
APO = 18.0           # hexagon apothem (half the across-flats width)
CRANE = (-9.0, -4.0)  # crane pin (x, y): the cylinder swings out to the left
RAKE = 22.0


def build():
    m = Model("rhino", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # barrel shroud with vented rib, muzzle at its bottom front
    # ======================================================================
    g = "frame"
    shroud = [(0, -9), (0, 12), (10, 24), (150, 24), (150, -9)]
    k.prof("shroud", shroud, -11, 11, "alloy", g, step=12, bevel=2.6)
    k.cyl("muzzle_crown", 0, -0.6, 0, 7.6, "steel", g)
    k.cyl("muzzle_bore", 0, -0.8, -0.6, 4.6, "bore", g)
    for side, x in (("l", -11.2), ("r", 11)):
        k.b("shroud_flute_a_" + side, x, 6, 20, x + 0.2, 10, 140, "steel_dark", g)
        k.b("shroud_flute_b_" + side, x, -4, 30, x + 0.2, 0, 140, "steel_dark", g)
        k.b("shroud_mark_" + side, x - 0.05 if side == "l" else x, 13, 40, x + 0.2 if side == "l" else x + 0.25,
            19, 120, "text", g, text={"west" if side == "l" else "east": "RHINO 60DS 357"})
    k.b("rib_base", -5, 24, 6, 5, 26, 150, "steel", g)
    for i in range(12):
        z = 12 + i * 11
        k.b("rib_post_%02d" % i, -5, 26, z, 5, 29, z + 5, "steel", g)
    k.b("rib_top", -5, 29, 8, 5, 30.5, 150, "steel", g, "serration")
    k.bv("front_sight", -2, 30.5, 8, 2, 37, 18, 0.4, "steel_dark", g, axis="y")
    k.cyl("fiber", 34, 8, 14, 1.4, "red", g)
    # frame round the cylinder window and behind it
    frame = [(150, 24), (150, 31), (206, 31), (214, 30), (226, 22), (238, 22), (246, 12), (247, 4), (250, -20),
             (256, -55), (262, -92), (262, -104), (230, -104), (222, -84), (212, -55), (206, -36), (202, -30),
             (198, -33), (196, -43), (190, -46), (166, -46), (160, -42), (158, -14), (150, -9)]
    window = [(150, 24), (198, 24), (198, -3), (150, -3)]
    hole = [(165, -14), (196, -14), (196, -17), (193, -20), (192, -39), (188, -42), (168, -42), (165, -38)]
    k.prof("frame", [frame, window, hole], -10.5, 10.5, "alloy", g, step=10, bevel=2.2)
    k.prof("rear_sight", [(198, 31), (200, 36), (212, 36), (213, 31)], -7, 7, "steel_dark", g, step=6, t=2,
           bevel=0.6)
    k.b("rear_notch", -1.4, 33, 199.5, 1.4, 36.1, 212.5, "bore", g)
    for side, xx in (("l", -5), ("r", 4)):
        k.b("rear_dot_" + side, xx, 33.5, 213, xx + 1, 34.7, 213.1, "green", g)
    # cylinder release lever (left) and pins
    k.prof("cyl_release", [(200, 2), (212, 2), (214, 14), (208, 18), (200, 14)], -12.5, -10.5, "steel_dark", g,
           "knurl", step=6, t=2, bevel=0.5)
    for side, (a, b) in (("l", (-11.1, -10.5)), ("r", (10.5, 11.1))):
        k.pin("pin_a_" + side, (a + b) / 2, -8, 210, 1.6, a, b, "steel_light", g)
        k.pin("pin_b_" + side, (a + b) / 2, 10, 228, 1.6, a, b, "steel_light", g)
    # grip
    grip = [(212, -40), (248, -2), (252, -22), (257, -55), (261, -90), (261, -101), (233, -101), (224, -82),
            (216, -58)]
    for side, (a, b) in (("l", (-14, -10.5)), ("r", (10.5, 14))):
        k.prof("grip_" + side, grip, a, b, "wood", g, "checker", step=10, t=5, bevel=1.4)
        k.b("grip_logo_" + side, a - 0.05 if side == "l" else b - 0.2, -66, 236, a + 0.2 if side == "l" else b + 0.05,
            -58, 250, "wood_dark", g)

    # ======================================================================
    # crane, cylinder (child) and rounds (grandchild)
    # ======================================================================
    g = "crane"
    cx, cy = CRANE
    k.bv("crane_arm", cx - 3, cy - 3, CZ0 - 6, -3, CY, CZ0 - 1, 0.6, "steel", g)
    k.cyl("crane_pin", cy, CZ0 - 6, CZ0 + 2, 3, "steel_light", g, x=cx)
    k.cyl("ejector_rod", CY, CZ0 - 8, CZ0, 3.2, "steel_light", g)

    g = "cylinder"
    zc = (CZ0 + CZ1) / 2
    side = 2 * APO * math.tan(math.radians(30))
    for i, ang in enumerate((0, 60, 120)):
        with k.frame("z", ang, 0, CY, zc):
            k.b("cyl_hex_%d" % i, -side / 2, CY - APO, CZ0, side / 2, CY + APO, CZ1, "steel", g)
    for i in range(6):
        a = math.radians(-90 + 60 * i)
        x, y = 12.6 * math.cos(a), CY + 12.6 * math.sin(a)
        k.cyl("chamber_%d" % i, y, CZ0 - 0.3, CZ0, 4.8, "bore", g, x=x)
    k.cyl("cyl_ratchet", CY, CZ1, CZ1 + 2, 9, "steel_dark", g)

    g = "rounds"
    for i in range(6):
        a = math.radians(-90 + 60 * i)
        x, y = 12.6 * math.cos(a), CY + 12.6 * math.sin(a)
        k.cyl("round_case_%d" % i, y, CZ0 + 6, CZ1 + 1, 4.6, "brass", g, x=x)
        k.cyl("round_rim_%d" % i, y, CZ1 + 1, CZ1 + 2, 5.4, "brass", g, x=x)
        k.cyl("round_bullet_%d" % i, y, CZ0 - 0.6, CZ0 + 6, 3.6, "lead", g, x=x)

    g = "trigger"
    trig = [(176, -16), (182, -16), (185, -24), (185, -34), (181, -38), (177, -38), (179, -32), (178, -24)]
    k.prof("trigger", trig, -3.5, 3.5, "steel_dark", g, step=4, t=2, bevel=0.5)

    g = "hammer"
    ham = [(232, 18), (240, 18), (246, 24), (252, 30), (250, 34), (242, 32), (234, 26)]
    k.prof("cocking_lever", ham, -4, 4, "steel_dark", g, "knurl", step=6, t=3, bevel=0.6)

    m.parents = {"cylinder": "crane", "rounds": "cylinder"}
    m.regroup({}, pivots={"trigger": k.P(0, -16, 180), "hammer": k.P(0, 18, 234),
                          "crane": k.P(cx, cy, CZ0), "cylinder": k.P(0, CY, zc), "rounds": k.P(0, CY, zc)})
    m.dynamic = {"crane", "cylinder", "rounds", "trigger", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, -50, 238)

ARMS = {
    "grip": ((226, -20), (244, -100)), "trigger": (181, -28),
    "left": {"kind": "support"}, "right_dir": (24, 10), "left_dir": (28, -18),
}

DISPLAY = {"hand": 0.25, "fp": 0.31, "gui": 0.4, "tilt": 0}

ANIM = {
    "mag": None, "hammer": 28, "trigger": True, "trigger_angle": 18,
    "recoil": 2.6, "recoil_time": 0.34, "shot_time": 0.36,
    "arm_job_rot": {"left_arm": [38, 0, 0]},
    "hands": {"left_arm": [("crane", "ejector_rod", None), ("rounds", "round_case", ("reload", "reload_empty"))]},
}


def _turn_cylinder(a, t0, t1):
    """Double action: the cylinder indexes one chamber (60 deg) while the
    trigger comes back; the hammer rises and falls."""
    a.rot("cylinder", t0, anims.ZERO)
    a.rot("cylinder", t1, [0, 0, 60], "easeInOutSine")
    a.rot("hammer", t0, anims.ZERO)
    a.rot("hammer", t1, [ANIM["hammer"], 0, 0], "easeInQuad")
    a.rot("hammer", t1 + 0.015, anims.ZERO, "easeInQuad")


def _shoot(c):
    a = anims.Anim(c["shot_time"] + 0.08)
    anims._trigger(a, c, 0.0, hold=0.08)
    _turn_cylinder(a, 0.0, 0.08)
    anims._recoil(a, c, 0.085)
    return a


def _dry_fire(c, aimed=False):
    a = anims.dry_fire(c, aimed)
    _turn_cylinder(a, 0.0, 0.08)
    return a


def _reload(c):
    """Press the release, swing the cylinder out, punch the empties out,
    load six, close it with a flick."""
    L = 3.1
    a = anims.Anim(L)
    tilt, lift = [4, 18, -34], [-2.5, -1.5, -4.0]
    a.track("root", "rotation", [(0, anims.ZERO), (0.3, tilt, "easeInOutSine"),
                                 (0.62, anims.add(tilt, [-28, 0, 0]), "easeInOutSine"),      # muzzle up: empties out
                                 (0.95, anims.add(tilt, [-28, 0, 0])),
                                 (1.2, anims.add(tilt, [18, 0, 0]), "easeInOutSine"),        # muzzle down: load
                                 (2.0, anims.add(tilt, [18, 0, 0])),
                                 (2.3, tilt, "easeInOutSine"), (L, anims.ZERO, "easeInOutSine")])
    a.track("root", "position", [(0, anims.ZERO), (0.3, lift, "easeInOutSine"), (2.4, lift),
                                 (L, anims.ZERO, "easeInOutSine")])
    # crane out and back in
    a.track("crane", "rotation", [(0, anims.ZERO), (0.3, anims.ZERO), (0.5, [0, 0, 80], "easeOutQuad"),
                                  (2.05, [0, 0, 80]), (2.2, anims.ZERO, "easeInQuad")])
    # empties pushed out, fall away; new rounds come in from behind
    far = [0, -60, 70]
    a.track("rounds", "position", [(0, anims.ZERO), (0.62, anims.ZERO), (0.75, [0, 0, 6], "easeOutQuad"),
                                   (0.95, [0, -8, 40], "easeInQuad"), (0.96, far, "step"),
                                   (1.3, far), (1.65, [0, 0, 12], "easeOutCubic"), (1.85, anims.ZERO, "easeInQuad")])
    a.track("crane", "position", [(0, anims.ZERO), (0.62, anims.ZERO), (0.7, [0, 0, -1.2], "easeOutQuad"),
                                  (0.8, anims.ZERO)])
    return a


ANIMATIONS = anims.build(ANIM, {"shoot": _shoot, "dry_fire": _dry_fire,
                               "dry_fire_aim": lambda c: _dry_fire(c, True),
                               "reload": _reload, "reload_empty": _reload})

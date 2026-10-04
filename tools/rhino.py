"""Chiappa Rhino 60DS (6"), stainless "Aristocrat" finish: the revolver
that fires from the bottom chamber - low barrel under a slab-sided shroud
with four lightening cuts and a top rib, hexagonal six-shot cylinder above
the bore, cocking lever at the back, adjustable rear sight, black stippled
grip with the Rhino medallion and a wood heel.

Outlines are measured on a side photo (right side, mirrored; 3.79 px per
mm, muzzle at x=10, bore at y=220); widths from real dimensions (shroud
22 mm, cylinder 36 mm across corners).  1 model unit = 7 mm.

Bones: the crane (yoke) swings out to the left about its pin; the cylinder
is its child and turns 60 deg per shot about its own axis; the rounds are
the cylinder's child and get ejected / loaded.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "ss": Material((200, 202, 207), 3),
    "ss_dark": Material((150, 152, 158), 3),
    "ss_deep": Material((96, 98, 104), 3),
    "black": Material((30, 30, 33), 3),
    "grip": Material((58, 55, 54), 5),
    "grip_dark": Material((36, 34, 34), 4),
    "wood": Material((92, 76, 68), 5),
    "brass": Material((184, 148, 70), 5),
    "lead": Material((120, 110, 100), 4),
    "red": Material((220, 40, 30), 2, edge=False),
    "text": Material((198, 200, 205), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
S = Silhouette("rhino", 3.79, 10, 220)
Z, Y, P = S.zmm, S.ymm, S.poly
CY = Y(173.5)        # cylinder axis above the bore
CZ0, CZ1 = Z(566), Z(716)
R_CYL = 18.0         # hexagon circumradius (corners up and down, a flat to each side)
R_CH = CY            # chamber circle: the bottom chamber lines up with the bore
CRANE = (-9.0, -4.0)  # crane pin (x, y): the cylinder swings out to the left
RAKE = 22.0
FW = 11.0


def circle(cx, cy, r, n=10):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def slot(x0, x1, y0, y1, n=6):
    """rounded lightening cut (px)"""
    r = (y1 - y0) / 2
    pts = []
    for i in range(n + 1):
        a = math.pi / 2 + math.pi * i / n
        pts.append((x0 + r + r * math.cos(a), y0 + r - r * math.sin(a)))
    for i in range(n + 1):
        a = -math.pi / 2 + math.pi * i / n
        pts.append((x1 - r + r * math.cos(a), y0 + r - r * math.sin(a)))
    return P(pts)


def build():
    m = Model("rhino", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # frame: shroud with four cuts, cylinder window, guard; top rib
    # ======================================================================
    g = "frame"
    frame = P([(16, 80), (772, 80), (786, 79), (813, 81), (806, 108), (837, 134), (884, 146), (897, 155),
               (903, 160), (903, 175), (860, 195), (800, 280), (744, 366), (732, 354), (704, 366), (674, 394),
               (658, 399), (571, 399), (555, 395), (537, 382), (475, 300), (465, 292), (461, 282), (444, 267),
               (431, 262), (18, 258), (9, 239), (9, 96)])
    window = P([(555, 95), (722, 95), (722, 247), (555, 247)])
    guard = P([(547, 309), (566, 303), (595, 304), (640, 310), (665, 315), (689, 346), (686, 362), (663, 382),
               (623, 385), (607, 384), (560, 381), (534, 357), (532, 330)])
    cuts = [slot(40, 140, 120, 165), slot(160, 255, 120, 165), slot(275, 365, 120, 165), slot(385, 470, 120, 165)]
    k.prof("frame", [frame, window, guard] + cuts, -FW, FW, "ss", g, step=14, bevel=2.4)
    rib = P([(16, 48), (772, 48), (772, 80), (9, 96), (12, 60)])
    k.prof("rib", rib, -FW + 2, FW - 2, "ss_dark", g, "brushed", step=14, bevel=1.6)
    k.cyl("muzzle_crown", Y(220), Z(8.4), Z(10), 8.0, "ss_dark", g)
    k.cyl("muzzle_bore", Y(220), Z(8.2), Z(8.4), 4.6, "bore", g)
    k.cyl("barrel", Y(220), Z(10), Z(560), 8.0, "ss_deep", g)
    for side, x in (("l", -FW - 0.15), ("r", FW)):
        k.b("mark_a_" + side, x, Y(235), Z(100), x + 0.15, Y(195), Z(290), "text", g,
            text={"west" if side == "l" else "east": "LONDON ENGLAND"})
        k.b("mark_b_" + side, x, Y(245), Z(430), x + 0.15, Y(195), Z(550), "text", g,
            text={"west" if side == "l" else "east": "RHINO 60DS"})
    # sights: black front ramp, adjustable rear with its screw, knurled wheel
    k.prof("front_sight", P([(16, 48), (21, 10), (78, 10), (118, 48)]), -2.2, 2.2, "black", g, step=8, t=3,
           bevel=0.5)
    k.cyl("fiber", Y(16), Z(22), Z(40), 1.4, "red", g)
    k.prof("rear_sight", P([(735, 49), (740, 38), (772, 36), (785, 38), (785, 49)]), -6, 6, "black", g, step=6,
           t=2, bevel=0.5)
    k.b("rear_notch", -1.4, Y(48), Z(770), 1.4, Y(35), Z(787), "bore", g)
    k.cylx("sight_screw", -6.6, 6.6, Y(62), Z(751), 2.8, "ss_dark", g)
    k.cylx("wheel", -5, 5, Y(62), Z(666), 4.4, "ss_dark", g, "knurl")
    # cylinder release (left) and screws
    k.prof("cyl_release", P([(728, 160), (752, 158), (756, 200), (740, 214), (728, 200)]), -FW - 2, -FW, "ss_dark",
           g, "knurl", step=6, t=2, bevel=0.5)
    for side, (a, b) in (("l", (-FW - 0.6, -FW)), ("r", (FW, FW + 0.6))):
        for j, (cx, cy) in enumerate(((757, 99), (849, 153), (597, 266), (480, 265))):
            k.pin("screw_%s_%d" % (side, j), (a + b) / 2, Y(cy), Z(cx), 1.8, a, b, "ss_deep", g)

    # wrap-around grip: stippled body with the medallion, wood heel
    grip = P([(903, 175), (879, 208), (876, 236), (891, 273), (958, 384), (990, 464), (1007, 521), (1010, 540),
              (822, 546), (821, 524), (782, 403), (776, 392), (754, 370), (744, 366), (800, 280), (860, 195)])
    k.prof("grip", grip, -15, 15, "grip", g, "stipple", step=14, bevel=3)
    heel = P([(822, 544), (1010, 538), (1013, 553), (1012, 586), (1001, 611), (974, 638), (960, 645), (921, 654),
              (848, 655), (808, 648), (796, 642), (780, 605), (778, 589), (788, 577), (803, 573), (817, 558)])
    k.prof("grip_heel", heel, -16, 16, "wood", g, "wood", step=14, bevel=3)
    for side, (a, b) in (("l", (-15.5, -15)), ("r", (15, 15.5))):
        k.prof("medallion_" + side, circle(872, 385, 38, 12), a, b, "grip_dark", g, step=8, t=2, bevel=0.2)

    # ======================================================================
    # crane, cylinder (child) and rounds (grandchild)
    # ======================================================================
    g = "crane"
    cx, cy = CRANE
    k.bv("crane_arm", cx - 3, cy - 3, CZ0 - 6, -3, CY, CZ0 - 1, 0.6, "ss", g)
    k.cyl("crane_pin", cy, CZ0 - 6, CZ0 + 2, 3, "ss_dark", g, x=cx)
    k.cyl("ejector_rod", CY, CZ0 - 8, CZ0, 3.2, "ss_dark", g)

    g = "cylinder"
    zc = (CZ0 + CZ1) / 2
    apo = R_CYL * math.cos(math.radians(30))
    side = R_CYL
    for i, ang in enumerate((30, 90, 150)):
        with k.frame("z", ang, 0, CY, zc):
            k.b("cyl_hex_%d" % i, -side / 2, CY - apo, CZ0, side / 2, CY + apo, CZ1, "ss", g, "brushed")
    for side_x, x in (("l", -apo - 0.1), ("r", apo)):
        for j, yy in enumerate((Y(129), Y(201))):
            k.b("cyl_notch_%s_%d" % (side_x, j), x, yy - 0.8, Z(670), x + 0.1, yy + 0.8, Z(695), "ss_deep", g)
    for i in range(6):
        a = math.radians(-90 + 60 * i)
        x, y = R_CH * math.cos(a), CY + R_CH * math.sin(a)
        k.cyl("chamber_%d" % i, y, CZ0 - 0.3, CZ0, 4.8, "bore", g, x=x)
    k.cyl("cyl_ratchet", CY, CZ1, CZ1 + 2, 9, "ss_dark", g)

    g = "rounds"
    for i in range(6):
        a = math.radians(-90 + 60 * i)
        x, y = R_CH * math.cos(a), CY + R_CH * math.sin(a)
        k.cyl("round_case_%d" % i, y, CZ0 + 6, CZ1 + 1, 4.6, "brass", g, x=x)
        k.cyl("round_rim_%d" % i, y, CZ1 + 1, CZ1 + 2, 5.4, "brass", g, x=x)
        k.cyl("round_bullet_%d" % i, y, CZ0 - 0.6, CZ0 + 6, 3.6, "lead", g, x=x)

    g = "trigger"
    trig = P([(612, 305), (632, 312), (640, 330), (632, 368), (622, 382), (618, 378), (626, 352), (624, 325)])
    k.prof("trigger", trig, -3.5, 3.5, "ss", g, step=6, t=2, bevel=0.5)

    g = "hammer"
    ham = P([(778, 92), (784, 79), (800, 77), (812, 84), (814, 100), (786, 104)])
    k.prof("cocking_lever", ham, -4, 4, "ss_dark", g, "knurl", step=6, t=3, bevel=0.6)

    m.parents = {"cylinder": "crane", "rounds": "cylinder"}
    m.regroup({}, pivots={"trigger": k.P(0, Y(305), Z(615)), "hammer": k.P(0, Y(102), Z(790)),
                          "crane": k.P(cx, cy, CZ0), "cylinder": k.P(0, CY, zc), "rounds": k.P(0, CY, zc)})
    m.dynamic = {"crane", "cylinder", "rounds", "trigger", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(420), Z(880))

ARMS = {
    "grip": ((Z(855), Y(260)), (Z(905), Y(600))), "trigger": (Z(625), Y(345)),
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

"""MK18 Mod 1 (CQBR) as in the reference photo, without sights or
accessories: 10.3" barrel with A2 birdcage, Daniel Defense RIS II with tan
ladder rail covers, black flat-top upper and Mil-Spec lower, tan oversized
trigger guard, tan ergonomic grip and tan adjustable stock, grey 30 rd
aluminium magazine.

Outlines are measured on the photo (levelled along the bore, muzzle at
x=32, bore at y=268, perspective-corrected scale, see scale()); widths from
real dimensions.
1 model unit = 15.6 mm.  Muzzle at z=0 pointing -Z, bore at y=0.
"""

import math

import anims
from bbgen import Material, MM, Model

MATERIALS = {
    "alu": Material((52, 53, 57), 4),          # black anodised aluminium
    "alu_dark": Material((32, 33, 36), 3),
    "steel": Material((58, 58, 62), 5),
    "steel_light": Material((112, 112, 116), 5),
    "steel_dark": Material((28, 28, 31), 3),
    "tan": Material((176, 150, 112), 6),       # FDE furniture
    "tan_dark": Material((132, 110, 80), 5),
    "mag": Material((78, 80, 82), 4),          # grey aluminium magazine
    "mag_light": Material((120, 122, 124), 4),
    "brass": Material((176, 140, 64), 5),
    "bore": Material((6, 6, 6), 1, edge=False),
    "white": Material((205, 205, 198), 2, edge=False),
    "text": Material((52, 53, 57), 3, edge=False),
}

U = 15.6
# The photo is taken from above the stock, so the scale grows towards the
# rear: px per mm = S0 + SB * (x - 75), calibrated on the flash hider
# (22 mm) and buffer tube (30 mm) diameters.
MX, BY, S0, SB = 32.0, 268.0, 1.64, 0.36 / 925


def scale(x):
    return S0 + SB * (x - 75)


def Z(x):
    return math.log(scale(x) / scale(MX)) / SB


def Y(y, x=760):
    return (BY - y) / scale(x)


def P(pts):
    return [(Z(x), Y(y, x)) for x, y in pts]


def build():
    m = Model("mk18", MATERIALS, density=7)
    k = MM(m, U)

    # ======================================================================
    # barrel: A2 birdcage flash hider, barrel stub
    # ======================================================================
    g = "barrel"
    k.cyl("flash_hider", 0, Z(32), Z(118), 10.5, "steel", g)
    k.cyl("fh_crown", 0, Z(31), Z(32), 8.5, "steel_dark", g)
    k.cyl("muzzle_bore", 0, Z(30.6), Z(31), 3.2, "bore", g)
    for i, ang in enumerate((0, 60, -60, 120, -120)):          # closed bottom
        with k.frame("z", ang, 0, 0, Z(70)):
            k.b("fh_slot_%d" % i, -1.4, 9.9, Z(46), 1.4, 10.7, Z(98), "bore", g)
    k.cyl("barrel", 0, Z(118), Z(140), 7.4, "steel", g)

    # ======================================================================
    # RIS II handguard: black rails, tan ladder covers on the sides / bottom
    # ======================================================================
    g = "handguard"
    z0, z1 = Z(136), Z(496)
    k.bv("hg_body", -24, -24, z0, 24, 30, z1, 5, "alu", g)
    k.bv("hg_front_ring", -25, -25.5, z0 - 2, 25, 31, z0 + 4, 5, "alu_dark", g)
    k.b("hg_top_base", -10.6, 30, z0, 10.6, 32.5, z1, "alu", g)
    m.teeth_z("hg_top_t", "up", k.X(-10.6), k.X(10.6), k.Y(32.5), 3.2 / U, k.Z(z0 + 1), k.Z(z1),
              "alu", g, period=10 / U, tooth=5.3 / U)
    # ladder covers: tan plate with dark slots (sides and bottom)
    n_rungs = int((z1 - z0 - 8) / 13)
    for side, (a, b) in (("l", (-30, -24)), ("r", (24, 30))):
        k.bv("cover_" + side, a, -12, z0 + 3, b, 16, z1 - 3, 1.6, "tan", g)
        for i in range(n_rungs):
            zz = z0 + 7 + i * 13
            xs = (a - 0.2, a + 0.4) if side == "l" else (b - 0.4, b + 0.2)
            k.b("cover_slot_%s_%02d" % (side, i), xs[0], -8, zz, xs[1], 12, zz + 5.5, "alu_dark", g)
    k.bv("cover_b", -14, -30, z0 + 3, 14, -24, z1 - 3, 1.6, "tan", g)
    for i in range(n_rungs):
        zz = z0 + 7 + i * 13
        k.b("cover_slot_b_%02d" % i, -10, -30.4, zz, 10, -29.6, zz + 5.5, "alu_dark", g)
    for side, x in (("l", -24.4), ("r", 24)):
        k.b("hg_mark_" + side, x, 18, Z(440), x + 0.4, 26, Z(490), "text", g,
            text={"west" if side == "l" else "east": "L17"})

    # ======================================================================
    # upper receiver: flat-top rail, ejection port, forward assist
    # ======================================================================
    g = "upper"
    upper = P([(496, 226), (943, 226), (943, 296), (930, 300), (565, 300), (540, 296), (512, 292),
               (496, 284)])
    k.prof("upper", upper, -15.5, 15.5, "alu", g, step=14, bevel=2.5)
    rz0, rz1 = Z(498), Z(940)
    k.b("rail_base", -10.6, Y(226), rz0, 10.6, Y(226) + 3, rz1, "alu", g)
    m.teeth_z("rail_t", "up", k.X(-10.6), k.X(10.6), k.Y(Y(226) + 3), 3.2 / U, k.Z(rz0 + 1), k.Z(rz1),
              "alu", g, period=10 / U, tooth=5.3 / U)
    for i in range(0, 34, 4):
        zz = rz0 + 2 + i * 10
        k.b("rail_num_%02d" % i, -10.7, Y(226) + 1, zz, -10.6, Y(226) + 2.5, zz + 3, "white", g)
    k.b("ejection_port", 15.5, Y(262), Z(640), 15.8, Y(236), Z(800), "bore", g)
    k.cylx("forward_assist", 15, 25, Y(246), Z(880), 6.5, "alu", g)
    k.cylx("fa_button", 25, 28, Y(246), Z(880), 5, "steel", g, "knurl")
    k.bv("brass_deflector", 15, Y(262), Z(805), 21, Y(236), Z(840), 1.5, "alu", g)
    k.b("upper_line_l", -15.8, Y(298), Z(560), -15.5, Y(296), Z(930), "alu_dark", g)
    k.cyl("barrel_nut", 0, Z(486), Z(500), 17, "alu_dark", g)

    g = "bolt"
    k.b("bcg_side", 15.8, Y(258), Z(652), 16.0, Y(240), Z(788), "steel", g)
    k.b("bcg_cut", 16.0, Y(254), Z(700), 16.1, Y(246), Z(740), "steel_light", g)

    g = "dust_cover"
    k.b("dust_cover", 15.6, Y(268), Z(640), 16.4, Y(262), Z(800), "alu", g)

    g = "charging_handle"
    k.bv("ch_body", -8, Y(242, 940), Z(925), 8, Y(228, 940), Z(950), 1, "alu", g)
    k.bv("ch_handle", -17, Y(242, 950), Z(944), 17, Y(228, 950), Z(960), 1.4, "alu", g)
    k.bv("ch_latch", -21, Y(241, 950), Z(944), -14, Y(229, 950), Z(964), 0.8, "alu_dark", g)

    # ======================================================================
    # lower receiver, trigger group controls, tan guard and grip
    # ======================================================================
    g = "lower"
    lower = P([(526, 300), (943, 300), (946, 328), (936, 352), (813, 358), (700, 353), (687, 423),
               (560, 387), (548, 330), (532, 316)])
    k.prof("lower", lower, -16, 16, "alu", g, step=14, bevel=2.5)
    for side, (a, b) in (("l", (-16.4, -16)), ("r", (16, 16.4))):
        k.prof("magwell_recess_" + side, P([(585, 312), (684, 312), (680, 380), (575, 360)]), a, b,
               "alu_dark", g, step=12, t=2, bevel=0.1)
        for nm, (px, py) in (("pivot", (545, 310)), ("takedown", (925, 312)), ("tpin", (760, 330)),
                             ("hpin", (800, 330))):
            k.pin("%s_%s" % (nm, side), (a + b) / 2, Y(py), Z(px), 2.6 if nm in ("pivot", "takedown") else 1.8,
                  a - 0.3 if side == "l" else a, b if side == "l" else b + 0.3, "steel", g)
    k.b("safe_mark", -16.5, Y(318), Z(860), -16.4, Y(310), Z(905), "text", g, text={"west": "SAFE"})
    k.b("semi_mark", -16.5, Y(345), Z(860), -16.4, Y(337), Z(905), "text", g, text={"west": "SEMI"})
    k.cyl("castle_nut", 0, Z(943), Z(957), 19, "alu_dark", g)
    k.b("end_plate", -20, Y(305, 945), Z(943), 20, Y(236, 945), Z(947), "steel", g)
    # tan oversized trigger guard
    guard = P([(694, 353), (702, 353), (706, 408), (750, 422), (795, 414), (806, 400), (806, 358),
               (814, 358), (814, 406), (800, 424), (750, 433), (702, 421)])
    k.prof("trigger_guard", guard, -7, 7, "tan", g, step=6, t=4, bevel=1.4)
    # tan ergonomic grip
    grip = P([(813, 358), (907, 344), (921, 394), (950, 466), (986, 537), (993, 580), (990, 594),
              (950, 600), (880, 596), (871, 580), (843, 516), (818, 466), (812, 410)])
    k.prof("grip", grip, -16, 16, "tan", g, "stipple", step=12, bevel=6)

    g = "bolt_catch"
    k.prof("bolt_catch", P([(686, 318), (700, 318), (702, 350), (690, 352)]), -18.5, -16, "alu_dark", g,
           step=6, t=2, bevel=0.6)
    g = "mag_release"
    k.cylx("mag_release", 16, 19.5, Y(342), Z(698), 4.5, "alu_dark", g, "knurl")
    g = "selector"
    k.pin("selector_hub", -16.8, Y(330), Z(852), 4.5, -18, -16, "steel", g)
    k.bv("selector_lever", -18.8, Y(334), Z(852), -16.8, Y(326), Z(890), 0.6, "steel", g, axis="x")
    g = "trigger"
    k.prof("trigger_blade", P([(758, 355), (768, 355), (776, 378), (778, 405), (772, 408), (768, 385),
                               (760, 370)]), -3, 3, "steel", g, step=5, t=3, bevel=0.6)

    # ======================================================================
    # buffer tube and tan adjustable stock
    # ======================================================================
    g = "stock"
    k.cyl("buffer_tube", 0, Z(957), Z(1100), 15.5, "alu", g)
    stock = P([(1043, 232), (1395, 227), (1436, 230), (1436, 501), (1371, 509), (1293, 434), (1243, 394),
               (1200, 380), (1143, 334), (1071, 330), (1050, 320), (1043, 300)])
    k.prof("stock_body", stock, -22, 22, "tan", g, step=14, bevel=6)
    k.prof("butt_pad", P([(1402, 228), (1438, 230), (1438, 502), (1400, 506)]), -23.5, 23.5, "tan_dark", g,
           "ribs", step=10, bevel=4)
    for side, (a, b) in (("l", (-22.3, -22)), ("r", (22, 22.3))):
        k.b("stock_seam_" + side, a, Y(256, 1220), Z(1050), b, Y(254, 1220), Z(1395), "tan_dark", g)
        for i, x in enumerate((1120, 1160, 1200, 1240, 1280, 1320)):
            k.cylx("stock_hole_%s_%d" % (side, i), a - 0.1, b + 0.1, Y(348, x), Z(x), 4, "tan_dark", g)
        k.cylx("qd_socket_" + side, a - 0.6 if side == "l" else a, b if side == "l" else b + 0.6, Y(395, 1340),
               Z(1340), 7, "steel", g)
    k.prof("adjust_lever", P([(1110, 360), (1185, 362), (1190, 384), (1120, 384)]), -6, 6, "tan_dark", g,
           step=8, t=3, bevel=1)
    k.cyl("lever_knob", Y(392, 1165), Z(1160), Z(1172), 5, "steel_dark", g)

    # ======================================================================
    # 30 rd aluminium magazine with its ribs
    # ======================================================================
    g = "magazine"
    mag = P([(585, 380), (688, 380), (680, 413), (660, 500), (640, 580), (619, 638), (612, 642),
             (520, 609), (523, 600), (560, 500), (597, 400)])
    k.prof("mag", mag, -12, 12, "mag", g, step=10, bevel=2)
    for j, off in enumerate((-30, 0, 30)):
        pts = [(640 + off * 0.9, 410), (622 + off * 0.95, 480), (602 + off, 550), (585 + off, 600)]
        for side, x in (("l", -12.4), ("r", 12)):
            for i in range(len(pts) - 1):
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                zc, yc = Z((x0 + x1) / 2), Y((y0 + y1) / 2, (x0 + x1) / 2)
                ang = -math.degrees(math.atan2(x1 - x0, y1 - y0))
                L = math.hypot(x1 - x0, y1 - y0) / scale((x0 + x1) / 2) / 2
                with k.frame("x", ang, 0, yc, zc):
                    k.b("mag_rib_%s_%d_%d" % (side, j, i), x, yc - L, zc - 1.6, x + 0.4, yc + L, zc + 1.6,
                        "mag_light", g)
    k.prof("mag_floor", P([(518, 604), (526, 600), (616, 634), (618, 646), (610, 648), (516, 614)]), -13, 13,
           "steel_dark", g, step=8, t=3, bevel=1)
    k.b("mag_round", -4, Y(384), Z(600), 4, Y(378), Z(680), "brass", g)

    m.regroup({}, pivots={"trigger": k.P(0, Y(356), Z(765)), "dust_cover": k.P(16, Y(268), Z(720)),
                          "magazine": k.P(0, Y(390), Z(635)), "bolt": k.P(0, 0, Z(720)),
                          "charging_handle": k.P(0, Y(235, 950), Z(950)), "selector": k.P(-17, Y(330), Z(852)),
                          "bolt_catch": k.P(-17, Y(320), Z(693)), "mag_release": k.P(17, Y(342), Z(698))})
    m.dynamic = {"bolt", "charging_handle", "trigger", "dust_cover", "magazine", "bolt_catch",
                 "mag_release", "selector"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(470, 905), Z(905))

ARMS = {
    "grip": ((Z(862), Y(358, 862)), (Z(930), Y(590, 930))), "trigger": (Z(770), Y(385)),
    "left": {"kind": "forend", "z": Z(330), "y_top": Y(205, 330), "y_bot": Y(318, 330), "w": 30},
}

DISPLAY = {"hand": 0.38, "fp": 0.39, "gui": 0.31, "tilt": 30}

ANIM = {
    "hands": {"left_arm": [("magazine", None, None), ("charging_handle", "ch_handle", None)]},
    "aim_above_mm": 42,
    "action": "bolt", "travel": 2.6, "locks_back": True,
    "charging": ("charging_handle", 2.8),
    "trigger": True, "trigger_angle": 12,
    "stop": {"bone": "bolt_catch", "rot": [-8, 0, 0]},
    "release": ("mag_release", [-0.18, 0, 0]),
    "selector": ("selector", [90, 0, 0]),
    "mag_dir": [0, -1, -0.1], "mag_far": 18, "recoil": 0.55, "recoil_time": 0.12, "shot_time": 0.1,
    "reload_time": 2.1, "reload_empty_time": 2.6,
}


def _shoot(c):
    a = anims.shoot(c)
    # the dust cover bounces on its hinge
    a.rot("dust_cover", 0.0, [0, 0, 0])
    a.rot("dust_cover", 0.03, [0, 0, -8], "easeOutQuad")
    a.rot("dust_cover", 0.1, [0, 0, 0], "easeOutBounce")
    return a


ANIMATIONS = anims.build(ANIM, {"shoot": _shoot})

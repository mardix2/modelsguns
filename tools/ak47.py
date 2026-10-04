"""AK-47: stamped receiver, wooden handguards, pistol grip and stock,
curved ribbed steel magazine.

Outlines are traced from a side photo (tools/silhouettes/ak47*.png,
1.376 px per mm, muzzle at x=25, bore at y=100); widths from real dimensions.
1 model unit = 16 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "steel": Material((92, 94, 100), 4),
    "steel_dark": Material((40, 41, 45), 4),
    "steel_light": Material((120, 122, 128), 5),
    "blued": Material((36, 38, 46), 4),
    "mag": Material((96, 98, 104), 4),
    "wood": Material((150, 82, 38), 5),
    "wood_dark": Material((100, 52, 24), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((222, 222, 212), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 16.0
S = Silhouette("ak47", 1.376, 25, 100)
Z, Y, P = S.zmm, S.ymm, S.poly


def build():
    m = Model("ak47", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # muzzle nut, front sight block, barrel, cleaning rod
    # ======================================================================
    g = "barrel"
    k.cyl("muzzle_nut", 0, Z(23), Z(60), 9.5, "blued", g)
    k.cyl("muzzle_nut_rear", 0, Z(60), Z(95), 8.6, "blued", g)
    k.cyl("muzzle_bore", 0, Z(22.5), Z(23), 4.2, "bore", g)
    for i, x in enumerate((40, 52)):
        k.b("muzzle_flat_%d" % i, -9.8, -3, Z(x), 9.8, 3, Z(x + 5), "steel_dark", g)
    fsb = P([(96, 88), (104, 88), (114, 40), (132, 40), (145, 88), (148, 120), (96, 120)])
    k.prof("front_sight_block", fsb, -9, 9, "blued", g, step=8, bevel=2)
    k.b("fs_window", -9.2, Y(80), Z(117), 9.2, Y(58), Z(130), "bore", g)
    k.cyl("fs_post", Y(52), Z(122), Z(125), 1.2, "steel_dark", g)
    k.cylx("fs_drum", -9.6, 9.6, Y(58), Z(120), 5.0, "steel", g)
    k.b("bayonet_lug", -4, Y(126), Z(100), 4, Y(118), Z(140), "blued", g)
    k.cyl("barrel", 0, Z(145), Z(600), 7.6, "blued", g)
    k.cyl("cleaning_rod", Y(117), Z(110), Z(385), 3.0, "steel_light", g)
    # gas block and gas tube with vent holes
    gb = P([(215, 118), (215, 94), (240, 72), (268, 66), (272, 118)])
    k.prof("gas_block", gb, -10, 10, "blued", g, step=8, bevel=2)
    k.cyl("gas_tube", Y(74), Z(262), Z(380), 9.5, "blued", g)
    for i in range(4):
        z = Z(290 + i * 18)
        for side, x in (("l", -9.9), ("r", 9.6)):
            k.b("gas_vent_%s_%d" % (side, i), x, Y(77), z, x + 0.3, Y(71), z + 6, "bore", g)

    # ======================================================================
    # wooden handguards (traced)
    # ======================================================================
    g = "handguard"
    up = P([(386, 51), (392, 46), (514, 46), (519, 51), (519, 80), (386, 80)])
    k.prof("upper_handguard", up, -16, 16, "wood", g, "wood", step=10, bevel=4)
    lo = P([(386, 80), (560, 80), (578, 72), (588, 76), (588, 138), (548, 140), (386, 134), (382, 108)])
    k.prof("lower_handguard", lo, -20, 20, "wood", g, "wood", step=10, bevel=5)
    for side, x in (("l", -16.3), ("r", 16)):
        k.b("vent_a_" + side, x, Y(82), Z(395), x + 0.3, Y(74), Z(430), "wood_dark", g)
        k.b("vent_b_" + side, x, Y(82), Z(460), x + 0.3, Y(74), Z(495), "wood_dark", g)
    k.cyl("handguard_ferrule", Y(100), Z(372), Z(384), 13, "blued", g)

    # ======================================================================
    # receiver (traced): trunnion, rear sight block, top cover, rivets
    # ======================================================================
    g = "receiver"
    rcv = S.rings([(583, 58), (935, 58), (935, 142), (583, 142)], src="metal")
    k.prof("receiver", rcv, -13, 13, "steel", g, step=10, bevel=2.5)
    rsb = P([(522, 78), (522, 58), (530, 46), (600, 40), (610, 46), (612, 78)])
    k.prof("rear_sight_block", rsb, -12, 12, "steel", g, step=8, bevel=2)
    k.prof("rear_sight_leaf", P([(540, 46), (548, 38), (612, 34), (612, 40)]), -6, 6, "steel_light", g,
           step=8, bevel=0.8)
    k.bv("rear_sight_slider", -8, Y(46), Z(568), 8, Y(36), Z(580), 1, "steel_light", g)
    k.pin("rear_sight_pivot", 0, Y(50), Z(533), 6, -12.6, 12.6, "steel_light", g)
    # stamped recesses, rivets
    for side, x in (("l", -13.3), ("r", 13)):
        k.b("trunnion_" + side, x, Y(120), Z(587), x + 0.3, Y(84), Z(700), "steel_dark", g)
        k.b("rcv_line_" + side, x, Y(122), Z(700), x + 0.3, Y(120), Z(915), "steel_dark", g)
        for i, (rx, ry) in enumerate(((600, 92), (618, 108), (690, 108), (740, 132), (760, 130),
                                      (900, 106), (870, 135))):
            k.pin("rivet_%s_%d" % (side, i), x + 0.15, Y(ry), Z(rx), 2.0,
                  x - 0.3 if side == "l" else x, x + 0.3 if side == "l" else x + 0.6, "steel_light", g)
    k.b("serial", -13.35, Y(132), Z(780), -13.3, Y(124), Z(825), "steel", g, text={"west": "1KZ334"})

    g = "top_cover"
    k.bv("top_cover", -12.6, Y(80), Z(612), 12.6, Y(58), Z(905), 3, "steel", g, edges="top")
    for i, z in enumerate((680, 740, 800, 860)):
        k.b("cover_rib_%d" % i, -12.8, Y(75), Z(z), 12.8, Y(64), Z(z + 6), "steel", g)
    k.b("cover_latch", -4, Y(84), Z(905), 4, Y(70), Z(925), "steel_light", g)

    # right side: ejection port, bolt carrier with charging handle, selector
    g = "bolt"
    k.b("ejection_port", 13, Y(100), Z(700), 13.2, Y(80), Z(790), "bore", g)
    k.b("bolt_carrier", 11, Y(92), Z(690), 13.1, Y(80), Z(800), "steel_light", g)
    k.bv("charging_handle", 13, Y(92), Z(700), 26, Y(84), Z(712), 1, "steel_light", g, axis="x")
    k.cylx("charging_knob", 22, 30, Y(88), Z(706), 4.5, "steel_light", g)

    g = "selector"
    k.pin("selector_pivot", 13.6, Y(98), Z(905), 4, 13, 14.6, "steel_light", g)
    k.bv("selector_lever", 13.2, Y(102), Z(760), 14.6, Y(94), Z(905), 0.4, "steel_light", g, axis="x")
    k.bv("selector_tab", 13.2, Y(114), Z(760), 16, Y(94), Z(775), 0.4, "steel_light", g, axis="x")

    # trigger guard and magazine catch
    g = "receiver"
    guard = P([(758, 140), (766, 140), (768, 180), (776, 184), (818, 184), (826, 176), (828, 140),
               (836, 140), (832, 182), (822, 192), (772, 192), (762, 186)])
    k.prof("trigger_guard", guard, -6, 6, "steel", g, step=6, t=3, bevel=1)
    k.prof("mag_catch", P([(740, 140), (752, 140), (752, 176), (746, 180), (740, 172)]), -6, 6, "steel", g,
           step=6, t=3, bevel=1)

    g = "trigger"
    k.prof("trigger", P([(800, 140), (808, 140), (818, 160), (822, 178), (816, 180), (808, 162), (800, 150)]),
           -3.5, 3.5, "steel_light", g, step=6, t=3, bevel=0.6)

    # ======================================================================
    # pistol grip and stock (traced)
    # ======================================================================
    g = "stock"
    grip = P([(837, 142), (880, 138), (905, 188), (924, 211), (946, 247), (944, 262), (924, 277),
              (905, 280), (887, 261), (855, 211), (833, 161)])
    k.prof("grip", grip, -15, 15, "wood", g, "wood", step=10, bevel=5)
    stock = P([(923, 95), (1000, 103), (1060, 100), (1130, 95), (1212, 95), (1218, 102), (1222, 161),
               (1218, 220), (1209, 236), (1200, 238), (1082, 197), (991, 168), (945, 152), (923, 150)])
    k.prof("stock", stock, -19, 19, "wood", g, "wood", step=12, bevel=6)
    k.prof("butt_plate", P([(1212, 96), (1219, 101), (1224, 161), (1219, 221), (1210, 238), (1205, 237)]), -19.5, 19.5,
           "steel", g, step=8, t=3, bevel=2)
    k.prof("stock_tang", P([(918, 92), (935, 92), (935, 142), (918, 150)]), -12, 12, "steel", g, step=6,
           bevel=2)
    k.pin("sling_swivel", 0, Y(181), Z(1050), 4, -19.6, 19.6, "steel_light", g)

    # ======================================================================
    # magazine (traced) with ribs and a round
    # ======================================================================
    g = "magazine"
    mag = P([(669, 138), (653, 179), (633, 211), (610, 238), (587, 265), (583, 271), (646, 333),
             (651, 328), (665, 302), (692, 256), (710, 220), (724, 179), (730, 138)])
    k.prof("mag", mag, -12, 12, "mag", g, step=8, bevel=2.5)
    # ribs follow the curve: segments between centre points on the photo
    pts = [(700, 142), (690, 179), (672, 215), (651, 247), (628, 280)]
    for side, x in (("l", -12.5), ("r", 12)):
        for j, off in enumerate((-14, 0, 14)):
            for i in range(len(pts) - 1):
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                zc, yc = Z((x0 + x1) / 2 + off), Y((y0 + y1) / 2)
                ang = -math.degrees(math.atan2(x1 - x0, y1 - y0))
                with k.frame("x", ang, 0, yc, zc):
                    k.b("mag_rib_%s_%d_%d" % (side, j, i), x, yc - 15, zc - 1.6, x + 0.5, yc + 15, zc + 1.6,
                        "steel_light", g)
    k.b("mag_round", -4.5, Y(142), Z(672), 4.5, Y(136), Z(728), "brass", g)

    m.regroup({}, pivots={"magazine": k.P(0, Y(140), Z(700)), "trigger": k.P(0, Y(142), Z(804)),
                          "bolt": k.P(13, Y(88), Z(745)), "selector": k.P(13.6, Y(98), Z(905)),
                          "top_cover": k.P(0, Y(70), Z(905))})
    m.dynamic = {"magazine", "trigger", "bolt", "selector", "top_cover"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(210), Z(888))


ARMS = {
    "grip": ((Z(858), Y(146)), (Z(925), Y(272))), "grip_w": 15, "grip_d": 15.5,
    "trigger": (Z(812), Y(166)),
    "left": {"kind": "forend", "z": Z(470), "y_top": Y(60), "y_bot": Y(134), "w": 20},
}

DISPLAY = {"hand": 0.34, "fp": 0.36, "gui": 0.27, "tilt": 30, "push": -2.5}

ANIM = {
    "action": "bolt", "travel": 120 / U, "locks_back": False,
    "trigger": True, "trigger_angle": 12,
    "selector": ("selector", [14, 0, 0]),
    "mag_rock": 20, "mag_dir": [0, -1, -0.1], "mag_far": 22, "mag_gap": 0.55,
    "recoil": 0.8, "recoil_time": 0.12, "shot_time": 0.1, "cycle_back": 0.025, "cycle_fwd": 0.05,
    "reload_time": 2.3, "reload_empty_time": 2.9,
    "reload_tilt": [6, 12, -26], "reload_lift": [-1.0, 1.2, -1.5],
}

ANIMATIONS = anims.build(ANIM)

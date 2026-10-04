"""Colt M1911A1 (.45 ACP), WWII parkerized finish: barrel bushing and
recoil spring plug, narrow slide nose, low ejection port, vertical rear
serrations, GI blade sights, spur hammer, grip safety with short tang,
arched serrated mainspring housing with lanyard loop, checkered brown grips.

Outlines are measured on a side photo (right side, mirrored; 4.6 px per mm,
muzzle at x=8, bore at y=150); widths from real dimensions (slide 23.4 mm,
frame 22 mm, 33 mm over the grips).  1 model unit = 7 mm.
"""

import math

import anims
from bbgen import Material, MM, Model
from trace import Silhouette

MATERIALS = {
    "park": Material((128, 126, 114), 4),
    "park_dark": Material((84, 82, 74), 4),
    "park_light": Material((160, 158, 146), 4),
    "park_deep": Material((58, 57, 52), 3),
    "grip": Material((104, 52, 42), 5),
    "grip_dark": Material((66, 32, 26), 4),
    "brass": Material((178, 142, 66), 5),
    "text": Material((128, 126, 114), 4, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

U = 7.0
S = Silhouette("m1911", 4.6, 8, 150)
Z, Y, P = S.zmm, S.ymm, S.poly
RAKE = 18.0
SW, FW = 11.7, 11.0          # half widths: slide, frame


def circle(cx, cy, r, n=10):
    return P([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)])


def side_x(side, a, b):
    """outer face x of a side part spanning a..b"""
    return a if side == "l" else b


def build():
    m = Model("m1911", MATERIALS, density=8)
    k = MM(m, U)

    # ======================================================================
    # slide: full-width upper body, narrower rounded nose around the recoil
    # spring, rear serrations, GI sights, low ejection port (right)
    # ======================================================================
    g = "slide"
    body = P([(20, 104), (28, 95), (40, 93), (850, 94), (862, 108), (872, 140), (877, 207), (200, 207),
              (160, 192), (130, 177), (20, 175)])
    k.prof("slide", body, -SW, SW, "park", g, step=14, bevel=2.2)
    nose = P([(20, 175), (130, 177), (160, 192), (200, 207), (205, 207), (204, 253), (30, 253), (20, 244)])
    k.prof("slide_nose", nose, -SW + 0.9, SW - 0.9, "park", g, step=12, bevel=3)
    for side, x in (("l", -SW - 0.2), ("r", SW)):
        for i in range(20):
            xs = 666 + i * 7.2
            k.b("serr_%s_%02d" % (side, i), x, Y(206), Z(xs), x + 0.2, Y(120), Z(xs + 3.4), "park_deep", g)
    k.b("slide_line_l", -SW - 0.15, Y(124), Z(22), -SW, Y(122), Z(660), "park_dark", g)
    k.b("slide_line_r", SW, Y(124), Z(22), SW + 0.15, Y(122), Z(440), "park_dark", g)
    k.b("ejection_port", SW - 0.9, Y(132), Z(438), SW + 0.05, Y(97), Z(568), "park_deep", g)
    k.b("port_chamber", SW - 0.5, Y(127), Z(446), SW + 0.1, Y(98), Z(562), "park_light", g)
    k.b("extractor", SW, Y(118), Z(568), SW + 0.3, Y(106), Z(650), "park_dark", g)
    k.prof("front_sight", P([(35, 94), (45, 84), (60, 81), (70, 84), (80, 94)]), -1.3, 1.3, "park", g,
           step=6, t=2, bevel=0.4)
    k.prof("rear_sight", P([(784, 95), (792, 86), (797, 76), (806, 76), (812, 86), (820, 95)]), -5.5, 5.5,
           "park", g, step=6, t=2, bevel=0.6)
    k.b("rear_notch", -1.2, Y(86), Z(790), 1.2, Y(75), Z(822), "bore", g)

    # ======================================================================
    # barrel: bushing with the recoil spring plug, crown, hood in the port
    # ======================================================================
    g = "barrel"
    k.cyl("bushing", Y(150), Z(9), Z(21), 10.4, "park_dark", g)
    k.cyl("barrel_crown", Y(150), Z(8.6), Z(9), 7.3, "park_light", g)
    k.cyl("muzzle_bore", Y(150), Z(8.4), Z(8.6), 5.7, "bore", g)
    k.cyl("barrel_body", Y(150), Z(21), Z(600), 7.3, "park_light", g)
    k.b("hood_top", 1, Y(130), Z(440), SW - 1, Y(97) + 0.08, Z(566), "park_light", g)
    k.cyl("spring_plug", Y(222), Z(9), Z(24), 5.6, "park", g)

    # ======================================================================
    # frame: dust cover, round trigger guard, grip, tang
    # ======================================================================
    g = "frame"
    frame = P([(205, 207), (870, 207), (882, 205), (898, 225), (902, 237), (931, 246), (974, 252), (988, 263),
               (990, 278), (982, 285), (936, 289), (908, 304), (891, 328), (887, 345), (888, 369), (921, 438),
               (909, 447), (958, 523), (958, 530), (995, 606), (998, 617), (996, 660), (990, 668), (955, 673),
               (849, 688), (749, 690), (697, 523), (678, 448), (669, 430), (653, 413), (623, 400), (505, 400),
               (477, 392), (459, 378), (448, 362), (442, 344), (440, 306), (435, 294), (420, 277), (395, 267),
               (216, 266), (209, 264), (205, 254)])
    hole = P([(470, 282), (490, 278), (580, 280), (596, 293), (606, 320), (608, 345), (602, 362), (588, 378),
              (572, 386), (560, 387), (495, 387), (478, 380), (465, 366), (458, 345), (456, 320), (460, 298)])
    k.prof("frame", [frame, hole], -FW, FW, "park", g, step=14, bevel=2)
    k.b("model_mark", FW, Y(224), Z(330), FW + 0.15, Y(210), Z(470), "text", g,
        text={"east": "M1911 A1 U.S. ARMY"})
    k.b("frame_mark", FW, Y(232), Z(560), FW + 0.15, Y(214), Z(700), "text", g,
        text={"east": "UNITED STATES PROPERTY"})
    k.b("serial", FW, Y(250), Z(590), FW + 0.15, Y(236), Z(680), "text", g, text={"east": "No 923665"})
    # grip safety (tang and the lever along the back strap)
    gs = P([(870, 207), (882, 205), (898, 225), (902, 237), (931, 246), (974, 252), (988, 263), (990, 278),
            (982, 285), (936, 289), (908, 304), (891, 328), (887, 345), (888, 369), (921, 438), (909, 447),
            (895, 442), (871, 430), (861, 386), (865, 342), (879, 302), (888, 280), (878, 240)])
    k.prof("grip_safety", gs, -FW - 0.25, FW + 0.25, "park", g, step=10, bevel=1.4)
    # arched mainspring housing, finely serrated, lanyard loop
    msh = P([(898, 446), (912, 446), (958, 523), (958, 530), (995, 606), (998, 617), (996, 660), (990, 668),
             (950, 673), (930, 600), (905, 500)])
    k.prof("mainspring_housing", msh, -FW - 0.25, FW + 0.25, "park_dark", g, "serration", step=10, bevel=1)
    k.cylx("lanyard_loop", -2.5, 2.5, Y(682), Z(970), 2.4, "park_dark", g)
    # checkered grips with slotted screws
    grip = P([(657, 254), (667, 242), (682, 233), (801, 229), (810, 233), (814, 242), (826, 305), (845, 367),
              (867, 430), (904, 492), (932, 555), (948, 617), (951, 674), (945, 681), (750, 682), (745, 676),
              (714, 555), (689, 430), (670, 336), (657, 262)])
    for side, (a, b) in (("l", (-FW - 2.6, -FW)), ("r", (FW, FW + 2.6))):
        k.prof("grip_" + side, grip, a, b, "grip", g, "checker", step=12, bevel=1)
        o = side_x(side, a, b)
        for j, (cx, cy) in enumerate(((740, 282), (866, 622))):
            k.prof("grip_bush_%s_%d" % (side, j), circle(cx, cy, 15, 10), o - 0.2 if side == "l" else o - 0.4,
                   o + 0.4 if side == "l" else o + 0.2, "grip_dark", g, step=6, t=2, bevel=0.3)
            k.pin("grip_screw_%s_%d" % (side, j), o, Y(cy), Z(cx), 2.4, o - 0.6 if side == "l" else o - 0.2,
                  o + 0.2 if side == "l" else o + 0.6, "park_light", g)
            k.b("screw_slot_%s_%d" % (side, j), o - 0.65 if side == "l" else o + 0.55, Y(cy) - 0.4, Z(cx) - 2,
                o - 0.55 if side == "l" else o + 0.65, Y(cy) + 0.4, Z(cx) + 2, "park_deep", g)
    # thumb safety (left), magazine catch, pins
    k.prof("thumb_safety", P([(812, 209), (872, 209), (880, 222), (860, 236), (820, 232)]), -FW - 1.6, -FW,
           "park", g, step=8, t=2, bevel=0.5)
    k.prof("safety_paddle", P([(792, 205), (826, 205), (826, 216), (792, 216)]), -FW - 3.6, -FW, "park", g,
           "knurl", step=6, t=2, bevel=0.5)
    k.pin("mag_catch", -FW - 0.7, Y(360), Z(646), 4.4, -FW - 1.4, -FW, "park", g)
    k.prof("mag_catch_lock", P([(636, 346), (672, 343), (690, 352), (690, 370), (672, 378), (646, 380),
                                (633, 368)]), FW, FW + 0.2, "park_light", g, step=6, t=2, bevel=0.1)
    k.pin("mag_catch_end", FW + 0.25, Y(360), Z(646), 2.6, FW, FW + 0.5, "park_dark", g)
    for side, (a, b) in (("l", (-FW - 0.6, -FW)), ("r", (FW, FW + 0.6))):
        k.pin("sear_pin_" + side, (a + b) / 2, Y(263), Z(818), 1.6, a, b, "park_light", g)
        k.pin("hammer_pin_" + side, (a + b) / 2, Y(233), Z(863), 1.8, a, b, "park_light", g)
        k.pin("gs_pin_" + side, (a + b) / 2, Y(260), Z(908), 1.6, a, b, "park_light", g)
    k.pin("slide_stop_pin_end", FW + 0.3, Y(232), Z(515), 2.2, FW, FW + 0.6, "park_light", g)

    g = "slide_stop"
    k.prof("slide_stop", P([(500, 224), (612, 216), (640, 208), (672, 206), (672, 222), (645, 232), (500, 242)]),
           -FW - 1.6, -FW, "park", g, "knurl", step=8, t=2, bevel=0.5)
    k.pin("slide_stop_pin", -FW - 0.8, Y(232), Z(515), 2.6, -FW - 1.9, -FW, "park_light", g)

    g = "trigger"
    trig = P([(573, 279), (580, 280), (596, 293), (606, 320), (608, 345), (602, 362), (588, 378), (572, 386),
              (570, 382), (582, 366), (589, 345), (589, 315), (584, 295)])
    k.prof("trigger", trig, -3.5, 3.5, "park_dark", g, "serration", step=6, t=2, bevel=0.5)

    g = "hammer"
    ham = P([(866, 128), (876, 124), (902, 124), (926, 113), (941, 118), (941, 128), (911, 141), (889, 162),
             (883, 182), (884, 204), (870, 206)])
    k.prof("hammer", ham, -3.6, 3.6, "park_dark", g, "knurl", step=8, t=3, bevel=0.6)

    # ======================================================================
    # magazine: tube in the grip, flat base
    # ======================================================================
    g = "magazine"
    mz, my = Z(762), Y(500)
    with k.frame("x", -RAKE, 0, my, mz):
        k.b("mag_body", -10, Y(688), mz - 13, 10, Y(330), mz + 13, "park_dark", g)
        k.b("mag_round", -5.5, Y(330), mz - 12, 5.5, Y(306), mz + 12, "brass", g)
    k.prof("mag_base", P([(736, 688), (850, 686), (850, 694), (738, 701)]), -10.5, 10.5, "park_dark", g,
           step=8, t=3, bevel=1)

    m.regroup({}, pivots={"trigger": k.P(0, Y(300), Z(580)), "magazine": k.P(0, my, mz),
                          "slide": k.P(0, Y(150), Z(450)), "barrel": k.P(0, Y(150), Z(300)),
                          "slide_stop": k.P(-12, Y(232), Z(515)), "hammer": k.P(0, Y(200), Z(878))})
    m.dynamic = {"slide", "barrel", "magazine", "trigger", "slide_stop", "hammer"}
    return m


GRIP_POINT = MM(None, U).P(0, Y(480), Z(820))

ARMS = {
    "grip": ((Z(790), Y(300)), (Z(870), Y(660))), "trigger": (Z(578), Y(330)),
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

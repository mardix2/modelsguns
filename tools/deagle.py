"""Desert Eagle Mark XIX (.50 AE), brushed stainless with black controls.

Real proportions: 270 mm long, 150 mm tall, 32 mm wide, 152 mm barrel.
Scale: 1 unit ~= 7 mm.  Muzzle points north (-Z), bore axis x=8, y=17.8.
"""

from bbgen import Material, Model

MATERIALS = {
    "ss": Material((166, 169, 175), 3),          # brushed stainless
    "ss_dark": Material((126, 129, 135), 3),
    "ss_deep": Material((88, 90, 95), 3),
    "black": Material((36, 36, 39), 3),
    "rubber": Material((30, 30, 31), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((236, 236, 228), 2, edge=False),
    "red": Material((184, 34, 30), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

BY = 17.8   # bore axis height


def build():
    m = Model("deagle", MATERIALS, density=8)
    B = m.box

    # ======================================================================
    # barrel: polygonal top with integral Picatinny rail, gas lug below
    # ======================================================================
    g = "barrel"
    B("barrel_side", 6.0, 15.8, 0.0, 10.0, 19.85, 17.9, "ss", g, "brushed",
      text={"west": "DESERT EAGLE .50 AE", "east": "MAGNUM .50 AE"})
    B("barrel_top", 7.05, 19.85, 0.0, 8.95, 20.9, 17.9, "ss", g, "brushed")
    m.edge("barrel_slope_l", "z", 0.0, 17.9, 6.0, 20.9, -1, 1, 1.05, "ss", g)
    m.edge("barrel_slope_r", "z", 0.0, 17.9, 10.0, 20.9, 1, 1, 1.05, "ss", g)
    m.edge("barrel_low_l", "z", 0.0, 17.9, 6.0, 15.8, -1, -1, 0.3, "ss", g)
    m.edge("barrel_low_r", "z", 0.0, 17.9, 10.0, 15.8, 1, -1, 0.3, "ss", g)
    B("barrel_groove_l", 5.98, 16.35, 0.6, 6.0, 16.5, 17.3, "ss_deep", g)
    B("barrel_groove_r", 10.0, 16.35, 0.6, 10.02, 16.5, 17.3, "ss_deep", g)
    # muzzle face: big bore with crown, chamfered front edges
    m.cyl_z("muzzle_crown", 8.0, BY, -0.06, 0.02, 1.15, "ss_dark", g)
    m.cyl_z("muzzle_bore", 8.0, BY, -0.1, -0.06, 0.82, "bore", g)
    # integral rail
    B("rail_base", 7.15, 20.9, 0.9, 8.85, 21.1, 17.2, "ss", g)
    m.teeth_z("rail_t", "up", 7.15, 8.85, 21.1, 0.3, 1.1, 17.2, "ss", g, period=1.43, tooth=0.85)
    # front sight on the rail front
    m.bevel("front_sight", 7.68, 21.1, 0.25, 8.32, 22.45, 1.85, 0.08, "black", g, axis="y")
    B("front_sight_dot", 7.92, 21.95, 1.85, 8.08, 22.11, 1.87, "white", g)
    # gas lug under the barrel
    m.bevel("gas_lug", 6.55, 14.55, 0.25, 9.45, 15.85, 15.5, 0.25, "ss", g, "brushed")
    m.cyl_z("gas_port", 8.0, 15.2, 0.21, 0.25, 0.32, "bore", g)

    # ======================================================================
    # slide
    # ======================================================================
    g = "slide"
    B("slide_body", 5.72, 15.3, 17.9, 10.28, 19.5, 31.4, "ss", g, "brushed")
    B("slide_top", 6.62, 19.5, 17.9, 9.38, 20.4, 38.3, "ss", g, "brushed")
    m.edge("slide_chamfer_l", "z", 17.9, 38.3, 5.72, 20.4, -1, 1, 0.9, "ss", g)
    m.edge("slide_chamfer_r", "z", 17.9, 38.3, 10.28, 20.4, 1, 1, 0.9, "ss", g)
    m.edge("slide_front_top", "x", 6.62, 9.38, 20.4, 17.9, 1, -1, 0.35, "ss", g)
    m.edge("slide_low_l", "z", 17.9, 38.3, 5.72, 15.3, -1, -1, 0.22, "ss", g)
    m.edge("slide_low_r", "z", 17.9, 38.3, 10.28, 15.3, 1, -1, 0.22, "ss", g)
    for side, (a, b) in (("l", (5.7, 5.72)), ("r", (10.28, 10.3))):
        B("slide_groove_" + side, a, 16.05, 18.3, b, 16.2, 31.2, "ss_deep", g)
        B("slide_groove_top_" + side, a, 19.05, 18.3, b, 19.15, 31.2, "ss_deep", g)
    # rear serrations
    B("slide_serr_core", 5.92, 15.3, 31.4, 10.08, 19.5, 38.3, "ss_dark", g)
    z, i = 31.6, 0
    while z + 0.3 <= 37.7:
        B("slide_serr_%02d" % i, 5.72, 15.55, z, 10.28, 19.3, z + 0.3, "ss", g, "brushed")
        z, i = z + 0.6, i + 1
    B("slide_rear_band", 5.72, 15.3, 37.7, 10.28, 19.5, 38.3, "ss", g, "brushed")
    m.bevel("slide_rear_plate", 6.2, 15.5, 38.3, 9.8, 20.0, 38.45, 0.25, "ss_dark", g)
    # ejection port with the rotating bolt visible
    B("ejection_port", 10.28, 18.3, 19.6, 10.3, 19.9, 24.2, "bore", g)
    m.cyl_z("bolt_body", 9.65, 19.1, 19.8, 24.0, 0.66, "ss_dark", g)
    for k in range(3):
        B("bolt_lug_%d" % k, 10.1, 18.55 + k * 0.32, 19.8, 10.3, 18.75 + k * 0.32, 20.3, "ss_deep", g)
    B("extractor", 10.28, 18.45, 24.2, 10.36, 18.9, 26.7, "ss_dark", g)
    # ambidextrous slide safety levers (on "fire": lever down, red dot shown)
    for side, (a, b, s_) in (("l", (5.38, 5.72, -1)), ("r", (10.28, 10.62, 1))):
        m.pin_x("safety_hub_" + side, (a + b) / 2, 18.5, 36.6, 0.42, a, b, "black", g)
        with m.frame(("x", 28, (8, 18.5, 36.6))):
            m.bevel("safety_lever_" + side, a + 0.04, 17.95, 33.9, b - 0.04, 18.55, 36.6, 0.08, "black", g,
                    "knurl", axis="x")
        B("safety_red_" + side, a - 0.01 if s_ < 0 else b - 0.01, 19.1, 36.35,
          a + 0.01 if s_ < 0 else b + 0.01, 19.35, 36.6, "red", g)
    # rear sight with two white dots
    m.bevel("rs_base", 6.95, 20.4, 35.8, 9.05, 20.85, 37.6, 0.12, "black", g)
    m.bevel("rs_ear_l", 6.95, 20.85, 35.8, 7.75, 21.6, 37.6, 0.08, "black", g)
    m.bevel("rs_ear_r", 8.25, 20.85, 35.8, 9.05, 21.6, 37.6, 0.08, "black", g)
    B("rs_dot_l", 7.27, 21.05, 37.6, 7.43, 21.21, 37.62, "white", g)
    B("rs_dot_r", 8.57, 21.05, 37.6, 8.73, 21.21, 37.62, "white", g)

    # ======================================================================
    # frame
    # ======================================================================
    g = "frame"
    m.bevel("dust_cover", 6.3, 13.15, 6.8, 9.7, 15.35, 17.95, 0.35, "ss", g, "brushed")
    for k, x in enumerate((7.3, 8.7)):
        m.cyl_z("guide_rod_%d" % k, x, 14.2, 6.74, 6.8, 0.3, "ss_deep", g)
    m.bevel("frame_rail", 6.0, 13.15, 17.9, 10.0, 15.35, 38.0, 0.2, "ss", g, "brushed")
    m.bevel("frame_tang", 6.6, 13.4, 37.9, 9.4, 14.9, 39.4, 0.3, "ss", g, "brushed")
    # trigger guard (rounded, small hook in front)
    m.bevel("tg_front", 7.45, 10.2, 13.6, 8.55, 13.3, 14.5, 0.14, "ss", g, axis="y")
    m.bevel("tg_bottom", 7.45, 9.35, 14.3, 8.55, 10.1, 24.3, 0.14, "ss", g)
    m.edge("tg_corner", "x", 7.47, 8.53, 9.35, 13.6, -1, -1, 0.95, "ss", g)
    # barrel release (left, front), slide stop, magazine release, pins
    m.pin_x("barrel_release", 6.1, 14.1, 15.6, 0.48, 5.85, 6.35, "black", g)
    B("barrel_release_grip", 5.83, 13.95, 15.25, 5.85, 14.25, 15.95, "ss_deep", g)
    m.bevel("slide_stop", 5.75, 14.85, 22.5, 6.0, 15.35, 28.0, 0.08, "black", g, axis="x")
    m.bevel("slide_stop_pad", 5.6, 14.65, 26.6, 6.0, 15.45, 28.2, 0.1, "black", g, "knurl", axis="x")
    m.pin_x("mag_release", 5.85, 12.6, 23.1, 0.42, 5.6, 6.05, "black", g)
    for side, (a, b) in (("l", (5.94, 6.02)), ("r", (9.98, 10.06))):
        m.pin_x("pin_a_" + side, (a + b) / 2, 14.1, 19.4, 0.14, a, b, "ss_dark", g)
        m.pin_x("pin_b_" + side, (a + b) / 2, 14.3, 34.6, 0.14, a, b, "ss_dark", g)
        m.pin_x("pin_c_" + side, (a + b) / 2, 13.6, 31.0, 0.14, a, b, "ss_dark", g)

    g = "trigger"
    m.bevel("trigger_top", 7.65, 12.2, 17.6, 8.35, 13.25, 18.3, 0.08, "black", g, axis="y")
    with m.frame(("x", 18, (8, 12.25, 17.95))):
        m.bevel("trigger_mid", 7.65, 11.1, 17.6, 8.35, 12.3, 18.3, 0.08, "black", g, axis="y")
    with m.frame(("x", 42, (8, 11.15, 17.75))):
        m.bevel("trigger_tip", 7.65, 10.55, 17.45, 8.35, 11.2, 18.1, 0.08, "black", g, axis="y")

    g = "hammer"
    with m.frame(("x", -24, (8, 15.6, 38.6))):
        m.bevel("hammer_body", 7.55, 15.0, 38.2, 8.45, 17.4, 39.0, 0.12, "black", g, axis="y")
        m.bevel("hammer_spur", 7.5, 17.1, 38.4, 8.5, 17.75, 40.1, 0.1, "black", g, "knurl")
        m.pin_x("hammer_pin", 8.0, 15.6, 38.6, 0.2, 7.45, 8.55, "ss_dark", g)

    # ======================================================================
    # grip (18 deg rake): metal frame, wrap-around checkered panels
    # ======================================================================
    g = "grip"
    with m.frame(("x", -18, (8, 13.2, 26.6))):
        m.bevel("grip_frame", 6.05, 0.75, 26.2, 9.95, 13.5, 33.8, 0.3, "ss", g, "brushed", axis="y")
        m.bevel("grip_backstrap", 6.4, 1.0, 33.6, 9.6, 13.0, 34.15, 0.22, "ss", g, "serration", axis="y")
        m.bevel("grip_beaver", 6.5, 12.6, 33.6, 9.5, 13.6, 35.6, 0.25, "ss", g)
        m.bevel("grip_front_strap", 6.5, 1.2, 25.85, 9.5, 12.2, 26.3, 0.2, "ss_dark", g, "checker",
                axis="y")
        for side, (a, b) in (("l", (5.72, 6.06)), ("r", (9.94, 10.28))):
            m.bevel("panel_" + side, a, 1.5, 26.6, b, 12.3, 33.3, 0.18, "rubber", g, "checker",
                    axis="x")
            m.pin_x("panel_screw_" + side, (a + b) / 2 + (-0.05 if side == "l" else 0.05), 6.9, 30.0,
                    0.22, a - 0.06 if side == "l" else b - 0.02, a + 0.02 if side == "l" else b + 0.06,
                    "ss_dark", g)
            B("panel_logo_" + side, a - 0.01 if side == "l" else b - 0.01, 10.3, 28.5,
              a + 0.01 if side == "l" else b + 0.01, 11.3, 31.4, "rubber", g)

    g = "magazine"
    with m.frame(("x", -18, (8, 13.2, 26.6))):
        B("mag_body", 6.5, 0.75, 26.6, 9.5, 12.1, 33.0, "ss_deep", g)
        B("mag_round", 7.2, 12.1, 27.0, 8.8, 12.7, 32.4, "brass", g)
        m.cyl_z("mag_round_tip", 8.0, 12.4, 26.4, 27.0, 0.3, "brass", g)
        m.bevel("mag_base", 6.0, 0.05, 25.9, 10.0, 0.75, 34.0, 0.2, "ss", g, "brushed", axis="y")
        B("mag_base_lip", 6.6, 0.15, 25.55, 9.4, 0.65, 25.9, "ss", g)

    m.regroup({}, pivots={"trigger": (8, 13.2, 17.95), "hammer": (8, 15.6, 38.6),
                          "magazine": (8, 13.0, 26.6), "slide": (8, 18.0, 28.0)})
    m.dynamic = {"slide", "trigger", "hammer", "magazine"}
    return m


GRIP_POINT = (8.0, 7.5, 28.2)

DISPLAY = {"hand": 0.24, "fp": 0.27, "gui": 0.38, "tilt": 0, "push": 0.0}

_D = (0.951, 0.309)   # 18 deg grip axis
ANIMATIONS = {
    "shoot": (0.24, {
        "slide": {"position": {0.0: [0, 0, 0], 0.05: [0, 0, 5.6], 0.24: [0, 0, 0]}},
        "hammer": {"rotation": {0.0: [0, 0, 0], 0.05: [35, 0, 0], 0.24: [0, 0, 0]}},
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [-14, 0, 0], 0.16: [0, 0, 0]}},
    }),
    "reload": (1.9, {
        "magazine": {"position": {0.0: [0, 0, 0], 0.25: [0, -5 * _D[0], 5 * _D[1]],
                                  0.55: [0, -24 * _D[0], 24 * _D[1]], 0.56: [0, -24 * _D[0], 24 * _D[1]],
                                  1.05: [0, -5 * _D[0], 5 * _D[1]], 1.2: [0, 0, 0]}},
        "slide": {"position": {1.4: [0, 0, 0], 1.55: [0, 0, 5.6], 1.7: [0, 0, 0]}},
    }),
}

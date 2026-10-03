"""IMI / Magnum Research Desert Eagle Mark XIX (.50 AE), satin stainless.

Scale: 1 model unit ~= 9 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((150, 152, 158), 5),      # satin stainless
    "steel_mid": Material((118, 120, 126), 5),
    "steel_dark": Material((58, 59, 63), 4),
    "black": Material((34, 34, 36), 4),
    "rubber": Material((30, 30, 30), 5),
    "brass": Material((178, 142, 66), 6),
    "white": Material((232, 232, 224), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("deagle", MATERIALS, density=8)
    B = m.box

    # ======================================================================
    # fixed barrel: triangular profile, top rail, under-lug
    # ======================================================================
    g = "barrel"
    B("barrel_lower", 6.6, 15.2, 0.0, 9.4, 17.9, 15.4, "steel", g,
      text={"west": "DESERT EAGLE", "east": ".50 AE"})
    B("barrel_top", 7.2, 17.9, 0.0, 8.8, 18.5, 15.4, "steel", g)
    m.edge("barrel_shoulder_l", "z", 0.0, 15.4, 6.6, 18.5, -1, 1, 0.6, "steel", g)
    m.edge("barrel_shoulder_r", "z", 0.0, 15.4, 9.4, 18.5, 1, 1, 0.6, "steel", g)
    m.edge("barrel_bottom_l", "z", 0.0, 15.4, 6.6, 15.2, -1, -1, 0.25, "steel", g)
    m.edge("barrel_bottom_r", "z", 0.0, 15.4, 9.4, 15.2, 1, -1, 0.25, "steel", g)
    m.edge("barrel_nose", "x", 7.2, 8.8, 18.5, 0.0, 1, -1, 0.35, "steel", g)
    m.rail_z("barrel_rail", 7.4, 8.6, 18.67, 0.8, 14.8, "steel_mid", g,
             period=1.1, tooth=0.7, h=0.2)
    # under-lug with the gas port hole
    m.bevel("barrel_lug", 7.0, 13.6, 0.2, 9.0, 15.25, 9.0, 0.3, "steel", g)
    B("gas_port", 7.7, 14.15, 0.16, 8.3, 14.75, 0.2, "bore", g)
    # big .50 muzzle
    m.cyl_z("muzzle_crown", 8.0, 16.6, -0.08, 0.02, 0.95, "steel_mid", g)
    m.cyl_z("muzzle_bore", 8.0, 16.6, -0.12, -0.08, 0.6, "bore", g)
    # front sight blade
    B("front_sight", 7.85, 18.85, 0.5, 8.15, 19.55, 1.5, "black", g)
    B("front_sight_dot", 7.92, 19.2, 1.5, 8.08, 19.36, 1.52, "white", g)

    # ======================================================================
    # slide
    # ======================================================================
    g = "slide"
    B("slide_body", 6.65, 15.0, 15.4, 9.35, 17.85, 25.0, "steel", g)
    B("slide_top", 7.1, 17.85, 15.4, 8.9, 18.3, 29.6, "steel", g)
    m.edge("slide_chamfer_l", "z", 15.4, 29.6, 6.65, 18.3, -1, 1, 0.45, "steel", g)
    m.edge("slide_chamfer_r", "z", 15.4, 29.6, 9.35, 18.3, 1, 1, 0.45, "steel", g)
    B("slide_serr_core", 6.8, 15.0, 25.0, 9.2, 17.85, 29.6, "steel_mid", g)
    z = 25.15
    i = 0
    while z + 0.25 <= 29.4:
        B("slide_serr_%d" % i, 6.65, 15.25, z, 9.35, 17.6, z + 0.25, "steel", g)
        z += 0.5
        i += 1
    B("slide_rear_plate", 6.8, 15.2, 29.6, 9.2, 18.1, 29.8, "steel", g)
    B("ejection_port", 9.35, 16.4, 16.0, 9.37, 17.8, 19.6, "bore", g)
    B("bolt_head", 9.32, 16.6, 16.3, 9.36, 17.6, 17.4, "steel_dark", g)
    # ambidextrous slide safety
    for side, (a, b, k0, k1) in (("l", (6.35, 6.65, 6.15, 6.4)), ("r", (9.35, 9.65, 9.6, 9.85))):
        B("safety_" + side, a, 16.15, 27.0, b, 16.6, 28.8, "black", g)
        m.pin_x("safety_knob_" + side, (k0 + k1) / 2, 16.38, 28.3, 0.3, k0, k1, "black", g)
    # rear sight
    B("rs_base", 7.0, 18.3, 27.6, 9.0, 18.65, 28.9, "black", g)
    B("rs_ear_l", 7.0, 18.65, 27.6, 7.75, 19.15, 28.9, "black", g)
    B("rs_ear_r", 8.25, 18.65, 27.6, 9.0, 19.15, 28.9, "black", g)
    B("rs_dot_l", 7.3, 18.8, 28.9, 7.46, 18.96, 28.92, "white", g)
    B("rs_dot_r", 8.54, 18.8, 28.9, 8.7, 18.96, 28.92, "white", g)

    # ======================================================================
    # frame
    # ======================================================================
    g = "frame"
    m.bevel("dust_cover", 6.8, 13.4, 9.0, 9.2, 15.2, 15.4, 0.25, "steel", g)
    m.bevel("frame_upper", 6.75, 13.4, 15.4, 9.25, 15.0, 29.0, 0.15, "steel", g)
    m.bevel("beavertail", 7.0, 13.6, 29.0, 9.0, 14.7, 30.3, 0.25, "steel", g)
    # rounded trigger guard
    m.bevel("tg_front", 7.45, 10.1, 9.6, 8.55, 13.5, 10.4, 0.12, "steel", g, axis="y")
    m.bevel("tg_bottom", 7.45, 9.3, 10.4, 8.55, 9.95, 20.4, 0.12, "steel", g)
    m.edge("tg_corner", "x", 7.47, 8.53, 9.3, 9.6, -1, -1, 0.8, "steel", g)
    # barrel release (left), slide stop, magazine release
    m.pin_x("barrel_release", 6.68, 14.3, 10.1, 0.4, 6.55, 6.8, "black", g)
    m.pin_x("barrel_release_r", 9.32, 14.3, 10.1, 0.3, 9.2, 9.45, "steel_mid", g)
    B("slide_stop", 6.55, 14.65, 16.4, 6.75, 15.15, 20.6, "black", g)
    B("slide_stop_pad", 6.45, 14.6, 19.6, 6.75, 15.2, 20.6, "black", g, "knurl")
    m.pin_x("mag_release", 6.28, 12.75, 19.3, 0.35, 6.12, 6.45, "black", g)
    for side, (a, b) in (("l", (6.7, 6.76)), ("r", (9.24, 9.3))):
        m.pin_x("frame_pin_a_" + side, (a + b) / 2, 14.1, 12.2, 0.13, a, b, "steel_mid", g)
        m.pin_x("frame_pin_b_" + side, (a + b) / 2, 14.2, 27.3, 0.13, a, b, "steel_mid", g)

    g = "trigger"
    B("trigger_top", 7.7, 12.1, 12.4, 8.3, 13.45, 12.95, "black", g)
    B("trigger_low", 7.7, 10.55, 12.4, 8.3, 12.15, 12.95, "black", g,
      rot=("x", 22.5, (8, 12.12, 12.68)))

    g = "hammer"
    hr = ("x", -22.5, (8, 15.6, 29.9))
    B("hammer_body", 7.6, 15.0, 29.6, 8.4, 16.6, 30.4, "black", g, rot=hr)
    B("hammer_spur", 7.55, 16.6, 29.9, 8.45, 17.05, 31.0, "black", g, "knurl", rot=hr)

    # ======================================================================
    # grip with wrap-around rubber panels (22.5 deg)
    # ======================================================================
    g = "grip"
    gr = ("x", -22.5, (8, 13.4, 21.6))
    B("grip_neck", 6.75, 12.9, 18.6, 9.25, 14.9, 24.6, "steel", g, rot=gr)
    m.bevel("grip_frame", 6.15, 2.6, 18.4, 9.85, 13.6, 25.0, 0.25, "steel", g, axis="y", rot=gr)
    B("grip_panel_l", 6.03, 3.1, 18.7, 6.15, 12.7, 24.4, "rubber", g, "stipple", rot=gr)
    B("grip_panel_r", 9.85, 3.1, 18.7, 9.97, 12.7, 24.4, "rubber", g, "stipple", rot=gr)
    B("grip_front_rubber", 6.4, 3.1, 18.25, 9.6, 12.4, 18.4, "rubber", g, "stipple", rot=gr)
    for k in range(3):
        y = 5.0 + k * 2.3
        B("grip_finger_%d" % k, 6.5, y, 18.1, 9.5, y + 0.9, 18.25, "rubber", g, rot=gr)
    B("grip_backstrap_lines", 6.6, 3.4, 25.0, 9.4, 12.0, 25.06, "steel", g, "serration", rot=gr)
    m.pin_x("grip_screw_l", 6.0, 7.8, 21.6, 0.18, 5.98, 6.03, "steel_mid", g, rot=gr)
    m.pin_x("grip_screw_r", 10.0, 7.8, 21.6, 0.18, 9.97, 10.02, "steel_mid", g, rot=gr)

    g = "magazine"
    B("mag_body", 6.55, 2.6, 18.7, 9.45, 12.9, 24.6, "steel_dark", g, rot=gr)
    B("mag_round", 7.25, 12.9, 19.2, 8.75, 13.5, 23.6, "brass", g, rot=gr)
    m.bevel("mag_base", 6.2, 1.85, 18.35, 9.8, 2.6, 25.0, 0.12, "steel", g, axis="y", rot=gr)
    B("mag_base_lip", 6.6, 1.9, 18.05, 9.4, 2.55, 18.35, "steel", g, rot=gr)

    m.regroup({}, pivots={"trigger": (8, 13.4, 12.7), "hammer": (8, 15.6, 29.9),
                          "magazine": (8, 13.0, 21.6), "slide": (8, 16.6, 22)})
    m.dynamic = {"slide", "trigger", "hammer", "magazine"}
    return m


GRIP_POINT = (8.0, 8.5, 23.6)

DISPLAY = {"hand": 0.3, "fp": 0.34, "gui": 0.5, "tilt": 0, "push": 0.0}

_D = (0.924, 0.383)
ANIMATIONS = {
    "shoot": (0.22, {
        "slide": {"position": {0.0: [0, 0, 0], 0.05: [0, 0, 4.2], 0.22: [0, 0, 0]}},
        "hammer": {"rotation": {0.0: [0, 0, 0], 0.05: [-35, 0, 0], 0.22: [0, 0, 0]}},
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [14, 0, 0], 0.15: [0, 0, 0]}},
    }),
    "reload": (1.8, {
        "magazine": {"position": {0.0: [0, 0, 0], 0.25: [0, -4 * _D[0], 4 * _D[1]],
                                  0.55: [0, -18 * _D[0], 18 * _D[1]], 0.56: [0, -18 * _D[0], 18 * _D[1]],
                                  1.05: [0, -4 * _D[0], 4 * _D[1]], 1.2: [0, 0, 0]}},
        "slide": {"position": {1.35: [0, 0, 0], 1.5: [0, 0, 4.2], 1.65: [0, 0, 0]}},
    }),
}

"""Accuracy International AWM (.338 Lapua Magnum), olive drab thumbhole stock.
No optic, only the Picatinny rail it would sit on.

Scale: 1 model unit ~= 27 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((44, 45, 49), 5),
    "steel_dark": Material((28, 28, 31), 4),
    "steel_light": Material((96, 97, 102), 6),
    "od": Material((84, 92, 60), 6),             # olive drab stock
    "od_dark": Material((64, 70, 46), 5),
    "rubber": Material((26, 26, 26), 5),
    "brass": Material((178, 142, 66), 6),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("awm", MATERIALS, density=8)
    B = m.box
    cx, cy = 8.0, 10.0

    # ======================================================================
    # muzzle brake, fluted barrel
    # ======================================================================
    g = "barrel"
    m.cyl_z("brake_core", cx, cy, -15.5, -14.0, 0.48, "steel_dark", g)
    m.ring_z("brake_ports", cx, cy, -15.3, -14.2, 0.62, 0.14, 0.55, "steel", g)
    m.cyl_z("brake_front", cx, cy, -15.6, -15.3, 0.62, "steel", g)
    m.cyl_z("brake_rear", cx, cy, -14.2, -13.9, 0.62, "steel", g)
    B("muzzle_bore", 7.78, 9.78, -15.64, 8.22, 10.22, -15.62, "bore", g)
    m.cyl_z("barrel", cx, cy, -13.9, 3.2, 0.42, "steel", g)
    for k, (x0, y0, x1, y1) in enumerate(((7.56, 9.9, 7.58, 10.1), (8.42, 9.9, 8.44, 10.1),
                                         (7.9, 10.42, 8.1, 10.44))):
        B("flute_%d" % k, x0, y0, -11.0, x1, y1, -1.0, "steel_dark", g)

    # ======================================================================
    # action, rail, bolt
    # ======================================================================
    g = "action"
    m.bevel("action", 7.25, 9.35, 3.0, 8.75, 11.3, 14.2, 0.35, "steel", g,
            text={"west": "AWM .338 LM"})
    m.rail_z("action_rail", 7.3, 8.7, 11.62, 2.6, 13.6, "steel", g, period=0.55, tooth=0.35,
             h=0.15, neck=0.15)
    B("ejection_port", 8.75, 10.05, 8.0, 8.77, 11.0, 11.0, "bore", g)
    B("bolt_body_seen", 8.7, 10.2, 8.3, 8.75, 10.85, 10.8, "steel_light", g)
    for side, (a, b) in (("l", (7.2, 7.25)), ("r", (8.75, 8.8))):
        m.pin_x("action_screw_f_" + side, (a + b) / 2, 9.7, 4.0, 0.12, a, b, "steel_light", g)
        m.pin_x("action_screw_b_" + side, (a + b) / 2, 9.7, 13.4, 0.12, a, b, "steel_light", g)

    g = "bolt"
    m.cyl_z("bolt_shroud", cx, 10.35, 14.2, 15.5, 0.55, "steel_dark", g)
    B("cocking_indicator", 7.85, 10.85, 15.0, 8.15, 11.0, 15.5, "steel_light", g)
    m.cyl_x("bolt_handle", 8.75, 10.25, 10.4, 12.9, 0.17, "steel_light", g)
    m.cyl_x("bolt_knob", 10.2, 11.0, 10.4, 12.9, 0.38, "steel_dark", g)

    # ======================================================================
    # chassis / forend
    # ======================================================================
    g = "stock"
    m.bevel("forend", 6.75, 7.6, -3.0, 9.25, 9.75, 10.4, 0.45, "od", g)
    B("forend_channel_l", 7.2, 9.75, -3.0, 7.5, 10.1, 3.0, "od", g)
    B("forend_channel_r", 8.5, 9.75, -3.0, 8.8, 10.1, 3.0, "od", g)
    B("side_panel_l", 6.7, 8.0, -2.4, 6.75, 9.4, 9.6, "od_dark", g, "stipple")
    B("side_panel_r", 9.25, 8.0, -2.4, 9.3, 9.4, 9.6, "od_dark", g, "stipple")
    m.bevel("bipod_stud", 7.75, 7.2, -2.4, 8.25, 7.6, -1.6, 0.1, "steel_dark", g)
    for k in range(4):
        z = -0.6 + k * 1.6
        B("forend_vent_l_%d" % k, 6.73, 8.4, z, 6.75, 9.0, z + 0.9, "od_dark", g)
        B("forend_vent_r_%d" % k, 9.25, 8.4, z, 9.27, 9.0, z + 0.9, "od_dark", g)
    m.bevel("chassis_mid", 7.0, 6.8, 10.4, 9.0, 9.4, 14.2, 0.3, "od", g)
    # trigger guard and magazine catch
    B("tg_front", 7.62, 6.3, 9.85, 8.38, 6.85, 10.2, "od", g)
    m.bevel("tg_bottom", 7.6, 5.95, 9.85, 8.4, 6.35, 13.4, 0.1, "od", g)
    m.edge("tg_corner", "x", 7.62, 8.38, 5.95, 9.85, -1, -1, 0.35, "od", g)
    B("mag_catch", 7.55, 6.55, 9.2, 8.45, 7.2, 9.6, "steel_dark", g)

    g = "trigger"
    B("trigger_top", 7.88, 6.6, 11.15, 8.12, 7.0, 11.45, "steel_light", g)
    B("trigger_low", 7.88, 6.05, 11.15, 8.12, 6.7, 11.45, "steel_light", g,
      rot=("x", 22.5, (8, 6.68, 11.3)))

    # ======================================================================
    # thumbhole butt
    # ======================================================================
    g = "butt"
    gr = ("x", -22.5, (8, 7.4, 14.6))
    B("grip_neck", 7.1, 6.6, 13.6, 8.9, 7.8, 15.6, "od", g, rot=gr)
    m.bevel("grip", 7.05, 3.4, 13.55, 8.95, 7.5, 15.65, 0.22, "od", g, "stipple", axis="y", rot=gr)
    m.bevel("bridge", 7.2, 9.0, 14.2, 8.8, 10.45, 20.4, 0.3, "od", g)
    m.bevel("thumbhole_post", 7.2, 4.6, 18.4, 8.8, 9.2, 20.2, 0.3, "od", g)
    m.bevel("grip_heel", 7.2, 3.3, 15.6, 8.8, 4.6, 20.2, 0.3, "od", g)
    m.bevel("butt_body", 7.15, 3.3, 20.0, 8.85, 9.4, 28.6, 0.35, "od", g)
    B("fold_hinge_l", 7.1, 5.0, 19.9, 7.15, 9.2, 20.4, "steel_dark", g)
    B("fold_hinge_r", 8.85, 5.0, 19.9, 8.9, 9.2, 20.4, "steel_dark", g)
    B("butt_lightening_l", 7.13, 4.6, 21.4, 7.15, 8.2, 26.8, "od_dark", g)
    B("butt_lightening_r", 8.85, 4.6, 21.4, 8.87, 8.2, 26.8, "od_dark", g)
    # adjustable cheek piece
    m.bevel("cheek_piece", 7.2, 9.45, 20.6, 8.8, 10.7, 27.8, 0.3, "od", g)
    m.cyl_z("cheek_post_f", cx, 9.6, 21.2, 21.7, 0.25, "steel_dark", g)
    m.cyl_x("cheek_knob", 6.6, 7.15, 9.0, 21.5, 0.32, "steel_dark", g, "knurl")
    # butt spacers + pad, monopod
    B("butt_spacer_a", 7.15, 3.4, 28.6, 8.85, 9.6, 28.85, "steel_dark", g)
    B("butt_spacer_b", 7.15, 3.4, 28.85, 8.85, 9.6, 29.1, "od_dark", g)
    m.bevel("butt_pad", 7.05, 3.25, 29.1, 8.95, 9.75, 29.9, 0.25, "rubber", g, "ribs")
    m.bevel("monopod_leg", 7.75, 2.2, 26.0, 8.25, 3.35, 26.6, 0.08, "steel_dark", g, axis="y")
    m.cyl_x("monopod_wheel", 7.55, 8.45, 2.85, 26.3, 0.4, "steel_dark", g, "knurl")
    m.bevel("monopod_foot", 7.6, 1.95, 25.85, 8.4, 2.2, 26.75, 0.08, "rubber", g, axis="y")
    m.pin_x("qd_cup_l", 7.0, 5.0, 27.6, 0.3, 6.9, 7.15, "steel_dark", g)

    # ======================================================================
    # 5 round box magazine
    # ======================================================================
    g = "magazine"
    m.bevel("mag_body", 7.3, 6.5, 6.4, 8.7, 9.4, 9.2, 0.12, "steel_dark", g, axis="y")
    B("mag_round", 7.55, 9.4, 6.6, 8.45, 9.75, 9.0, "brass", g)
    m.bevel("mag_floor", 7.2, 6.25, 6.3, 8.8, 6.55, 9.3, 0.08, "steel", g, axis="y")

    m.regroup({}, pivots={"trigger": (8, 7.0, 11.3), "bolt": (8, 10.35, 13),
                          "magazine": (8, 8.0, 7.8)})
    m.dynamic = {"bolt", "trigger", "magazine"}
    return m


GRIP_POINT = (8.0, 5.2, 15.4)

DISPLAY = {"hand": 0.42, "fp": 0.44, "gui": 0.32, "tilt": 30, "push": -3.5}

ANIMATIONS = {
    "shoot": (0.1, {
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [10, 0, 0], 0.08: [0, 0, 0]}},
    }),
    # bolt up, back, forward, down
    "bolt": (1.1, {
        "bolt": {
            "rotation": {0.0: [0, 0, 0], 0.15: [0, 0, 60], 0.85: [0, 0, 60], 1.0: [0, 0, 0]},
            "position": {0.15: [0, 0, 0], 0.4: [0, 0, 4.0], 0.55: [0, 0, 4.0], 0.85: [0, 0, 0]}},
    }),
    "reload": (1.8, {
        "magazine": {"position": {0.0: [0, 0, 0], 0.3: [0, -2, 0], 0.6: [0, -10, 0],
                                  0.61: [0, -10, 0], 1.1: [0, -2, 0], 1.3: [0, 0, 0]}},
    }),
}

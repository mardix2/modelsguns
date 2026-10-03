"""H&K MP5A5: retractable stock (collapsed), slim handguard, SEF trigger group,
tri-lug muzzle, drum rear sight, curved 30 round magazine.

Scale: 1 model unit ~= 13 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((50, 51, 55), 5),         # black-painted stamped steel
    "steel_dark": Material((32, 32, 35), 4),
    "steel_light": Material((92, 93, 98), 6),
    "polymer": Material((40, 40, 39), 6),
    "rubber": Material((28, 28, 28), 5),
    "brass": Material((178, 142, 66), 6),
    "white": Material((214, 214, 206), 3, edge=False),
    "red": Material((170, 34, 30), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("mp5a5", MATERIALS, density=8)
    B = m.box
    cx, cy = 8.0, 10.0
    ty = 11.45  # cocking tube axis

    # ======================================================================
    # muzzle, barrel, front sight
    # ======================================================================
    g = "barrel"
    m.cyl_z("trilug", cx, cy, -13.0, -11.9, 0.55, "steel", g)
    for i, (x0, y0) in enumerate(((7.25, 10.35), (8.45, 10.35), (7.85, 9.25))):
        B("trilug_lug_%d" % i, x0, y0, -12.9, x0 + 0.3, y0 + 0.4, -12.3, "steel", g)
    B("muzzle_bore", 7.78, 9.78, -13.04, 8.22, 10.22, -13.02, "bore", g)
    m.cyl_z("barrel", cx, cy, -11.9, -9.5, 0.38, "steel", g)
    m.bevel("fs_base", 7.3, 9.35, -11.95, 8.7, 12.25, -10.7, 0.22, "steel", g)
    m.ring_z("fs_hood", cx, 12.95, -11.85, -11.0, 0.78, 0.18, 1.0, "steel", g, skip=(4,))
    B("fs_post", 7.92, 12.2, -11.55, 8.08, 12.95, -11.35, "steel_dark", g)
    B("fs_post_dot", 7.94, 12.75, -11.35, 8.06, 12.87, -11.33, "white", g)

    # ======================================================================
    # cocking tube + handle (left side)
    # ======================================================================
    g = "cocking"
    m.cyl_z("cocking_tube", cx, ty, -10.7, -3.2, 0.6, "steel", g)
    B("cocking_slot", 7.38, ty - 0.12, -9.8, 7.41, ty + 0.12, -4.4, "bore", g)
    m.cyl_z("tube_cap", cx, ty, -10.9, -10.7, 0.5, "steel_dark", g)

    g = "cocking_handle"
    B("ch_stem", 6.7, ty - 0.12, -9.5, 7.45, ty + 0.12, -9.05, "steel_light", g)
    m.bevel("ch_knob", 6.05, ty - 0.35, -9.75, 6.75, ty + 0.35, -8.8, 0.12, "steel_light", g)

    # ======================================================================
    # slim handguard
    # ======================================================================
    g = "handguard"
    m.bevel("handguard", 6.75, 7.9, -9.6, 9.25, 10.85, -3.3, 0.55, "polymer", g, "ribs_z")
    B("hg_flare", 6.65, 7.75, -9.75, 9.35, 10.95, -9.5, "polymer", g)
    B("hg_top_l", 6.95, 10.85, -9.4, 7.45, 11.25, -3.4, "polymer", g)
    B("hg_top_r", 8.55, 10.85, -9.4, 9.05, 11.25, -3.4, "polymer", g)
    m.pin_x("hg_pin_l", 6.72, 9.9, -3.9, 0.12, 6.69, 6.76, "steel_light", g)
    m.pin_x("hg_pin_r", 9.28, 9.9, -3.9, 0.12, 9.24, 9.31, "steel_light", g)

    # ======================================================================
    # stamped receiver
    # ======================================================================
    g = "receiver"
    m.bevel("receiver", 7.0, 9.2, -3.4, 9.0, 12.05, 9.6, 0.4, "steel", g)
    for side, (a, b) in (("l", (6.95, 7.0)), ("r", (9.0, 9.05))):
        B("rib_" + side, a, 10.95, -3.2, b, 11.1, 9.4, "steel", g)
        B("rib_low_" + side, a, 9.45, -3.2, b, 9.6, 2.3, "steel", g)
    for i, z in enumerate((-0.4, 0.4, 4.4, 5.2)):
        B("claw_dimple_%d" % i, 7.6, 12.05, z, 8.4, 12.15, z + 0.4, "steel", g)
    B("ejection_port", 9.0, 10.2, 2.6, 9.02, 11.35, 5.0, "bore", g)
    B("case_deflector", 9.0, 10.35, 5.0, 9.3, 11.45, 5.6, "steel", g)
    B("bolt_face", 8.96, 10.4, 4.3, 9.0, 11.2, 4.95, "steel_light", g)
    m.bevel("end_cap", 6.9, 9.0, 9.6, 9.1, 12.2, 10.2, 0.3, "steel", g)
    B("stock_latch", 7.55, 12.2, 9.3, 8.45, 12.5, 10.3, "steel_dark", g, "knurl")
    # magazine well and release
    m.bevel("magwell", 7.2, 7.55, 2.35, 8.8, 9.3, 4.95, 0.15, "steel", g, axis="y")
    B("magwell_lip", 7.1, 7.4, 2.25, 8.9, 7.6, 5.05, "steel", g)
    B("mag_paddle", 7.6, 7.0, 4.95, 8.4, 7.6, 5.35, "steel_dark", g)
    m.pin_x("mag_button", 9.12, 8.75, 5.25, 0.22, 9.0, 9.25, "steel_dark", g)
    # rear drum sight
    B("drum_base", 7.4, 12.05, 7.4, 8.6, 12.4, 9.2, "steel", g)
    m.cyl_x("drum", 7.3, 8.7, 12.95, 8.3, 0.62, "steel", g)
    B("drum_aperture", 7.9, 12.85, 8.9, 8.1, 13.05, 8.93, "bore", g)
    B("drum_ear_l", 7.15, 12.4, 7.6, 7.3, 13.6, 9.0, "steel", g)
    B("drum_ear_r", 8.7, 12.4, 7.6, 8.85, 13.6, 9.0, "steel", g)

    # ======================================================================
    # polymer SEF trigger group with integral grip
    # ======================================================================
    g = "lower"
    m.bevel("housing", 7.15, 7.3, 5.0, 8.85, 9.25, 10.6, 0.15, "polymer", g,
            text={"west": "S E F"})
    for side, (a, b) in (("l", (7.05, 7.15)), ("r", (8.85, 8.95))):
        m.pin_x("push_pin_f_" + side, (a + b) / 2, 8.85, 5.45, 0.16, a, b, "steel_light", g)
        m.pin_x("push_pin_b_" + side, (a + b) / 2, 8.85, 10.15, 0.16, a, b, "steel_light", g)
    B("tg_front", 7.55, 6.4, 5.6, 8.45, 7.3, 6.0, "polymer", g)
    m.bevel("tg_bottom", 7.55, 6.0, 6.0, 8.45, 6.45, 9.6, 0.1, "polymer", g)
    m.edge("tg_corner", "x", 7.57, 8.43, 6.0, 5.6, -1, -1, 0.4, "polymer", g)
    # selector lever (left) with pictogram dots
    m.pin_x("selector_hub", 7.05, 8.45, 10.2, 0.32, 6.9, 7.15, "steel_dark", g)
    B("selector_lever", 6.88, 8.3, 9.2, 7.02, 8.6, 10.2, "steel_dark", g)
    B("selector_mark_s", 7.13, 8.9, 8.5, 7.15, 9.1, 8.7, "white", g)
    B("selector_mark_f", 7.13, 7.6, 8.9, 7.15, 7.8, 9.1, "red", g)
    gr = ("x", -22.5, (8, 7.3, 9.9))
    B("grip_neck", 7.2, 7.0, 8.8, 8.8, 8.2, 11.0, "polymer", g, rot=gr)
    m.bevel("grip", 7.1, 2.7, 8.7, 8.9, 7.4, 11.1, 0.2, "polymer", g, "stipple", axis="y", rot=gr)
    for k in range(3):
        y = 3.4 + k * 1.15
        B("grip_finger_%d" % k, 7.25, y, 8.52, 8.75, y + 0.5, 8.7, "polymer", g, rot=gr)
    m.bevel("grip_cap", 7.05, 2.45, 8.6, 8.95, 2.7, 11.2, 0.08, "polymer", g, axis="y", rot=gr)

    g = "trigger"
    B("trigger_top", 7.88, 7.45, 7.15, 8.12, 7.95, 7.45, "steel_dark", g)
    B("trigger_low", 7.88, 6.7, 7.15, 8.12, 7.5, 7.45, "steel_dark", g,
      rot=("x", 22.5, (8, 7.48, 7.3)))

    # ======================================================================
    # retractable stock (collapsed)
    # ======================================================================
    g = "stock"
    for side, (a, b) in (("l", (6.65, 6.9)), ("r", (9.1, 9.35))):
        B("stock_rod_" + side, a, 10.7, 3.4, b, 11.05, 13.6, "steel", g)
        B("rod_guide_" + side, a - 0.05, 10.6, 8.6, b + 0.05, 11.15, 9.5, "steel", g)
    B("stock_yoke", 6.65, 10.6, 12.9, 9.35, 11.15, 13.6, "steel", g)
    m.bevel("butt_plate", 6.45, 6.7, 13.6, 9.55, 12.3, 14.3, 0.3, "rubber", g, "ribs")
    m.bevel("butt_hook_top", 6.7, 11.6, 12.9, 9.3, 12.35, 13.6, 0.2, "steel", g)
    m.bevel("butt_toe", 6.7, 6.7, 13.0, 9.3, 7.4, 13.6, 0.2, "steel", g)
    B("sling_loop_a", 6.25, 7.6, 13.65, 6.45, 7.8, 14.25, "steel", g)
    B("sling_loop_b", 6.25, 7.8, 13.65, 6.45, 8.6, 13.8, "steel", g)

    # ======================================================================
    # curved 30 round magazine
    # ======================================================================
    g = "magazine"
    B("mag_top", 7.35, 4.2, 2.55, 8.65, 8.9, 4.75, "steel", g)
    B("mag_round", 7.6, 8.9, 2.75, 8.4, 9.2, 4.6, "brass", g)
    B("mag_fill", 7.35, 3.85, 3.6, 8.65, 4.3, 4.75, "steel", g)
    for i in range(4):
        y = 4.5 + i * 0.6
        B("mag_rib_l_%d" % i, 7.3, y, 2.7, 7.35, y + 0.22, 4.6, "steel", g)
        B("mag_rib_r_%d" % i, 8.65, y, 2.7, 8.7, y + 0.22, 4.6, "steel", g)
    mr = ("x", 22.5, (8, 4.3, 3.65))
    B("mag_curve", 7.35, 1.6, 2.55, 8.65, 4.4, 4.75, "steel", g, rot=mr)
    for i in range(3):
        y = 1.9 + i * 0.8
        B("mag_crib_l_%d" % i, 7.3, y, 2.7, 7.35, y + 0.25, 4.6, "steel", g, rot=mr)
        B("mag_crib_r_%d" % i, 8.65, y, 2.7, 8.7, y + 0.25, 4.6, "steel", g, rot=mr)
    m.bevel("mag_floor", 7.25, 1.25, 2.4, 8.75, 1.6, 4.95, 0.08, "steel_dark", g, axis="y", rot=mr)

    m.regroup({}, pivots={"magazine": (8, 8.0, 3.65), "trigger": (8, 7.9, 7.3),
                          "cocking_handle": (6.6, ty, -9.2)})
    m.dynamic = {"magazine", "trigger", "cocking_handle"}
    return m


GRIP_POINT = (8.0, 5.0, 10.4)

DISPLAY = {"hand": 0.42, "fp": 0.44, "gui": 0.36, "tilt": 25, "push": -1.0}

ANIMATIONS = {
    "shoot": (0.09, {
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [12, 0, 0], 0.08: [0, 0, 0]}},
    }),
    "reload": (2.4, {
        "magazine": {"position": {0.0: [0, 0, 0], 0.3: [0, -3, 0], 0.6: [0, -14, 0],
                                  0.61: [0, -14, 0], 1.1: [0, -3, 0], 1.3: [0, 0, 0]}},
        # the famous "HK slap": handle back, then slapped forward
        "cocking_handle": {"position": {0.0: [0, 0, 0], 0.15: [0, 0, 5.2], 0.2: [0, 0.4, 5.2],
                                        1.6: [0, 0.4, 5.2], 1.7: [0, 0, 0]}},
    }),
}

"""AK-47 (Type 3, milled receiver) with wooden furniture.

Scale: 1 model unit ~= 19 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((54, 55, 58), 5),        # blued steel
    "steel_dark": Material((34, 34, 37), 4),
    "steel_light": Material((96, 96, 100), 6),
    "wood": Material((128, 74, 38), 5),         # laminated birch / walnut
    "wood_dark": Material((96, 54, 28), 5),
    "wood_s": Material((128, 74, 38), 5, edge=False),   # seamless slices
    "bakelite": Material((112, 46, 26), 5),     # orange-brown magazine
    "bore": Material((6, 6, 6), 1, edge=False),
    "brass": Material((178, 142, 66), 6),
    "white": Material((214, 214, 206), 3, edge=False),
}


def build():
    m = Model("ak47", MATERIALS, density=8)
    B = m.box
    cx, cy = 8.0, 10.0

    # ======================================================================
    # barrel, muzzle nut, front sight block, cleaning rod
    # ======================================================================
    g = "barrel"
    m.cyl_z("muzzle_nut", cx, cy, -15.4, -14.5, 0.48, "steel", g, "knurl")
    B("muzzle_bore", 7.78, 9.78, -15.44, 8.22, 10.22, -15.42, "bore", g)
    m.cyl_z("barrel", cx, cy, -14.5, -4.4, 0.4, "steel", g)
    # front sight block with protective ears and post
    m.bevel("fsb_base", 7.3, 9.35, -14.3, 8.7, 10.65, -12.9, 0.18, "steel", g)
    B("fsb_tower", 7.45, 10.65, -14.1, 8.55, 11.1, -13.1, "steel", g)
    B("fsb_ear_l", 7.4, 11.1, -14.0, 7.6, 12.7, -13.2, "steel", g)
    B("fsb_ear_r", 8.4, 11.1, -14.0, 8.6, 12.7, -13.2, "steel", g)
    B("fsb_post", 7.93, 11.1, -13.7, 8.07, 12.45, -13.5, "steel_dark", g)
    B("fsb_post_drum", 7.75, 11.05, -13.85, 8.25, 11.4, -13.35, "steel", g)
    B("bayonet_lug", 7.75, 8.85, -14.2, 8.25, 9.35, -13.2, "steel", g)
    m.cyl_z("cleaning_rod", cx, 8.95, -14.6, -4.6, 0.12, "steel_light", g)
    B("cleaning_rod_head", 7.8, 8.78, -14.75, 8.2, 9.12, -14.55, "steel_light", g)
    # gas block + exposed gas tube
    m.bevel("gas_block", 7.3, 9.35, -6.6, 8.7, 11.75, -5.4, 0.2, "steel", g)
    B("gas_block_vent_l", 7.28, 10.9, -6.3, 7.3, 11.3, -5.7, "bore", g)
    B("gas_block_vent_r", 8.7, 10.9, -6.3, 8.72, 11.3, -5.7, "bore", g)
    m.cyl_z("gas_tube", cx, 11.25, -5.4, -3.8, 0.4, "steel", g)
    m.cyl_z("barrel_ferrule", cx, 9.9, -4.6, -4.2, 0.95, "steel", g)

    # ======================================================================
    # wooden handguards
    # ======================================================================
    g = "handguard"
    m.bevel("lower_hg", 6.85, 8.35, -4.2, 9.15, 10.75, 2.0, 0.45, "wood", g, "wood")
    for i in range(5):
        z = -3.2 + i * 1.0
        B("lower_hg_groove_l_%d" % i, 6.83, 9.0, z, 6.85, 10.2, z + 0.25, "wood_dark", g)
        B("lower_hg_groove_r_%d" % i, 9.15, 9.0, z, 9.17, 10.2, z + 0.25, "wood_dark", g)
    m.bevel("upper_hg", 7.15, 10.75, -3.8, 8.85, 11.95, 1.4, 0.38, "wood", g, "wood")
    B("upper_hg_cap", 7.25, 10.75, 1.4, 8.75, 11.85, 1.65, "steel", g)
    m.bevel("hg_retainer", 6.95, 8.4, 2.0, 9.05, 10.7, 2.55, 0.3, "steel", g)
    B("hg_retainer_lever", 9.05, 9.6, 2.05, 9.15, 10.4, 2.5, "steel_dark", g)

    # ======================================================================
    # rear sight block + tangent leaf
    # ======================================================================
    g = "sight"
    m.bevel("rs_block", 7.2, 9.6, 2.55, 8.8, 11.55, 4.3, 0.3, "steel", g)
    B("rs_leaf", 7.45, 11.55, 3.0, 8.55, 11.75, 6.1, "steel", g, text={"up": "1 3 5 8"})
    B("rs_notch_l", 7.45, 11.75, 2.9, 7.9, 12.05, 3.2, "steel", g)
    B("rs_notch_r", 8.1, 11.75, 2.9, 8.55, 12.05, 3.2, "steel", g)
    B("rs_slider", 7.35, 11.5, 4.3, 8.65, 11.9, 4.85, "steel_light", g)
    B("rs_slider_btn_l", 7.25, 11.55, 4.4, 7.35, 11.85, 4.75, "steel_light", g)
    B("rs_slider_btn_r", 8.65, 11.55, 4.4, 8.75, 11.85, 4.75, "steel_light", g)

    # ======================================================================
    # milled receiver, dust cover, bolt carrier, selector
    # ======================================================================
    g = "receiver"
    m.bevel("receiver", 7.1, 7.4, 4.3, 8.9, 10.55, 14.6, 0.15, "steel", g)
    for side, (a, b) in (("l", (7.07, 7.1)), ("r", (8.9, 8.93))):
        B("lightening_cut_" + side, a, 8.2, 6.3, b, 9.1, 8.6, "steel_dark", g)
        for i, (y, z) in enumerate(((10.1, 4.7), (10.1, 5.4), (7.8, 4.7), (7.8, 13.9), (10.1, 13.9))):
            m.pin_x("rivet_%s_%d" % (side, i), (a + b) / 2, y, z, 0.1,
                    a - 0.03 if side == "l" else a, b if side == "l" else b + 0.03, "steel_light", g)
    B("trunnion_ring", 7.0, 9.35, 4.3, 9.0, 10.65, 4.75, "steel", g)
    # dust cover with ribbed top and rear latch
    m.bevel("dust_cover", 7.15, 10.55, 5.6, 8.85, 11.35, 15.0, 0.3, "steel", g)
    B("dust_cover_rib", 7.65, 11.33, 7.0, 8.35, 11.4, 14.4, "steel", g)
    B("dust_cover_lip", 7.1, 10.5, 14.85, 8.9, 11.2, 15.05, "steel", g)
    m.cyl_z("rear_latch", cx, 10.35, 14.6, 15.2, 0.25, "steel_light", g)
    B("recoil_guide_end", 7.75, 10.6, 15.0, 8.25, 11.0, 15.15, "steel_light", g)
    # ejection port (right side)
    B("ejection_port", 8.9, 9.95, 7.2, 8.92, 10.5, 9.7, "bore", g)
    # safety / selector lever (right)
    B("selector_plate", 8.92, 9.55, 9.6, 8.98, 10.15, 14.0, "steel", g)
    B("selector_tab", 8.92, 9.05, 9.3, 9.02, 10.15, 9.75, "steel", g)
    m.pin_x("selector_axle", 8.97, 9.85, 13.8, 0.2, 8.95, 9.02, "steel_light", g)
    # magazine well lip and release paddle
    B("magwell_lip", 7.05, 7.25, 5.6, 8.95, 7.45, 8.9, "steel", g)
    B("mag_release", 7.65, 6.6, 8.95, 8.35, 7.45, 9.35, "steel", g)
    B("mag_release_tab", 7.55, 6.45, 9.1, 8.45, 6.7, 9.55, "steel", g)
    # trigger guard
    B("tg_front", 7.65, 6.45, 9.55, 8.35, 7.4, 9.85, "steel", g)
    m.bevel("tg_bottom", 7.6, 6.2, 9.55, 8.4, 6.5, 12.6, 0.08, "steel", g)
    B("tg_rear", 7.65, 6.2, 12.4, 8.35, 7.4, 12.7, "steel", g)
    for side, (a, b) in (("l", (7.04, 7.1)), ("r", (8.9, 8.96))):
        m.pin_x("trigger_pin_" + side, (a + b) / 2, 8.15, 10.95, 0.12, a, b, "steel_light", g)
        m.pin_x("hammer_pin_" + side, (a + b) / 2, 8.25, 12.1, 0.12, a, b, "steel_light", g)

    g = "trigger"
    B("trigger_top", 7.88, 7.55, 10.75, 8.12, 8.2, 11.05, "steel", g)
    B("trigger_low", 7.88, 6.85, 10.75, 8.12, 7.6, 11.05, "steel", g,
      rot=("x", 22.5, (8, 7.58, 10.9)))

    g = "bolt"
    B("bolt_carrier", 8.82, 10.05, 7.2, 8.9, 10.45, 13.2, "steel_light", g)
    B("bolt_face", 8.8, 10.0, 7.2, 8.88, 10.5, 7.6, "steel", g)
    m.cyl_x("charging_handle_stem", 8.9, 9.6, 10.25, 9.95, 0.17, "steel_light", g)
    m.cyl_x("charging_handle_knob", 9.6, 10.15, 10.25, 9.95, 0.3, "steel_light", g)

    # ======================================================================
    # pistol grip (raked 22.5 deg) and fixed wooden stock
    # ======================================================================
    g = "grip"
    gr = ("x", -22.5, (8, 7.4, 13.0))
    B("grip_neck", 7.15, 6.9, 11.95, 8.85, 8.4, 14.05, "wood", g, "wood", rot=gr)
    m.bevel("grip_body", 7.15, 3.6, 11.95, 8.85, 7.45, 14.05, 0.22, "wood", g, "wood", axis="y", rot=gr)
    B("grip_screw_cap", 7.75, 3.45, 12.6, 8.25, 3.6, 13.3, "steel", g, rot=gr)
    B("grip_finger_l", 7.13, 4.3, 12.0, 7.15, 7.0, 12.15, "wood_dark", g, rot=gr)
    B("grip_finger_r", 8.85, 4.3, 12.0, 8.87, 7.0, 12.15, "wood_dark", g, rot=gr)

    g = "stock"
    B("stock_tang", 7.35, 8.0, 14.6, 8.65, 10.2, 15.4, "steel", g)
    # stock built from slices: the comb drops slightly, the belly drops steeply
    # from the wrist and then runs straight to the toe; the stock widens
    # towards the butt
    def lerp(pts, z):
        for (z0, v0), (z1, v1) in zip(pts, pts[1:]):
            if z0 <= z <= z1:
                return v0 + (v1 - v0) * (z - z0) / (z1 - z0)
        return pts[-1][1]
    top_pts = [(15.2, 10.35), (30.1, 9.75)]
    bot_pts = [(15.2, 7.45), (18.6, 6.55), (30.1, 4.45)]
    wid_pts = [(15.2, 0.72), (30.1, 0.95)]
    z = 15.2
    i = 0
    while z < 30.09:
        z2 = min(30.1, z + 1.0)
        zm = (z + z2) / 2
        top, bot, hw = lerp(top_pts, zm), lerp(bot_pts, zm), lerp(wid_pts, zm)
        m.bevel("stock_slice_%02d" % i, 8 - hw, bot, z, 8 + hw, top, z2 + (0.02 if z2 < 30.1 else 0),
                min(0.35, hw * 0.45), "wood_s", g, "wood")
        z = z2
        i += 1
    # steel butt plate with trap door and sling loop
    m.bevel("butt_plate", 7.0, 4.25, 30.1, 9.0, 10.3, 30.45, 0.2, "steel", g)
    B("trap_door", 7.5, 6.0, 30.45, 8.5, 8.6, 30.5, "steel", g)
    B("trap_door_hinge", 7.6, 8.6, 30.45, 8.4, 8.75, 30.55, "steel_light", g)
    B("sling_loop_a", 6.85, 5.0, 27.6, 7.05, 5.2, 28.8, "steel", g)
    B("sling_loop_b", 6.85, 5.2, 27.6, 7.05, 5.7, 27.75, "steel", g)
    B("sling_loop_c", 6.85, 5.2, 28.65, 7.05, 5.7, 28.8, "steel", g)

    # ======================================================================
    # curved 30 round magazine
    # ======================================================================
    g = "magazine"
    B("mag_top", 7.3, 4.6, 5.85, 8.7, 7.4, 8.85, "bakelite", g)
    B("mag_feed_lips", 7.45, 7.4, 6.0, 8.55, 7.6, 8.6, "steel", g)
    B("mag_round", 7.65, 7.45, 6.2, 8.35, 7.75, 8.5, "brass", g)
    B("mag_catch_lug", 7.6, 6.9, 8.85, 8.4, 7.3, 9.0, "steel", g)
    for i in range(3):
        y = 4.9 + i * 0.75
        B("mag_rib_l_%d" % i, 7.25, y, 6.0, 7.3, y + 0.25, 8.7, "bakelite", g)
        B("mag_rib_r_%d" % i, 8.7, y, 6.0, 8.75, y + 0.25, 8.7, "bakelite", g)
    r1 = ("x", 22.5, (8, 4.7, 7.35))
    B("mag_mid", 7.3, 1.3, 5.85, 8.7, 4.8, 8.85, "bakelite", g, rot=r1)
    for i in range(3):
        y = 1.6 + i * 1.0
        B("mag_mid_rib_l_%d" % i, 7.25, y, 6.0, 7.3, y + 0.3, 8.7, "bakelite", g, rot=r1)
        B("mag_mid_rib_r_%d" % i, 8.7, y, 6.0, 8.75, y + 0.3, 8.7, "bakelite", g, rot=r1)
    B("mag_spine_mid", 7.7, 1.3, 8.85, 8.3, 4.8, 9.0, "bakelite", g, rot=r1)
    # lowest section, 45 deg, pivoting at the end of the middle one
    r2 = ("x", 45, (8, 1.46, 6.0))
    B("mag_low", 7.3, -0.9, 4.5, 8.7, 1.7, 7.5, "bakelite", g, rot=r2)
    B("mag_spine_low", 7.7, -0.9, 7.5, 8.3, 1.4, 7.65, "bakelite", g, rot=r2)
    m.bevel("mag_floorplate", 7.2, -1.25, 4.4, 8.8, -0.9, 7.6, 0.08, "steel", g, axis="y", rot=r2)

    m.regroup({}, pivots={"magazine": (8, 7.0, 7.3), "trigger": (8, 8.1, 10.9),
                          "bolt": (9, 10.25, 10)})
    m.dynamic = {"magazine", "trigger", "bolt"}
    return m


GRIP_POINT = (8.0, 5.6, 13.6)

DISPLAY = {"hand": 0.4, "fp": 0.42, "gui": 0.33, "tilt": 30, "push": -2.0}

ANIMATIONS = {
    "shoot": (0.1, {
        "bolt": {"position": {0.0: [0, 0, 0], 0.025: [0, 0, 3.0], 0.1: [0, 0, 0]}},
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [12, 0, 0], 0.08: [0, 0, 0]}},
    }),
    "reload": (2.2, {
        "magazine": {
            "rotation": {0.0: [0, 0, 0], 0.25: [-25, 0, 0], 0.5: [-25, 0, 0], 1.1: [-25, 0, 0],
                         1.35: [0, 0, 0]},
            "position": {0.0: [0, 0, 0], 0.25: [0, -1, -1], 0.6: [0, -16, -2], 0.61: [0, -16, -2],
                         1.1: [0, -1, -1], 1.35: [0, 0, 0]}},
        "bolt": {"position": {1.6: [0, 0, 0], 1.75: [0, 0, 3.4], 1.9: [0, 0, 0]}},
    }),
}

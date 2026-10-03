"""AK-47 Type 3 (milled receiver), wooden furniture, steel 30 rd magazine.

Real proportions (880 mm overall, 415 mm barrel).  Scale: 1 unit ~= 19 mm.
Muzzle points north (-Z), bore axis at x=8, y=10.
"""

from bbgen import Material, Model

MATERIALS = {
    "steel": Material((50, 51, 56), 4),         # blued steel
    "steel_dark": Material((33, 33, 37), 4),
    "steel_light": Material((104, 105, 110), 5),
    "steel_mag": Material((44, 45, 49), 4),
    "wood": Material((132, 72, 36), 4),
    "wood_dark": Material((92, 48, 24), 4),
    "wood_s": Material((132, 72, 36), 4, edge=False),
    "brass": Material((182, 146, 70), 5),
    "white": Material((220, 220, 210), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

CX, CY = 8.0, 10.0
GT_Y = 11.12  # gas tube axis


def build():
    m = Model("ak47", MATERIALS, density=8)
    B = m.box

    # ======================================================================
    # muzzle nut, front sight block, exposed barrel
    # ======================================================================
    g = "barrel"
    m.cyl_z("muzzle_nut", CX, CY, -17.65, -17.0, 0.5, "steel", g, "knurl")
    m.cyl_z("muzzle_nut_face", CX, CY, -17.7, -17.65, 0.42, "steel", g)
    m.cyl_z("bore", CX, CY, -17.74, -17.7, 0.2, "bore", g)
    # front sight block: barrel ring, tower, protective ears, post, bayonet lug
    m.cyl_z("fsb_ring_front", CX, CY, -17.0, -16.55, 0.62, "steel", g)
    m.bevel("fsb_body", 7.35, 9.25, -16.6, 8.65, 10.75, -14.9, 0.22, "steel", g)
    m.bevel("fsb_tower", 7.5, 10.75, -16.35, 8.5, 11.35, -15.15, 0.15, "steel", g)
    with m.frame(("x", -12, (8, 11.35, -15.15))):
        m.bevel("fsb_ear_l", 7.38, 11.25, -16.25, 7.62, 12.85, -15.55, 0.06, "steel", g, axis="y")
        m.bevel("fsb_ear_r", 8.38, 11.25, -16.25, 8.62, 12.85, -15.55, 0.06, "steel", g, axis="y")
    m.cyl_z("fsb_drum", CX, 11.5, -16.0, -15.6, 0.28, "steel", g)
    B("fsb_post", 7.93, 11.6, -15.9, 8.07, 12.6, -15.72, "steel_dark", g)
    B("fsb_post_tip", 7.9, 12.45, -15.92, 8.1, 12.62, -15.7, "steel_dark", g)
    m.pin_x("fsb_detent", 8.66, 11.0, -15.45, 0.12, 8.6, 8.72, "steel_light", g)
    m.bevel("bayonet_lug", 7.75, 8.75, -16.9, 8.25, 9.3, -15.3, 0.1, "steel", g)
    B("cleaning_rod_catch", 7.82, 8.75, -15.3, 8.18, 9.05, -14.95, "steel", g)
    m.pin_x("fsb_pin", 8.0, 9.6, -16.05, 0.09, 7.3, 8.7, "steel_light", g)
    # barrel
    m.cyl_z("barrel_front", CX, CY, -15.0, -11.15, 0.4, "steel", g)
    m.cyl_z("barrel_shoulder", CX, CY, -11.3, -11.1, 0.46, "steel", g)
    # cleaning rod (under the barrel, T-head at the front)
    m.cyl_z("cleaning_rod", CX, 8.98, -16.95, -9.0, 0.11, "steel_light", g)
    m.bevel("cleaning_rod_head", 7.78, 8.76, -17.15, 8.22, 9.2, -16.9, 0.06, "steel_light", g)

    # ======================================================================
    # gas block, gas tube, front sling swivel
    # ======================================================================
    g = "gas"
    m.bevel("gas_block_ring", 7.36, 9.32, -11.25, 8.64, 10.68, -9.15, 0.24, "steel", g)
    with m.frame(("x", -45, (8, 10.65, -10.4))):
        m.bevel("gas_block_riser", 7.45, 10.2, -10.95, 8.55, 11.6, -10.1, 0.12, "steel", g)
    m.bevel("gas_block_head", 7.42, 10.6, -11.25, 8.58, 11.65, -9.2, 0.25, "steel", g)
    for k in range(3):
        z = -11.0 + k * 0.5
        B("gas_vent_l_%d" % k, 7.4, 11.0, z, 7.42, 11.25, z + 0.25, "bore", g)
        B("gas_vent_r_%d" % k, 8.58, 11.0, z, 8.6, 11.25, z + 0.25, "bore", g)
    m.cyl_z("gas_tube_front", CX, GT_Y, -9.2, -8.7, 0.45, "steel", g)
    # front sling swivel (left)
    m.pin_x("swivel_rivet", 7.33, 9.65, -10.1, 0.13, 7.28, 7.36, "steel_light", g)
    B("swivel_a", 7.1, 8.85, -10.6, 7.22, 9.05, -9.6, "steel_light", g)
    B("swivel_b", 7.1, 9.05, -10.6, 7.22, 9.65, -10.45, "steel_light", g)
    B("swivel_c", 7.1, 9.05, -9.75, 7.22, 9.65, -9.6, "steel_light", g)

    # ======================================================================
    # wooden handguards with steel ferrule / retainer
    # ======================================================================
    g = "handguard"
    m.bevel("hg_ferrule", 7.0, 8.48, -9.1, 9.0, 10.85, -8.7, 0.32, "steel", g)
    # lower handguard: slightly swelling, round-ish section, flat finger flutes
    with m.frame(("x", -1.6, (8, 8.6, -8.7))):
        m.bevel("hg_lower", 6.9, 8.5, -8.7, 9.1, 10.8, 0.15, 0.55, "wood", g, "wood")
    m.bevel("hg_lower_belly", 7.25, 8.3, -7.4, 8.75, 8.8, -0.6, 0.18, "wood", g, "wood")
    for k, (y0, y1) in enumerate(((9.15, 9.45), (9.85, 10.15))):
        B("hg_flute_l_%d" % k, 6.88, y0, -7.6, 6.9, y1, -0.9, "wood_dark", g)
        B("hg_flute_r_%d" % k, 9.1, y0, -7.6, 9.12, y1, -0.9, "wood_dark", g)
    m.bevel("hg_retainer", 6.92, 8.45, 0.15, 9.08, 10.85, 0.6, 0.35, "steel", g)
    B("hg_retainer_lever", 9.08, 9.4, 0.2, 9.2, 10.5, 0.55, "steel", g)
    m.pin_x("hg_retainer_pin", 9.15, 9.95, 0.38, 0.13, 9.12, 9.24, "steel_light", g)
    # upper handguard (over the gas tube) with its steel cap
    m.bevel("hg_upper", 7.22, 10.82, -8.6, 8.78, 11.85, -0.35, 0.42, "wood", g, "wood")
    m.bevel("hg_upper_cap", 7.28, 10.85, -0.4, 8.72, 11.82, 0.4, 0.38, "steel", g)
    m.cyl_z("gas_tube_rear", CX, GT_Y, 0.35, 0.9, 0.42, "steel", g)

    # ======================================================================
    # rear sight block + tangent leaf (graduated)
    # ======================================================================
    g = "rear_sight"
    m.bevel("rs_block", 7.2, 9.45, 0.6, 8.8, 11.45, 4.35, 0.32, "steel", g)
    m.bevel("rs_block_low", 7.35, 8.9, 1.0, 8.65, 9.5, 4.3, 0.15, "steel", g)
    B("rs_spring_slot", 7.7, 11.42, 0.9, 8.3, 11.46, 2.4, "bore", g)
    m.pin_x("rs_leaf_pivot", 8.0, 11.6, 4.0, 0.16, 7.18, 8.82, "steel_light", g)
    with m.frame(("x", 3.0, (8, 11.6, 4.0))):
        m.bevel("rs_leaf", 7.42, 11.45, 1.25, 8.58, 11.7, 4.15, 0.05, "steel", g,
                text={"up": "10 8 6 4 2 P"})
        B("rs_notch_l", 7.42, 11.7, 1.25, 7.9, 12.0, 1.55, "steel", g)
        B("rs_notch_r", 8.1, 11.7, 1.25, 8.58, 12.0, 1.55, "steel", g)
        m.bevel("rs_slider", 7.3, 11.4, 2.6, 8.7, 11.85, 3.15, 0.08, "steel_light", g)
        B("rs_slider_btn_l", 7.18, 11.48, 2.7, 7.3, 11.78, 3.05, "steel_light", g, "knurl")
        B("rs_slider_btn_r", 8.7, 11.48, 2.7, 8.82, 11.78, 3.05, "steel_light", g, "knurl")
    B("rs_front_sight_white", 7.9, 11.72, 1.24, 8.1, 11.88, 1.26, "white", g)

    # ======================================================================
    # milled receiver
    # ======================================================================
    g = "receiver"
    m.bevel("rcv_trunnion", 7.12, 7.8, 4.3, 8.88, 10.65, 5.6, 0.25, "steel", g)
    m.bevel("rcv_body", 7.18, 7.8, 5.6, 8.82, 10.6, 16.6, 0.18, "steel", g)
    m.bevel("rcv_rear", 7.25, 7.95, 16.6, 8.75, 10.55, 17.5, 0.3, "steel", g)
    # lightening cuts above the magazine well, both sides
    for side, (a, b) in (("l", (7.15, 7.18)), ("r", (8.82, 8.85))):
        B("rcv_cut_" + side, a, 8.55, 6.4, b, 9.55, 9.6, "steel_dark", g)
        B("rcv_cut_low_" + side, a, 8.1, 6.6, b, 8.45, 9.4, "steel_dark", g)
        for k, (y, z) in enumerate(((10.2, 4.9), (8.15, 4.9), (8.15, 16.9), (10.2, 16.9))):
            m.pin_x("rcv_rivet_%s_%d" % (side, k), (a + b) / 2, y, z, 0.11,
                    a - 0.04 if side == "l" else a, b if side == "l" else b + 0.04, "steel_light", g)
        m.pin_x("trigger_pin_" + side, (a + b) / 2, 8.55, 12.15, 0.12,
                a - 0.05 if side == "l" else a, b if side == "l" else b + 0.05, "steel_light", g)
        m.pin_x("hammer_pin_" + side, (a + b) / 2, 8.75, 13.65, 0.12,
                a - 0.05 if side == "l" else a, b if side == "l" else b + 0.05, "steel_light", g)
    # ejection port
    B("ejection_port", 8.82, 9.85, 7.3, 8.84, 10.55, 10.1, "bore", g)
    B("ejection_port_rim", 8.82, 9.78, 7.25, 8.86, 9.85, 10.15, "steel", g)
    # magazine well lip
    m.bevel("magwell_lip", 7.1, 7.55, 5.55, 8.9, 7.85, 9.85, 0.12, "steel", g)
    # magazine release paddle
    m.bevel("mag_release", 7.62, 6.75, 9.9, 8.38, 7.8, 10.3, 0.08, "steel", g)
    with m.frame(("x", 18, (8, 6.8, 10.1))):
        m.bevel("mag_release_tab", 7.55, 6.45, 9.9, 8.45, 6.8, 10.55, 0.08, "steel", g, "knurl")
    # trigger guard with front hook
    m.bevel("tg_front", 7.62, 6.6, 10.3, 8.38, 7.8, 10.65, 0.08, "steel", g, axis="y")
    m.bevel("tg_bottom", 7.6, 6.35, 10.45, 8.4, 6.7, 13.6, 0.1, "steel", g)
    m.edge("tg_corner", "x", 7.62, 8.38, 6.35, 10.3, -1, -1, 0.35, "steel", g)
    m.bevel("tg_rear", 7.62, 6.35, 13.4, 8.38, 7.8, 13.75, 0.08, "steel", g, axis="y")

    # selector lever (right side): long stamped lever with finger tab
    g = "selector"
    m.pin_x("selector_axle", 8.92, 9.95, 15.6, 0.32, 8.82, 9.0, "steel", g)
    with m.frame(("x", -5.0, (8.9, 9.95, 15.6))):
        m.bevel("selector_plate", 8.86, 9.65, 10.2, 8.98, 10.25, 15.8, 0.08, "steel", g, axis="x")
        B("selector_rib", 8.98, 9.85, 10.6, 9.02, 10.05, 15.3, "steel", g)
    with m.frame(("x", 30.0, (8.9, 9.75, 10.4))):
        m.bevel("selector_tab", 8.86, 8.95, 10.1, 9.06, 9.85, 10.6, 0.06, "steel", g, "knurl", axis="x")
    for k, y in enumerate((9.25, 8.85, 8.45)):
        B("selector_detent_%d" % k, 8.82, y, 11.0, 8.85, y + 0.18, 11.3, "steel_light", g)

    # ======================================================================
    # top cover (dust cover) with recoil spring button
    # ======================================================================
    g = "top_cover"
    m.bevel("cover", 7.12, 10.5, 5.7, 8.88, 11.3, 17.3, 0.38, "steel", g)
    B("cover_ridge", 7.6, 11.28, 6.0, 8.4, 11.36, 16.9, "steel", g)
    m.bevel("cover_rear_lip", 7.18, 10.35, 17.1, 8.82, 11.12, 17.45, 0.2, "steel", g)
    m.cyl_z("recoil_button", CX, 10.62, 17.4, 17.75, 0.22, "steel_light", g)
    m.cyl_z("rear_trunnion_lug", CX, 10.62, 17.4, 17.55, 0.32, "steel", g)

    # ======================================================================
    # trigger, bolt carrier with charging handle
    # ======================================================================
    g = "trigger"
    B("trigger_top", 7.88, 7.4, 11.7, 8.12, 7.85, 12.0, "steel", g)
    with m.frame(("x", 14, (8, 7.45, 11.85))):
        B("trigger_mid", 7.88, 6.95, 11.7, 8.12, 7.5, 12.0, "steel", g)
    with m.frame(("x", 34, (8, 7.0, 11.7))):
        B("trigger_tip", 7.88, 6.7, 11.62, 8.12, 7.05, 11.92, "steel", g)

    g = "bolt"
    m.bevel("bolt_carrier", 8.72, 9.9, 7.4, 8.86, 10.5, 13.4, 0.05, "steel_light", g, axis="x")
    B("bolt_head", 8.7, 9.95, 7.35, 8.84, 10.45, 7.95, "steel", g)
    B("bolt_extractor", 8.84, 10.05, 7.4, 8.88, 10.35, 7.9, "steel_dark", g)
    m.cyl_x("charging_stem", 8.86, 9.55, 10.18, 9.6, 0.17, "steel_light", g)
    with m.frame(("y", -12, (9.55, 10.18, 9.6))):
        m.cyl_x("charging_knob", 9.5, 10.15, 10.18, 9.6, 0.3, "steel_light", g)
        B("charging_knob_cap", 10.15, 9.95, 9.37, 10.2, 10.41, 9.83, "steel_light", g)

    # ======================================================================
    # wooden pistol grip (17 deg rake)
    # ======================================================================
    g = "grip"
    with m.frame(("x", -17, (8, 7.85, 14.5))):
        m.bevel("grip_neck", 7.22, 7.2, 13.55, 8.78, 8.15, 15.45, 0.15, "wood", g, "wood", axis="x")
        m.bevel("grip_body", 7.18, 3.0, 13.6, 8.82, 7.6, 15.45, 0.42, "wood", g, "wood", axis="y")
        m.bevel("grip_belly", 7.24, 3.6, 13.42, 8.76, 6.6, 13.7, 0.12, "wood", g, "wood", axis="y")
        m.bevel("grip_cap", 7.25, 2.8, 13.7, 8.75, 3.05, 15.35, 0.14, "steel", g, axis="y")
        m.cyl_z("grip_bolt_nut", CX, 2.72, 14.25, 14.85, 0.22, "steel_light", g)
        for k in range(5):
            y = 3.6 + k * 0.75
            B("grip_check_l_%d" % k, 7.16, y, 13.85, 7.18, y + 0.4, 15.15, "wood_dark", g)
            B("grip_check_r_%d" % k, 8.82, y, 13.85, 8.84, y + 0.4, 15.15, "wood_dark", g)

    # ======================================================================
    # wooden butt stock: top slab (comb), bottom slab (belly), wrist,
    # steel butt plate with trap door, sling swivel
    # ======================================================================
    g = "stock"
    m.bevel("stock_tang", 7.4, 8.1, 17.4, 8.6, 10.4, 18.3, 0.2, "steel", g)
    # three slabs of identical width so their sides blend into one surface;
    # only the outer edges (comb top, belly bottom) carry visible chamfers
    with m.frame(("x", 2.3, (8, 10.3, 17.6))):
        m.bevel("stock_comb", 7.15, 7.6, 17.6, 8.85, 10.3, 28.95, 0.45, "wood_s", g, "wood", edges="top")
    with m.frame(("x", 11.0, (8, 7.55, 18.4))):
        B("stock_mid", 7.16, 7.0, 18.4, 8.84, 9.6, 29.0, "wood_s", g, "wood")
    with m.frame(("x", 20.0, (8, 7.55, 18.4))):
        m.bevel("stock_belly", 7.17, 7.55, 18.4, 8.83, 10.0, 29.3, 0.45, "wood_s", g, "wood", edges="bottom")
    with m.frame(("x", 24.0, (8, 7.9, 17.6))):
        m.bevel("stock_wrist", 7.24, 7.9, 17.6, 8.76, 9.8, 19.4, 0.38, "wood_s", g, "wood")
    with m.frame(("x", 6.0, (8, 6.4, 29.0))):
        m.bevel("butt_plate", 7.05, 3.3, 29.0, 8.95, 10.1, 29.4, 0.32, "steel", g)
        m.bevel("trap_door", 7.5, 4.9, 29.4, 8.5, 8.5, 29.47, 0.12, "steel", g)
        B("trap_door_hinge", 7.65, 8.5, 29.38, 8.35, 8.7, 29.51, "steel_light", g)
        B("trap_door_latch", 7.85, 4.7, 29.4, 8.15, 4.9, 29.5, "steel_light", g)
        for k, y in enumerate((3.7, 9.7)):
            m.pin_x("butt_screw_%d" % k, 8.0, y, 29.45, 0.12, 7.9, 8.1, "steel_light", g,
                    rot=("y", 90, (8.0, y, 29.45)))
    # sling swivel on the left of the stock
    with m.frame(("x", 20.0, (8, 7.55, 18.4))):
        m.pin_x("stock_swivel_base", 7.08, 8.4, 26.6, 0.26, 6.98, 7.15, "steel", g)
        B("stock_swivel_a", 6.88, 8.25, 26.0, 6.98, 8.4, 27.2, "steel_light", g)
        B("stock_swivel_b", 6.88, 7.4, 26.0, 6.98, 8.25, 26.15, "steel_light", g)
        B("stock_swivel_c", 6.88, 7.4, 27.05, 6.98, 8.25, 27.2, "steel_light", g)
        B("stock_swivel_d", 6.88, 7.25, 26.0, 6.98, 7.4, 27.2, "steel_light", g)

    # ======================================================================
    # steel 30 round magazine, smoothly curved (12 segments)
    # ======================================================================
    g = "magazine"
    zc = 7.65
    B("mag_feed_lips", 7.45, 7.75, 5.95, 8.55, 8.15, 9.3, "steel_mag", g)
    B("mag_round", 7.6, 8.15, 6.2, 8.4, 8.42, 9.2, "brass", g)
    m.cyl_z("mag_round_bullet", CX, 8.28, 5.85, 6.25, 0.13, "brass", g)
    B("mag_front_lug", 7.62, 7.5, 5.8, 8.38, 7.95, 6.0, "steel_mag", g)
    B("mag_rear_lug", 7.58, 7.1, 9.35, 8.42, 7.6, 9.6, "steel_mag", g)
    seg = 0.92
    angles = [0, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25]
    last = None
    for k, (rot, (yt, z0)) in enumerate(m.chain((7.8, zc), seg, angles)):
        with m.frame(rot):
            d0, d1 = z0 - 1.62, z0 + 1.62
            m.bevel("mag_seg_%02d" % k, 7.26, yt - seg - 0.03, d0, 8.74, yt, d1, 0.18, "steel_mag", g,
                    axis="y")
            # stamped side ribs
            B("mag_rib_l_%02d" % k, 7.22, yt - seg - 0.02, d0 + 0.75, 7.26, yt, d0 + 1.25, "steel_mag", g)
            B("mag_rib_r_%02d" % k, 8.74, yt - seg - 0.02, d0 + 0.75, 8.78, yt, d0 + 1.25, "steel_mag", g)
            B("mag_rib2_l_%02d" % k, 7.22, yt - seg - 0.02, d1 - 1.0, 7.26, yt, d1 - 0.6, "steel_mag", g)
            B("mag_rib2_r_%02d" % k, 8.74, yt - seg - 0.02, d1 - 1.0, 8.78, yt, d1 - 0.6, "steel_mag", g)
        last = (rot, yt - seg, z0)
    rot, yb, z0 = last
    with m.frame(rot):
        m.bevel("mag_floorplate", 7.18, yb - 0.32, z0 - 1.78, 8.82, yb + 0.02, z0 + 1.7, 0.1, "steel_mag", g,
                axis="y")
        B("mag_floor_tab", 7.75, yb - 0.35, z0 + 1.7, 8.25, yb - 0.05, z0 + 1.95, "steel_mag", g)
        m.pin_x("mag_floor_button", 8.0, yb - 0.33, z0 + 0.6, 0.18, 7.8, 8.2, "steel_light", g,
                rot=("z", 90, (8.0, yb - 0.33, z0 + 0.6)))

    m.regroup({}, pivots={"magazine": (8, 7.8, 6.0), "trigger": (8, 7.8, 11.85),
                          "bolt": (9.0, 10.2, 10.0), "selector": (8.9, 9.95, 15.6),
                          "top_cover": (8, 10.6, 17.4)})
    m.dynamic = {"magazine", "trigger", "bolt", "selector", "top_cover"}
    return m


GRIP_POINT = (8.0, 5.6, 15.0)

DISPLAY = {"hand": 0.38, "fp": 0.4, "gui": 0.31, "tilt": 30, "push": -2.5}

ANIMATIONS = {
    "shoot": (0.1, {
        "bolt": {"position": {0.0: [0, 0, 0], 0.025: [0, 0, 3.6], 0.1: [0, 0, 0]}},
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [-12, 0, 0], 0.08: [0, 0, 0]}},
    }),
    # rock-in magazine change, then rack the charging handle
    "reload": (2.4, {
        "magazine": {
            "rotation": {0.0: [0, 0, 0], 0.25: [22, 0, 0], 0.7: [22, 0, 0], 1.15: [22, 0, 0],
                         1.4: [0, 0, 0]},
            "position": {0.0: [0, 0, 0], 0.25: [0, -0.6, -0.4], 0.65: [0, -18, -2.0], 0.66: [0, -18, -2.0],
                         1.15: [0, -0.6, -0.4], 1.4: [0, 0, 0]}},
        "bolt": {"position": {1.75: [0, 0, 0], 1.9: [0, 0, 4.2], 2.05: [0, 0, 0]}},
    }),
}

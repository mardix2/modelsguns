"""MK18 Mod 1 (CQBR), bare rifle without optics or accessories.

10.3" barrel with birdcage flash hider, Daniel Defense RIS II handguard,
flat-top upper with open ejection port (bolt carrier visible), Mil-Spec lower,
Magpul-style grip, CTR stock and a curved 30 rd PMAG.

Scale: 1 model unit ~= 15.6 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "alu": Material((60, 61, 66), 5),          # black anodised aluminium
    "alu_dark": Material((40, 41, 44), 4),
    "steel": Material((60, 60, 64), 7),        # phosphated steel
    "steel_light": Material((92, 92, 96), 7),  # bolt / carrier
    "steel_dark": Material((32, 32, 35), 5),
    "polymer": Material((48, 48, 46), 6),
    "fde": Material((160, 133, 94), 8),        # Magpul FDE
    "fde_dark": Material((132, 108, 74), 7),
    "rubber": Material((26, 26, 26), 5),
    "brass": Material((176, 140, 64), 8),
    "bore": Material((6, 6, 6), 1, edge=False),
    "red": Material((150, 30, 26), 4, edge=False),
    "white": Material((205, 205, 198), 3, edge=False),
}


def build():
    m = Model("mk18", MATERIALS, density=8)
    B = m.box
    cx, cy = 8.0, 10.0  # bore axis

    # ======================================================================
    # barrel + A2 style birdcage
    # ======================================================================
    g = "barrel"
    m.cyl_z("fh_front_ring", cx, cy, -14.4, -14.1, 0.56, "steel_dark", g)
    m.ring_z("fh_cage", cx, cy, -14.1, -12.75, 0.56, 0.14, 0.62, "steel_dark", g)
    B("fh_cage_floor", 7.55, 9.44, -14.1, 8.45, 9.6, -12.75, "steel_dark", g)
    m.cyl_z("fh_inner", cx, cy, -14.08, -12.75, 0.3, "bore", g)
    m.cyl_z("fh_body", cx, cy, -12.75, -11.95, 0.56, "steel_dark", g)
    m.cyl_z("crush_washer", cx, cy, -11.95, -11.8, 0.5, "steel", g)
    B("fh_bore", 7.76, 9.76, -14.44, 8.24, 10.24, -14.42, "bore", g, "bore")
    m.cyl_z("barrel", cx, cy, -11.8, -10.6, 0.4, "steel", g)
    m.cyl_z("barrel_shoulder", cx, cy, -10.85, -10.6, 0.46, "steel", g)

    # ======================================================================
    # Daniel Defense RIS II handguard
    # ======================================================================
    g = "handguard"
    z0, z1 = -10.5, 5.0
    B("hg_core_h", 6.65, 9.25, z0, 9.35, 10.75, z1, "alu", g)
    B("hg_core_v", 7.25, 8.65, z0 + 0.005, 8.75, 11.35, z1 - 0.005, "alu", g)
    for i, ang in enumerate((45, -45)):
        B("hg_chamfer%d" % i, cx - 1.45, cy - 0.45, z0 + 0.02, cx + 1.45, cy + 0.45, z1 - 0.02,
          "alu", g, rot=("z", ang, (cx, cy, (z0 + z1) / 2)))
    rz0, rz1 = -10.4, 4.9
    tz0 = -10.3
    # top rail
    B("rail_top_neck", 7.4, 11.35, rz0, 8.6, 11.55, rz1, "alu", g)
    B("rail_top_base", 7.25, 11.55, rz0, 8.75, 11.72, rz1, "alu", g)
    m.teeth_z("rail_top_t", "up", 7.25, 8.75, 11.72, 0.2, tz0, rz1, "alu", g)
    # bottom rail
    B("rail_bot_neck", 7.4, 8.45, rz0, 8.6, 8.65, rz1, "alu", g)
    B("rail_bot_base", 7.25, 8.28, rz0, 8.75, 8.45, rz1, "alu", g)
    m.teeth_z("rail_bot_t", "down", 7.25, 8.75, 8.28, 0.2, tz0, rz1, "alu", g)
    # right rail
    B("rail_r_neck", 9.35, 9.4, rz0, 9.55, 10.6, rz1, "alu", g)
    B("rail_r_base", 9.55, 9.25, rz0, 9.72, 10.75, rz1, "alu", g)
    m.teeth_z("rail_r_t", "right", 9.25, 10.75, 9.72, 0.2, tz0, rz1, "alu", g)
    # left rail
    B("rail_l_neck", 6.45, 9.4, rz0, 6.65, 10.6, rz1, "alu", g)
    B("rail_l_base", 6.28, 9.25, rz0, 6.45, 10.75, rz1, "alu", g)
    m.teeth_z("rail_l_t", "left", 9.25, 10.75, 6.28, 0.2, tz0, rz1, "alu", g)
    # 45 deg dovetail flanks under each rail base
    for nm, (px_, py_) in {"top": (0, 1), "bot": (0, -1), "r": (1, 0), "l": (-1, 0)}.items():
        for k, sgn in enumerate((-1, 1)):
            if py_:
                xc, yc = cx + sgn * 0.68, cy + py_ * 1.48
                ang = 45 if sgn * py_ > 0 else -45
                B("rail_%s_dove_%d" % (nm, k), xc - 0.12, yc - 0.05, rz0 + 0.01, xc + 0.12, yc + 0.05,
                  rz1 - 0.01, "alu", g, rot=("z", ang, (xc, yc, (rz0 + rz1) / 2)))
            else:
                xc, yc = cx + px_ * 1.48, cy + sgn * 0.68
                ang = -45 if sgn * px_ > 0 else 45
                B("rail_%s_dove_%d" % (nm, k), xc - 0.05, yc - 0.12, rz0 + 0.01, xc + 0.05, yc + 0.12,
                  rz1 - 0.01, "alu", g, rot=("z", ang, (xc, yc, (rz0 + rz1) / 2)))
    # rail end stops
    for nm, box in {"top": (7.3, 11.72, 8.7, 11.92), "bot": (7.3, 8.08, 8.7, 8.28),
                    "r": (9.72, 9.3, 9.92, 10.7), "l": (6.08, 9.3, 6.28, 10.7)}.items():
        B("rail_%s_stop" % nm, box[0], box[1], -10.45, box[2], box[3], -10.3, "alu_dark", g)
    # front end cap with sling loop
    m.bevel("hg_front_cap", 6.8, 8.8, -10.62, 9.2, 11.2, -10.5, 0.3, "alu_dark", g)
    B("hg_sling_loop_a", 6.2, 8.5, -10.3, 6.4, 8.7, -9.3, "steel", g)
    B("hg_sling_loop_b", 6.2, 8.7, -10.3, 6.4, 9.2, -10.15, "steel", g)
    B("hg_sling_loop_c", 6.2, 8.7, -9.45, 6.4, 9.2, -9.3, "steel", g)
    # cross bolts on the lower diagonals (rail locking bolts)
    for i, zc in enumerate((-1.0, 2.6)):
        for j, ang in enumerate((45, -45)):
            B("hg_bolt_%d_%d" % (i, j), cx - 0.2, cy - 1.57, zc - 0.2, cx + 0.2, cy - 1.42, zc + 0.2,
              "steel_dark", g, rot=("z", ang, (cx, cy, zc)))
    for i, zc in enumerate((-1.0, 2.6)):
        for j, ang in enumerate((45, -45)):
            B("hg_nut_%d_%d" % (i, j), cx - 0.22, cy + 1.42, zc - 0.22, cx + 0.22, cy + 1.57, zc + 0.22,
              "steel_dark", g, rot=("z", ang, (cx, cy, zc)))
    # rail locking lever at the bottom rear
    B("hg_lock_lever", 7.65, 7.88, 3.4, 8.35, 8.08, 4.85, "steel_dark", g)
    B("hg_lock_lever_tab", 7.55, 7.75, 4.55, 8.45, 7.9, 4.85, "steel_dark", g)
    # barrel nut with wrench notches
    m.cyl_z("barrel_nut", cx, cy, 4.98, 5.4, 1.2, "steel_dark", g)
    for i, (a, b) in enumerate(((7.75, 8.25),)):
        B("nut_notch_top", a, 11.08, 5.0, b, 11.22, 5.38, "bore", g)
        B("nut_notch_bot", a, 8.78, 5.0, b, 8.92, 5.38, "bore", g)
        B("nut_notch_r", 9.08, 9.75, 5.0, 9.22, 10.25, 5.38, "bore", g)
        B("nut_notch_l", 6.78, 9.75, 5.0, 6.92, 10.25, 5.38, "bore", g)

    # ======================================================================
    # upper receiver (flat top, ejection port open)
    # ======================================================================
    g = "upper"
    B("upper_left", 7.2, 9.0, 5.4, 8.2, 11.05, 15.6, "alu", g)
    B("upper_left_top", 7.5, 11.05, 5.4, 8.2, 11.35, 15.6, "alu", g)
    B("upper_top_r", 8.2, 10.55, 5.4, 8.8, 11.05, 15.6, "alu", g)
    B("upper_top_r_top", 8.2, 11.05, 5.4, 8.5, 11.35, 15.6, "alu", g)
    m.edge("upper_chamfer_l", "z", 5.4, 15.6, 7.2, 11.35, -1, 1, 0.3, "alu", g)
    m.edge("upper_chamfer_r", "z", 5.4, 15.6, 8.8, 11.35, 1, 1, 0.3, "alu", g)
    B("upper_bot_r", 8.2, 9.0, 5.4, 8.8, 9.5, 15.6, "alu", g)
    B("upper_front_r", 8.2, 9.5, 5.4, 8.8, 10.55, 8.3, "alu", g)
    B("upper_rear_r", 8.2, 9.5, 11.2, 8.8, 10.55, 15.6, "alu", g)
    B("upper_reinforce_l", 7.1, 9.55, 5.4, 7.2, 10.45, 6.6, "alu", g)
    B("upper_reinforce_r", 8.8, 9.55, 5.4, 8.9, 10.45, 6.6, "alu", g)
    B("upper_lip_l", 7.15, 9.0, 6.6, 7.2, 9.15, 15.4, "alu_dark", g)
    # bolt carrier group seen through the port
    B("bcg_carrier", 7.9, 9.5, 8.3, 8.45, 10.55, 11.2, "steel_light", g)
    B("bcg_carrier_serr", 8.45, 9.6, 9.9, 8.5, 10.45, 11.15, "steel_light", g, "serration")
    m.pin_x("bcg_cam_pin", 8.47, 10.05, 9.4, 0.17, 8.4, 8.5, "steel", g)
    B("bcg_bolt", 7.95, 9.7, 8.3, 8.47, 10.4, 8.95, "steel", g)
    B("bcg_extractor", 8.47, 9.95, 8.3, 8.51, 10.35, 8.9, "steel_dark", g)
    B("port_rim_top", 8.8, 10.5, 8.25, 8.86, 10.6, 11.25, "alu_dark", g)
    # dust cover hanging open on its hinge rod
    B("dust_hinge_rod", 8.8, 9.32, 8.1, 8.95, 9.47, 11.4, "steel", g)
    B("dust_cover", 8.86, 8.3, 8.3, 8.94, 9.38, 11.2, "steel_dark", g)
    B("dust_cover_bump", 8.94, 8.55, 8.7, 9.0, 8.75, 10.8, "steel_dark", g)
    B("dust_cover_lip", 8.86, 8.22, 8.3, 9.02, 8.3, 11.2, "steel_dark", g)
    B("dust_hinge_boss_f", 8.8, 9.25, 7.95, 9.0, 9.55, 8.15, "alu", g)
    B("dust_hinge_boss_b", 8.8, 9.25, 11.35, 9.0, 9.55, 11.55, "alu", g)
    for i in range(3):
        B("dust_spring_%d" % i, 8.95, 9.3, 11.0 - i * 0.18, 9.02, 9.5, 11.08 - i * 0.18, "steel", g)
    B("upper_pivot_lug", 7.6, 8.75, 6.6, 8.4, 9.0, 7.4, "alu", g)
    B("upper_takedown_lug", 7.6, 8.75, 15.0, 8.4, 9.0, 15.6, "alu", g)
    # brass deflector
    B("brass_deflector", 8.8, 9.9, 11.3, 9.3, 11.0, 12.1, "alu", g)
    B("brass_deflector_ramp", 8.8, 10.0, 11.05, 9.08, 10.9, 11.3, "alu", g)
    # forward assist
    m.bevel("fa_housing", 8.8, 9.95, 12.1, 9.5, 10.95, 13.9, 0.12, "alu", g)
    m.cyl_z("fa_button", 9.2, 10.45, 13.9, 14.75, 0.36, "steel_dark", g, "knurl")
    B("fa_button_cap", 9.0, 10.25, 14.75, 9.4, 10.65, 14.85, "steel_dark", g)
    # charging handle
    B("ch_shaft", 7.6, 10.75, 15.6, 8.4, 11.3, 16.3, "alu", g)
    m.bevel("ch_handle", 6.7, 10.75, 16.3, 9.3, 11.3, 16.75, 0.08, "alu", g, axis="x")
    B("ch_latch", 6.35, 10.8, 15.85, 6.95, 11.25, 16.75, "steel_dark", g)
    for i in range(3):
        B("ch_latch_grip_%d" % i, 6.3, 10.85, 16.0 + i * 0.25, 6.35, 11.2, 16.12 + i * 0.25,
          "steel_dark", g)
    # flat-top rail
    B("upper_rail_neck", 7.4, 11.35, 5.4, 8.6, 11.55, 15.4, "alu", g)
    B("upper_rail_base", 7.25, 11.55, 5.4, 8.75, 11.72, 15.4, "alu", g)
    m.teeth_z("upper_rail_t", "up", 7.25, 8.75, 11.72, 0.2, 5.5, 15.4, "alu", g)

    # ======================================================================
    # lower receiver
    # ======================================================================
    g = "lower"
    m.bevel("lower_top", 7.25, 8.2, 7.1, 8.75, 9.0, 16.0, 0.05, "alu", g)
    B("lower_pocket_l", 7.22, 7.4, 10.9, 7.3, 8.15, 12.2, "alu_dark", g)
    B("lower_pocket_r", 8.7, 7.4, 10.9, 8.78, 8.15, 12.2, "alu_dark", g)
    B("magwell_bevel", 7.15, 5.95, 6.75, 8.85, 6.6, 7.25, "alu", g, rot=("x", -22.5, (8, 6.3, 7.0)))
    B("lower_mid", 7.3, 7.3, 10.3, 8.7, 8.2, 15.6, "alu", g,
      text={"west": "SAFE SEMI"})
    m.bevel("magwell", 7.05, 5.9, 7.0, 8.95, 9.0, 10.3, 0.18, "alu", g, axis="y",
      text={"west": "MK18\nMOD 1\n5.56", "east": "CAL\n5.56"})
    B("magwell_front_rib", 7.6, 6.15, 6.85, 8.4, 8.8, 7.0, "alu", g)
    B("magwell_rim_l", 6.95, 5.65, 6.9, 7.05, 6.15, 10.4, "alu", g)
    B("magwell_rim_r", 8.95, 5.65, 6.9, 9.05, 6.15, 10.4, "alu", g)
    B("magwell_rim_f", 7.05, 5.65, 6.9, 8.95, 6.15, 7.0, "alu", g)
    B("magwell_rim_b", 7.05, 5.65, 10.3, 8.95, 6.15, 10.4, "alu", g)
    B("receiver_ring", 7.35, 8.2, 15.6, 8.65, 10.9, 16.0, "alu", g)
    B("receiver_tang", 7.4, 7.3, 15.4, 8.6, 7.85, 16.4, "alu", g)
    # pins (both sides)
    for side, (a, b) in (("l", (7.17, 7.25)), ("r", (8.75, 8.83))):
        m.pin_x("front_pivot_" + side, (a + b) / 2, 8.62, 7.45, 0.17, a, b, "steel", g)
        m.pin_x("rear_takedown_" + side, (a + b) / 2, 8.62, 15.45, 0.17, a, b, "steel", g)
        m.pin_x("trigger_pin_" + side, (a + b) / 2, 8.45, 11.5, 0.12, a, b, "steel", g)
        m.pin_x("hammer_pin_" + side, (a + b) / 2, 8.5, 12.55, 0.12, a, b, "steel", g)
    # bolt catch
    B("bc_boss_f", 7.0, 7.6, 9.4, 7.25, 8.9, 9.5, "alu", g)
    B("bc_boss_r", 7.0, 7.6, 10.7, 7.25, 8.9, 10.8, "alu", g)
    B("bolt_catch", 6.98, 7.7, 9.6, 7.25, 8.8, 10.6, "steel_dark", g)
    B("bolt_catch_paddle", 6.9, 8.55, 9.5, 7.25, 8.88, 10.7, "steel_dark", g, "knurl")
    B("bolt_catch_lower", 6.92, 7.6, 9.7, 7.25, 7.85, 10.5, "steel_dark", g, "knurl")
    m.pin_x("bolt_catch_roll_pin", 6.96, 8.15, 10.1, 0.08, 6.94, 6.98, "steel", g)
    # magazine release + fence
    B("mag_release", 8.75, 7.5, 10.35, 9.08, 8.1, 10.85, "steel_dark", g, "knurl")
    B("mag_fence_f", 8.75, 7.35, 10.15, 8.98, 8.25, 10.3, "alu", g)
    B("mag_fence_b", 8.75, 7.35, 10.9, 8.98, 8.25, 11.05, "alu", g)
    B("mag_fence_low", 8.75, 7.3, 10.15, 8.98, 7.45, 11.05, "alu", g)
    B("mag_catch_l", 7.15, 7.6, 10.4, 7.25, 8.0, 10.8, "steel", g)
    # safety selector (ambi, on SAFE)
    m.pin_x("selector_hub_l", 7.1, 8.45, 14.1, 0.28, 6.98, 7.25, "steel_dark", g)
    B("selector_lever_l", 6.93, 8.3, 12.85, 7.12, 8.6, 14.15, "steel_dark", g)
    B("selector_tip_l", 6.88, 8.25, 12.75, 7.12, 8.65, 13.15, "steel_dark", g, "knurl")
    B("selector_mark_safe", 7.23, 9.0 - 0.25, 12.9, 7.26, 8.95, 13.1, "white", g)
    B("selector_mark_fire", 7.23, 7.65, 14.0, 7.26, 7.85, 14.2, "red", g)
    m.pin_x("selector_hub_r", 8.9, 8.45, 14.1, 0.2, 8.75, 8.95, "steel_dark", g)
    B("selector_lever_r", 8.88, 8.32, 14.1, 9.02, 8.58, 14.75, "steel_dark", g)
    # trigger (curved, three segments)
    B("trigger_top", 7.87, 7.75, 11.3, 8.13, 8.4, 11.6, "steel", g)
    B("trigger_mid", 7.87, 7.1, 11.3, 8.13, 7.8, 11.6, "steel", g,
      rot=("x", 22.5, (8, 7.78, 11.45)))
    B("trigger_tip", 7.87, 6.7, 11.0, 8.13, 7.1, 11.3, "steel", g,
      rot=("x", 45, (8, 7.1, 11.15)))
    # trigger guard (enhanced, dropped rear)
    B("tg_front_ear", 7.55, 6.1, 10.3, 8.45, 6.9, 10.55, "polymer", g)
    B("tg_bottom", 7.6, 6.1, 10.3, 8.4, 6.45, 12.4, "polymer", g)
    B("tg_rear", 7.6, 5.9, 12.3, 8.4, 6.3, 13.5, "polymer", g)
    B("tg_rear_rise", 7.6, 6.2, 13.2, 8.4, 7.35, 13.55, "polymer", g)
    m.pin_x("tg_roll_pin", 7.53, 6.6, 10.42, 0.08, 7.5, 7.56, "steel", g)

    # pistol grip, raked back 22.5 deg (all parts share one pivot)
    gr = ("x", -22.5, (8, 7.3, 14.05))
    B("grip_neck", 7.25, 7.2, 12.9, 8.75, 8.2, 15.2, "polymer", g, rot=gr)
    m.bevel("grip_body", 7.05, 3.4, 12.7, 8.95, 7.4, 15.4, 0.15, "polymer", g, "stipple", axis="y", rot=gr)
    B("grip_panel_l", 6.98, 4.0, 13.0, 7.05, 6.7, 15.0, "polymer", g, "stipple", rot=gr)
    B("grip_panel_r", 8.95, 4.0, 13.0, 9.02, 6.7, 15.0, "polymer", g, "stipple", rot=gr)
    B("grip_frontstrap", 7.25, 3.6, 12.55, 8.75, 7.0, 12.7, "polymer", g, "stipple", rot=gr)
    B("grip_finger_bump", 7.35, 5.1, 12.35, 8.65, 5.7, 12.55, "polymer", g, rot=gr)
    for i in range(3):
        y = 4.3 + i * 0.85
        B("grip_finger_line_%d" % i, 7.3, y, 12.5, 8.7, y + 0.12, 12.56, "polymer", g, rot=gr)
    B("grip_backstrap", 7.25, 4.0, 15.4, 8.75, 7.2, 15.6, "polymer", g, "stipple", rot=gr)
    B("grip_beavertail", 7.3, 7.0, 15.4, 8.7, 7.4, 16.15, "polymer", g, rot=gr)
    m.bevel("grip_cap", 7.0, 3.12, 12.6, 9.0, 3.4, 15.5, 0.1, "polymer", g, axis="y", rot=gr)
    B("grip_cap_door", 7.4, 3.08, 13.2, 8.6, 3.12, 15.1, "polymer", g, rot=gr)
    B("grip_cap_latch", 7.8, 3.05, 15.1, 8.2, 3.2, 15.35, "polymer", g, rot=gr)
    B("grip_screw", 7.9, 3.06, 13.4, 8.1, 3.08, 13.6, "steel", g, rot=gr)

    # ======================================================================
    # buffer tube + Magpul CTR stock
    # ======================================================================
    g = "stock"
    B("end_plate", 6.95, 8.7, 16.0, 9.05, 10.9, 16.25, "steel_dark", g)
    B("end_plate_qd", 6.6, 9.3, 16.0, 6.95, 9.9, 16.55, "steel_dark", g)
    B("end_plate_qd_hole", 6.58, 9.45, 16.12, 6.6, 9.75, 16.42, "bore", g)
    m.cyl_z("castle_nut_core", cx, 9.95, 16.25, 16.75, 0.62, "steel_dark", g)
    m.ring_z("castle_nut", cx, 9.95, 16.25, 16.75, 0.74, 0.14, 0.7, "steel_dark", g)
    m.cyl_z("buffer_tube", cx, 9.95, 16.75, 27.0, 0.58, "alu", g)
    B("castle_nut_stake_l", 7.33, 9.25, 16.75, 7.4, 9.4, 16.85, "steel", g)
    B("castle_nut_stake_r", 8.6, 9.25, 16.75, 8.67, 9.4, 16.85, "steel", g)
    m.cyl_z("tube_thread_ring", cx, 9.95, 16.75, 16.95, 0.64, "alu_dark", g)
    B("tube_key_rib", 7.72, 9.2, 16.75, 8.28, 9.42, 21.2, "alu", g)
    for i in range(6):
        z = 17.0 + i * 0.65
        B("tube_pos_hole_%d" % i, 7.86, 9.18, z, 8.14, 9.2, z + 0.3, "bore", g)
    m.bevel("stock_nose", 7.3, 9.3, 19.8, 8.7, 10.8, 20.5, 0.15, "polymer", g)
    m.bevel("stock_top", 7.15, 9.1, 20.5, 8.85, 11.0, 28.6, 0.18, "polymer", g)
    m.bevel("stock_cheek", 7.35, 10.95, 21.0, 8.65, 11.3, 28.5, 0.12, "polymer", g)
    B("stock_cheek_ramp", 7.4, 10.6, 20.3, 8.6, 10.95, 21.6, "polymer", g,
      rot=("x", 22.5, (8, 10.95, 21.0)))
    for i in range(4):
        z = 22.2 + i * 1.4
        B("stock_dimple_l_%d" % i, 7.12, 9.6, z, 7.15, 10.5, z + 0.9, "polymer", g, "stipple")
        B("stock_dimple_r_%d" % i, 8.85, 9.6, z, 8.88, 10.5, z + 0.9, "polymer", g, "stipple")
    # adjustment / friction lock levers
    B("ctr_lock_body", 7.55, 8.55, 20.0, 8.45, 9.1, 22.6, "polymer", g)
    B("ctr_lock_paddle", 7.5, 8.3, 21.8, 8.5, 8.55, 22.8, "polymer", g, "knurl")
    m.pin_x("ctr_lock_pin_l", 7.52, 8.82, 20.4, 0.1, 7.5, 7.55, "steel", g)
    m.pin_x("ctr_lock_pin_r", 8.48, 8.82, 20.4, 0.1, 8.45, 8.5, "steel", g)
    B("ctr_latch", 7.65, 8.75, 19.6, 8.35, 9.1, 20.0, "polymer", g)
    # skeleton: strut, rear web, toe
    m.bevel("stock_strut", 7.3, 8.4, 21.0, 8.7, 9.5, 27.2, 0.12, "polymer", g,
            rot=("x", 22.5, (8, 9.0, 21.2)))
    m.bevel("stock_web", 7.25, 4.6, 26.2, 8.75, 9.1, 28.6, 0.15, "polymer", g, axis="y")
    m.bevel("stock_toe", 7.3, 4.6, 25.4, 8.7, 5.6, 26.2, 0.12, "polymer", g)
    m.bevel("stock_brace", 7.4, 6.2, 22.6, 8.6, 6.75, 26.4, 0.1, "polymer", g,
            rot=("x", 22.5, (8, 6.4, 26.2)))
    B("stock_top_ridge_l", 7.3, 11.0, 21.2, 7.4, 11.12, 28.3, "polymer", g)
    B("stock_top_ridge_r", 8.6, 11.0, 21.2, 8.7, 11.12, 28.3, "polymer", g)
    B("stock_web_rib_l", 7.2, 5.0, 26.6, 7.25, 8.8, 26.9, "polymer", g)
    B("stock_web_rib_r", 8.75, 5.0, 26.6, 8.8, 8.8, 26.9, "polymer", g)
    # sling slots and QD cups
    B("sling_slot_l", 7.12, 9.5, 27.3, 7.15, 10.6, 28.2, "bore", g)
    B("sling_slot_r", 8.85, 9.5, 27.3, 8.88, 10.6, 28.2, "bore", g)
    for side, (a, b, h0, h1) in (("l", (6.95, 7.25, 6.93, 6.95)), ("r", (8.75, 9.05, 9.05, 9.07))):
        m.pin_x("qd_cup_" + side, (a + b) / 2, 6.4, 27.4, 0.38, a, b, "steel_dark", g)
        B("qd_cup_hole_" + side, h0, 6.25, 27.25, h1, 6.55, 27.55, "bore", g)
    # butt pad with ribs
    m.bevel("butt_pad", 6.95, 4.3, 28.6, 9.05, 11.4, 29.4, 0.2, "rubber", g, axis="z")
    i = 0
    y = 4.55
    while y + 0.25 <= 11.2:
        B("butt_rib_%d" % i, 7.05, y, 29.4, 8.95, y + 0.25, 29.62, "rubber", g)
        y += 0.5
        i += 1

    # ======================================================================
    # magazine (curved 30 rd PMAG)
    # ======================================================================
    g = "magazine"
    m.bevel("mag_top", 7.15, 2.9, 7.25, 8.85, 7.6, 10.0, 0.06, "fde", g, axis="y")
    B("mag_round", 7.6, 7.6, 7.5, 8.4, 7.95, 9.7, "brass", g)
    B("mag_fill", 7.15, 2.45, 8.9, 8.85, 3.0, 10.0, "fde", g)
    B("mag_spine_f", 7.6, 2.9, 7.12, 8.4, 5.9, 7.25, "fde", g)
    B("mag_spine_b", 7.6, 2.9, 10.0, 8.4, 5.9, 10.12, "fde", g)
    for i in range(5):
        y = 3.15 + i * 0.5
        B("mag_rib_l_%d" % i, 7.1, y, 7.45, 7.15, y + 0.2, 9.8, "fde", g)
        B("mag_rib_r_%d" % i, 8.85, y, 7.45, 8.9, y + 0.2, 9.8, "fde", g)
    for i in range(3):
        for j in range(2):
            z = 7.6 + i * 0.75
            y = 5.25 + j * 0.35
            B("mag_dot_l_%d%d" % (i, j), 7.1, y, z, 7.15, y + 0.2, z + 0.5, "fde_dark", g)
            B("mag_dot_r_%d%d" % (i, j), 8.85, y, z, 8.9, y + 0.2, z + 0.5, "fde_dark", g)
    mr = ("x", 22.5, (8, 3.1, 8.6))
    B("mag_curve", 7.15, -0.3, 7.25, 8.85, 3.1, 10.0, "fde", g, rot=mr)
    B("mag_curve_spine_f", 7.6, -0.3, 7.12, 8.4, 3.1, 7.25, "fde", g, rot=mr)
    B("mag_curve_spine_b", 7.6, -0.3, 10.0, 8.4, 3.1, 10.12, "fde", g, rot=mr)
    for i in range(5):
        y = -0.05 + i * 0.6
        B("mag_crib_l_%d" % i, 7.1, y, 7.45, 7.15, y + 0.22, 9.8, "fde", g, rot=mr)
        B("mag_crib_r_%d" % i, 8.85, y, 7.45, 8.9, y + 0.22, 9.8, "fde", g, rot=mr)
    m.bevel("mag_floorplate", 7.02, -0.72, 7.05, 8.98, -0.3, 10.3, 0.08, "fde_dark", g, axis="y", rot=mr)
    B("mag_floor_tab_f", 7.3, -0.6, 6.85, 8.7, -0.35, 7.05, "fde_dark", g, rot=mr)
    B("mag_floor_tab_b", 7.3, -0.75, 10.3, 8.7, -0.4, 10.6, "fde_dark", g, rot=mr)
    B("mag_floor_grip", 7.25, -0.76, 7.6, 8.75, -0.72, 9.8, "fde_dark", g, "knurl", rot=mr)
    # top round + follower visible at the magwell edge is hidden; add witness window
    B("mag_window_l", 7.12, 3.6, 9.55, 7.14, 5.6, 9.75, "bore", g)
    B("mag_window_r", 8.86, 3.6, 9.55, 8.88, 5.6, 9.75, "bore", g)
    for i in range(3):
        y = 3.75 + i * 0.6
        B("mag_round_l_%d" % i, 7.11, y, 9.57, 7.13, y + 0.25, 9.73, "brass", g)
        B("mag_round_r_%d" % i, 8.87, y, 9.57, 8.89, y + 0.25, 9.73, "brass", g)

    m.regroup({"bcg_": "bolt", "ch_": "charging_handle", "trigger_": "trigger",
               "dust_": "dust_cover"},
              pivots={"trigger": (8, 8.3, 11.45), "dust_cover": (8.87, 9.4, 9.75),
                      "magazine": (8, 6.0, 8.6), "bolt": (8, 10, 9.7),
                      "charging_handle": (8, 11.0, 16.2)})
    m.dynamic = {"bolt", "charging_handle", "trigger", "dust_cover", "magazine"}
    return m


# point (model units) that should sit in the player's hand
GRIP_POINT = (8.0, 5.5, 14.4)

DISPLAY = {"hand": 0.4, "fp": 0.42, "gui": 0.34, "tilt": 30, "push": -2.0}

# keyframes in model space (units = model pixels, degrees)
ANIMATIONS = {
    "shoot": (0.12, {
        "bolt": {"position": {0.0: [0, 0, 0], 0.03: [0, 0, 2.2], 0.12: [0, 0, 0]}},
        "trigger": {"rotation": {0.0: [0, 0, 0], 0.02: [-12, 0, 0], 0.1: [0, 0, 0]}},
    }),
    "reload": (2.0, {
        "magazine": {"position": {0.0: [0, 0, 0], 0.3: [0, -3, 0], 0.6: [0, -14, 0],
                                  0.61: [0, -14, 0], 1.1: [0, -3, 0], 1.3: [0, 0, 0]}},
        "charging_handle": {"position": {1.45: [0, 0, 0], 1.6: [0, 0, 2.8], 1.75: [0, 0, 0]}},
        "bolt": {"position": {1.45: [0, 0, 0], 1.6: [0, 0, 2.8], 1.75: [0, 0, 0]}},
    }),
}

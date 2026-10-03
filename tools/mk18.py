"""MK18 Mod 1 (CQBR): 10.3" barrel, Daniel Defense RIS II, EOTech EXPS3,
SureFire light, vertical grip, Magpul CTR stock and FDE PMAG.

Scale: 1 model unit ~= 15.6 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "alu": Material((52, 53, 57), 5),          # black anodised aluminium
    "steel": Material((58, 58, 62), 7),        # phosphated steel
    "steel_dark": Material((32, 32, 35), 5),
    "polymer": Material((42, 42, 40), 6),
    "fde": Material((160, 133, 94), 8),        # Magpul FDE
    "fde_dark": Material((132, 108, 74), 7),
    "rubber": Material((24, 24, 24), 5),
    "glass": Material((120, 175, 205), 4, alpha=90, edge=False),
    "lens": Material((240, 240, 215), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("mk18", MATERIALS, density=4)
    B = m.box
    cx, cy = 8.0, 10.0  # bore axis

    # ---- barrel / muzzle ---------------------------------------------------
    g = "barrel"
    m.cyl_z("flash_hider", cx, cy, -14.0, -12.4, 0.56, "steel_dark", g, "flash")
    B("muzzle_bore", 7.72, 9.72, -14.06, 8.28, 10.28, -14.03, "bore", g, "bore")
    m.cyl_z("barrel", cx, cy, -12.4, -10.5, 0.4, "steel", g)

    # ---- Daniel Defense RIS II handguard ----------------------------------
    g = "handguard"
    z0, z1 = -10.5, 5.0
    B("hg_core_h", 6.65, 9.25, z0, 9.35, 10.75, z1, "alu", g)
    B("hg_core_v", 7.25, 8.65, z0, 8.75, 11.35, z1, "alu", g)
    for i, ang in enumerate((45, -45)):
        B("hg_chamfer%d" % i, cx - 1.45, cy - 0.45, z0 + 0.02, cx + 1.45, cy + 0.45, z1 - 0.02,
          "alu", g, rot=("z", ang, (cx, cy, (z0 + z1) / 2)))
    rz0, rz1 = -10.4, 4.9
    # picatinny rails: narrow neck + slotted top on each side
    B("rail_top_neck", 7.4, 11.35, rz0, 8.6, 11.55, rz1, "alu", g)
    B("rail_top", 7.25, 11.55, rz0, 8.75, 11.9, rz1, "alu", g, "rail")
    B("rail_bot_neck", 7.4, 8.45, rz0, 8.6, 8.65, rz1, "alu", g)
    B("rail_bot", 7.25, 8.1, rz0, 8.75, 8.45, rz1, "alu", g, "rail")
    B("rail_r_neck", 9.35, 9.4, rz0, 9.55, 10.6, rz1, "alu", g)
    B("rail_r", 9.55, 9.25, rz0, 9.9, 10.75, rz1, "alu", g, "rail")
    B("rail_l_neck", 6.45, 9.4, rz0, 6.65, 10.6, rz1, "alu", g)
    B("rail_l", 6.1, 9.25, rz0, 6.45, 10.75, rz1, "alu", g, "rail")
    B("hg_front_cap", 6.8, 8.8, -10.62, 9.2, 11.2, -10.5, "steel_dark", g)
    B("barrel_nut", 6.9, 8.9, 4.98, 9.1, 11.1, 5.3, "steel_dark", g, "knurl")

    # ---- accessories on the rail ------------------------------------------
    g = "accessories"
    # folding front sight (deployed)
    B("fsight_base", 7.1, 11.9, -9.7, 8.9, 12.3, -8.3, "alu", g)
    B("fsight_ear_l", 7.2, 12.3, -9.4, 7.5, 13.7, -8.7, "alu", g)
    B("fsight_ear_r", 8.5, 12.3, -9.4, 8.8, 13.7, -8.7, "alu", g)
    B("fsight_post", 7.9, 12.3, -9.15, 8.1, 13.45, -8.95, "steel_dark", g)
    # vertical fore grip
    B("vfg_clamp", 7.05, 7.6, -5.2, 8.95, 8.1, -3.2, "polymer", g)
    B("vfg_body", 7.25, 4.7, -4.95, 8.75, 7.6, -3.45, "polymer", g, "stipple")
    B("vfg_cap", 7.15, 4.45, -5.05, 8.85, 4.7, -3.35, "polymer", g)
    # weapon light on the right rail
    B("light_mount", 9.9, 9.45, -8.6, 10.5, 10.55, -6.4, "alu", g)
    lx = 11.05
    m.cyl_z("light_body", lx, cy, -9.6, -5.5, 0.55, "steel", g)
    m.cyl_z("light_bezel", lx, cy, -10.95, -9.6, 0.7, "alu", g, "knurl")
    B("light_lens", lx - 0.5, cy - 0.5, -10.98, lx + 0.5, cy + 0.5, -10.96, "lens", g, "lens")
    m.cyl_z("light_tailcap", lx, cy, -5.5, -5.05, 0.42, "rubber", g)

    # ---- upper receiver ----------------------------------------------------
    g = "upper"
    B("upper_body", 7.2, 9.0, 5.0, 8.8, 11.35, 15.6, "alu", g, "logo")
    B("upper_rail_neck", 7.4, 11.35, 5.3, 8.6, 11.55, 15.4, "alu", g)
    B("upper_rail", 7.25, 11.55, 5.3, 8.75, 11.9, 15.4, "alu", g, "rail")
    B("dust_cover", 8.8, 9.5, 8.3, 8.87, 10.55, 11.2, "steel_dark", g)
    B("dust_cover_rod", 8.8, 9.35, 8.2, 8.92, 9.5, 11.3, "steel", g)
    B("brass_deflector", 8.8, 9.9, 11.3, 9.3, 11.0, 12.1, "alu", g)
    B("fwd_assist_housing", 8.8, 10.0, 12.1, 9.45, 10.9, 13.9, "alu", g)
    B("fwd_assist_knob", 8.9, 10.1, 13.9, 9.55, 10.8, 14.75, "steel_dark", g, "knurl")
    B("charging_handle", 7.6, 10.75, 15.6, 8.4, 11.3, 16.3, "alu", g)
    B("charging_handle_t", 6.7, 10.75, 16.3, 9.3, 11.3, 16.75, "alu", g)
    B("charging_latch", 6.4, 10.8, 15.9, 6.9, 11.25, 16.75, "steel_dark", g)

    # ---- lower receiver ----------------------------------------------------
    g = "lower"
    B("lower_body", 7.25, 7.3, 7.1, 8.75, 9.0, 16.0, "alu", g, "logo")
    B("magwell", 7.05, 5.9, 7.0, 8.95, 9.0, 10.3, "alu", g)
    B("magwell_flare", 6.95, 5.65, 6.9, 9.05, 6.15, 10.4, "alu", g)
    B("trigger_guard", 7.6, 6.1, 10.3, 8.4, 6.45, 13.4, "polymer", g)
    B("trigger_upper", 7.87, 7.4, 11.3, 8.13, 8.2, 11.6, "steel", g)
    B("trigger_lower", 7.87, 6.75, 11.3, 8.13, 7.5, 11.6, "steel", g,
      rot=("x", 22.5, (8, 7.45, 11.45)))
    B("bolt_catch", 6.98, 7.7, 9.6, 7.25, 8.8, 10.6, "steel_dark", g)
    B("mag_release", 8.75, 7.5, 10.3, 9.05, 8.1, 10.9, "steel_dark", g, "knurl")
    B("safety_lever", 6.95, 8.2, 12.9, 7.25, 8.55, 14.2, "steel_dark", g)
    B("safety_hub", 6.95, 8.1, 13.9, 7.25, 8.7, 14.4, "steel_dark", g)
    for side, (a, b) in (("l", (7.15, 7.25)), ("r", (8.75, 8.85))):
        B("front_pin_" + side, a, 8.45, 7.3, b, 8.8, 7.65, "steel", g)
        B("rear_pin_" + side, a, 8.45, 15.3, b, 8.8, 15.65, "steel", g)
    B("receiver_tang", 7.4, 7.3, 15.4, 8.6, 7.85, 16.4, "alu", g)
    # pistol grip, raked back 22.5 deg
    gr = ("x", -22.5, (8, 7.3, 14.05))
    B("pistol_grip", 7.05, 3.4, 12.7, 8.95, 7.4, 15.4, "polymer", g, "stipple", rot=gr)
    B("pistol_grip_neck", 7.25, 7.2, 12.9, 8.75, 8.2, 15.2, "polymer", g, rot=gr)
    B("pistol_grip_cap", 7.0, 3.15, 12.6, 9.0, 3.4, 15.5, "polymer", g, rot=gr)
    B("pistol_grip_front", 7.15, 4.0, 12.55, 8.85, 7.0, 12.7, "polymer", g, rot=gr)

    # ---- buffer tube + stock ----------------------------------------------
    g = "stock"
    B("end_plate", 6.95, 8.7, 16.0, 9.05, 10.9, 16.25, "steel_dark", g)
    m.cyl_z("castle_nut", cx, 9.95, 16.25, 16.75, 0.72, "steel_dark", g, "knurl")
    m.cyl_z("buffer_tube", cx, 9.95, 16.75, 27.0, 0.58, "alu", g)
    B("stock_nose", 7.3, 9.3, 19.8, 8.7, 10.8, 20.5, "polymer", g)
    B("stock_top", 7.15, 9.1, 20.5, 8.85, 11.0, 28.6, "polymer", g)
    B("stock_cheek", 7.35, 11.0, 21.0, 8.65, 11.3, 28.5, "polymer", g)
    B("stock_lever", 7.6, 8.55, 20.0, 8.4, 9.1, 22.6, "polymer", g)
    B("stock_strut", 7.3, 8.4, 21.0, 8.7, 9.5, 27.2, "polymer", g,
      rot=("x", 22.5, (8, 9.0, 21.2)))
    B("stock_web", 7.25, 4.6, 26.2, 8.75, 9.1, 28.6, "polymer", g)
    B("stock_toe", 7.3, 4.6, 25.4, 8.7, 5.6, 26.2, "polymer", g)
    B("butt_pad", 6.95, 4.3, 28.6, 9.05, 11.4, 29.6, "rubber", g, "ribs")
    B("sling_cup", 7.1, 5.6, 26.6, 7.25, 6.4, 27.4, "steel", g)

    # ---- EOTech EXPS3 ------------------------------------------------------
    g = "optic"
    B("eo_base", 6.95, 11.9, 6.3, 9.05, 12.5, 12.6, "alu", g)
    B("eo_qd_lever", 6.6, 11.95, 10.6, 6.95, 12.45, 11.9, "steel_dark", g)
    B("eo_body", 7.0, 12.5, 10.0, 9.0, 13.3, 12.6, "alu", g)
    B("eo_btn_1", 6.8, 12.7, 10.6, 7.0, 13.1, 11.0, "rubber", g)
    B("eo_btn_2", 6.8, 12.7, 11.3, 7.0, 13.1, 11.7, "rubber", g)
    B("eo_lower_window_box", 7.0, 12.5, 6.3, 9.0, 12.9, 10.0, "alu", g)
    B("eo_hood_l", 6.95, 12.9, 6.3, 7.25, 15.6, 10.0, "alu", g)
    B("eo_hood_r", 8.75, 12.9, 6.3, 9.05, 15.6, 10.0, "alu", g)
    B("eo_hood_top", 7.25, 15.3, 6.3, 8.75, 15.6, 10.0, "alu", g)
    B("eo_window_front", 7.25, 12.9, 6.45, 8.75, 15.3, 6.55, "glass", g)
    B("eo_window_rear", 7.25, 12.9, 8.4, 8.75, 15.3, 8.5, "glass", g, "reticle")
    # folded rear back-up iron sight behind the optic
    B("buis_folded", 7.2, 11.9, 13.2, 8.8, 12.55, 14.9, "polymer", g)

    # ---- magazine (curved 30 rd PMAG) -------------------------------------
    g = "magazine"
    B("mag_top", 7.15, 2.9, 7.25, 8.85, 6.0, 10.0, "fde", g, "ribs")
    B("mag_fill", 7.15, 2.45, 8.9, 8.85, 3.0, 10.0, "fde", g)
    mr = ("x", 22.5, (8, 3.1, 8.6))
    B("mag_curve", 7.15, -0.3, 7.25, 8.85, 3.1, 10.0, "fde", g, "ribs", rot=mr)
    B("mag_floorplate", 7.05, -0.7, 7.1, 8.95, -0.3, 10.25, "fde_dark", g, rot=mr)

    return m


# point (model units) that should sit in the player's hand
GRIP_POINT = (8.0, 5.5, 14.4)

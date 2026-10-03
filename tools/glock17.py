"""Glock 17 Gen 5, stock pistol (factory sights only, no accessories).

Scale: 1 model unit ~= 7 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "slide": Material((58, 59, 63), 5),        # nDLC slide
    "slide_dark": Material((38, 39, 42), 4),
    "frame": Material((48, 48, 46), 6),        # polymer frame
    "frame_dark": Material((32, 32, 31), 5),
    "steel": Material((70, 71, 75), 7),
    "barrel": Material((82, 82, 86), 6),
    "steel_dark": Material((24, 24, 26), 4),
    "white": Material((232, 232, 224), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("glock17", MATERIALS, density=8)
    B = m.box

    # ======================================================================
    # slide
    # ======================================================================
    g = "slide"
    # inner core (shows between the serrations and on the lower edge chamfer)
    B("slide_core_f", 6.35, 15.0, 1.2, 9.65, 18.6, 4.2, "slide_dark", g)
    B("slide_core_b", 6.35, 15.0, 20.8, 9.65, 18.6, 26.0, "slide_dark", g)
    B("slide_chamfer", 6.35, 15.0, 0.6, 9.65, 15.15, 26.6, "slide_dark", g)
    # Gen 5 bevelled nose
    B("slide_nose_a", 6.45, 15.2, 0.3, 9.55, 18.45, 0.6, "slide", g)
    B("slide_nose_b", 6.75, 15.45, 0.0, 9.25, 18.15, 0.3, "slide", g)
    B("slide_front", 6.2, 15.15, 0.6, 9.8, 18.6, 1.2, "slide", g)
    # front serrations
    z = 1.45
    i = 0
    while z + 0.25 <= 4.2:
        B("front_serr_%d" % i, 6.2, 15.35, z, 9.8, 18.3, z + 0.25, "slide", g)
        z += 0.5
        i += 1
    # main body: lower band + upper band interrupted by the ejection port
    B("slide_lower", 6.2, 15.15, 4.2, 9.8, 17.8, 20.8, "slide", g,
      text={"west": "GLOCK  17 GEN5  AUSTRIA 9x19", "east": "BKRS512"})
    B("slide_upper_front", 6.2, 17.8, 4.2, 9.8, 18.6, 7.5, "slide", g)
    B("slide_upper_rear", 6.2, 17.8, 12.3, 9.8, 18.6, 20.8, "slide", g)
    B("slide_port_wall_l", 6.2, 17.8, 7.5, 7.0, 18.6, 12.3, "slide", g)
    B("slide_upper_ff", 6.35, 17.8, 1.2, 9.65, 18.6, 4.2, "slide", g)
    # rear serrations
    z = 20.95
    i = 0
    while z + 0.22 <= 26.0:
        B("rear_serr_%d" % i, 6.2, 15.3, z, 9.8, 18.45, z + 0.22, "slide", g)
        z += 0.45
        i += 1
    B("slide_rear", 6.2, 15.15, 26.0, 9.8, 18.6, 26.6, "slide", g)
    # flat top with large 45 deg chamfers on both upper edges (highlighted)
    for nm, (a, b) in {"front": (0.6, 7.5), "rear": (12.3, 26.45)}.items():
        B("slide_top_" + nm, 6.75, 18.6, a, 9.25, 19.15, b, "slide", g)
    B("slide_top_port", 6.75, 18.6, 7.5, 7.0, 19.15, 12.3, "slide", g)
    m.edge("slide_chamfer_l", "z", 0.6, 26.45, 6.2, 19.15, -1, 1, 0.55, "slide", g)
    m.edge("slide_chamfer_r_f", "z", 0.6, 7.5, 9.8, 19.15, 1, 1, 0.55, "slide", g)
    m.edge("slide_chamfer_r_b", "z", 12.3, 26.45, 9.8, 19.15, 1, 1, 0.55, "slide", g)
    m.edge("slide_chamfer_front", "x", 6.75, 9.25, 19.15, 0.6, 1, -1, 0.4, "slide", g)
    m.edge("slide_chamfer_rear", "x", 6.75, 9.25, 19.15, 26.45, 1, 1, 0.3, "slide", g)
    B("port_rim_front", 9.0, 17.8, 7.45, 9.8, 18.6, 7.5, "slide_dark", g)
    B("port_rim_low", 9.0, 17.75, 7.5, 9.8, 17.8, 12.3, "slide_dark", g)
    B("slide_stop_notch_l", 6.18, 15.15, 12.9, 6.2, 15.5, 13.9, "slide_dark", g)
    B("port_breech_face", 7.0, 16.35, 12.25, 9.65, 18.6, 12.3, "steel_dark", g)
    # extractor with loaded-chamber bump
    B("extractor", 9.8, 17.05, 12.3, 9.88, 17.55, 15.0, "steel", g)
    B("extractor_claw", 9.6, 17.1, 12.05, 9.82, 17.5, 12.3, "steel", g)
    B("extractor_bump", 9.88, 17.2, 12.5, 9.93, 17.4, 13.1, "steel", g)
    # slide cover plate with striker channel
    B("slide_cover_plate", 6.6, 15.4, 26.6, 9.4, 18.4, 26.7, "frame", g)
    B("striker_channel", 7.85, 16.35, 26.7, 8.15, 16.65, 26.72, "bore", g)
    B("cover_plate_notch", 7.6, 15.4, 26.68, 8.4, 15.6, 26.72, "frame_dark", g)
    # front sight with white dot
    B("fs_base", 7.6, 19.1, 0.7, 8.4, 19.3, 1.9, "steel_dark", g)
    B("fs_post", 7.7, 19.3, 0.8, 8.3, 19.85, 1.7, "steel_dark", g)
    B("fs_dot", 7.9, 19.48, 1.7, 8.1, 19.68, 1.72, "white", g)
    # rear sight with white U outline
    B("rs_base", 6.7, 19.1, 24.4, 9.3, 19.5, 25.6, "steel_dark", g)
    B("rs_ramp", 6.75, 19.1, 24.15, 9.25, 19.35, 24.45, "steel_dark", g,
      rot=("x", 22.5, (8, 19.1, 24.4)))
    B("rs_ear_l", 6.7, 19.5, 24.4, 7.65, 20.05, 25.6, "steel_dark", g)
    B("rs_ear_r", 8.35, 19.5, 24.4, 9.3, 20.05, 25.6, "steel_dark", g)
    B("rs_u_left", 7.52, 19.5, 25.6, 7.65, 19.95, 25.62, "white", g)
    B("rs_u_right", 8.35, 19.5, 25.6, 8.48, 19.95, 25.62, "white", g)
    B("rs_u_bottom", 7.52, 19.36, 25.6, 8.48, 19.5, 25.62, "white", g)
    m.pin_x("rs_screw", 8.0, 19.3, 25.0, 0.1, 9.28, 9.32, "steel", g)

    # ======================================================================
    # barrel + recoil spring assembly
    # ======================================================================
    g = "barrel"
    B("barrel_hood", 7.0, 16.4, 7.5, 9.0, 18.95, 12.25, "barrel", g, text={"up": "9x19"})
    B("barrel_chamber", 9.0, 16.6, 10.6, 9.06, 17.4, 12.25, "barrel", g)
    B("barrel_lug_side", 9.0, 17.7, 7.5, 9.06, 18.8, 8.1, "barrel", g)
    m.cyl_z("barrel_muzzle", 8.0, 16.6, -0.05, 0.1, 0.62, "barrel", g)
    B("barrel_bore", 7.72, 16.32, -0.07, 8.28, 16.88, -0.05, "bore", g)
    B("guide_rod_hole", 7.62, 15.55, -0.02, 8.38, 16.05, 0.0, "bore", g)
    B("guide_rod_tip", 7.8, 15.68, -0.03, 8.2, 15.92, -0.02, "steel", g)

    # ======================================================================
    # frame
    # ======================================================================
    g = "frame"
    m.bevel("dust_cover", 6.4, 13.7, 0.6, 9.6, 15.0, 9.6, 0.12, "frame", g,
            text={"west": "GEN5", "east": "AUSTRIA"})
    B("dust_cover_nose", 6.6, 13.85, 0.45, 9.4, 14.85, 0.6, "frame", g)
    # accessory rail with a single cross slot
    B("rail_body", 6.9, 13.35, 1.2, 9.1, 13.7, 7.0, "frame", g)
    B("rail_lip_f", 6.7, 13.18, 1.2, 9.3, 13.35, 3.7, "frame", g)
    B("rail_lip_b", 6.7, 13.18, 4.3, 9.3, 13.35, 7.0, "frame", g)
    B("rail_slot", 6.9, 13.2, 3.7, 9.1, 13.35, 4.3, "frame_dark", g)
    B("serial_plate", 7.55, 13.66, 7.15, 8.45, 13.7, 7.85, "steel", g)
    m.bevel("frame_upper", 6.3, 13.6, 9.6, 9.7, 15.0, 26.4, 0.1, "frame", g)
    m.bevel("beavertail", 6.6, 13.8, 26.4, 9.4, 14.9, 27.6, 0.15, "frame", g)
    # Gen 5 thumb rests (stippled recess)
    B("thumb_rest_l", 6.27, 13.75, 14.4, 6.3, 14.45, 16.6, "frame_dark", g, "stipple")
    B("thumb_rest_r", 9.7, 13.75, 14.4, 9.73, 14.45, 16.6, "frame_dark", g, "stipple")
    # trigger guard, square front with serrations
    m.bevel("tg_front", 7.45, 10.75, 7.9, 8.55, 13.7, 8.7, 0.1, "frame", g, axis="y")
    m.edge("tg_corner", "x", 7.47, 8.53, 10.25, 7.9, -1, -1, 0.5, "frame", g)
    for k in range(5):
        y = 10.9 + k * 0.45
        B("tg_serr_%d" % k, 7.55, y, 7.83, 8.45, y + 0.2, 7.9, "frame", g)
    m.bevel("tg_bottom", 7.45, 10.25, 8.4, 8.55, 10.9, 16.6, 0.1, "frame", g)
    B("tg_undercut", 7.5, 10.9, 15.2, 8.5, 11.4, 16.2, "frame", g)
    # trigger with safety blade
    B("trigger_shoe_top", 7.75, 12.3, 11.55, 8.25, 13.6, 12.0, "frame", g)
    B("trigger_shoe_mid", 7.75, 11.3, 11.55, 8.25, 12.35, 12.0, "frame", g,
      rot=("x", 22.5, (8, 12.3, 11.78)))
    B("trigger_shoe_tip", 7.75, 10.95, 11.3, 8.25, 11.4, 11.7, "frame", g,
      rot=("x", 45, (8, 11.35, 11.5)))
    B("trigger_safety_top", 7.95, 12.3, 11.42, 8.05, 13.2, 11.55, "steel_dark", g)
    B("trigger_safety_low", 7.95, 11.55, 11.42, 8.05, 12.35, 11.55, "steel_dark", g,
      rot=("x", 22.5, (8, 12.3, 11.5)))
    B("trigger_bar_slot", 7.8, 13.55, 11.9, 8.2, 13.62, 13.4, "frame_dark", g)
    B("trigger_bar", 7.88, 13.0, 12.0, 8.12, 13.55, 13.3, "steel", g)
    B("trigger_bar_spring", 7.9, 13.2, 13.3, 8.1, 13.4, 13.9, "steel", g)
    # pins: locking block, trigger, trigger housing
    for side, (a, b) in (("l", (6.22, 6.3)), ("r", (9.7, 9.78))):
        m.pin_x("block_pin_" + side, (a + b) / 2, 14.3, 11.05, 0.13, a, b, "steel", g)
        m.pin_x("trigger_pin_" + side, (a + b) / 2, 14.25, 13.7, 0.13, a, b, "steel", g)
        m.pin_x("housing_pin_" + side, (a + b) / 2, 14.2, 23.9, 0.13, a, b, "steel", g)
    # ambidextrous slide stop and take-down lever
    for side, (a, b, c_) in (("l", (6.12, 6.3, 6.08)), ("r", (9.7, 9.88, 9.92))):
        B("slide_stop_" + side, a, 14.65, 12.2, b, 15.1, 15.4, "steel_dark", g)
        for k in range(3):
            z = 14.55 + k * 0.28
            lo, hi = (c_, a) if side == "l" else (b, c_)
            B("slide_stop_serr_%s_%d" % (side, k), lo, 14.72, z, hi, 15.05, z + 0.14, "steel_dark", g)
        B("takedown_" + side, a + 0.03, 14.45, 9.8, b - 0.03, 15.0, 10.6, "steel_dark", g)
        for k in range(2):
            z = 9.95 + k * 0.32
            lo, hi = (a, a + 0.03) if side == "l" else (b - 0.03, b)
            B("takedown_serr_%s_%d" % (side, k), lo, 14.5, z, hi, 14.95, z + 0.15, "steel_dark", g)
    # reversible magazine catch
    m.bevel("mag_catch", 5.8, 12.4, 15.0, 10.2, 13.3, 15.8, 0.08, "frame", g, "knurl", axis="x")

    # ======================================================================
    # grip (22 deg grip angle, all parts share one pivot)
    # ======================================================================
    g = "grip"
    gr = ("x", -22.5, (8, 13.4, 18.4))
    B("grip_neck", 6.3, 13.0, 15.4, 9.7, 14.6, 21.4, "frame", g, rot=gr)
    m.bevel("grip_body", 5.9, 2.2, 15.2, 10.1, 13.6, 21.6, 0.22, "frame", g, axis="y", rot=gr)
    B("grip_panel_l", 5.85, 3.0, 15.7, 5.9, 11.6, 21.1, "frame", g, "stipple", rot=gr)
    B("grip_panel_r", 10.1, 3.0, 15.7, 10.15, 11.6, 21.1, "frame", g, "stipple", rot=gr)
    for side, (a, b) in (("l", (5.83, 5.85)), ("r", (10.15, 10.17))):
        B("grip_border_top_" + side, a, 11.45, 15.7, b, 11.6, 21.1, "frame", g, rot=gr)
        B("grip_border_bot_" + side, a, 3.0, 15.7, b, 3.15, 21.1, "frame", g, rot=gr)
        B("grip_border_f_" + side, a, 3.0, 15.7, b, 11.6, 15.85, "frame", g, rot=gr)
        B("grip_border_b_" + side, a, 3.0, 20.95, b, 11.6, 21.1, "frame", g, rot=gr)
    for side, (a, b) in (("l", (5.78, 5.8)), ("r", (10.2, 10.22))):
        B("magwell_cut_" + side, a, 1.75, 15.7, b, 2.45, 16.6, "frame_dark", g, rot=gr)
    B("grip_logo_l", 5.84, 11.75, 16.6, 5.9, 12.85, 20.2, "frame", g, rot=gr, text={"west": "GLOCK"})
    B("grip_logo_r", 10.1, 11.75, 16.6, 10.16, 12.85, 20.2, "frame", g, rot=gr, text={"east": "GLOCK"})
    m.bevel("grip_frontstrap", 6.2, 2.6, 14.95, 9.8, 12.2, 15.2, 0.1, "frame", g, "stipple", axis="y", rot=gr)
    m.bevel("grip_backstrap", 6.1, 2.6, 21.6, 9.9, 13.4, 22.25, 0.15, "frame", g, "stipple", axis="y", rot=gr)
    m.pin_x("backstrap_pin_l", 6.07, 12.4, 21.9, 0.12, 6.04, 6.1, "steel", g, rot=gr)
    m.pin_x("backstrap_pin_r", 9.93, 12.4, 21.9, 0.12, 9.9, 9.96, "steel", g, rot=gr)
    B("lanyard_hole", 7.55, 2.85, 22.25, 8.45, 3.35, 22.27, "bore", g, rot=gr)
    # flared magwell with the Gen 5 front cut-out
    B("flare_l", 5.8, 1.6, 15.0, 6.3, 2.6, 21.8, "frame", g, rot=gr)
    B("flare_r", 9.7, 1.6, 15.0, 10.2, 2.6, 21.8, "frame", g, rot=gr)
    B("flare_b", 6.3, 1.6, 21.0, 9.7, 2.6, 21.8, "frame", g, rot=gr)
    B("flare_f_l", 6.3, 1.6, 15.0, 7.25, 2.6, 15.6, "frame", g, rot=gr)
    B("flare_f_r", 8.75, 1.6, 15.0, 9.7, 2.6, 15.6, "frame", g, rot=gr)
    # magazine tube visible in the cut-out, baseplate
    B("mag_tube", 6.5, 1.6, 15.35, 9.5, 3.4, 20.9, "steel_dark", g, rot=gr)
    B("mag_tube_spine", 7.6, 1.6, 15.25, 8.4, 3.2, 15.35, "steel_dark", g, rot=gr)
    m.bevel("mag_baseplate", 6.2, 0.9, 15.4, 9.8, 1.6, 21.0, 0.1, "frame", g, axis="y", rot=gr)
    B("mag_base_lip_f", 6.6, 1.0, 15.1, 9.4, 1.5, 15.4, "frame", g, rot=gr)
    B("mag_base_lip_b", 6.6, 0.95, 21.0, 9.4, 1.45, 21.35, "frame", g, rot=gr)
    B("mag_base_hole", 7.85, 0.88, 17.5, 8.15, 0.9, 17.8, "bore", g, rot=gr)

    return m


GRIP_POINT = (8.0, 9.0, 20.5)

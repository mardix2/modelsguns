"""Glock 17 Gen 5.

Scale: 1 model unit ~= 7 mm.  Muzzle points north (-Z), bore axis at x=8.
"""

from bbgen import Material, Model

MATERIALS = {
    "slide": Material((50, 51, 54), 5),        # nDLC slide
    "frame": Material((42, 42, 40), 6),        # polymer frame
    "steel": Material((70, 71, 75), 7),
    "barrel": Material((82, 82, 86), 6),
    "steel_dark": Material((22, 22, 24), 4),
    "white": Material((230, 230, 222), 3, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}


def build():
    m = Model("glock17", MATERIALS, density=4)
    B = m.box

    # ---- slide ---------------------------------------------------------------
    g = "slide"
    B("slide_nose", 6.4, 15.2, 0.0, 9.6, 18.3, 0.6, "slide", g)
    B("slide_front_serr", 6.2, 15.0, 0.6, 9.8, 17.8, 4.2, "slide", g, "serration")
    B("slide_mid", 6.2, 15.0, 4.2, 9.8, 17.8, 20.5, "slide", g, "logo")
    B("slide_rear_serr", 6.2, 15.0, 20.5, 9.8, 17.8, 26.6, "slide", g, "serration")
    # upper band, interrupted by the ejection port on the right
    B("slide_top_front", 6.2, 17.8, 0.6, 9.8, 18.6, 7.5, "slide", g)
    B("slide_top_rear", 6.2, 17.8, 12.3, 9.8, 18.6, 26.6, "slide", g, "serration")
    B("slide_port_wall_l", 6.2, 17.8, 7.5, 7.0, 18.6, 12.3, "slide", g)
    B("slide_cap_front", 6.5, 18.6, 0.6, 9.5, 19.1, 7.5, "slide", g)
    B("slide_cap_rear", 6.5, 18.6, 12.3, 9.5, 19.1, 26.4, "slide", g)
    B("slide_cap_port_l", 6.5, 18.6, 7.5, 7.0, 19.1, 12.3, "slide", g)
    B("slide_cover_plate", 6.6, 15.4, 26.6, 9.4, 18.6, 26.7, "frame", g)
    B("extractor", 9.8, 17.0, 12.3, 9.9, 17.6, 14.6, "steel", g)
    # sights
    B("front_sight", 7.65, 19.1, 0.8, 8.35, 19.75, 1.8, "steel_dark", g, "dot")
    B("rear_sight_base", 6.7, 19.1, 24.4, 9.3, 19.55, 25.6, "steel_dark", g)
    B("rear_sight_l", 6.7, 19.55, 24.4, 7.65, 20.0, 25.6, "steel_dark", g, "dot")
    B("rear_sight_r", 8.35, 19.55, 24.4, 9.3, 20.0, 25.6, "steel_dark", g, "dot")

    # ---- barrel ----------------------------------------------------------------
    g = "barrel"
    B("barrel_hood", 7.0, 16.4, 7.5, 9.0, 18.95, 12.5, "barrel", g)
    B("barrel_muzzle", 7.35, 15.95, -0.04, 8.65, 17.25, 0.0, "barrel", g)
    B("barrel_bore", 7.75, 16.35, -0.06, 8.25, 16.85, -0.04, "bore", g, "bore")
    B("guide_rod_hole", 7.6, 15.15, -0.04, 8.4, 15.65, 0.0, "bore", g, "bore")

    # ---- frame -----------------------------------------------------------------
    g = "frame"
    B("dust_cover", 6.4, 13.7, 0.6, 9.6, 15.0, 9.6, "frame", g)
    B("accessory_rail", 6.7, 13.2, 1.2, 9.3, 13.7, 7.0, "frame", g, "rail_pistol")
    B("frame_upper", 6.3, 13.6, 9.6, 9.7, 15.0, 26.4, "frame", g)
    B("beavertail", 6.6, 13.8, 26.4, 9.4, 14.9, 27.6, "frame", g)
    B("trigger_guard_front", 7.5, 10.6, 8.0, 8.5, 13.7, 8.8, "frame", g)
    B("trigger_guard_bottom", 7.5, 10.3, 8.0, 8.5, 10.9, 16.6, "frame", g)
    B("trigger_upper", 7.75, 12.2, 11.6, 8.25, 13.6, 12.1, "frame", g)
    B("trigger_lower", 7.75, 11.0, 11.6, 8.25, 12.3, 12.1, "frame", g,
      rot=("x", 22.5, (8, 12.2, 11.85)))
    B("trigger_safety", 7.93, 11.3, 11.45, 8.07, 12.9, 11.6, "steel_dark", g)
    B("slide_stop", 6.12, 14.7, 12.2, 6.3, 15.15, 15.4, "steel_dark", g)
    for side, (a, b) in (("l", (6.15, 6.3)), ("r", (9.7, 9.85))):
        B("takedown_" + side, a, 14.5, 9.8, b, 15.0, 10.6, "steel_dark", g)
        B("trigger_pin_" + side, a, 14.05, 13.5, b, 14.45, 13.9, "steel", g)
        B("block_pin_" + side, a, 14.15, 10.9, b, 14.45, 11.2, "steel", g)
    B("mag_catch", 5.8, 12.4, 15.0, 10.2, 13.3, 15.8, "frame", g, "knurl")

    # ---- grip (22 deg grip angle) ---------------------------------------------
    g = "grip"
    gr = ("x", -22.5, (8, 13.4, 18.4))
    B("grip_body", 5.9, 2.2, 15.2, 10.1, 13.6, 21.6, "frame", g, "stipple", rot=gr)
    B("grip_neck", 6.3, 13.0, 15.4, 9.7, 14.6, 21.4, "frame", g, rot=gr)
    B("grip_backstrap", 6.1, 9.8, 21.6, 9.9, 13.4, 22.3, "frame", g, "stipple", rot=gr)
    B("grip_frontstrap", 6.2, 2.6, 14.95, 9.8, 12.2, 15.2, "frame", g, "stipple", rot=gr)
    B("magwell_flare", 5.8, 1.6, 15.0, 10.2, 2.6, 21.8, "frame", g, rot=gr)
    B("mag_baseplate", 6.2, 0.9, 15.4, 9.8, 1.6, 21.0, "frame", g, rot=gr)

    return m


GRIP_POINT = (8.0, 9.0, 20.5)

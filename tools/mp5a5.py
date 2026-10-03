"""H&K MP5A5: retractable stock (collapsed), slim handguard, SEF trigger
group, tri-lug muzzle, hooded front sight, drum rear sight, curved 30 rd mag.

Real proportions: 550 mm collapsed, 225 mm barrel, 50 mm handguard.
Scale: 1 unit ~= 11 mm.  Muzzle points north (-Z), bore axis x=8, y=10.
"""

import anims
from bbgen import Material, Model

MATERIALS = {
    "steel": Material((52, 53, 57), 3),          # black painted stamped steel
    "steel_dark": Material((34, 34, 37), 3),
    "steel_light": Material((98, 99, 104), 4),
    "polymer": Material((44, 44, 43), 4),
    "polymer_dark": Material((32, 32, 31), 4),
    "rubber": Material((28, 28, 28), 4),
    "brass": Material((184, 148, 70), 5),
    "white": Material((222, 222, 214), 2, edge=False),
    "red": Material((176, 34, 30), 2, edge=False),
    "bore": Material((6, 6, 6), 1, edge=False),
}

CX, CY = 8.0, 10.0
TY = 12.0      # cocking tube axis


def build():
    m = Model("mp5a5", MATERIALS, density=8)
    B = m.box

    # ======================================================================
    # barrel, tri-lug, hooded front sight
    # ======================================================================
    g = "barrel"
    m.cyl_z("trilug_collar", CX, CY, -20.5, -19.2, 0.95, "steel", g)
    for i, ang in enumerate((0, 120, 240)):
        with m.frame(("z", ang, (CX, CY, -19.9))):
            m.bevel("trilug_lug_%d" % i, 7.7, 10.85, -20.45, 8.3, 11.25, -19.6, 0.08, "steel", g)
    m.cyl_z("muzzle_face", CX, CY, -20.55, -20.5, 0.6, "steel_dark", g)
    m.cyl_z("muzzle_bore", CX, CY, -20.58, -20.55, 0.36, "bore", g)
    m.cyl_z("barrel", CX, CY, -19.3, -14.8, 0.68, "steel", g)
    # front sight base: clamps barrel and cocking tube
    m.bevel("fs_base_low", 6.95, 8.95, -19.2, 9.05, 11.0, -17.2, 0.45, "steel", g)
    m.bevel("fs_base_high", 7.05, 11.0, -19.1, 8.95, 12.9, -17.3, 0.4, "steel", g)
    # hood: ring of 8 slats around the post
    m.ring_z("fs_hood", CX, 14.25, -18.95, -17.6, 1.35, 0.3, 1.0, "steel", g, skip=(4,))
    m.bevel("fs_hood_root", 7.45, 12.8, -18.95, 8.55, 13.15, -17.6, 0.08, "steel", g)
    B("fs_post", 7.88, 12.9, -18.4, 8.12, 14.35, -18.1, "steel_dark", g)
    B("fs_post_tip", 7.84, 14.15, -18.42, 8.16, 14.4, -18.08, "steel_dark", g)
    m.pin_x("fs_pin", 8.0, 10.0, -18.2, 0.13, 6.92, 9.08, "steel_light", g)

    # ======================================================================
    # cocking tube + cocking handle (left)
    # ======================================================================
    g = "cocking"
    m.cyl_z("cocking_tube", CX, TY, -17.3, -2.0, 1.0, "steel", g)
    m.cyl_z("cocking_tube_cap", CX, TY, -17.5, -17.3, 0.85, "steel_dark", g)
    B("cocking_slot", 6.97, TY - 0.2, -14.6, 7.01, TY + 0.2, -3.0, "bore", g)
    B("cocking_slot_notch", 6.97, TY + 0.2, -3.6, 7.01, TY + 0.55, -3.0, "bore", g)

    g = "cocking_handle"
    m.bevel("ch_stem", 6.3, TY - 0.18, -14.4, 7.05, TY + 0.18, -13.75, 0.06, "steel_dark", g, axis="x")
    with m.frame(("y", 22, (6.3, TY, -14.1))):
        m.bevel("ch_knob", 5.25, TY - 0.45, -14.65, 6.4, TY + 0.45, -13.55, 0.2, "polymer", g, axis="x")
        B("ch_knob_cap", 5.2, TY - 0.3, -14.5, 5.25, TY + 0.3, -13.7, "polymer", g)

    # ======================================================================
    # slim handguard
    # ======================================================================
    g = "handguard"
    m.bevel("hg_body", 5.75, 7.2, -15.0, 10.25, 10.95, -2.1, 0.75, "polymer", g)
    m.bevel("hg_flare", 5.55, 7.0, -15.35, 10.45, 11.15, -14.7, 0.75, "polymer", g)
    m.bevel("hg_top_l", 6.0, 10.9, -14.7, 7.05, 11.55, -2.3, 0.2, "polymer", g)
    m.bevel("hg_top_r", 8.95, 10.9, -14.7, 10.0, 11.55, -2.3, 0.2, "polymer", g)
    for k in range(9):
        z = -13.9 + k * 1.25
        B("hg_groove_b_%d" % k, 6.8, 7.18, z, 9.2, 7.2, z + 0.55, "polymer_dark", g)
        B("hg_groove_l_%d" % k, 5.73, 7.9, z, 5.75, 9.6, z + 0.55, "polymer_dark", g)
        B("hg_groove_r_%d" % k, 10.25, 7.9, z, 10.27, 9.6, z + 0.55, "polymer_dark", g)
    m.pin_x("hg_pin_l", 5.72, 9.05, -2.9, 0.18, 5.66, 5.78, "steel_light", g)
    m.pin_x("hg_pin_r", 10.28, 9.05, -2.9, 0.18, 10.22, 10.34, "steel_light", g)

    # ======================================================================
    # stamped receiver
    # ======================================================================
    g = "receiver"
    m.bevel("rcv_lower", 6.45, 8.35, -2.2, 9.55, 11.3, 20.0, 0.25, "steel", g)
    m.bevel("rcv_upper", 6.75, 11.2, -2.2, 9.25, 13.05, 20.0, 0.75, "steel", g)
    m.bevel("rcv_front_ring", 6.6, 8.5, -2.45, 9.4, 12.95, -2.0, 0.6, "steel", g)
    # long stamped channels on both sides
    for side, (a, b) in (("l", (6.42, 6.45)), ("r", (9.55, 9.58))):
        B("rcv_channel_" + side, a, 10.75, -1.6, b, 11.0, 19.4, "steel_dark", g)
        B("rcv_channel_low_" + side, a, 8.75, 8.3, b, 8.95, 19.4, "steel_dark", g)
        B("rcv_weld_" + side, a, 9.6, -1.9, b, 9.7, 3.6, "steel_light", g)
        # retractable-stock guide rails welded to the receiver
        m.bevel("stock_guide_" + side, a - 0.25 if side == "l" else b, 11.15, 8.6,
                a if side == "l" else b + 0.25, 11.85, 19.9, 0.06, "steel", g)
    # HK claw-mount dimples on top
    for k, z in enumerate((1.0, 2.6, 9.5, 11.1)):
        m.bevel("claw_dimple_%d" % k, 7.45, 13.0, z, 8.55, 13.18, z + 0.8, 0.05, "steel", g)
    # ejection port with case deflector bump, bolt visible
    B("ejection_port", 9.55, 10.0, 5.6, 9.57, 11.35, 9.0, "bore", g)
    m.bevel("bolt_face", 9.45, 10.15, 7.7, 9.56, 11.2, 8.95, 0.05, "steel_light", g, axis="x")
    m.bevel("case_deflector", 9.55, 10.2, 9.0, 9.95, 11.6, 9.75, 0.1, "steel", g)
    # end cap with sling loop and stock latch
    m.bevel("end_cap", 6.55, 8.4, 20.0, 9.45, 12.95, 20.75, 0.6, "steel", g)
    m.pin_x("end_cap_pin_l", 6.5, 9.3, 19.6, 0.18, 6.42, 6.58, "steel_light", g)
    m.pin_x("end_cap_pin_r", 9.5, 9.3, 19.6, 0.18, 9.42, 9.58, "steel_light", g)
    m.bevel("stock_latch", 7.4, 12.95, 19.1, 8.6, 13.4, 20.8, 0.12, "steel_dark", g, "knurl")
    # magazine well and releases
    m.bevel("magwell", 6.85, 6.9, 3.9, 9.15, 8.5, 7.9, 0.2, "steel", g, axis="y")
    m.bevel("magwell_lip", 6.7, 6.7, 3.75, 9.3, 7.0, 8.05, 0.15, "steel", g, axis="y")
    m.bevel("mag_paddle", 7.45, 6.2, 8.0, 8.55, 7.3, 8.4, 0.08, "steel_dark", g)
    with m.frame(("x", 22, (8, 6.25, 8.2))):
        m.bevel("mag_paddle_tab", 7.4, 5.85, 8.0, 8.6, 6.25, 8.75, 0.08, "steel_dark", g, "knurl")
    m.pin_x("mag_button", 9.6, 7.6, 8.15, 0.32, 9.45, 9.75, "steel_dark", g)
    # drum rear sight
    m.bevel("drum_base", 7.15, 13.0, 15.0, 8.85, 13.45, 18.0, 0.15, "steel", g)
    m.bevel("drum_ear_l", 6.9, 13.3, 15.3, 7.2, 15.25, 17.7, 0.08, "steel", g, axis="x")
    m.bevel("drum_ear_r", 8.8, 13.3, 15.3, 9.1, 15.25, 17.7, 0.08, "steel", g, axis="x")
    m.cyl_x("drum", 7.2, 8.8, 14.4, 16.5, 0.95, "steel", g)
    for k, (dy, dz) in enumerate(((0.95, 0), (-0.95, 0), (0, 0.95), (0, -0.95))):
        B("drum_aperture_%d" % k, 7.9, 14.4 + dy - 0.12 if dy else 14.28, 16.5 + dz - 0.12 if dz else 16.38,
          8.1, 14.4 + dy + 0.12 if dy else 14.52, 16.5 + dz + 0.12 if dz else 16.62, "bore", g)
    m.cyl_x("drum_knob", 8.8, 9.25, 14.4, 16.5, 0.45, "steel_dark", g, "knurl")

    # ======================================================================
    # polymer SEF trigger group with integral grip
    # ======================================================================
    g = "lower"
    m.bevel("housing", 6.6, 6.0, 7.9, 9.4, 8.45, 16.2, 0.25, "polymer", g)
    m.bevel("housing_rear", 6.75, 6.2, 16.0, 9.25, 8.4, 18.4, 0.3, "polymer", g)
    B("pictogram_panel", 6.57, 7.3, 13.0, 6.6, 8.3, 15.8, "polymer_dark", g, text={"west": "S E F"})
    for side, (a, b) in (("l", (6.5, 6.6)), ("r", (9.4, 9.5))):
        m.pin_x("push_pin_f_" + side, (a + b) / 2, 7.9, 8.6, 0.22, a, b, "steel_light", g)
        m.pin_x("push_pin_b_" + side, (a + b) / 2, 7.95, 17.6, 0.22, a, b, "steel_light", g)
    # oval trigger guard
    m.bevel("tg_front", 7.5, 4.9, 8.6, 8.5, 6.2, 9.1, 0.12, "polymer", g, axis="y")
    m.bevel("tg_bottom", 7.5, 4.4, 9.0, 8.5, 4.95, 13.2, 0.14, "polymer", g)
    m.edge("tg_corner", "x", 7.52, 8.48, 4.4, 8.6, -1, -1, 0.7, "polymer", g)
    # selector (left) with pictograms
    m.pin_x("selector_hub", 6.45, 7.7, 15.2, 0.5, 6.25, 6.6, "steel_dark", g)
    with m.frame(("x", -60, (6.4, 7.7, 15.2))):
        m.bevel("selector_lever", 6.2, 7.5, 13.2, 6.45, 7.9, 15.2, 0.06, "steel_dark", g, axis="x")
        B("selector_tip", 6.15, 7.45, 13.1, 6.45, 7.95, 13.45, "steel_dark", g, "knurl")
    B("mark_safe", 6.56, 8.35, 14.85, 6.58, 8.55, 15.05, "white", g)
    B("mark_semi", 6.56, 8.1, 13.9, 6.58, 8.3, 14.1, "red", g)
    B("mark_auto", 6.56, 7.25, 14.0, 6.58, 7.45, 14.2, "red", g)
    # grip (12 deg), stippled, finger grooves on the front strap
    with m.frame(("x", -12, (8, 6.2, 15.3))):
        m.bevel("grip_neck", 6.75, 5.6, 13.6, 9.25, 6.5, 17.2, 0.25, "polymer", g, axis="y")
        m.bevel("grip", 6.65, -0.3, 13.5, 9.35, 5.9, 17.1, 0.5, "polymer", g, "stipple", axis="y")
        for k in range(3):
            y = 0.9 + k * 1.65
            m.bevel("grip_finger_%d" % k, 6.85, y, 13.2, 9.15, y + 0.9, 13.55, 0.25, "polymer", g,
                    axis="x")
        m.bevel("grip_cap", 6.6, -0.6, 13.45, 9.4, -0.3, 17.15, 0.15, "polymer_dark", g, axis="y")
        B("grip_lanyard", 7.6, -0.65, 16.2, 8.4, -0.55, 16.9, "bore", g)

    g = "trigger"
    m.bevel("trigger_top", 7.7, 6.0, 10.35, 8.3, 6.8, 10.85, 0.06, "steel_dark", g, axis="y")
    with m.frame(("x", 16, (8, 6.05, 10.6))):
        m.bevel("trigger_mid", 7.7, 5.2, 10.35, 8.3, 6.1, 10.85, 0.06, "steel_dark", g, axis="y")
    with m.frame(("x", 40, (8, 5.25, 10.4))):
        m.bevel("trigger_tip", 7.7, 4.95, 10.2, 8.3, 5.3, 10.65, 0.06, "steel_dark", g, axis="y")

    # ======================================================================
    # retractable stock (collapsed): rods, yoke, curved butt plate
    # ======================================================================
    g = "stock"
    for side, x0 in (("l", 5.85), ("r", 9.75)):
        m.cyl_z("stock_rod_" + side, x0 + 0.2, 11.5, 9.0, 25.4, 0.28, "steel", g)
    m.bevel("stock_yoke", 5.75, 10.95, 24.2, 10.25, 12.05, 25.0, 0.2, "steel", g)
    with m.frame(("x", 4, (8, 8.8, 25.0))):
        m.bevel("butt_plate", 5.7, 4.2, 25.0, 10.3, 13.6, 25.85, 0.5, "rubber", g, "ribs")
        m.bevel("butt_frame_top", 6.2, 12.4, 23.9, 9.8, 13.3, 25.1, 0.3, "steel", g)
        m.bevel("butt_frame_low", 6.2, 4.4, 24.0, 9.8, 5.3, 25.1, 0.3, "steel", g)
        m.bevel("butt_strut", 7.55, 5.3, 24.2, 8.45, 12.4, 24.9, 0.15, "steel", g, axis="y")
        B("sling_loop_a", 5.45, 5.0, 24.3, 5.7, 5.25, 25.6, "steel_light", g)
        B("sling_loop_b", 5.45, 5.25, 24.3, 5.7, 6.4, 24.55, "steel_light", g)
        B("sling_loop_c", 5.45, 5.25, 25.35, 5.7, 6.4, 25.6, "steel_light", g)

    # ======================================================================
    # curved 30 round magazine
    # ======================================================================
    g = "magazine"
    zc = 5.9
    B("mag_feed_lips", 7.1, 8.4, 4.3, 8.9, 8.75, 7.6, "steel", g)
    B("mag_round", 7.45, 8.75, 4.6, 8.55, 9.05, 7.4, "brass", g)
    m.cyl_z("mag_round_tip", CX, 8.9, 4.2, 4.65, 0.22, "brass", g)
    seg = 1.15
    angles = [0, 0, 0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15]
    last = None
    for k, (rot, (yt, z0)) in enumerate(m.chain((8.5, zc), seg, angles)):
        with m.frame(rot):
            d0, d1 = z0 - 1.55, z0 + 1.55
            m.bevel("mag_seg_%02d" % k, 7.15, yt - seg - 0.03, d0, 8.85, yt, d1, 0.3, "steel", g, axis="y")
            B("mag_rib_l_%02d" % k, 7.11, yt - seg - 0.02, d0 + 0.55, 7.15, yt, d0 + 1.05, "steel", g)
            B("mag_rib_r_%02d" % k, 8.85, yt - seg - 0.02, d0 + 0.55, 8.89, yt, d0 + 1.05, "steel", g)
            if k % 3 == 1:
                B("mag_window_l_%02d" % k, 7.12, yt - 0.6, d1 - 0.7, 7.15, yt - 0.3, d1 - 0.4, "bore", g)
        last = (rot, yt - seg, z0)
    rot, yb, z0 = last
    with m.frame(rot):
        m.bevel("mag_floor", 7.05, yb - 0.4, z0 - 1.7, 8.95, yb + 0.02, z0 + 1.7, 0.15, "steel_dark", g,
                axis="y")
        B("mag_floor_tab", 7.6, yb - 0.38, z0 + 1.7, 8.4, yb - 0.08, z0 + 1.95, "steel_dark", g)

    m.regroup({}, pivots={"magazine": (8, 8.4, 4.4), "trigger": (8, 6.8, 10.6),
                          "cocking_handle": (6.6, TY, -14.1)})
    m.dynamic = {"magazine", "trigger", "cocking_handle"}
    return m


GRIP_POINT = (8.0, 3.0, 16.0)

DISPLAY = {"hand": 0.34, "fp": 0.36, "gui": 0.29, "tilt": 25, "push": -1.5}

ANIM = {
    "trigger": True, "trigger_angle": 12,
    "charging": ("cocking_handle", 10.6), "charging_moves_action": False,
    "mag_dir": [0, -1, 0], "mag_far": 22, "mag_gap": 0.5,
    "recoil": 0.45, "recoil_time": 0.09, "shot_time": 0.08,
    "reload_time": 2.0, "reload_empty_time": 3.0,
    "reload_tilt": [6, 12, -24], "reload_lift": [-1.0, 1.0, -1.5],
}


def _reload_empty(c):
    """The HK slap: handle locked back first, magazine swapped, then slapped home."""
    a = anims.Anim(c["reload_empty_time"])
    a.pos("cocking_handle", 0.0, anims.ZERO)
    a.pos("cocking_handle", 0.25, [0, 0, 10.6], "easeInOutSine")
    a.pos("cocking_handle", 0.33, [0, 0.45, 10.6], "easeOutQuad")       # flicked into the notch
    seat = anims._mag_swap(a, c, 0.55)
    t = seat + 0.45
    a.pos("cocking_handle", t, [0, 0.45, 10.6])
    a.pos("cocking_handle", t + 0.05, [0, 0, 10.4], "easeOutQuad")
    a.pos("cocking_handle", t + 0.12, anims.ZERO, "easeInCubic")
    anims._tilt(a, c, 0.4, t + 0.2, c["reload_empty_time"])
    a.track("root", "position", [(t + 0.1, c["reload_lift"]),
                                 (t + 0.15, anims.add(c["reload_lift"], [0.4, 0.3, 0.6]), "easeOutQuad"),
                                 (t + 0.4, c["reload_lift"], "easeInOutSine")])
    return a


ANIMATIONS = anims.build(ANIM, {"reload_empty": _reload_empty})

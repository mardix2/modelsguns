"""First-person Minecraft arms holding the gun.

Each arm is the player's arm: a 4 x 12 x 4 texel box (plus the 0.25 texel
sleeve overlay) mapped exactly like the arms of a 64 x 64 player skin, so
the mod can draw the bones `right_arm` / `left_arm` with the player's own
skin (see geckolib/example GunRenderer).  The gun's texture atlas keeps its
top-left 64 x 64 corner in skin layout with Steve-like arms as a default.

Arms keep the same on-screen size on every gun: one skin texel is 0.045
block in first-person view space (vanilla arms: 0.0625), so in model units
it is 0.72 / (first-person display scale).

Spec per gun (gun mm space: z back, y up, x right):

    ARMS = {
        "grip": ((z_top, y_top), (z_bottom, y_bottom)),   # pistol grip centre line
        "trigger": (z, y),
        "left": {"kind": "forend", "z": .., "y_top": .., "y_bot": .., "w": ..}
              or {"kind": "support"},                     # pistols
        "right_dir": (pitch, yaw), "left_dir": (pitch, yaw),   # optional, degrees
    }
"""

import math
import random

from bbgen import Material

SKIN = {  # skin texture origin (u, v) of the 4x12x4 box: arm, sleeve overlay
    "right_arm": ((40, 16), (40, 32)),
    "left_arm": ((32, 48), (48, 48)),
}
INFLATE = 0.25       # overlay layer, in texels (as in vanilla)


TEXEL_VIEW = 0.036   # one skin texel in first-person view space (blocks)


def texel(fp_scale, unit_mm):
    """Size of one skin texel in gun mm."""
    return TEXEL_VIEW * 16 / fp_scale * unit_mm


def direction(pitch, yaw):
    """Unit vector from the hand towards the shoulder."""
    p, y = math.radians(pitch), math.radians(yaw)
    return (math.cos(p) * math.sin(y), -math.sin(p), math.cos(p) * math.cos(y))


def _arm(k, bone, end, pitch, yaw, t):
    """Arm box with its hand end centred on `end` (mm), body along direction()."""
    x, y, z = end
    (u, v), (ou, ov) = SKIN[bone]
    with k.frame("y", yaw, x, y, z):
        with k.frame("x", 90 + pitch, x, y, z):
            c = k.b(bone + "_arm", x - 2 * t, y, z - 2 * t, x + 2 * t, y + 12 * t, z + 2 * t, "skin", bone)
            c.skin_uv = (u, v, "arm")
            e = INFLATE * t
            c = k.b(bone + "_sleeve", x - 2 * t - e, y - e, z - 2 * t - e, x + 2 * t + e, y + 12 * t + e,
                    z + 2 * t + e, "skin", bone)
            c.skin_uv = (ou, ov, "arm")
            # upper arm: carries on past the shoulder so the arm leaves the
            # screen; textured with the sleeve rows of the skin
            c = k.b(bone + "_upper", x - 2 * t + 0.01, y + 12 * t, z - 2 * t + 0.01, x + 2 * t - 0.01, y + 26 * t,
                    z + 2 * t - 0.01, "skin", bone)
            c.skin_uv = (u, v, "upper")


def add(m, k, spec, fp_scale):
    """Add both arms (bones right_arm / left_arm) to model m via MM helper k.
    Returns (bone pivots, palm points) in model units."""
    m.materials.setdefault("skin", Material((180, 132, 106), 0, edge=False))
    t = texel(fp_scale, k.u)
    (tz, ty), (bz, by) = spec["grip"]
    f = spec.get("grip_at", 0.55)                                   # where the hand closes
    g = (0.0, ty + f * (by - ty), tz + f * (bz - tz))
    rp, ryw = spec.get("right_dir", (48, 14))
    dr = direction(rp, ryw)
    r_end = tuple(g[i] - dr[i] * 1.8 * t for i in range(3))
    _arm(k, "right_arm", r_end, rp, ryw, t)

    lf = spec["left"]
    if lf["kind"] == "forend":
        lp, lyw = spec.get("left_dir", (40, -38))
        dl = direction(lp, lyw)
        f = (-0.4 * t, lf["y_bot"] - 1.7 * t, lf["z"])
        l_end = tuple(f[i] - dl[i] * 1.4 * t for i in range(3))
    else:  # pistol: the support hand closes beside and under the shooting hand
        lp, lyw = spec.get("left_dir", (26, -22))
        dl = direction(lp, lyw)
        l_end = (r_end[0] - 3.8 * t, r_end[1] - 0.9 * t, r_end[2] + 0.6 * t)
    _arm(k, "left_arm", l_end, lp, lyw, t)

    m.dynamic |= {"right_arm", "left_arm"}
    palms = {"right_arm": k.P(*[r_end[i] + dr[i] * 1.5 * t for i in range(3)]),
             "left_arm": k.P(*[l_end[i] + dl[i] * 1.0 * t for i in range(3)])}
    return {"right_arm": k.P(*r_end), "left_arm": k.P(*l_end)}, palms


# ---------------------------------------------------------------------------
# default (Steve-like) arm texture in skin layout

SHIRT = (0, 168, 168)
SKIN_RGB = (176, 128, 102)


def skin_faces(u, v, part="arm"):
    """Skin-layout rectangles of the 4x12x4 box at (u, v): face -> (u0, v0, u1, v1),
    named in model (Java) space for the vertical arm (as GeckoLib's box UV).
    part "upper": the sides use only the 4 shoulder rows."""
    x, y, d = 4, 12, 4
    if part == "upper":
        y = 4
    return {
        "east": (u, v + d, u + d, v + d + y),
        "north": (u + d, v + d, u + d + x, v + d + y),
        "west": (u + d + x, v + d, u + 2 * d + x, v + d + y),
        "south": (u + 2 * d + x, v + d, u + 2 * d + 2 * x, v + d + y),
        "up": (u + d, v, u + d + x, v + d),                       # shoulder
        "down": (u + d + x, v, u + d + 2 * x, v + d),             # hand end
    }


def geo_faces(u, v, part="arm"):
    """Per-face Bedrock UVs equal to GeckoLib's box UV for the 4x12x4 box."""
    x, y, d = 4, 12, 4
    if part == "upper":
        y = 4
    return {
        "east": {"uv": [u, v + d], "uv_size": [d, y]},
        "west": {"uv": [u + d + x, v + d], "uv_size": [d, y]},
        "north": {"uv": [u + d, v + d], "uv_size": [x, y]},
        "south": {"uv": [u + 2 * d + x, v + d], "uv_size": [x, y]},
        "up": {"uv": [u + d, v], "uv_size": [x, d]},
        "down": {"uv": [u + d + x, v + d], "uv_size": [x, -d]},
    }


def paint_default(px):
    """Steve-like arms (cyan sleeve, skin) in the 64x64 corner; overlays stay clear."""
    rng = random.Random(7)
    for bone, ((u, v), _) in SKIN.items():
        for face, (u0, v0, u1, v1) in skin_faces(u, v).items():
            for yy in range(v0, v1):
                for xx in range(u0, u1):
                    row = yy - v0
                    if face == "up":
                        col = SHIRT
                    elif face == "down":
                        col = SKIN_RGB
                    else:
                        col = SHIRT if row < 4 else SKIN_RGB
                    shade = {"north": 0, "east": -10, "west": -10, "south": -18, "up": 8, "down": -14}[face]
                    if col == SKIN_RGB and face not in ("up", "down") and row == 11:
                        shade -= 8           # hand end a touch darker
                    if col == SHIRT and row == 3 and face not in ("up", "down"):
                        shade -= 16          # sleeve hem
                    n = rng.randint(-5, 5)
                    px[xx, yy] = tuple(max(0, min(255, c + shade + n)) for c in col) + (255,)

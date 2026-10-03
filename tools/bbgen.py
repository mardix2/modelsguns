"""Tiny toolkit for building Blockbench / Minecraft Java item models from code.

A model is a list of axis-aligned cubes (optionally rotated on one axis by a
multiple of 22.5 degrees, as Minecraft Java requires).  From that list we:

  * procedurally paint a texture atlas (every face gets its own UV island),
  * export a Blockbench project (.bbmodel, "Java Block/Item" format),
  * export a vanilla Java item model (.json + .png),
  * render preview images with a small software rasteriser (for checking).
"""

import base64
import io
import json
import math
import random
import uuid
import zlib

from PIL import Image, ImageChops, ImageDraw

FACES = ("north", "east", "south", "west", "up", "down")
ALLOWED_ANGLES = (-45.0, -22.5, 0.0, 22.5, 45.0)


class Material:
    def __init__(self, rgb, noise=6, alpha=255, edge=True):
        self.rgb = rgb
        self.noise = noise
        self.alpha = alpha
        self.edge = edge


class Cube:
    def __init__(self, name, frm, to, mat, group, pattern=None, rot=None):
        self.name = name
        self.frm = [min(a, b) for a, b in zip(frm, to)]
        self.to = [max(a, b) for a, b in zip(frm, to)]
        self.mat = mat
        self.group = group
        self.pattern = pattern
        # rot = (axis, angle, origin)
        if rot is not None:
            axis, angle, origin = rot
            assert axis in "xyz" and float(angle) in ALLOWED_ANGLES, rot
            rot = (axis, float(angle), list(origin))
        self.rot = rot
        self.uv = {}

    def shift(self, d):
        self.frm = [a + b for a, b in zip(self.frm, d)]
        self.to = [a + b for a, b in zip(self.to, d)]
        if self.rot:
            self.rot = (self.rot[0], self.rot[1], [a + b for a, b in zip(self.rot[2], d)])


class Model:
    def __init__(self, name, materials, density=4):
        self.name = name
        self.materials = materials
        self.density = density  # texels per model unit
        self.cubes = []
        self.groups = []  # ordered group names

    # -- building helpers -------------------------------------------------
    def box(self, name, x0, y0, z0, x1, y1, z1, mat, group, pattern=None, rot=None):
        if group not in self.groups:
            self.groups.append(group)
        c = Cube(name, (x0, y0, z0), (x1, y1, z1), mat, group, pattern, rot)
        self.cubes.append(c)
        return c

    def cyl_z(self, name, cx, cy, z0, z1, r, mat, group, pattern=None):
        """Octagonal 'cylinder' along Z made of four bars (0/45/90/135 deg)."""
        t = r * math.tan(math.radians(22.5))
        e = 0.01
        self.box(name, cx - r, cy - t, z0, cx + r, cy + t, z1, mat, group, pattern)
        self.box(name + "_v", cx - t, cy - r, z0 + e, cx + t, cy + r, z1 - e, mat, group, pattern)
        for i, ang in enumerate((45, -45)):
            ee = e * (2 + i)
            self.box(name + "_d%d" % i, cx - r, cy - t, z0 + ee, cx + r, cy + t, z1 - ee,
                     mat, group, pattern, rot=("z", ang, (cx, cy, (z0 + z1) / 2)))

    def bounds(self):
        pts = [p for c in self.cubes for p in world_corners(c)]
        lo = [min(p[i] for p in pts) for i in range(3)]
        hi = [max(p[i] for p in pts) for i in range(3)]
        return lo, hi

    def center_yz(self, step=0.25):
        """Move the model so its Y/Z bounding box is centred on 8 (x is kept)."""
        lo, hi = self.bounds()
        d = [0.0]
        for i in (1, 2):
            c = (lo[i] + hi[i]) / 2
            d.append(round((8 - c) / step) * step)
        for c in self.cubes:
            c.shift(d)
        return d

    def check_java_limits(self):
        for c in self.cubes:
            for v in c.frm + c.to:
                assert -16 <= v <= 32, (c.name, v)

    # -- texture ----------------------------------------------------------
    def face_dims(self, c, face):
        sx, sy, sz = (c.to[i] - c.frm[i] for i in range(3))
        w, h = {"north": (sx, sy), "south": (sx, sy), "east": (sz, sy),
                "west": (sz, sy), "up": (sx, sz), "down": (sx, sz)}[face]
        d = self.density
        return max(1, int(round(w * d))), max(1, int(round(h * d)))

    def build_texture(self):
        items = []
        for ci, c in enumerate(self.cubes):
            for f in FACES:
                w, h = self.face_dims(c, f)
                items.append((h, w, ci, f))
        # shelf packing, tallest first; grow the square atlas until it fits
        items.sort(key=lambda t: (-t[0], -t[1]))
        size = 64
        while True:
            placed = pack(items, size)
            if placed is not None:
                break
            size *= 2
        self.size = size
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        px = img.load()
        for (h, w, ci, f), (ux, uy) in placed.items():
            c = self.cubes[ci]
            c.uv[f] = (ux, uy, ux + w, uy + h)
            paint_face(px, c, f, ux, uy, w, h, self.materials[c.mat])
        self.texture = img
        return img

    # -- exporters --------------------------------------------------------
    def java_json(self, namespace, display):
        s = 16.0 / self.size
        elements = []
        for c in self.cubes:
            el = {"name": c.name, "from": rnd(c.frm), "to": rnd(c.to)}
            if c.rot:
                el["rotation"] = {"angle": c.rot[1], "axis": c.rot[0], "origin": rnd(c.rot[2])}
            el["faces"] = {f: {"uv": rnd([v * s for v in c.uv[f]]), "texture": "#0"} for f in FACES}
            elements.append(el)
        groups = []
        for g in self.groups:
            groups.append({"name": g, "origin": [8, 8, 8], "color": 0,
                           "children": [i for i, c in enumerate(self.cubes) if c.group == g]})
        tex = "%s:item/%s" % (namespace, self.name)
        return {
            "credit": "Generated by modelsguns/tools (editable in Blockbench)",
            "texture_size": [self.size, self.size],
            "textures": {"0": tex, "particle": tex},
            "gui_light": "front",
            "elements": elements,
            "display": display,
            "groups": groups,
        }

    def bbmodel(self, display, texture_rel_path):
        def uid(*parts):
            return str(uuid.uuid5(uuid.NAMESPACE_URL, "modelsguns/" + "/".join(map(str, parts))))

        elements, outliner = [], []
        for i, c in enumerate(self.cubes):
            rot = [0, 0, 0]
            origin = [8, 8, 8]
            if c.rot:
                rot["xyz".index(c.rot[0])] = c.rot[1]
                origin = c.rot[2]
            elements.append({
                "name": c.name, "box_uv": False, "rescale": False, "locked": False,
                "render_order": "default", "allow_mirror_modeling": True,
                "from": rnd(c.frm), "to": rnd(c.to), "autouv": 0,
                "color": self.groups.index(c.group) % 8,
                "rotation": rot, "origin": rnd(origin),
                "faces": {f: {"uv": list(c.uv[f]), "texture": 0} for f in FACES},
                "type": "cube", "uuid": uid(self.name, "cube", i, c.name),
            })
        for gi, g in enumerate(self.groups):
            outliner.append({
                "name": g, "origin": [8, 8, 8], "color": gi % 8,
                "uuid": uid(self.name, "group", g), "export": True, "mirror_uv": False,
                "isOpen": False, "locked": False, "visibility": True, "autouv": 0,
                "children": [e["uuid"] for e, c in zip(elements, self.cubes) if c.group == g],
            })
        buf = io.BytesIO()
        self.texture.save(buf, "PNG")
        src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        return {
            "meta": {"format_version": "4.10", "model_format": "java_block", "box_uv": False},
            "name": self.name,
            "parent": "",
            "ambientocclusion": True,
            "front_gui_light": True,
            "visible_box": [1, 1, 0],
            "variable_placeholders": "",
            "variable_placeholder_buttons": [],
            "unhandled_root_fields": {},
            "resolution": {"width": self.size, "height": self.size},
            "elements": elements,
            "outliner": outliner,
            "textures": [{
                "path": "", "name": self.name + ".png", "folder": "item",
                "namespace": "modelsguns", "id": "0", "group": "",
                "width": self.size, "height": self.size,
                "uv_width": self.size, "uv_height": self.size,
                "particle": True, "use_as_default": True, "layers_enabled": False,
                "sync_to_project": "", "render_mode": "default", "render_sides": "auto",
                "frame_time": 1, "frame_order_type": "loop", "frame_order": "",
                "frame_interpolate": False, "visible": True, "internal": True,
                "saved": True, "uuid": uid(self.name, "texture"),
                "relative_path": texture_rel_path, "source": src,
            }],
            "display": display,
        }


# ---------------------------------------------------------------------------
# helpers

def rnd(v):
    out = []
    for x in v:
        x = round(float(x), 4)
        out.append(int(x) if x == int(x) else x)
    return out


def pack(items, size):
    x = y = shelf_h = 0
    placed = {}
    for it in items:
        h, w = it[0], it[1]
        if w > size:
            return None
        if x + w > size:
            x, y = 0, y + shelf_h
            shelf_h = 0
        if y + h > size:
            return None
        placed[it] = (x, y)
        x += w
        shelf_h = max(shelf_h, h)
    return placed


def face_corners(c, f):
    """World (unrotated) corners TL, TR, BL of a face, matching its UV layout."""
    x0, y0, z0 = c.frm
    x1, y1, z1 = c.to
    return {
        "north": ((x1, y1, z0), (x0, y1, z0), (x1, y0, z0)),
        "south": ((x0, y1, z1), (x1, y1, z1), (x0, y0, z1)),
        "east": ((x1, y1, z1), (x1, y1, z0), (x1, y0, z1)),
        "west": ((x0, y1, z0), (x0, y1, z1), (x0, y0, z0)),
        "up": ((x0, y1, z0), (x1, y1, z0), (x0, y1, z1)),
        "down": ((x0, y0, z1), (x1, y0, z1), (x0, y0, z0)),
    }[f]


def clamp(v):
    return max(0, min(255, int(v)))


def paint_face(px, c, f, ux, uy, w, h, mat):
    tl, tr, bl = face_corners(c, f)
    seed = zlib.crc32((c.name + '/' + f).encode())
    rng = random.Random(seed)
    pat = PATTERNS.get(c.pattern)
    for v in range(h):
        for u in range(w):
            a, b = (u + 0.5) / w, (v + 0.5) / h
            p = tuple(tl[i] + a * (tr[i] - tl[i]) + b * (bl[i] - tl[i]) for i in range(3))
            r, g, bb = mat.rgb
            alpha = mat.alpha
            d = rng.uniform(-mat.noise, mat.noise)
            if mat.edge and w >= 3 and h >= 3:
                if v == 0 or u == 0:
                    d += 16
                elif v == h - 1 or u == w - 1:
                    d -= 14
            col = None
            if pat:
                res = pat(p, f, u, v, w, h, c, rng)
                if isinstance(res, tuple):
                    col = res
                elif res:
                    d += res
            if col is not None:
                r, g, bb = col[:3]
                if len(col) == 4:
                    alpha = col[3]
                px[ux + u, uy + v] = (clamp(r + d * 0.3), clamp(g + d * 0.3), clamp(bb + d * 0.3), alpha)
            else:
                px[ux + u, uy + v] = (clamp(r + d), clamp(g + d), clamp(bb + d), alpha)


# --- surface patterns -------------------------------------------------------

def _along_z(f):
    return f in ("east", "west", "up", "down")


def pat_rail(period, slot):
    def fn(p, f, u, v, w, h, c, rng):
        if _along_z(f) and (p[2] - c.frm[2]) % period < slot:
            return -26
        return 0
    return fn


def pat_serration(p, f, u, v, w, h, c, rng):
    if f in ("east", "west") and (p[2] % 0.5) < 0.25:
        return -22
    return 0


def pat_stipple(p, f, u, v, w, h, c, rng):
    return rng.choice((-9, -5, 0, 4, 8))


def pat_knurl(p, f, u, v, w, h, c, rng):
    return -12 if (u + v) % 2 else 6


def pat_ribs(p, f, u, v, w, h, c, rng):
    if f in ("east", "west") and (p[1] % 0.75) < 0.25:
        return -14
    return 0


def pat_flash(p, f, u, v, w, h, c, rng):
    # longitudinal slots near the front of a flash hider
    if f in ("north", "south"):
        return 0
    across, n = (u, w) if f in ("up", "down") else (v, h)
    if abs(across + 0.5 - n / 2) < 0.8 and p[2] - c.frm[2] < 1.1:
        return (6, 6, 6)
    return 0


def pat_bore(p, f, u, v, w, h, c, rng):
    return (5, 5, 5)


def pat_reticle(p, f, u, v, w, h, c, rng):
    if f not in ("north", "south"):
        return 0
    dx, dy = u + 0.5 - w / 2, v + 0.5 - h / 2
    r = math.hypot(dx, dy)
    ring = min(w, h) * 0.32
    if r < 0.8 or abs(r - ring) < 0.55:
        return (255, 40, 30, 230)
    return 0


def pat_dot(p, f, u, v, w, h, c, rng):
    if f == "south" and abs(u + 0.5 - w / 2) <= 1 and abs(v + 0.5 - h / 2) <= 1:
        return (235, 235, 225)
    return 0


def pat_lens(p, f, u, v, w, h, c, rng):
    if f == "north":
        r = math.hypot(u + 0.5 - w / 2, v + 0.5 - h / 2) / (min(w, h) / 2)
        return (255, 255, int(200 + 50 * (1 - min(r, 1))))
    return 0


def pat_logo(p, f, u, v, w, h, c, rng):
    # faint engraved rectangle (roll-mark style) on the sides
    if f in ("east", "west") and 2 <= u < w - 2 and v in (2, 3) and u % 3 != 0:
        return 22
    return 0


PATTERNS = {
    "rail": pat_rail(0.75, 0.25),
    "rail_pistol": pat_rail(1.5, 0.5),
    "serration": pat_serration,
    "stipple": pat_stipple,
    "knurl": pat_knurl,
    "ribs": pat_ribs,
    "flash": pat_flash,
    "bore": pat_bore,
    "reticle": pat_reticle,
    "dot": pat_dot,
    "lens": pat_lens,
    "logo": pat_logo,
}


# ---------------------------------------------------------------------------
# geometry / rendering

def rotate(p, rot):
    if not rot:
        return p
    axis, ang, o = rot
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    x, y, z = p[0] - o[0], p[1] - o[1], p[2] - o[2]
    if axis == "x":
        y, z = y * ca - z * sa, y * sa + z * ca
    elif axis == "y":
        x, z = x * ca + z * sa, -x * sa + z * ca
    else:
        x, y = x * ca - y * sa, x * sa + y * ca
    return (x + o[0], y + o[1], z + o[2])


def world_corners(c):
    out = []
    for x in (c.frm[0], c.to[0]):
        for y in (c.frm[1], c.to[1]):
            for z in (c.frm[2], c.to[2]):
                out.append(rotate((x, y, z), c.rot))
    return out


def render(model, yaw, pitch, width=1200, height=800, bg=(236, 238, 242), ss=2):
    """Orthographic textured render. yaw/pitch in degrees (camera orbit)."""
    W, H = width * ss, height * ss
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def view(p):
        x, y, z = p[0] - 8, p[1] - 8, p[2] - 8
        x, z = x * cy_ + z * sy_, -x * sy_ + z * cy_
        y, z = y * cp - z * sp, y * sp + z * cp
        return x, y, z  # z: towards camera

    light = (0.35, 0.85, 0.4)
    ln = math.sqrt(sum(v * v for v in light))
    light = tuple(v / ln for v in light)

    polys = []
    for c in model.cubes:
        for f in FACES:
            tl, tr, bl = (rotate(p, c.rot) for p in face_corners(c, f))
            br = tuple(tr[i] + bl[i] - tl[i] for i in range(3))
            e1 = [tr[i] - tl[i] for i in range(3)]
            e2 = [bl[i] - tl[i] for i in range(3)]
            n = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
            nl = math.sqrt(sum(v * v for v in n)) or 1
            n = tuple(-v / nl for v in n)  # outward normal
            vn = view((n[0] + 8, n[1] + 8, n[2] + 8))
            if vn[2] <= 1e-6:
                continue
            vs = [view(p) for p in (tl, tr, bl, br)]
            depth = sum(v[2] for v in vs) / 4
            shade = 0.55 + 0.45 * max(0.0, sum(n[i] * light[i] for i in range(3)))
            polys.append((depth, c, f, vs, shade))
    polys.sort(key=lambda t: t[0])

    lo, hi = model.bounds()
    corners = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    vc = [view(p) for p in corners]
    minx, maxx = min(v[0] for v in vc), max(v[0] for v in vc)
    miny, maxy = min(v[1] for v in vc), max(v[1] for v in vc)
    scale = 0.9 * min(W / (maxx - minx), H / (maxy - miny))
    ox = W / 2 - scale * (minx + maxx) / 2
    oy = H / 2 + scale * (miny + maxy) / 2

    def scr(v):
        return (ox + v[0] * scale, oy - v[1] * scale)

    img = Image.new("RGBA", (W, H), bg + (255,))
    tex = model.texture
    for _, c, f, vs, shade in polys:
        u0, v0, u1, v1 = c.uv[f]
        tw, th = u1 - u0, v1 - v0
        crop = tex.crop((u0, v0, u1, v1))
        r, g, b, a = crop.split()
        lut = [min(255, int(i * shade)) for i in range(256)]
        crop = Image.merge("RGBA", (r.point(lut), g.point(lut), b.point(lut), a))
        p0, p1, p2, p3 = (scr(v) for v in vs)
        xs = [p[0] for p in (p0, p1, p2, p3)]
        ys = [p[1] for p in (p0, p1, p2, p3)]
        bx0, by0 = int(math.floor(min(xs))), int(math.floor(min(ys)))
        bx1, by1 = int(math.ceil(max(xs))) + 1, int(math.ceil(max(ys))) + 1
        bw, bh = bx1 - bx0, by1 - by0
        if bw <= 0 or bh <= 0:
            continue
        A = ((p1[0] - p0[0]) / tw, (p1[1] - p0[1]) / tw)
        B = ((p2[0] - p0[0]) / th, (p2[1] - p0[1]) / th)
        det = A[0] * B[1] - B[0] * A[1]
        if abs(det) < 1e-9:
            continue
        ia, ib = B[1] / det, -B[0] / det
        ic, id_ = -A[1] / det, A[0] / det
        dx, dy = bx0 - p0[0], by0 - p0[1]
        data = (ia, ib, ia * dx + ib * dy, ic, id_, ic * dx + id_ * dy)
        patch = crop.transform((bw, bh), Image.AFFINE, data, resample=Image.NEAREST)
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).polygon(
            [(p[0] - bx0, p[1] - by0) for p in (p0, p1, p3, p2)], fill=255)
        alpha = patch.split()[3]
        mask = ImageChops.multiply(mask, alpha)
        img.paste(patch, (bx0, by0), mask)
    return img.resize((width, height), Image.LANCZOS)


def save_json(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1)
        fh.write("\n")

"""Gun animation library (GeckoLib / Bedrock animation 1.8.0).

Everything is authored in model space (the same space as the geometry):
  +X = right side (ejection port), +Y = up, -Z = muzzle direction.
  rotation X > 0 lifts the muzzle, Y > 0 swings the muzzle to the left,
  Z > 0 rolls the top of the gun to the left.
Positions are in model pixels.  `root` is the parent of every bone and
pivots at the grip, so moving it moves the whole gun.

A keyframe value is either [x, y, z] or ([x, y, z], "easing") where easing is
any GeckoLib easing name (easeOutQuad, easeInOutSine, easeOutBack, ...).
"""

ZERO = [0, 0, 0]


class Anim:
    def __init__(self, length, loop=False):
        self.length = length
        self.loop = loop
        self.bones = {}

    def key(self, bone, chan, t, vec, ease=None):
        ch = self.bones.setdefault(bone, {}).setdefault(chan, {})
        ch[round(t, 4)] = (list(vec), ease) if ease else list(vec)
        return self

    def pos(self, bone, t, vec, ease=None):
        return self.key(bone, "position", t, vec, ease)

    def rot(self, bone, t, vec, ease=None):
        return self.key(bone, "rotation", t, vec, ease)

    def track(self, bone, chan, keys):
        """keys: list of (t, vec) or (t, vec, ease)."""
        for k in keys:
            self.key(bone, chan, *k)
        return self

    def spec(self):
        return {"length": self.length, "loop": self.loop, "bones": self.bones}


def scale(v, s):
    return [a * s for a in v]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


# ---------------------------------------------------------------------------
# root motions shared by every gun

def idle(c):
    a = Anim(4.0, loop=True)
    a.track("root", "rotation", [(0, ZERO), (1.0, [0.35, 0.2, -0.25], "easeInOutSine"),
                                 (2.0, [0.1, -0.15, 0.2], "easeInOutSine"),
                                 (3.0, [-0.3, 0.1, 0.1], "easeInOutSine"), (4.0, ZERO, "easeInOutSine")])
    a.track("root", "position", [(0, ZERO), (1.0, [0, 0.12, 0], "easeInOutSine"),
                                 (2.0, [0, 0.0, 0.05], "easeInOutSine"),
                                 (3.0, [0, 0.1, 0], "easeInOutSine"), (4.0, ZERO, "easeInOutSine")])
    return a


def draw(c):
    a = Anim(c.get("draw_time", 0.6))
    L = a.length
    a.track("root", "position", [(0, [2, -12, 6]), (L * 0.6, [0, 0.6, -0.4], "easeOutCubic"),
                                 (L, ZERO, "easeInOutSine")])
    a.track("root", "rotation", [(0, [-55, 25, -35]), (L * 0.6, [3, -1, 2], "easeOutCubic"),
                                 (L, ZERO, "easeInOutSine")])
    if c.get("action") and c.get("rack_on_draw"):
        _action_cycle(a, c, L * 0.55, slow=True)
    return a


def holster(c):
    a = Anim(0.45)
    a.track("root", "position", [(0, ZERO), (0.45, [2, -12, 6], "easeInCubic")])
    a.track("root", "rotation", [(0, ZERO), (0.45, [-55, 25, -35], "easeInCubic")])
    return a


def sprint(c):
    a = Anim(0.8, loop=True)
    base_r = [-22, 32, 18]
    base_p = [-1.5, -2.5, 1.5]
    a.track("root", "rotation", [(0, base_r), (0.2, add(base_r, [2, 1.5, -2]), "easeInOutSine"),
                                 (0.4, base_r, "easeInOutSine"), (0.6, add(base_r, [2, -1.5, 2]), "easeInOutSine"),
                                 (0.8, base_r, "easeInOutSine")])
    a.track("root", "position", [(0, base_p), (0.2, add(base_p, [0.3, -0.5, 0]), "easeInOutSine"),
                                 (0.4, base_p, "easeInOutSine"), (0.6, add(base_p, [-0.3, -0.5, 0]), "easeInOutSine"),
                                 (0.8, base_p, "easeInOutSine")])
    return a


def _recoil(a, c, t0=0.0):
    kick = c.get("recoil", 1.0)
    rx = 2.5 * kick
    a.track("root", "position", [(t0, ZERO), (t0 + 0.03, [0, 0.15 * kick, 1.1 * kick], "easeOutQuad"),
                                 (t0 + c.get("recoil_time", 0.2), ZERO, "easeInOutSine")])
    a.track("root", "rotation", [(t0, ZERO), (t0 + 0.035, [rx, 0.4 * kick, -0.6 * kick], "easeOutQuad"),
                                 (t0 + c.get("recoil_time", 0.2), ZERO, "easeInOutSine")])


def _trigger(a, c, t0=0.0, hold=0.04):
    if "trigger" in c:
        a.track("trigger", "rotation", [(t0, ZERO), (t0 + 0.02, [-c.get("trigger_angle", 14), 0, 0], "easeOutQuad"),
                                        (t0 + 0.02 + hold, [-c.get("trigger_angle", 14), 0, 0]),
                                        (t0 + 0.08 + hold, ZERO, "easeInOutSine")])


def _action_cycle(a, c, t0, slow=False, stay_back=False):
    """Bolt / slide travelling back and forward."""
    act = c.get("action")
    if not act:
        return
    travel = c["travel"]
    back, fwd = (0.12, 0.12) if slow else (c.get("cycle_back", 0.03), c.get("cycle_fwd", 0.06))
    a.pos(act, t0, ZERO)
    a.pos(act, t0 + back, [0, 0, travel], "easeOutQuad")
    if not stay_back:
        a.pos(act, t0 + back + fwd, ZERO, "easeInQuad")
    for bone, k in c.get("followers", {}).items():   # e.g. pistol barrel tilting
        a.pos(bone, t0, ZERO)
        a.pos(bone, t0 + back * 0.6, scale(k["pos"], 1), "easeOutQuad")
        if "rot" in k:
            a.rot(bone, t0, ZERO)
            a.rot(bone, t0 + back * 0.6, k["rot"], "easeOutQuad")
        if not stay_back:
            a.pos(bone, t0 + back + fwd, ZERO, "easeInQuad")
            if "rot" in k:
                a.rot(bone, t0 + back + fwd, ZERO, "easeInQuad")
    if "hammer" in c:
        a.rot("hammer", t0, ZERO)
        a.rot("hammer", t0 + back, [c["hammer"], 0, 0], "easeOutQuad")
        if not stay_back:
            a.rot("hammer", t0 + back + fwd, [c["hammer"] * 0.95, 0, 0])


def shoot(c):
    a = Anim(c.get("shot_time", 0.15))
    _trigger(a, c)
    _recoil(a, c)
    if c.get("action") and c.get("cycles_on_shot", True):
        _action_cycle(a, c, 0.0)
    if "hammer" in c:   # hammer falls first, then is re-cocked by the slide
        a.track("hammer", "rotation", [(0, [c["hammer"], 0, 0]), (0.01, ZERO, "easeInQuad"),
                                       (0.04, [c["hammer"], 0, 0], "easeOutQuad")])
    return a


def shoot_last(c):
    """Last round: the bolt / slide locks back."""
    a = Anim(0.3)
    _trigger(a, c)
    _recoil(a, c)
    if c.get("action") and c.get("locks_back"):
        _action_cycle(a, c, 0.0, stay_back=True)
        if "stop" in c:
            a.rot(c["stop"]["bone"], 0.0, ZERO)
            a.rot(c["stop"]["bone"], 0.05, c["stop"]["rot"], "easeOutQuad")
    return a


def idle_empty(c):
    """Held while the gun is empty and locked open."""
    a = Anim(1.0, loop=True)
    if c.get("action") and c.get("locks_back"):
        a.pos(c["action"], 0, [0, 0, c["travel"]])
        a.pos(c["action"], 1.0, [0, 0, c["travel"]])
        for bone, k in c.get("followers", {}).items():
            a.pos(bone, 0, k["pos"])
            if "rot" in k:
                a.rot(bone, 0, k["rot"])
        if "stop" in c:
            a.rot(c["stop"]["bone"], 0, c["stop"]["rot"])
    return a


# ---------------------------------------------------------------------------
# magazine reloads

def _tilt(a, c, t_in, t_out, length):
    tilt = c.get("reload_tilt", [8, 14, -28])
    lift = c.get("reload_lift", [-1.0, 1.0, -1.5])
    a.track("root", "rotation", [(0, ZERO), (t_in, tilt, "easeInOutSine"),
                                 (t_out, add(tilt, [-2, 0, 3]), "easeInOutSine"), (length, ZERO, "easeInOutSine")])
    a.track("root", "position", [(0, ZERO), (t_in, lift, "easeInOutSine"),
                                 (t_out, lift, "easeInOutSine"), (length, ZERO, "easeInOutSine")])


def _mag_swap(a, c, t0):
    """Old magazine out, new one in.  Returns the time the new mag seats."""
    mag = c.get("mag", "magazine")
    d = c.get("mag_dir", [0, -1, 0])
    far = c.get("mag_far", 18)
    rock = c.get("mag_rock")            # AK style: rock forward before dropping
    if "release" in c:
        rb, rv = c["release"]
        a.pos(rb, t0, ZERO)
        a.pos(rb, t0 + 0.06, rv, "easeOutQuad")
        a.pos(rb, t0 + 0.2, ZERO, "easeInQuad")
    if rock:
        a.rot(mag, t0, ZERO)
        a.rot(mag, t0 + 0.15, [rock, 0, 0], "easeOutQuad")
        a.rot(mag, t0 + 0.5, [rock, 0, 0])
    a.pos(mag, t0, ZERO)
    a.pos(mag, t0 + 0.06, scale(d, 1.2), "easeOutQuad")              # unlatches
    a.pos(mag, t0 + 0.32, scale(d, far), "easeInQuad")                # falls out
    t_new = t0 + c.get("mag_gap", 0.45)
    a.pos(mag, t_new, scale(d, far), "step")                           # new mag appears
    a.pos(mag, t_new + 0.3, scale(d, 3.0), "easeOutCubic")             # brought to the well
    if rock:
        a.rot(mag, t_new, [rock, 0, 0], "step")
        a.rot(mag, t_new + 0.3, [rock, 0, 0])
        a.rot(mag, t_new + 0.45, ZERO, "easeInOutSine")
    a.pos(mag, t_new + 0.45, scale(d, 1.5), "easeInOutSine")
    seat = t_new + 0.55
    a.pos(mag, seat, scale(d, -0.25), "easeInQuad")                    # slapped home
    a.pos(mag, seat + 0.08, ZERO, "easeOutQuad")
    # the gun jolts as the magazine seats
    return seat


def reload(c):
    L = c.get("reload_time", 2.0)
    a = Anim(L)
    seat = _mag_swap(a, c, 0.3)
    _tilt(a, c, 0.3, seat + 0.25, L)
    a.track("root", "position", [(seat, c.get("reload_lift", [-1.0, 1.0, -1.5])),
                                 (seat + 0.05, add(c.get("reload_lift", [-1.0, 1.0, -1.5]), [0, 0.6, 0]), "easeOutQuad"),
                                 (seat + 0.25, c.get("reload_lift", [-1.0, 1.0, -1.5]), "easeInOutSine")])
    return a


def reload_empty(c):
    L = c.get("reload_empty_time", 2.6)
    a = Anim(L)
    act = c.get("action")
    seat = _mag_swap(a, c, 0.3)
    _tilt(a, c, 0.3, seat + 0.7, L)
    t_rel = seat + 0.3
    if act and c.get("locks_back"):
        travel = c["travel"]
        a.pos(act, 0, [0, 0, travel])
        a.pos(act, t_rel, [0, 0, travel])
        a.pos(act, t_rel + 0.06, ZERO, "easeInCubic")                 # slams home
        for bone, k in c.get("followers", {}).items():
            a.pos(bone, 0, k["pos"])
            a.pos(bone, t_rel, k["pos"])
            a.pos(bone, t_rel + 0.06, ZERO, "easeInCubic")
            if "rot" in k:
                a.rot(bone, 0, k["rot"])
                a.rot(bone, t_rel, k["rot"])
                a.rot(bone, t_rel + 0.06, ZERO, "easeInCubic")
        if "stop" in c:
            sb, sr = c["stop"]["bone"], c["stop"]["rot"]
            a.rot(sb, 0, sr)
            a.rot(sb, t_rel - 0.04, add(sr, scale(sr, 0.4)), "easeOutQuad")   # thumb presses it
            a.rot(sb, t_rel, ZERO, "easeInQuad")
    elif "charging" in c:
        _charge(a, c, t_rel - 0.1)
    elif act:
        _action_cycle(a, c, t_rel, slow=True)
    a.track("root", "position", [(t_rel + 0.05, c.get("reload_lift", [-1.0, 1.0, -1.5])),
                                 (t_rel + 0.1, add(c.get("reload_lift", [-1.0, 1.0, -1.5]), [0, 0.4, 0.8]), "easeOutQuad"),
                                 (t_rel + 0.35, c.get("reload_lift", [-1.0, 1.0, -1.5]), "easeInOutSine")])
    return a


def _charge(a, c, t0):
    """Pull a separate charging handle (AR / MP5 / AK) and let it go."""
    ch, travel = c["charging"]
    a.pos(ch, t0, ZERO)
    a.pos(ch, t0 + 0.22, [0, 0, travel], "easeInOutSine")
    a.pos(ch, t0 + 0.3, [0, 0, travel])
    a.pos(ch, t0 + 0.36, ZERO, "easeInCubic")
    if c.get("action") and c.get("charging_moves_action", True):
        a.pos(c["action"], t0, ZERO)
        a.pos(c["action"], t0 + 0.22, [0, 0, c["travel"]], "easeInOutSine")
        a.pos(c["action"], t0 + 0.3, [0, 0, c["travel"]])
        a.pos(c["action"], t0 + 0.36, ZERO, "easeInCubic")


# ---------------------------------------------------------------------------
# inspection: show both sides, then a press check

def inspect(c):
    L = 3.6
    a = Anim(L)
    a.track("root", "rotation", [(0, ZERO), (0.45, [6, 48, -12], "easeInOutSine"),
                                 (1.25, [10, 52, -16], "easeInOutSine"),
                                 (1.75, [-6, -38, 34], "easeInOutSine"),
                                 (2.55, [-8, -42, 38], "easeInOutSine"),
                                 (3.1, [4, -6, 8], "easeInOutSine"), (L, ZERO, "easeInOutSine")])
    a.track("root", "position", [(0, ZERO), (0.45, [-2.5, 1.5, -2], "easeInOutSine"),
                                 (1.25, [-2.5, 1.7, -2], "easeInOutSine"),
                                 (1.75, [-1.0, 1.0, -1], "easeInOutSine"),
                                 (2.55, [-1.0, 1.2, -1], "easeInOutSine"), (L, ZERO, "easeInOutSine")])
    t = 2.0
    if "charging" in c:
        ch, travel = c["charging"]
        a.pos(ch, t, ZERO)
        a.pos(ch, t + 0.2, [0, 0, travel * 0.45], "easeInOutSine")
        a.pos(ch, t + 0.45, [0, 0, travel * 0.45])
        a.pos(ch, t + 0.6, ZERO, "easeInOutSine")
        if c.get("action") and c.get("charging_moves_action", True):
            a.pos(c["action"], t, ZERO)
            a.pos(c["action"], t + 0.2, [0, 0, c["travel"] * 0.45], "easeInOutSine")
            a.pos(c["action"], t + 0.45, [0, 0, c["travel"] * 0.45])
            a.pos(c["action"], t + 0.6, ZERO, "easeInOutSine")
    elif c.get("action") and c.get("press_check", True):
        act = c["action"]
        a.pos(act, t, ZERO)
        a.pos(act, t + 0.2, [0, 0, c["travel"] * 0.35], "easeInOutSine")
        a.pos(act, t + 0.45, [0, 0, c["travel"] * 0.35])
        a.pos(act, t + 0.6, ZERO, "easeInOutSine")
    if c.get("inspect_mag", True) and c.get("mag", "magazine"):
        d = c.get("mag_dir", [0, -1, 0])
        mag = c.get("mag", "magazine")
        a.pos(mag, 0.6, ZERO)
        a.pos(mag, 0.75, scale(d, 1.5), "easeOutQuad")
        a.pos(mag, 1.05, scale(d, 1.5))
        a.pos(mag, 1.15, ZERO, "easeInQuad")
    return a


def firemode(c):
    a = Anim(0.45)
    if "selector" in c:
        b, r = c["selector"]
        a.rot(b, 0, ZERO)
        a.rot(b, 0.12, r, "easeOutBack")
        a.rot(b, 0.3, r)
        a.rot(b, 0.42, ZERO, "easeInOutSine")
    a.track("root", "rotation", [(0, ZERO), (0.15, [0, 2, -6], "easeInOutSine"), (0.45, ZERO, "easeInOutSine")])
    return a


def build(c, extra=None):
    """Full standard set for one gun; `extra` adds or overrides animations."""
    anims = {
        "idle": idle(c), "draw": draw(c), "holster": holster(c), "sprint": sprint(c),
        "shoot": shoot(c), "inspect": inspect(c),
    }
    if c.get("mag", "magazine"):
        anims["reload"] = reload(c)
        anims["reload_empty"] = reload_empty(c)
    if c.get("locks_back"):
        anims["shoot_last"] = shoot_last(c)
        anims["idle_empty"] = idle_empty(c)
    if "selector" in c:
        anims["firemode"] = firemode(c)
    for k, v in (extra or {}).items():
        anims[k] = v(c) if callable(v) else v
    return {k: v.spec() for k, v in anims.items()}

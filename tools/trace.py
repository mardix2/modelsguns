"""Turn a side silhouette (tools/silhouettes/<gun>.png) into profile outlines.

A gun spec gives the photo scale (px per mm), the muzzle x and the bore y in
the normalised silhouette frame.  A part is the silhouette clipped by a
region polygon (px); its contours (outer rings and holes) are simplified and
converted to mm so MM.prof() can extrude them.
"""

import os

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


class Silhouette:
    def __init__(self, gun, px_per_mm, muzzle_x, bore_y):
        path = os.path.join(HERE, "silhouettes", gun + ".png")
        self.mask = (np.array(Image.open(path)) > 127).astype(np.uint8)
        mpath = os.path.join(HERE, "silhouettes", gun + "_mat.png")
        self.mat = ((np.array(Image.open(mpath)) > 127).astype(np.uint8)
                    if os.path.exists(mpath) else np.zeros_like(self.mask))
        self.ppm = float(px_per_mm)
        self.mx = float(muzzle_x)
        self.by = float(bore_y)

    def mm(self, X, Y):
        """photo px -> (z_mm, y_mm)"""
        return ((X - self.mx) / self.ppm, (self.by - Y) / self.ppm)

    def zmm(self, X):
        return (X - self.mx) / self.ppm

    def ymm(self, Y):
        return (self.by - Y) / self.ppm

    def rings(self, region=None, eps=2.0, min_area=12, extra=None, cut=None, src="mask",
              smooth=1.5, min_edge=3.0):
        """Contours of (source ∩ region) [∪ extra] [- cut], in mm.

        src: "mask" (whole silhouette), "mat" (furniture only) or "metal"
        (silhouette without furniture)."""
        m = {"mask": self.mask, "mat": self.mat & self.mask, "metal": self.mask & (1 - self.mat)}[src].copy()
        if region is not None:
            r = np.zeros_like(m)
            cv2.fillPoly(r, [np.array(region, np.int32)], 1)
            m &= r
        if extra is not None:
            for poly in extra:
                cv2.fillPoly(m, [np.array(poly, np.int32)], 1)
        if cut is not None:
            for poly in cut:
                cv2.fillPoly(m, [np.array(poly, np.int32)], 0)
        if smooth:
            m = (cv2.GaussianBlur(m.astype(np.float32), (0, 0), smooth) > 0.5).astype(np.uint8)
        cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        out = []
        for c in cs:
            if cv2.contourArea(c) < min_area:
                continue
            a = cv2.approxPolyDP(c, eps, True)[:, 0, :].astype(float)
            # drop vertices closer than min_edge px to the previous one
            pts = [a[0]]
            for p in a[1:]:
                if np.hypot(*(p - pts[-1])) >= min_edge:
                    pts.append(p)
            if len(pts) > 3 and np.hypot(*(pts[0] - pts[-1])) < min_edge:
                pts.pop()
            a = pts
            if len(a) >= 3:
                out.append([self.mm(float(x), float(y)) for x, y in a])
        return out

    def poly(self, pts):
        """Manual outline in photo px -> ring in mm."""
        return [self.mm(x, y) for x, y in pts]

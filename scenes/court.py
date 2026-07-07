"""Reusable to-scale tennis court Mobject for Manim animations."""
from manim import *
import numpy as np
from scenes.theme import HOST_COLOR, GUEST_COLOR


# Court dimensions in meters (ITF standard)
COURT_LENGTH = 23.77
DOUBLES_WIDTH = 10.97
SINGLES_WIDTH = 8.23
SERVICE_LINE_DIST = 6.4

# Scale: 1 meter = SCALE Manim units
SCALE = 0.22

# Colors
CLAY_COLOR = "#C65D3F"
CLAY_DARK = "#A04A30"
LINE_COLOR = "#FFFFFF"


def court_to_manim(x, y, sf=SCALE, landscape=False):
    """Convert SwingVision court coordinates (meters) to Manim scene coords."""
    if landscape:
        return np.array([y * sf, -x * sf, 0])
    return np.array([x * sf, y * sf, 0])


class TennisCourt(VGroup):
    """A to-scale tennis court rendered in clay-court style."""

    def __init__(self, scale_factor=SCALE, landscape=False, **kwargs):
        self.sf = scale_factor
        self.landscape = landscape
        super().__init__(**kwargs)
        self._build()

    def _build(self):
        sf = self.sf
        L = self.landscape
        hw = DOUBLES_WIDTH / 2
        hsw = SINGLES_WIDTH / 2
        bl = COURT_LENGTH / 2

        def c2p(x, y):
            return court_to_manim(x, y, sf, L)

        if L:
            surf_w = COURT_LENGTH * sf
            surf_h = DOUBLES_WIDTH * sf
        else:
            surf_w = DOUBLES_WIDTH * sf
            surf_h = COURT_LENGTH * sf

        surface = Rectangle(
            width=surf_w, height=surf_h,
            fill_color=CLAY_COLOR, fill_opacity=0.88, stroke_width=0,
        )

        if L:
            alley_h = (DOUBLES_WIDTH - SINGLES_WIDTH) / 2 * sf
            alley_top = Rectangle(width=surf_w, height=alley_h, fill_color=CLAY_DARK, fill_opacity=0.35, stroke_width=0)
            alley_top.move_to(surface.get_top() + DOWN * alley_h / 2)
            alley_bottom = alley_top.copy().move_to(surface.get_bottom() + UP * alley_h / 2)
            alleys = VGroup(alley_top, alley_bottom)
        else:
            alley_w = (DOUBLES_WIDTH - SINGLES_WIDTH) / 2 * sf
            alley_left = Rectangle(width=alley_w, height=surf_h, fill_color=CLAY_DARK, fill_opacity=0.35, stroke_width=0)
            alley_left.move_to(surface.get_left() + RIGHT * alley_w / 2)
            alley_right = alley_left.copy().move_to(surface.get_right() - LEFT * alley_w / 2)
            alleys = VGroup(alley_left, alley_right)

        outer = Rectangle(
            width=surf_w, height=surf_h,
            stroke_color=LINE_COLOR, stroke_width=2.5, fill_opacity=0,
        )

        if L:
            sl_y = hsw * sf
            singles_top = Line(
                surface.get_top() + LEFT * surf_w/2 + DOWN * sl_y,
                surface.get_top() + RIGHT * surf_w/2 + DOWN * sl_y,
                stroke_color=LINE_COLOR, stroke_width=2,
            )
            singles_bottom = Line(
                surface.get_bottom() + LEFT * surf_w/2 + UP * sl_y,
                surface.get_bottom() + RIGHT * surf_w/2 + UP * sl_y,
                stroke_color=LINE_COLOR, stroke_width=2,
            )
            sd = SERVICE_LINE_DIST * sf
            svc_left = Line(
                surface.get_center() + LEFT * sd + UP * hsw * sf,
                surface.get_center() + LEFT * sd + DOWN * hsw * sf,
                stroke_color=LINE_COLOR, stroke_width=2,
            )
            svc_right = Line(
                surface.get_center() + RIGHT * sd + UP * hsw * sf,
                surface.get_center() + RIGHT * sd + DOWN * hsw * sf,
                stroke_color=LINE_COLOR, stroke_width=2,
            )
            center_svc = Line(svc_left.get_center(), svc_right.get_center(), stroke_color=LINE_COLOR, stroke_width=2)
            net = Line(
                surface.get_center() + UP * hsw * sf,
                surface.get_center() + DOWN * hsw * sf,
                stroke_color="#EEEEEE", stroke_width=3,
            )
            cm_left = Line(surface.get_left() + UP*0.04, surface.get_left() + DOWN*0.04, stroke_color=LINE_COLOR, stroke_width=2)
            cm_right = cm_left.copy().move_to(surface.get_right())
            self.add(surface, alleys, outer, singles_top, singles_bottom,
                     svc_left, svc_right, center_svc, net, cm_left, cm_right)
        else:
            singles_left = Line(c2p(-hsw, -bl), c2p(-hsw, bl), stroke_color=LINE_COLOR, stroke_width=2)
            singles_right = Line(c2p(hsw, -bl), c2p(hsw, bl), stroke_color=LINE_COLOR, stroke_width=2)
            service_top = Line(c2p(-hsw, SERVICE_LINE_DIST), c2p(hsw, SERVICE_LINE_DIST), stroke_color=LINE_COLOR, stroke_width=2)
            service_bottom = Line(c2p(-hsw, -SERVICE_LINE_DIST), c2p(hsw, -SERVICE_LINE_DIST), stroke_color=LINE_COLOR, stroke_width=2)
            center_service = Line(c2p(0, -SERVICE_LINE_DIST), c2p(0, SERVICE_LINE_DIST), stroke_color=LINE_COLOR, stroke_width=2)
            net = Line(c2p(-hw, 0), c2p(hw, 0), stroke_color="#EEEEEE", stroke_width=3)
            center_mark_top = Line(c2p(0, bl) + UP*0.02, c2p(0, bl) + DOWN*0.02, stroke_color=LINE_COLOR, stroke_width=2)
            center_mark_bottom = center_mark_top.copy().shift(DOWN * 0.08)
            self.add(surface, alleys, outer, singles_left, singles_right,
                     service_top, service_bottom, center_service, net,
                     center_mark_top, center_mark_bottom)

    def court_point(self, x_meters, y_meters):
        """Convert SwingVision (x, y) in meters to a Manim point on this court."""
        return court_to_manim(x_meters, y_meters, self.sf, self.landscape) + self.get_center()

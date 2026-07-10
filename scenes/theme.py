"""Shared broadcast-style theme for PPD Manim visualizations.

Colors and fonts are sourced from courtviz integration artifacts
(@ppd/tokens). Regenerate via: pnpm --filter @ppd/tokens build
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

# Import generated token constants
_INTEGRATION = Path(__file__).resolve().parents[2] / "courtviz" / "integration" / "python"
if str(_INTEGRATION) not in sys.path:
    sys.path.insert(0, str(_INTEGRATION))

try:
    from style_generated import (  # type: ignore[import-not-found]
        ACCENT,
        BG_COLOR,
        BODY_FONT,
        DISPLAY_FONT,
        INK,
        INK_MUTED,
        PLAYER_GUEST,
        PLAYER_HOST,
        PRIMARY_BRIGHT,
    )
except ImportError:
    # Fallback if integration artifacts not yet built
    BG_COLOR = "#0F172A"
    INK = "#F2F5FA"
    INK_MUTED = "#9AA7BD"
    PRIMARY_BRIGHT = "#3B82F6"
    ACCENT = "#10B981"
    PLAYER_HOST = "#3B82F6"
    PLAYER_GUEST = "#F97316"
    DISPLAY_FONT = "Barlow Condensed"
    BODY_FONT = "Inter"

# ── Fonts ──
FONT_BOLD = DISPLAY_FONT
FONT_HEAVY = DISPLAY_FONT
FONT_REG = BODY_FONT

# ── Colors (mapped from @ppd/tokens) ──
HOST_COLOR = PLAYER_HOST
GUEST_COLOR = PLAYER_GUEST
GOLD = ACCENT
BG_TOP = BG_COLOR
BG_BOTTOM = "#1B263B"
PANEL_BG = "#162236"
TEXT_PRIMARY = INK
TEXT_SECONDARY = INK_MUTED
GRID_COLOR = "#2A3550"
ACCENT_BLUE = PRIMARY_BRIGHT

# ── Helpers ──

def make_background():
    """Navy gradient backdrop with subtle vignette."""
    bg = Rectangle(width=16, height=9, fill_color=BG_BOTTOM, fill_opacity=1, stroke_width=0)
    top_band = Rectangle(width=16, height=4.5, fill_color=BG_TOP, fill_opacity=0.7, stroke_width=0)
    top_band.to_edge(UP, buff=0)
    vignette = Rectangle(width=16, height=9, fill_color="#000000", fill_opacity=0.15, stroke_width=0)
    return VGroup(bg, top_band)


def make_title(text, color=TEXT_PRIMARY):
    """Broadcast-style uppercase condensed title with accent underline."""
    title = Text(text.upper(), font=FONT_HEAVY, font_size=36, color=color)
    underline = Rectangle(width=title.width + 0.4, height=0.06, fill_color=GOLD, fill_opacity=1, stroke_width=0)
    underline.next_to(title, DOWN, buff=0.12)
    return VGroup(title, underline)


def make_subtitle(text, color=TEXT_SECONDARY):
    """Smaller secondary text in regular weight."""
    return Text(text, font=FONT_REG, font_size=20, color=color)


def make_stat_chip(label, value, color, width=2.2):
    """Broadcast stat chip: label on top, big number below, colored border."""
    chip_bg = RoundedRectangle(
        width=width, height=1.1, corner_radius=0.1,
        fill_color=PANEL_BG, fill_opacity=0.9,
        stroke_color=color, stroke_width=1.5,
    )
    chip_label = Text(label.upper(), font=FONT_REG, font_size=13, color=TEXT_SECONDARY)
    chip_label.move_to(chip_bg.get_top() + DOWN * 0.22)
    chip_val = Text(str(value), font=FONT_HEAVY, font_size=32, color=color)
    chip_val.move_to(chip_bg.get_center() + DOWN * 0.1)
    return VGroup(chip_bg, chip_label, chip_val)


def make_player_name(name, color, font_size=36):
    """Player name in heavy condensed caps with color accent."""
    return Text(name.upper(), font=FONT_HEAVY, font_size=font_size, color=color)


def make_score_tile(score, color, width=1.2, height=1.2):
    """Rounded scoreboard tile with score number."""
    tile = RoundedRectangle(
        width=width, height=height, corner_radius=0.12,
        fill_color=PANEL_BG, fill_opacity=0.95,
        stroke_color=color, stroke_width=2,
    )
    num = Text(str(score), font=FONT_HEAVY, font_size=48, color=color)
    num.move_to(tile)
    return VGroup(tile, num)


def glow_dot(point, color, radius=0.06):
    """Dot with a soft glow halo."""
    halo = Dot(point, radius=radius * 2.5, color=color)
    halo.set_opacity(0.2)
    core = Dot(point, radius=radius, color=color)
    return VGroup(halo, core)


def fade_out_all(scene, run_time=0.8):
    """Fade out all mobjects smoothly."""
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)

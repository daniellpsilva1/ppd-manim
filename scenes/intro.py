"""Intro scene: broadcast-style title card with players, date, surface, and score reveal."""
import json
import os
from manim import *
from scenes.theme import *


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "match_boluda.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class IntroScene(Scene):
    def construct(self):
        data = load_data()
        match = data["match"]
        sets = data["sets"]
        host = match["host_player_names"][0]
        guest = match["guest_player_names"][0]
        surface = match["surface"]
        date = match["match_date"]

        self.add(make_background())

        # PPD branding
        ppd = Text("PEAK PERFORMANCE DATA", font=FONT_REG, font_size=16, color=TEXT_SECONDARY)
        ppd.to_corner(UL, buff=0.4)
        self.add(ppd)

        # Player names — sized to fit 16:9 frame
        host_name = make_player_name(host, HOST_COLOR, font_size=36)
        guest_name = make_player_name(guest, GUEST_COLOR, font_size=36)
        vs_badge = VGroup(
            Circle(radius=0.4, fill_color=PANEL_BG, fill_opacity=0.95, stroke_color=GOLD, stroke_width=2),
            Text("VS", font=FONT_HEAVY, font_size=22, color=GOLD),
        )
        vs_badge[1].move_to(vs_badge[0])

        players = VGroup(host_name, vs_badge, guest_name).arrange(RIGHT, buff=0.7)
        players.move_to(UP * 1.8)

        host_underline = Rectangle(width=host_name.width, height=0.08, fill_color=HOST_COLOR, fill_opacity=1, stroke_width=0)
        host_underline.next_to(host_name, DOWN, buff=0.08)
        guest_underline = Rectangle(width=guest_name.width, height=0.08, fill_color=GUEST_COLOR, fill_opacity=1, stroke_width=0)
        guest_underline.next_to(guest_name, DOWN, buff=0.08)

        info_text = Text(f"  {surface.upper()}  \u2022  {date}", font=FONT_REG, font_size=22, color=TEXT_SECONDARY)
        info_text.next_to(players, DOWN, buff=0.8)

        # Score tiles
        s1h, s1g = sets[0]["host_score"], sets[0]["guest_score"]
        s2h, s2g = sets[1]["host_score"], sets[1]["guest_score"]

        set1_tiles = VGroup(make_score_tile(s1h, HOST_COLOR), make_score_tile(s1g, GUEST_COLOR))
        set1_tiles.arrange(RIGHT, buff=0.3)
        set2_tiles = VGroup(make_score_tile(s2h, HOST_COLOR), make_score_tile(s2g, GUEST_COLOR))
        set2_tiles.arrange(RIGHT, buff=0.3)

        set_label_1 = Text("SET 1", font=FONT_REG, font_size=14, color=TEXT_SECONDARY)
        set_label_1.next_to(set1_tiles, UP, buff=0.1)
        set_label_2 = Text("SET 2", font=FONT_REG, font_size=14, color=TEXT_SECONDARY)
        set_label_2.next_to(set2_tiles, UP, buff=0.1)

        score_group = VGroup(
            VGroup(set_label_1, set1_tiles),
            VGroup(set_label_2, set2_tiles),
        ).arrange(RIGHT, buff=1.5)
        score_group.move_to(DOWN * 1.5)

        winner_banner = VGroup(
            RoundedRectangle(width=5, height=0.7, corner_radius=0.1, fill_color=HOST_COLOR, fill_opacity=0.15, stroke_color=GOLD, stroke_width=2),
            Text(f"{host.upper()} WINS", font=FONT_HEAVY, font_size=22, color=GOLD),
        )
        winner_banner[1].move_to(winner_banner[0])
        winner_banner.next_to(score_group, DOWN, buff=0.5)

        # Animations
        self.play(FadeIn(ppd), run_time=0.3)
        self.play(FadeIn(host_name, shift=RIGHT * 0.5), run_time=0.7)
        self.play(GrowFromCenter(host_underline), run_time=0.3)
        self.play(FadeIn(guest_name, shift=LEFT * 0.5), run_time=0.7)
        self.play(GrowFromCenter(guest_underline), run_time=0.3)
        self.play(GrowFromCenter(vs_badge), run_time=0.4)
        self.play(FadeIn(info_text, shift=UP * 0.2), run_time=0.5)
        self.wait(0.3)

        self.play(FadeIn(set_label_1), GrowFromEdge(set1_tiles[0], UP), GrowFromEdge(set1_tiles[1], UP), run_time=0.6)
        self.play(FadeIn(set_label_2), GrowFromEdge(set2_tiles[0], UP), GrowFromEdge(set2_tiles[1], UP), run_time=0.6)
        self.play(GrowFromCenter(winner_banner), run_time=0.6)
        self.wait(2)

        fade_out_all(self, 1.0)

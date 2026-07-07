"""Stats duel scene: mirrored head-to-head bar chart comparing key stats."""
import json
import os
from manim import *
from scenes.theme import *


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "match_boluda.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class StatsDuelScene(Scene):
    def construct(self):
        data = load_data()
        stats = data["stats"]
        match = data["match"]
        sets = data["sets"]
        host = match["host_player_names"][0]
        guest = match["guest_player_names"][0]

        self.add(make_background())

        title = make_title("Head-to-Head")
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Player labels (top corners)
        host_label = Text(host.upper(), font=FONT_HEAVY, font_size=24, color=HOST_COLOR)
        host_label.to_corner(UL, buff=1.0).shift(DOWN * 0.3)
        guest_label = Text(guest.upper(), font=FONT_HEAVY, font_size=24, color=GUEST_COLOR)
        guest_label.to_corner(UR, buff=1.0).shift(DOWN * 0.3)
        self.play(FadeIn(host_label), FadeIn(guest_label), run_time=0.4)

        def get_stat(player, name):
            for s in stats:
                if s["player"] == player and s["set_number"] == 0 and s["stat_name"] == name:
                    return s["stat_value"]
            return 0

        # 6 consolidated stats that fit on screen
        stat_names = [
            "Total Points Won",
            "Forehand Winners",
            "Backhand Winners",
            "Forehand Unforced Errors",
            "Backhand Unforced Errors",
            "Aces",
        ]

        stat_labels = [
            "POINTS WON",
            "FH WINNERS",
            "BH WINNERS",
            "FH ERRORS",
            "BH ERRORS",
            "ACES",
        ]

        host_vals = [get_stat("host", n) for n in stat_names]
        guest_vals = [get_stat("guest", n) for n in stat_names]

        max_val = max(max(host_vals), max(guest_vals), 1)
        bar_max_width = 3.0
        n_stats = len(stat_names)
        spacing = 1.1
        start_y = 2.0

        # Center divider line
        center_line = Line(UP * 3.0, DOWN * 3.0, stroke_color=GRID_COLOR, stroke_width=1.5)
        self.play(Create(center_line), run_time=0.3)

        # Build bars
        for i, (label, hv, gv) in enumerate(zip(stat_labels, host_vals, guest_vals)):
            y = start_y - i * spacing

            # Stat label ABOVE the bar pair (never overlapping)
            stat_text = Text(label, font=FONT_REG, font_size=14, color=TEXT_SECONDARY)
            stat_text.move_to(UP * y + UP * 0.35)

            # Minimum bar width so tiny values are still visible
            min_bar_w = 0.3
            h_width = max(hv / max_val * bar_max_width, min_bar_w if hv > 0 else 0)
            g_width = max(gv / max_val * bar_max_width, min_bar_w if gv > 0 else 0)

            # Host bar (extends LEFT from center)
            h_bar = Rectangle(
                width=h_width, height=0.38,
                fill_color=HOST_COLOR, fill_opacity=0.8, stroke_width=0,
            )
            h_bar.move_to(LEFT * h_width / 2 + UP * y)
            h_val_text = Text(str(int(hv)), font=FONT_HEAVY, font_size=18, color=HOST_COLOR)
            h_val_text.next_to(h_bar, LEFT, buff=0.12)

            # Guest bar (extends RIGHT from center)
            g_bar = Rectangle(
                width=g_width, height=0.38,
                fill_color=GUEST_COLOR, fill_opacity=0.8, stroke_width=0,
            )
            g_bar.move_to(RIGHT * g_width / 2 + UP * y)
            g_val_text = Text(str(int(gv)), font=FONT_HEAVY, font_size=18, color=GUEST_COLOR)
            g_val_text.next_to(g_bar, RIGHT, buff=0.12)

            self.play(
                FadeIn(stat_text),
                GrowFromEdge(h_bar, RIGHT),
                GrowFromEdge(g_bar, LEFT),
                FadeIn(h_val_text),
                FadeIn(g_val_text),
                run_time=0.4,
            )

        self.wait(1.0)

        # ── Winner card: full-screen final beat ──
        # Dim all existing content (use Group since some mobjects may not be VMobjects)
        from manim import Group
        to_dim = [m for m in self.mobjects if m is not title and m is not host_label and m is not guest_label]
        dim_group = Group(*to_dim)
        self.play(dim_group.animate.set_opacity(0.2), run_time=0.6)

        # Gold-trimmed winner banner
        winner_card = VGroup(
            RoundedRectangle(width=7, height=2.2, corner_radius=0.15, fill_color=PANEL_BG, fill_opacity=0.95, stroke_color=GOLD, stroke_width=3),
            Text("MATCH WINNER", font=FONT_REG, font_size=16, color=TEXT_SECONDARY),
            Text(host.upper(), font=FONT_HEAVY, font_size=36, color=HOST_COLOR),
            Text(f"{sets[0]['host_score']}-{sets[0]['guest_score']}  {sets[1]['host_score']}-{sets[1]['guest_score']}", font=FONT_HEAVY, font_size=24, color=GOLD),
        )
        winner_card[1].move_to(winner_card[0].get_top() + DOWN * 0.4)
        winner_card[2].next_to(winner_card[1], DOWN, buff=0.15)
        winner_card[3].next_to(winner_card[2], DOWN, buff=0.15)
        winner_card.move_to(ORIGIN)

        self.play(GrowFromCenter(winner_card), run_time=0.8)
        self.wait(2)

        fade_out_all(self, 1.0)

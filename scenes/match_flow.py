"""Match flow scene: point-by-point momentum timeline with score progression."""
import json
import os
from manim import *
from scenes.theme import *


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "match_boluda.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class MatchFlowScene(Scene):
    def construct(self):
        data = load_data()
        points = data["points"]
        sets = data["sets"]
        match = data["match"]
        host = match["host_player_names"][0]
        guest = match["guest_player_names"][0]

        self.add(make_background())

        title = make_title("Match Momentum")
        title.to_edge(UP, buff=0.35)
        self.add(title)

        # Compute running point differential (host - guest)
        n = len(points)
        diffs = []
        running = 0
        for p in points:
            if p["point_winner"] == "host":
                running += 1
            else:
                running -= 1
            diffs.append(running)

        max_abs = max(abs(max(diffs)), abs(min(diffs)), 10)
        ax_width = 12
        ax_height = 4.0
        ax = Axes(
            x_range=[0, n, n // 10],
            y_range=[-max_abs - 2, max_abs + 2, 5],
            x_length=ax_width,
            y_length=ax_height,
            axis_config={"color": GRID_COLOR, "stroke_width": 1.5, "font_size": 14, "color": TEXT_SECONDARY},
            tips=False,
        )
        ax.move_to(DOWN * 0.2)

        # Axis labels placed safely
        x_label = Text("POINT #", font=FONT_REG, font_size=14, color=TEXT_SECONDARY)
        x_label.next_to(ax, DOWN, buff=0.25)

        # Zero line
        zero_line = DashedLine(
            ax.c2p(0, 0), ax.c2p(n, 0),
            stroke_color="#555555", stroke_width=1.5,
        )

        # Player labels INSIDE chart zones (not below axis)
        host_label = Text(host.upper(), font=FONT_HEAVY, font_size=20, color=HOST_COLOR)
        host_label.move_to(ax.c2p(n * 0.03, max_abs * 0.75))
        guest_label = Text(guest.upper(), font=FONT_HEAVY, font_size=20, color=GUEST_COLOR)
        guest_label.move_to(ax.c2p(n * 0.03, -max_abs * 0.75))

        # Build ONE continuous momentum line (fixes the gap bug)
        line_points = [ax.c2p(0, 0)] + [ax.c2p(i + 1, diffs[i]) for i in range(n)]
        momentum_line = VMobject()
        momentum_line.set_points_smoothly(line_points)
        momentum_line.set_stroke(HOST_COLOR, width=3)

        # Set boundary markers
        set_boundaries = []
        prev_set = 1
        for i, p in enumerate(points):
            if p["set_number"] != prev_set:
                set_boundaries.append(i)
                prev_set = p["set_number"]

        # Break point markers
        break_points = []
        for i, p in enumerate(points):
            if p.get("break_point"):
                break_points.append(i)

        # ── Animate ──
        self.play(Create(ax), run_time=0.8)
        self.play(FadeIn(x_label), Create(zero_line), run_time=0.4)
        self.play(FadeIn(host_label), FadeIn(guest_label), run_time=0.3)

        # Draw the full momentum line in one go (no gaps!)
        self.play(Create(momentum_line), run_time=4.0, rate_func=linear)

        # Set boundary lines + labels (placed at top of chart, clear of player labels)
        for sb in set_boundaries:
            boundary = DashedLine(
                ax.c2p(sb, -max_abs - 2), ax.c2p(sb, max_abs + 2),
                stroke_color="#777777", stroke_width=1.5,
            )
            set_label = Text(f"SET {points[sb]['set_number']}", font=FONT_REG, font_size=14, color=GOLD)
            set_label.next_to(boundary, UP, buff=0.05)
            self.play(Create(boundary), FadeIn(set_label), run_time=0.4)

        # Break point dots (batch with LaggedStart)
        bp_dots = VGroup()
        for bp in break_points:
            bp_dot = glow_dot(ax.c2p(bp + 1, diffs[bp]), GOLD, radius=0.05)
            bp_dots.add(bp_dot)
        self.play(LaggedStart(*[FadeIn(d) for d in bp_dots], lag_ratio=0.1), run_time=1.0)

        # Final score annotation (bottom-right, clear of axis label)
        final_score = VGroup(
            Text("FINAL", font=FONT_REG, font_size=16, color=TEXT_SECONDARY),
            Text(f"{sets[0]['host_score']}-{sets[0]['guest_score']}", font=FONT_HEAVY, font_size=24, color=HOST_COLOR),
            Text(f"{sets[1]['host_score']}-{sets[1]['guest_score']}", font=FONT_HEAVY, font_size=24, color=HOST_COLOR),
        ).arrange(RIGHT, buff=0.3)
        final_score.to_corner(DR, buff=0.4)

        self.play(FadeIn(final_score, shift=LEFT * 0.2), run_time=0.5)
        self.wait(2)

        fade_out_all(self, 1.0)

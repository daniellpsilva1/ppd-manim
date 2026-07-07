"""Shot map scene: landscape court with filtered bounce dots colored by result."""
import json
import os
from manim import *
from scenes.theme import *
from scenes.court import TennisCourt, COURT_LENGTH, DOUBLES_WIDTH


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "match_boluda.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Colors for shot results
RESULT_COLORS = {
    "In": "#66BB6A",
    "Out": "#EF5350",
    "Net": "#FFA726",
    "Winner": GOLD,
    "Ace": "#EC407A",
}


class ShotMapScene(Scene):
    def construct(self):
        data = load_data()
        shots = data["shots"]
        match = data["match"]
        host = match["host_player_names"][0]
        guest = match["guest_player_names"][0]

        self.add(make_background())

        title = make_title("Shot Placement Map")
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Build court in PORTRAIT orientation (traditional tennis court view)
        court = TennisCourt(scale_factor=0.17, landscape=False)
        court.move_to(DOWN * 0.3)
        self.play(Create(court), run_time=1.2)

        # Player labels above/below court (portrait orientation)
        host_label = Text(host.upper(), font=FONT_HEAVY, font_size=18, color=HOST_COLOR)
        host_label.next_to(court, DOWN, buff=0.2)
        guest_label = Text(guest.upper(), font=FONT_HEAVY, font_size=18, color=GUEST_COLOR)
        guest_label.next_to(court, UP, buff=0.2)
        self.play(FadeIn(host_label), FadeIn(guest_label), run_time=0.4)

        # Filter shots: non-serve, has bounce coords, AND within court bounds +2m tolerance
        bounce_shots = []
        for s in shots:
            if s["stroke"] == "Serve":
                continue
            if s.get("bounce_x") is None or s.get("bounce_y") is None:
                continue
            bx = float(s["bounce_x"])
            by = float(s["bounce_y"])
            # Filter out shots more than 2m outside the court
            if abs(bx) > DOUBLES_WIDTH / 2 + 2:
                continue
            if abs(by) > COURT_LENGTH / 2 + 2:
                continue
            bounce_shots.append(s)

        # Sample for performance
        sample = bounce_shots[::3]

        # Animate bounces in batches
        batch_size = 12
        for i in range(0, len(sample), batch_size):
            batch = sample[i:i + batch_size]
            batch_dots = VGroup()
            for s in batch:
                bx = float(s["bounce_x"])
                by = float(s["bounce_y"])
                point = court.court_point(bx, by)
                result = s.get("result", "In")
                color = RESULT_COLORS.get(result, "#888888")
                player = s.get("player", "host")
                ring_color = HOST_COLOR if player == "host" else GUEST_COLOR

                dot = Dot(point, radius=0.045, color=color)
                dot.set_stroke(ring_color, width=1)
                batch_dots.add(dot)

            self.play(FadeIn(batch_dots), run_time=0.1)

        # Legend (bottom-right, clear of title and court)
        legend_items = [
            ("IN", "#66BB6A"),
            ("OUT", "#EF5350"),
            ("NET", "#FFA726"),
            ("WINNER", GOLD),
        ]
        legend = VGroup()
        for label_text, color in legend_items:
            chip = VGroup(
                Dot(radius=0.05, color=color),
                Text(label_text, font=FONT_REG, font_size=12, color=TEXT_PRIMARY),
            ).arrange(RIGHT, buff=0.1)
            legend.add(chip)
        legend.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        legend.to_corner(DR, buff=0.4)

        self.play(FadeIn(legend), run_time=0.4)

        # Stats counter (bottom-left, clear of court)
        total_shots = len(bounce_shots)
        in_count = sum(1 for s in bounce_shots if s["result"] == "In")
        in_pct = in_count / total_shots * 100 if total_shots else 0
        stats = VGroup(
            make_stat_chip("Shots", total_shots, TEXT_PRIMARY, width=1.8),
            make_stat_chip("In %", f"{in_pct:.0f}%", "#66BB6A", width=1.8),
        ).arrange(RIGHT, buff=0.3)
        stats.to_corner(DL, buff=0.4)
        self.play(FadeIn(stats), run_time=0.5)
        self.wait(2)

        fade_out_all(self, 1.0)

"""Serve scene: serve speed distribution and 1st/2nd serve win percentages."""
import json
import os
from manim import *
from scenes.theme import *


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "match_boluda.json")


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class ServeScene(Scene):
    def construct(self):
        data = load_data()
        shots = data["shots"]
        stats = data["stats"]
        match = data["match"]
        host = match["host_player_names"][0]
        guest = match["guest_player_names"][0]

        self.add(make_background())

        title = make_title("Serve Analysis")
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Extract serve speeds by player
        host_serves = [s for s in shots if s["stroke"] == "Serve" and s["player"] == "host" and s.get("speed_kmh")]
        guest_serves = [s for s in shots if s["stroke"] == "Serve" and s["player"] == "guest" and s.get("speed_kmh")]
        host_speeds = [float(s["speed_kmh"]) for s in host_serves]
        guest_speeds = [float(s["speed_kmh"]) for s in guest_serves]

        def get_stat(player, name):
            for s in stats:
                if s["player"] == player and s["set_number"] == 0 and s["stat_name"] == name:
                    return s["stat_value"]
            return 0

        # ── Left: Speed histogram with correct bar coordinates ──
        all_speeds = host_speeds + guest_speeds
        min_speed = int(min(all_speeds) // 10 * 10)
        max_speed = int(max(all_speeds) // 10 * 10 + 10)
        n_bins = 10
        bin_width = (max_speed - min_speed) / n_bins

        def histogram(speeds):
            bins = [0] * n_bins
            for sp in speeds:
                idx = min(int((sp - min_speed) / bin_width), n_bins - 1)
                bins[idx] += 1
            return bins

        host_bins = histogram(host_speeds)
        guest_bins = histogram(guest_speeds)
        max_count = max(max(host_bins), max(guest_bins), 1)

        hist_width = 5.5
        hist_height = 3.2
        ax = Axes(
            x_range=[min_speed, max_speed, 20],
            y_range=[0, max_count + 2, max(2, max_count // 3)],
            x_length=hist_width,
            y_length=hist_height,
            axis_config={"color": GRID_COLOR, "stroke_width": 1.5, "font_size": 14, "include_ticks": True},
            tips=False,
        )
        ax.to_edge(LEFT, buff=1.2).shift(UP * 0.2)

        x_label = Text("SPEED (km/h)", font=FONT_REG, font_size=14, color=TEXT_SECONDARY)
        x_label.next_to(ax, DOWN, buff=0.25)

        hist_title = Text("SPEED DISTRIBUTION", font=FONT_HEAVY, font_size=18, color=TEXT_PRIMARY)
        hist_title.next_to(ax, UP, buff=0.2)

        # Bars: use ax.c2p with DATA coordinates (not scene lengths)
        bar_w = bin_width * 0.35  # in data units
        host_bars = VGroup()
        guest_bars = VGroup()

        for i in range(n_bins):
            bin_center = min_speed + (i + 0.5) * bin_width

            h_val = host_bins[i]
            if h_val > 0:
                # Bar from y=0 to y=h_val, positioned at bin_center - offset
                h_bar = Rectangle(
                    width=bar_w * hist_width / (max_speed - min_speed),
                    height=h_val / (max_count + 2) * hist_height,
                    fill_color=HOST_COLOR, fill_opacity=0.75, stroke_width=0,
                )
                # Place using ax.c2p in data coords: bottom-left corner at (bin_center - bar_w/2, 0)
                bottom_left = ax.c2p(bin_center - bar_w / 2, 0)
                h_bar.move_to(bottom_left + RIGHT * h_bar.width / 2 + UP * h_bar.height / 2)
                host_bars.add(h_bar)

            g_val = guest_bins[i]
            if g_val > 0:
                g_bar = Rectangle(
                    width=bar_w * hist_width / (max_speed - min_speed),
                    height=g_val / (max_count + 2) * hist_height,
                    fill_color=GUEST_COLOR, fill_opacity=0.75, stroke_width=0,
                )
                bottom_left = ax.c2p(bin_center + bar_w / 2, 0)
                g_bar.move_to(bottom_left + RIGHT * g_bar.width / 2 + UP * g_bar.height / 2)
                guest_bars.add(g_bar)

        self.play(Create(ax), FadeIn(x_label), FadeIn(hist_title), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(h, DOWN) for h in host_bars], lag_ratio=0.05), run_time=1.0)
        self.play(LaggedStart(*[GrowFromEdge(g, DOWN) for g in guest_bars], lag_ratio=0.05), run_time=1.0)

        # ── Right: Serve win % panels ──
        right_x = 4.8

        serve_title = Text("SERVE WIN %", font=FONT_HEAVY, font_size=18, color=TEXT_PRIMARY)
        serve_title.move_to(RIGHT * right_x + UP * 2.8)

        self.play(FadeIn(serve_title), run_time=0.3)

        for player_label, player_key, color, y_offset in [
            (host, "host", HOST_COLOR, 1.8),
            (guest, "guest", GUEST_COLOR, -0.8),
        ]:
            first_in = get_stat(player_key, "1st Serves In")
            first_won = get_stat(player_key, "1st Serves Won")
            second_in = get_stat(player_key, "2nd Serves In")
            second_won = get_stat(player_key, "2nd Serves Won")

            first_pct = first_won / first_in * 100 if first_in > 0 else 0
            second_pct = second_won / second_in * 100 if second_in > 0 else 0

            # Player name
            name_text = Text(player_label.upper(), font=FONT_HEAVY, font_size=20, color=color)
            name_text.move_to(RIGHT * right_x + UP * y_offset)

            # 1st serve bar
            bar_total_w = 3.2
            first_bg = Rectangle(width=bar_total_w, height=0.28, fill_color=PANEL_BG, fill_opacity=0.8, stroke_width=0)
            first_bg.move_to(RIGHT * right_x + UP * (y_offset - 0.45))
            first_fill = Rectangle(
                width=bar_total_w * first_pct / 100, height=0.28,
                fill_color=color, fill_opacity=0.85, stroke_width=0,
            )
            first_fill.move_to(first_bg.get_left() + RIGHT * first_fill.width / 2)
            first_label = Text(f"1ST  {first_pct:.0f}%  ({first_won}/{first_in})", font=FONT_REG, font_size=14, color=TEXT_PRIMARY)
            first_label.next_to(first_bg, DOWN, buff=0.08)

            # 2nd serve bar
            second_bg = Rectangle(width=bar_total_w, height=0.28, fill_color=PANEL_BG, fill_opacity=0.8, stroke_width=0)
            second_bg.move_to(RIGHT * right_x + UP * (y_offset - 1.05))
            second_fill = Rectangle(
                width=bar_total_w * second_pct / 100, height=0.28,
                fill_color=color, fill_opacity=0.5, stroke_width=0,
            )
            second_fill.move_to(second_bg.get_left() + RIGHT * second_fill.width / 2)
            second_label = Text(f"2ND  {second_pct:.0f}%  ({second_won}/{second_in})", font=FONT_REG, font_size=14, color=TEXT_PRIMARY)
            second_label.next_to(second_bg, DOWN, buff=0.08)

            self.play(
                FadeIn(name_text),
                GrowFromEdge(first_fill, LEFT),
                FadeIn(first_bg),
                FadeIn(first_label),
                run_time=0.5,
            )
            self.play(
                GrowFromEdge(second_fill, LEFT),
                FadeIn(second_bg),
                FadeIn(second_label),
                run_time=0.5,
            )

        # ── Speed stat chips (under histogram, not overlapping) ──
        avg_host = sum(host_speeds) / len(host_speeds) if host_speeds else 0
        max_host = max(host_speeds) if host_speeds else 0
        avg_guest = sum(guest_speeds) / len(guest_speeds) if guest_speeds else 0
        max_guest = max(guest_speeds) if guest_speeds else 0

        speed_chips = VGroup(
            make_stat_chip("AVG", f"{avg_host:.0f}", HOST_COLOR, width=1.5),
            make_stat_chip("MAX", f"{max_host:.0f}", HOST_COLOR, width=1.5),
            make_stat_chip("AVG", f"{avg_guest:.0f}", GUEST_COLOR, width=1.5),
            make_stat_chip("MAX", f"{max_guest:.0f}", GUEST_COLOR, width=1.5),
        ).arrange(RIGHT, buff=0.25)
        speed_chips.next_to(ax, DOWN, buff=0.7)
        # Shift up slightly so it doesn't collide with x_label
        speed_chips.shift(UP * 0.1)

        # Add km/h unit label
        kmh_label = Text("km/h", font=FONT_REG, font_size=12, color=TEXT_SECONDARY)
        kmh_label.next_to(speed_chips, DOWN, buff=0.1)

        self.play(FadeIn(speed_chips), FadeIn(kmh_label), run_time=0.5)
        self.wait(2)

        fade_out_all(self, 1.0)

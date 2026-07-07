"""Master scene: stitches all sub-scenes into one continuous video."""
from manim import *
from scenes.intro import IntroScene
from scenes.match_flow import MatchFlowScene
from scenes.shot_map import ShotMapScene
from scenes.serve_scene import ServeScene
from scenes.stats_duel import StatsDuelScene


class TennisMatchVisualization(Scene):
    """Full match visualization — runs all scenes in sequence."""

    def construct(self):
        # Run each sub-scene's construct logic
        for scene_cls in [IntroScene, MatchFlowScene, ShotMapScene, ServeScene, StatsDuelScene]:
            scene_cls.construct(self)

# PPD Manim — Tennis Match Visualizations

Data-driven tennis match visualizations built with [Manim Community Edition](https://www.manim.community/).

## Current Video: Quevedo vs Boluda (2025-04-09, Clay)

A cinematic deep-dive into the match **Kaitlin Quevedo d. Ángela Boluda 6-1, 7-6** on clay, powered by SwingVision data exported from Supabase.

### Scenes

| Scene | Description |
|---|---|
| **Intro** | Title card with players, date, surface, and animated final score reveal |
| **Match Flow** | Point-by-point momentum timeline with break-point markers and set boundaries |
| **Shot Map** | To-scale clay court with streaming bounce-location dots colored by result |
| **Serve Analysis** | Serve-speed histogram + 1st/2nd serve win-percentage bars for both players |
| **Stats Duel** | Mirrored head-to-head bar chart comparing winners, errors, break points, aces |

### Data Source

All data is exported from the `PeakPerformanceDataV2` Supabase project (`tennis_matches` and related tables: `tennis_match_sets`, `tennis_match_points`, `tennis_match_shots`, `tennis_match_stats`). The export is stored as a static JSON file in `data/match_boluda.json` — no live database connection needed at render time.

## Setup

```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Manim
pip install -r requirements.txt
```

## Render

```bash
# Render the full video (low quality for quick preview)
manim -ql main.py TennisMatchVisualization

# High quality (1080p60)
manim -qh main.py TennisMatchVisualization

# Render individual scenes
manim -ql scenes/intro.py IntroScene
manim -ql scenes/match_flow.py MatchFlowScene
manim -ql scenes/shot_map.py ShotMapScene
manim -ql scenes/serve_scene.py ServeScene
manim -ql scenes/stats_duel.py StatsDuelScene
```

Output videos are written to `media/videos/`.

## Project Structure

```
Manim/
├── data/
│   └── match_boluda.json      # Exported match data from Supabase
├── scenes/
│   ├── court.py               # Reusable to-scale tennis court Mobject
│   ├── intro.py               # Title card scene
│   ├── match_flow.py          # Momentum timeline scene
│   ├── shot_map.py            # Bounce placement heatmap scene
│   ├── serve_scene.py         # Serve speed & win % scene
│   └── stats_duel.py          # Head-to-head stats comparison scene
├── export_data.py             # Script to assemble JSON from Supabase exports
├── main.py                    # Master scene stitching all sub-scenes
├── requirements.txt
└── README.md
```

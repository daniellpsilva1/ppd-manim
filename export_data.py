#!/usr/bin/env python3
"""Assemble match data from Supabase MCP query outputs into a clean JSON file."""
import json
import re
import os

TEMP_DIR = "/var/folders/57/jv1yg1hd6jg3bz_rmd0__vk00000gn/T/windsurf"

# Match header (from inline query result)
match_header = {
    "id": "f6cd7d61-fc69-4dfc-8336-2c90a4ced93a",
    "match_date": "2025-04-09",
    "opponent_name": "Ángela Boluda",
    "surface": "clay",
    "indoor": None,
    "total_sets": 2,
    "total_games": 20,
    "total_points": 136,
    "sets_per_match": 3,
    "games_per_set": 6,
    "has_ad_scoring": True,
    "has_match_tiebreak": False,
    "is_doubles": False,
    "tournament_name": None,
    "tournament_round": None,
    "source": "swingvision",
    "host_player_names": ["Kaitlin Quevedo"],
    "guest_player_names": ["Ángela Boluda"],
}

# Sets (from inline query result)
sets = [
    {"set_number": 1, "host_score": 6, "guest_score": 1, "host_tiebreak": 0, "guest_tiebreak": 0, "set_winner": "host", "duration_sec": None, "is_super_tiebreak": False},
    {"set_number": 2, "host_score": 7, "guest_score": 6, "host_tiebreak": 7, "guest_tiebreak": 2, "set_winner": "host", "duration_sec": None, "is_super_tiebreak": False},
]

# Stats (from inline query result)
stats_raw = [
    {"player":"guest","set_number":0,"stat_name":"1st Returns","stat_value":47},
    {"player":"guest","set_number":0,"stat_name":"1st Returns Won","stat_value":19},
    {"player":"guest","set_number":0,"stat_name":"1st Serves","stat_value":71},
    {"player":"guest","set_number":0,"stat_name":"1st Serves In","stat_value":45},
    {"player":"guest","set_number":0,"stat_name":"1st Serves Won","stat_value":25},
    {"player":"guest","set_number":0,"stat_name":"2nd Returns","stat_value":18},
    {"player":"guest","set_number":0,"stat_name":"2nd Returns Won","stat_value":8},
    {"player":"guest","set_number":0,"stat_name":"2nd Serves","stat_value":26},
    {"player":"guest","set_number":0,"stat_name":"2nd Serves In","stat_value":19},
    {"player":"guest","set_number":0,"stat_name":"2nd Serves Won","stat_value":7},
    {"player":"guest","set_number":0,"stat_name":"Aces","stat_value":2},
    {"player":"guest","set_number":0,"stat_name":"Backhand Unforced Errors","stat_value":16},
    {"player":"guest","set_number":0,"stat_name":"Backhand Winners","stat_value":3},
    {"player":"guest","set_number":0,"stat_name":"Break Point Opportunities","stat_value":10},
    {"player":"guest","set_number":0,"stat_name":"Break Points","stat_value":13},
    {"player":"guest","set_number":0,"stat_name":"Break Points Saved","stat_value":7},
    {"player":"guest","set_number":0,"stat_name":"Break Points Won","stat_value":4},
    {"player":"guest","set_number":0,"stat_name":"Forehand Unforced Errors","stat_value":22},
    {"player":"guest","set_number":0,"stat_name":"Forehand Winners","stat_value":8},
    {"player":"guest","set_number":0,"stat_name":"Service Winners","stat_value":1},
    {"player":"guest","set_number":0,"stat_name":"Set Points Saved","stat_value":2},
    {"player":"guest","set_number":0,"stat_name":"Set Points Won","stat_value":0},
    {"player":"guest","set_number":0,"stat_name":"Total Points","stat_value":136},
    {"player":"guest","set_number":0,"stat_name":"Total Points Won","stat_value":59},
    {"player":"guest","set_number":1,"stat_name":"1st Returns","stat_value":24},
    {"player":"guest","set_number":1,"stat_name":"1st Returns Won","stat_value":8},
    {"player":"guest","set_number":1,"stat_name":"1st Serves","stat_value":27},
    {"player":"guest","set_number":1,"stat_name":"1st Serves In","stat_value":17},
    {"player":"guest","set_number":1,"stat_name":"1st Serves Won","stat_value":8},
    {"player":"guest","set_number":1,"stat_name":"2nd Returns","stat_value":1},
    {"player":"guest","set_number":1,"stat_name":"2nd Returns Won","stat_value":1},
    {"player":"guest","set_number":1,"stat_name":"2nd Serves","stat_value":10},
    {"player":"guest","set_number":1,"stat_name":"2nd Serves In","stat_value":7},
    {"player":"guest","set_number":1,"stat_name":"2nd Serves Won","stat_value":2},
    {"player":"guest","set_number":1,"stat_name":"Backhand Unforced Errors","stat_value":4},
    {"player":"guest","set_number":1,"stat_name":"Backhand Winners","stat_value":2},
    {"player":"guest","set_number":1,"stat_name":"Break Point Opportunities","stat_value":3},
    {"player":"guest","set_number":1,"stat_name":"Break Points","stat_value":6},
    {"player":"guest","set_number":1,"stat_name":"Break Points Saved","stat_value":3},
    {"player":"guest","set_number":1,"stat_name":"Break Points Won","stat_value":1},
    {"player":"guest","set_number":1,"stat_name":"Forehand Unforced Errors","stat_value":9},
    {"player":"guest","set_number":1,"stat_name":"Forehand Winners","stat_value":3},
    {"player":"guest","set_number":1,"stat_name":"Service Winners","stat_value":1},
    {"player":"guest","set_number":1,"stat_name":"Total Points","stat_value":52},
    {"player":"guest","set_number":1,"stat_name":"Total Points Won","stat_value":19},
    {"player":"guest","set_number":2,"stat_name":"1st Returns","stat_value":23},
    {"player":"guest","set_number":2,"stat_name":"1st Returns Won","stat_value":11},
    {"player":"guest","set_number":2,"stat_name":"1st Serves","stat_value":44},
    {"player":"guest","set_number":2,"stat_name":"1st Serves In","stat_value":28},
    {"player":"guest","set_number":2,"stat_name":"1st Serves Won","stat_value":17},
    {"player":"guest","set_number":2,"stat_name":"2nd Returns","stat_value":17},
    {"player":"guest","set_number":2,"stat_name":"2nd Returns Won","stat_value":7},
    {"player":"guest","set_number":2,"stat_name":"2nd Serves","stat_value":16},
    {"player":"guest","set_number":2,"stat_name":"2nd Serves In","stat_value":12},
    {"player":"guest","set_number":2,"stat_name":"2nd Serves Won","stat_value":5},
    {"player":"guest","set_number":2,"stat_name":"Aces","stat_value":2},
    {"player":"guest","set_number":2,"stat_name":"Backhand Unforced Errors","stat_value":12},
    {"player":"guest","set_number":2,"stat_name":"Backhand Winners","stat_value":1},
    {"player":"guest","set_number":2,"stat_name":"Break Point Opportunities","stat_value":7},
    {"player":"guest","set_number":2,"stat_name":"Break Points","stat_value":7},
    {"player":"guest","set_number":2,"stat_name":"Break Points Saved","stat_value":4},
    {"player":"guest","set_number":2,"stat_name":"Break Points Won","stat_value":3},
    {"player":"guest","set_number":2,"stat_name":"Forehand Unforced Errors","stat_value":13},
    {"player":"guest","set_number":2,"stat_name":"Forehand Winners","stat_value":5},
    {"player":"guest","set_number":2,"stat_name":"Set Points Saved","stat_value":2},
    {"player":"guest","set_number":2,"stat_name":"Total Points","stat_value":84},
    {"player":"guest","set_number":2,"stat_name":"Total Points Won","stat_value":40},
    {"player":"host","set_number":0,"stat_name":"1st Returns","stat_value":45},
    {"player":"host","set_number":0,"stat_name":"1st Returns Won","stat_value":20},
    {"player":"host","set_number":0,"stat_name":"1st Serves","stat_value":65},
    {"player":"host","set_number":0,"stat_name":"1st Serves In","stat_value":47},
    {"player":"host","set_number":0,"stat_name":"1st Serves Won","stat_value":28},
    {"player":"host","set_number":0,"stat_name":"2nd Returns","stat_value":26},
    {"player":"host","set_number":0,"stat_name":"2nd Returns Won","stat_value":19},
    {"player":"host","set_number":0,"stat_name":"2nd Serves","stat_value":18},
    {"player":"host","set_number":0,"stat_name":"2nd Serves In","stat_value":13},
    {"player":"host","set_number":0,"stat_name":"2nd Serves Won","stat_value":10},
    {"player":"host","set_number":0,"stat_name":"Aces","stat_value":1},
    {"player":"host","set_number":0,"stat_name":"Backhand Forced Errors","stat_value":1},
    {"player":"host","set_number":0,"stat_name":"Backhand Unforced Errors","stat_value":12},
    {"player":"host","set_number":0,"stat_name":"Backhand Winners","stat_value":4},
    {"player":"host","set_number":0,"stat_name":"Break Point Opportunities","stat_value":13},
    {"player":"host","set_number":0,"stat_name":"Break Points","stat_value":10},
    {"player":"host","set_number":0,"stat_name":"Break Points Saved","stat_value":6},
    {"player":"host","set_number":0,"stat_name":"Break Points Won","stat_value":6},
    {"player":"host","set_number":0,"stat_name":"Distance Run (KM)","stat_value":0.520684},
    {"player":"host","set_number":0,"stat_name":"Forehand Forced Errors","stat_value":1},
    {"player":"host","set_number":0,"stat_name":"Forehand Unforced Errors","stat_value":15},
    {"player":"host","set_number":0,"stat_name":"Forehand Winners","stat_value":7},
    {"player":"host","set_number":0,"stat_name":"Service Winners","stat_value":6},
    {"player":"host","set_number":0,"stat_name":"Set Point Opportunities","stat_value":4},
    {"player":"host","set_number":0,"stat_name":"Set Points Won","stat_value":2},
    {"player":"host","set_number":0,"stat_name":"Total Points","stat_value":136},
    {"player":"host","set_number":0,"stat_name":"Total Points Won","stat_value":77},
    {"player":"host","set_number":1,"stat_name":"1st Returns","stat_value":17},
    {"player":"host","set_number":1,"stat_name":"1st Returns Won","stat_value":9},
    {"player":"host","set_number":1,"stat_name":"1st Serves","stat_value":25},
    {"player":"host","set_number":1,"stat_name":"1st Serves In","stat_value":24},
    {"player":"host","set_number":1,"stat_name":"1st Serves Won","stat_value":16},
    {"player":"host","set_number":1,"stat_name":"2nd Returns","stat_value":10},
    {"player":"host","set_number":1,"stat_name":"2nd Returns Won","stat_value":8},
    {"player":"host","set_number":1,"stat_name":"2nd Serves","stat_value":1},
    {"player":"host","set_number":1,"stat_name":"2nd Serves In","stat_value":0},
    {"player":"host","set_number":1,"stat_name":"2nd Serves Won","stat_value":0},
    {"player":"host","set_number":1,"stat_name":"Backhand Forced Errors","stat_value":1},
    {"player":"host","set_number":1,"stat_name":"Backhand Unforced Errors","stat_value":2},
    {"player":"host","set_number":1,"stat_name":"Break Point Opportunities","stat_value":6},
    {"player":"host","set_number":1,"stat_name":"Break Points","stat_value":3},
    {"player":"host","set_number":1,"stat_name":"Break Points Saved","stat_value":2},
    {"player":"host","set_number":1,"stat_name":"Break Points Won","stat_value":3},
    {"player":"host","set_number":1,"stat_name":"Forehand Forced Errors","stat_value":1},
    {"player":"host","set_number":1,"stat_name":"Forehand Unforced Errors","stat_value":5},
    {"player":"host","set_number":1,"stat_name":"Forehand Winners","stat_value":4},
    {"player":"host","set_number":1,"stat_name":"Service Winners","stat_value":5},
    {"player":"host","set_number":1,"stat_name":"Set Point Opportunities","stat_value":1},
    {"player":"host","set_number":1,"stat_name":"Set Points Won","stat_value":1},
    {"player":"host","set_number":1,"stat_name":"Total Points","stat_value":52},
    {"player":"host","set_number":1,"stat_name":"Total Points Won","stat_value":33},
    {"player":"host","set_number":2,"stat_name":"1st Returns","stat_value":28},
    {"player":"host","set_number":2,"stat_name":"1st Returns Won","stat_value":11},
    {"player":"host","set_number":2,"stat_name":"1st Serves","stat_value":40},
    {"player":"host","set_number":2,"stat_name":"1st Serves In","stat_value":23},
    {"player":"host","set_number":2,"stat_name":"1st Serves Won","stat_value":12},
    {"player":"host","set_number":2,"stat_name":"2nd Returns","stat_value":16},
    {"player":"host","set_number":2,"stat_name":"2nd Returns Won","stat_value":11},
    {"player":"host","set_number":2,"stat_name":"2nd Serves","stat_value":17},
    {"player":"host","set_number":2,"stat_name":"2nd Serves In","stat_value":13},
    {"player":"host","set_number":2,"stat_name":"2nd Serves Won","stat_value":10},
    {"player":"host","set_number":2,"stat_name":"Aces","stat_value":1},
    {"player":"host","set_number":2,"stat_name":"Backhand Unforced Errors","stat_value":10},
    {"player":"host","set_number":2,"stat_name":"Backhand Winners","stat_value":4},
    {"player":"host","set_number":2,"stat_name":"Break Point Opportunities","stat_value":7},
    {"player":"host","set_number":2,"stat_name":"Break Points","stat_value":7},
    {"player":"host","set_number":2,"stat_name":"Break Points Saved","stat_value":4},
    {"player":"host","set_number":2,"stat_name":"Break Points Won","stat_value":3},
    {"player":"host","set_number":2,"stat_name":"Distance Run (KM)","stat_value":0.520684},
    {"player":"host","set_number":2,"stat_name":"Forehand Unforced Errors","stat_value":10},
    {"player":"host","set_number":2,"stat_name":"Forehand Winners","stat_value":3},
    {"player":"host","set_number":2,"stat_name":"Service Winners","stat_value":1},
    {"player":"host","set_number":2,"stat_name":"Set Point Opportunities","stat_value":3},
    {"player":"host","set_number":2,"stat_name":"Set Points Won","stat_value":1},
    {"player":"host","set_number":2,"stat_name":"Total Points","stat_value":84},
    {"player":"host","set_number":2,"stat_name":"Total Points Won","stat_value":44},
]


def extract_json_from_temp(filepath):
    """Extract JSON array from MCP output temp file."""
    with open(filepath, "r") as f:
        outer = json.load(f)
    result_str = outer["result"]
    # Find the JSON array - it starts with [{"points": or [{"shots":
    for key in ("points", "shots"):
        marker = f'[{{"{key}":'
        idx = result_str.find(marker)
        if idx != -1:
            # Find the matching closing bracket - the array ends with }]
            # Work backwards from the end
            end_idx = result_str.rfind("}]")
            if end_idx != -1:
                json_str = result_str[idx:end_idx + 2]
                arr = json.loads(json_str)
                return arr[0][key]
    raise ValueError(f"Could not extract JSON from {filepath}")


def main():
    # Read points and shots from temp files
    points_file = os.path.join(TEMP_DIR, "mcp_output_637c68c3823480b0.txt")
    shots_file = os.path.join(TEMP_DIR, "mcp_output_53178afafdf55c82.txt")

    points = extract_json_from_temp(points_file)
    shots = extract_json_from_temp(shots_file)

    # Assemble final JSON
    match_data = {
        "match": match_header,
        "sets": sets,
        "points": points,
        "shots": shots,
        "stats": stats_raw,
    }

    output_path = os.path.join(os.path.dirname(__file__), "data", "match_boluda.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(match_data, f, indent=2, ensure_ascii=False)

    print(f"Written {output_path}")
    print(f"  Points: {len(points)}")
    print(f"  Shots: {len(shots)}")
    print(f"  Stats: {len(stats_raw)}")
    print(f"  Sets: {len(sets)}")


if __name__ == "__main__":
    main()

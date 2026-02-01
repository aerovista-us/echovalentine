import os
import json
from pathlib import Path

pack_name = "anti_love_blackpink"
pack_dir = Path("packs") / pack_name
audio_dir = pack_dir / "assets" / "audio"
tracks_json_path = pack_dir / "tracks.json"

# Rename mapping
rename_map = {
    "left-on-read-ritual-of-detach.mp3": "ritual_detach_1.mp3",
    "left-on-read-ritual-of-detach-2.mp3": "ritual_detach_2.mp3",
    "left-on-read-ritual-of-detach-3.mp3": "ritual_detach_3.mp3",
    "left-on-read-ritual-of-detach-alt.mp3": "ritual_detach_alt.mp3",
    "no-valentine-hype-funny.mp3": "no_hype_1.mp3",
    "no-valentine-hype-funny-2.mp3": "no_hype_2.mp3",
    "no-valentine-hype-funny-alt.mp3": "no_hype_alt.mp3",
    "left_on_read_ritual_of_detach.mp3": "ritual_detach_1.mp3",
    "left_on_read_ritual_of_detach_2.mp3": "ritual_detach_2.mp3",
    "left_on_read_ritual_of_detach_3.mp3": "ritual_detach_3.mp3",
    "left_on_read_ritual_of_detach_alt.mp3": "ritual_detach_alt.mp3",
    "no_valentine_hype__funny.mp3": "no_hype_1.mp3",
    "no_valentine_hype__funny_2.mp3": "no_hype_2.mp3",
    "no_valentine_hype__funny_alt.mp3": "no_hype_alt.mp3",
}

# New track definitions
new_tracks = [
    {
      "id": "ritual_detach_1",
      "title": "Ritual of Detachment",
      "src": "assets/audio/ritual_detach_1.mp3"
    },
    {
      "id": "ritual_detach_2",
      "title": "Ritual of Detachment 2",
      "src": "assets/audio/ritual_detach_2.mp3"
    },
    {
      "id": "ritual_detach_3",
      "title": "Ritual of Detachment 3",
      "src": "assets/audio/ritual_detach_3.mp3"
    },
    {
      "id": "ritual_detach_alt",
      "title": "Ritual of Detachment (Alt)",
      "src": "assets/audio/ritual_detach_alt.mp3"
    },
    {
      "id": "no_hype_1",
      "title": "No Hype",
      "src": "assets/audio/no_hype_1.mp3"
    },
    {
      "id": "no_hype_2",
      "title": "No Hype 2",
      "src": "assets/audio/no_hype_2.mp3"
    },
    {
      "id": "no_hype_alt",
      "title": "No Hype (Alt)",
      "src": "assets/audio/no_hype_alt.mp3"
    }
]

def main():
    # Rename files
    for old_name, new_name in rename_map.items():
        old_path = audio_dir / old_name
        new_path = audio_dir / new_name
        if old_path.exists():
            if not new_path.exists():
                old_path.rename(new_path)
                print(f"Renamed {old_path} to {new_path}")
            else:
                os.remove(old_path)
                print(f"Removed duplicate file {old_path}")


    # Update tracks.json
    with open(tracks_json_path, "w") as f:
        json.dump({"tracks": new_tracks}, f, indent=2)
    print(f"Updated {tracks_json_path}")

if __name__ == "__main__":
    main()

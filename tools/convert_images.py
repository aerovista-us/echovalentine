import os
import subprocess
import json
from pathlib import Path

# List of packs and their png files that need to be converted
packs_to_process = {
    "alien_crush": {
        "cards": [
            "assets/cards/ac-st-07.png",
            "assets/cards/ac-st-08.png",
        ],
        "stickers": [
            "assets/stickers/ac-st-07.png",
            "assets/stickers/ac-st-08.png",
        ]
    },
    "anti_love_blackpink": {
        "stickers": [
            "assets/stickers/nope_sticker.png",
            "assets/stickers/nope.png",
            "assets/stickers/nope2_sticker.png",
            "assets/stickers/nope2.png",
            "assets/stickers/single1.png",
            "assets/stickers/single2.png",
            "assets/stickers/single3.png",
            "assets/stickers/single4.png",
            "assets/stickers/single5.png",
            "assets/stickers/single6.png",
            "assets/stickers/sticker.pk.1/blender_sticker.png",
            "assets/stickers/sticker.pk.1/blender.png",
            "assets/stickers/sticker.pk.1/business.png",
            "assets/stickers/sticker.pk.1/business2.png",
            "assets/stickers/sticker.pk.1/business3.png",
            "assets/stickers/sticker.pk.1/business4.png",
            "assets/stickers/sticker.pk.1/business5.png",
            "assets/stickers/sticker.pk.1/business6.png",
            "assets/stickers/sticker.pk.1/business7.png",
            "assets/stickers/sticker.pk.1/business8.png",
            "assets/stickers/sticker.pk.1/microwave_sticker.png",
            "assets/stickers/sticker.pk.1/microwave.png",
            "assets/stickers/trash.png",
            "assets/stickers/trash1.png",
            "assets/stickers/trash2.png",
            "assets/stickers/trash3.png",
            "assets/stickers/trash4.png",
        ]
    },
    "arcade_love_90s": {
        "cards": [
            "assets/cards/alen_dude.png",
        ],
        "stickers": [
            "assets/stickers/kiss.png",
        ]
    }
}

def convert_image(png_path):
    """Converts a png image to webp."""
    webp_path = png_path.with_suffix(".webp")
    command = [
        "ffmpeg",
        "-i", str(png_path),
        str(webp_path)
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"Successfully converted {png_path} to {webp_path}")
        os.remove(png_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {png_path}: {e.stderr.decode()}")
        return False

def update_json_file(json_path, old_path, new_path):
    """Updates the json file to point to the new webp image."""
    with open(json_path, "r+") as f:
        content = f.read()
        new_content = content.replace(old_path, new_path)
        f.seek(0)
        f.write(new_content)
        f.truncate()


def main():
    packs_dir = Path("packs")
    for pack_name, files in packs_to_process.items():
        pack_dir = packs_dir / pack_name
        
        if "cards" in files:
            cards_json_path = pack_dir / "cards.json"
            for png_file in files["cards"]:
                png_path = pack_dir / png_file
                if png_path.exists():
                    if convert_image(png_path):
                        webp_file = png_path.with_suffix(".webp").name
                        update_json_file(cards_json_path, png_path.name, webp_file)

        if "stickers" in files:
            stickers_json_path = pack_dir / "stickers.json"
            for png_file in files["stickers"]:
                png_path = pack_dir / png_file
                if png_path.exists():
                    if convert_image(png_path):
                        webp_file = png_path.with_suffix(".webp").name
                        update_json_file(stickers_json_path, png_path.name, webp_file)

if __name__ == "__main__":
    main()

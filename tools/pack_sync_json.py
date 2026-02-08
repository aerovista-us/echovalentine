#!/usr/bin/env python3
"""
Sync JSON files to match actual media files on disk.
Removes references to missing files and adds references to existing files.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, List, Any

def get_card_image_path(card: Dict[str, Any], pack_dir: Path) -> Path | None:
    """Get the actual card image path from card data."""
    # Try different possible field names
    src = card.get("src") or card.get("front_svg") or card.get("front_webp") or card.get("image")
    if not src:
        return None
    return pack_dir / src

def scan_media_files(pack_dir: Path) -> Dict[str, List[str]]:
    """Scan pack directory for actual media files."""
    media = {
        "cards": [],
        "stickers": [],
        "tracks": [],
        "covers": []
    }
    
    assets_dir = pack_dir / "assets"
    if not assets_dir.exists():
        return media
    
    # Scan cards
    cards_dir = assets_dir / "cards"
    if cards_dir.exists():
        for ext in ["svg", "webp", "png", "jpg", "jpeg"]:
            for file in cards_dir.glob(f"*.{ext}"):
                rel_path = file.relative_to(pack_dir)
                media["cards"].append(str(rel_path).replace("\\", "/"))
    
    # Scan stickers
    stickers_dir = assets_dir / "stickers"
    if stickers_dir.exists():
        for ext in ["svg", "webp", "png", "jpg", "jpeg"]:
            for file in stickers_dir.glob(f"*.{ext}"):
                rel_path = file.relative_to(pack_dir)
                media["stickers"].append(str(rel_path).replace("\\", "/"))
    
    # Scan covers
    covers_dir = assets_dir / "covers"
    if covers_dir.exists():
        for ext in ["svg", "webp", "png", "jpg", "jpeg"]:
            for file in covers_dir.glob(f"*.{ext}"):
                rel_path = file.relative_to(pack_dir)
                media["covers"].append(str(rel_path).replace("\\", "/"))
    
    # Scan audio tracks
    audio_dir = pack_dir / "audio"
    if audio_dir.exists():
        tracks_dir = audio_dir / "tracks"
        if tracks_dir.exists():
            for ext in ["mp3", "ogg", "wav", "m4a"]:
                for file in tracks_dir.glob(f"*.{ext}"):
                    rel_path = file.relative_to(pack_dir)
                    media["tracks"].append(str(rel_path).replace("\\", "/"))
    
    # Also check old-style audio location
    audio_old = assets_dir / "audio"
    if audio_old.exists():
        for ext in ["mp3", "ogg", "wav", "m4a"]:
            for file in audio_old.glob(f"*.{ext}"):
                rel_path = file.relative_to(pack_dir)
                media["tracks"].append(str(rel_path).replace("\\", "/"))
    
    return media

def sync_cards_json(pack_dir: Path, media_files: List[str]) -> tuple[bool, List[str]]:
    """Update cards.json to match actual card files."""
    # Try both locations
    cards_json_path = pack_dir / "cards.json"
    if not cards_json_path.exists():
        cards_json_path = pack_dir / "cards" / "cards.json"
        if not cards_json_path.exists():
            return False, ["cards.json not found"]
    
    changes = []
    
    try:
        with open(cards_json_path, "r", encoding="utf-8") as f:
            cards_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    
    # Handle both array and object formats
    if isinstance(cards_data, list):
        cards = cards_data
        cards_data = {"cards": cards}
    else:
        cards = cards_data.get("cards", [])
    
    # Track which files are referenced
    referenced_files = set()
    cards_to_remove = []
    
    # Check existing cards
    for i, card in enumerate(cards):
        card_path = get_card_image_path(card, pack_dir)
        if card_path:
            file_str = str(card_path.relative_to(pack_dir)).replace("\\", "/")
            referenced_files.add(file_str)
            
            if not card_path.exists():
                cards_to_remove.append(i)
                changes.append(f"Removed card {card.get('id', 'unknown')}: missing file {file_str}")
        else:
            # Card has no image reference - try to find matching file
            card_id = card.get("id", "")
            if card_id:
                # Look for file with matching ID
                for media_file in media_files:
                    file_name = Path(media_file).stem
                    file_id = file_name.replace("-", "_").replace(" ", "_").lower()
                    if file_id.lower() == card_id.lower():
                        # Add src field
                        if not card.get("src") and not card.get("front_svg"):
                            card["src"] = media_file
                            referenced_files.add(media_file)
                            changes.append(f"Added src to card {card_id}: {media_file}")
                        break
    
    # Remove cards with missing files (in reverse order to maintain indices)
    for i in reversed(cards_to_remove):
        cards.pop(i)
    
    # Find cards that exist but aren't referenced
    for media_file in media_files:
        if media_file not in referenced_files:
            # Try to match by filename to existing card
            file_name = Path(media_file).stem
            file_id = file_name.replace("-", "_").replace(" ", "_").lower()
            
            # Look for existing card with matching ID
            matched = False
            for card in cards:
                if card.get("id", "").lower() == file_id.lower():
                    # Add src field to existing card
                    if not card.get("src") and not card.get("front_svg"):
                        card["src"] = media_file
                        changes.append(f"Added src to card {card.get('id')}: {media_file}")
                        matched = True
                        break
            
            if not matched:
                # Generate new card entry
                card_id = file_id
                
                # Check if ID already exists, add number if needed
                existing_ids = {c.get("id", "") for c in cards}
                original_id = card_id
                counter = 1
                while card_id in existing_ids:
                    card_id = f"{original_id}_{counter}"
                    counter += 1
                
                new_card = {
                    "id": card_id,
                    "title": file_name.replace("_", " ").replace("-", " ").title(),
                    "src": media_file
                }
                cards.append(new_card)
                changes.append(f"Added card {card_id}: {media_file}")
    
    # Update cards_data
    cards_data["cards"] = cards
    
    # Write back
    with open(cards_json_path, "w", encoding="utf-8") as f:
        json.dump(cards_data, f, indent=2, ensure_ascii=False)
    
    return True, changes

def sync_stickers_json(pack_dir: Path, media_files: List[str]) -> tuple[bool, List[str]]:
    """Update stickers.json to match actual sticker files."""
    stickers_json_path = pack_dir / "stickers.json"
    if not stickers_json_path.exists():
        return False, ["stickers.json not found"]
    
    changes = []
    
    try:
        with open(stickers_json_path, "r", encoding="utf-8") as f:
            stickers_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    
    # Handle both array and object formats
    if isinstance(stickers_data, list):
        stickers = stickers_data
        stickers_data = {"stickers": stickers}
    else:
        stickers = stickers_data.get("stickers", [])
    
    # Track which files are referenced
    referenced_files = set()
    stickers_to_remove = []
    
    # Check existing stickers
    for i, sticker in enumerate(stickers):
        src = sticker.get("src")
        if src:
            file_str = src if not os.path.isabs(src) else src
            if not file_str.startswith("/"):
                file_path = pack_dir / file_str
                referenced_files.add(file_str)
                
                if not file_path.exists():
                    stickers_to_remove.append(i)
                    changes.append(f"Removed sticker {sticker.get('id', 'unknown')}: missing file {file_str}")
    
    # Remove stickers with missing files (in reverse order)
    for i in reversed(stickers_to_remove):
        stickers.pop(i)
    
    # Find stickers that exist but aren't referenced
    for media_file in media_files:
        if media_file not in referenced_files:
            # Generate sticker entry
            file_name = Path(media_file).stem
            sticker_id = file_name.replace("-", "_").replace(" ", "_").lower()
            
            # Check if ID already exists
            existing_ids = {s.get("id", "") for s in stickers}
            original_id = sticker_id
            counter = 1
            while sticker_id in existing_ids:
                sticker_id = f"{original_id}_{counter}"
                counter += 1
            
            new_sticker = {
                "id": sticker_id,
                "name": file_name.replace("_", " ").replace("-", " ").title(),
                "src": media_file
            }
            stickers.append(new_sticker)
            changes.append(f"Added sticker {sticker_id}: {media_file}")
    
    # Update stickers_data
    stickers_data["stickers"] = stickers
    
    # Write back
    with open(stickers_json_path, "w", encoding="utf-8") as f:
        json.dump(stickers_data, f, indent=2, ensure_ascii=False)
    
    return True, changes

def sync_tracks_json(pack_dir: Path, media_files: List[str]) -> tuple[bool, List[str]]:
    """Update tracks.json to match actual track files."""
    tracks_json_path = pack_dir / "tracks.json"
    if not tracks_json_path.exists():
        return False, ["tracks.json not found"]
    
    changes = []
    
    try:
        with open(tracks_json_path, "r", encoding="utf-8") as f:
            tracks_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    
    # Handle both array and object formats
    if isinstance(tracks_data, list):
        tracks = tracks_data
        tracks_data = {"tracks": tracks}
    else:
        tracks = tracks_data.get("tracks", [])
    
    # Track which files are referenced
    referenced_files = set()
    tracks_to_remove = []
    
    # Check existing tracks
    for i, track in enumerate(tracks):
        src = track.get("src", "")
        
        # Check for empty src first
        if not src or not src.strip():
            tracks_to_remove.append(i)
            changes.append(f"Removed track {track.get('id', 'unknown')}: empty src field")
            continue
        
        file_str = src if not os.path.isabs(src) else src
        if not file_str.startswith("/"):
            file_path = pack_dir / file_str
            referenced_files.add(file_str)
            
            if not file_path.exists():
                tracks_to_remove.append(i)
                changes.append(f"Removed track {track.get('id', 'unknown')}: missing file {file_str}")
    
    # Remove tracks with missing files (in reverse order)
    for i in reversed(tracks_to_remove):
        tracks.pop(i)
    
    # Find tracks that exist but aren't referenced
    for media_file in media_files:
        if media_file not in referenced_files:
            # Generate track entry
            file_name = Path(media_file).stem
            track_id = file_name.replace("-", "_").replace(" ", "_").lower()
            
            # Check if ID already exists
            existing_ids = {t.get("id", "") for t in tracks}
            original_id = track_id
            counter = 1
            while track_id in existing_ids:
                track_id = f"{original_id}_{counter}"
                counter += 1
            
            new_track = {
                "id": track_id,
                "title": file_name.replace("_", " ").replace("-", " ").title(),
                "src": media_file
            }
            tracks.append(new_track)
            changes.append(f"Added track {track_id}: {media_file}")
    
    # Update tracks_data
    tracks_data["tracks"] = tracks
    
    # Write back
    with open(tracks_json_path, "w", encoding="utf-8") as f:
        json.dump(tracks_data, f, indent=2, ensure_ascii=False)
    
    return True, changes

def sync_pack(pack_dir: Path) -> Dict[str, Any]:
    """Sync all JSON files for a pack."""
    pack_id = pack_dir.name
    result = {
        "pack_id": pack_id,
        "success": True,
        "changes": {
            "cards": [],
            "stickers": [],
            "tracks": []
        },
        "errors": []
    }
    
    # Scan actual media files
    media = scan_media_files(pack_dir)
    
    # Sync cards
    success, changes = sync_cards_json(pack_dir, media["cards"])
    if success:
        result["changes"]["cards"] = changes
    else:
        result["errors"].extend(changes)
    
    # Sync stickers
    success, changes = sync_stickers_json(pack_dir, media["stickers"])
    if success:
        result["changes"]["stickers"] = changes
    else:
        result["errors"].extend(changes)
    
    # Sync tracks
    success, changes = sync_tracks_json(pack_dir, media["tracks"])
    if success:
        result["changes"]["tracks"] = changes
    else:
        result["errors"].extend(changes)
    
    return result

def main():
    """Sync all packs."""
    packs_dir = Path("packs")
    manifest_path = packs_dir / "manifest.json"
    
    if not manifest_path.exists():
        print("Error: packs/manifest.json not found")
        return 1
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    print("=" * 80)
    print("SYNC JSON FILES TO MATCH ACTUAL MEDIA")
    print("=" * 80)
    print()
    
    all_results = []
    
    for pack_entry in manifest["packs"]:
        pack_id = pack_entry["id"]
        pack_dir = packs_dir / pack_id
        
        if not pack_dir.exists():
            print(f"ERROR: Pack directory not found: {pack_id}")
            continue
        
        print(f"Syncing: {pack_id}...")
        result = sync_pack(pack_dir)
        all_results.append(result)
        
        # Print summary
        total_changes = (
            len(result["changes"]["cards"]) +
            len(result["changes"]["stickers"]) +
            len(result["changes"]["tracks"])
        )
        
        if total_changes > 0:
            print(f"  [UPDATED] {total_changes} changes")
            if result["changes"]["cards"]:
                print(f"    Cards: {len(result['changes']['cards'])} changes")
            if result["changes"]["stickers"]:
                print(f"    Stickers: {len(result['changes']['stickers'])} changes")
            if result["changes"]["tracks"]:
                print(f"    Tracks: {len(result['changes']['tracks'])} changes")
        else:
            print(f"  [OK] No changes needed")
        
        if result["errors"]:
            print(f"  [ERRORS] {len(result['errors'])}")
            for error in result["errors"]:
                print(f"    - {error}")
    
    print()
    print("=" * 80)
    print("SYNC COMPLETE")
    print("=" * 80)
    
    # Summary
    total_changes = sum(
        len(r["changes"]["cards"]) +
        len(r["changes"]["stickers"]) +
        len(r["changes"]["tracks"])
        for r in all_results
    )
    
    print(f"\nTotal changes: {total_changes}")
    print(f"Packs processed: {len(all_results)}")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

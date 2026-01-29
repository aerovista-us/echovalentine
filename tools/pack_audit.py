#!/usr/bin/env python3
"""
Comprehensive pack audit tool.
Checks for dummy data, fake tracks, compliance with v2 standard, and file naming conventions.
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict

# Dummy/placeholder patterns
DUMMY_PATTERNS = {
    "placeholder": [
        r"placeholder",
        r"dummy",
        r"test",
        r"sample",
        r"example",
        r"lorem",
        r"ipsum",
        r"optional",
        r"todo",
        r"tbd",
        r"coming soon",
        r"\[.*\]",  # Bracketed placeholders
    ],
    "empty": [
        r"^\s*$",
        r"^\(optional\)",
        r"^optional",
    ],
    "generic": [
        r"^card \d+$",
        r"^card_\d+$",
        r"^sticker \d+$",
        r"^track \d+$",
        r"^untitled",
        r"^no title",
        r"^no name",
    ]
}

# V2 Standard requirements
V2_REQUIREMENTS = {
    "cover_size": (800, 520),
    "card_format": ["svg", "webp"],
    "sticker_format": ["svg", "webp"],
    "audio_format": ["mp3"],
    "max_filename_length": 50,
    "required_fields": {
        "pack.json": ["id", "name"],
        "cards.json": ["cards"],
        "stickers.json": ["stickers"],
        "tracks.json": ["tracks"],
    }
}

def check_dummy_data(text: str, context: str = "") -> List[str]:
    """Check if text contains dummy/placeholder patterns."""
    issues = []
    text_lower = text.lower()
    
    for category, patterns in DUMMY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                issues.append(f"{category}: matches '{pattern}'")
    
    return issues

def check_filename(filename: str) -> Tuple[bool, List[str]]:
    """Check filename against v2 standards."""
    issues = []
    name = Path(filename).name
    
    # Check length
    if len(name) > V2_REQUIREMENTS["max_filename_length"]:
        issues.append(f"Filename too long ({len(name)} > {V2_REQUIREMENTS['max_filename_length']})")
    
    # Check for spaces (should use underscores)
    if " " in name:
        issues.append("Filename contains spaces (use underscores)")
    
    # Check for special characters
    if re.search(r'[^a-zA-Z0-9._-]', name):
        issues.append("Filename contains special characters")
    
    # Check for long DALLE-style names
    if len(name.split("_")) > 5:
        issues.append("Filename may be a long DALLE name (should be short)")
    
    return len(issues) == 0, issues

def audit_pack(pack_dir: Path) -> Dict[str, Any]:
    """Audit a single pack."""
    pack_id = pack_dir.name
    report = {
        "pack_id": pack_id,
        "errors": [],
        "warnings": [],
        "info": [],
        "structure": {},
        "dummy_data": [],
        "file_issues": [],
        "compliance": {
            "v2_structure": False,
            "v2_naming": False,
            "v2_formats": False,
        }
    }
    
    # Check pack.json exists
    pack_json_path = pack_dir / "pack.json"
    if not pack_json_path.exists():
        report["errors"].append("Missing pack.json")
        return report
    
    try:
        with open(pack_json_path, "r", encoding="utf-8") as f:
            pack_data = json.load(f)
    except json.JSONDecodeError as e:
        report["errors"].append(f"Invalid pack.json: {e}")
        return report
    
    # Check required fields
    for field in V2_REQUIREMENTS["required_fields"]["pack.json"]:
        if field not in pack_data:
            report["errors"].append(f"Missing required field in pack.json: {field}")
    
    # Check for dummy data in pack.json
    for key, value in pack_data.items():
        if isinstance(value, str):
            issues = check_dummy_data(value, f"pack.json.{key}")
            if issues:
                report["dummy_data"].append({
                    "file": "pack.json",
                    "field": key,
                    "value": value,
                    "issues": issues
                })
    
    # Check structure
    assets_dir = pack_dir / "assets"
    report["structure"]["has_assets_dir"] = assets_dir.exists()
    
    if assets_dir.exists():
        cards_dir = assets_dir / "cards"
        stickers_dir = assets_dir / "stickers"
        covers_dir = assets_dir / "covers"
        
        report["structure"]["has_cards_dir"] = cards_dir.exists()
        report["structure"]["has_stickers_dir"] = stickers_dir.exists()
        report["structure"]["has_covers_dir"] = covers_dir.exists()
        
        # Check cover
        cover_svg = covers_dir / "cover.svg" if covers_dir.exists() else None
        cover_webp = covers_dir / "cover.webp" if covers_dir.exists() else None
        
        if cover_svg and cover_svg.exists():
            report["structure"]["has_cover_svg"] = True
        elif cover_webp and cover_webp.exists():
            report["structure"]["has_cover_webp"] = True
        else:
            report["warnings"].append("No cover.svg or cover.webp found")
    
    # Check cards.json
    cards_json_path = pack_dir / "cards.json"
    if cards_json_path.exists():
        try:
            with open(cards_json_path, "r", encoding="utf-8") as f:
                cards_data = json.load(f)
            
            # Handle both array and object formats
            if isinstance(cards_data, list):
                cards = cards_data
            else:
                cards = cards_data.get("cards", [])
            report["structure"]["cards_count"] = len(cards)
            
            # Check each card
            for card in cards:
                # Check for dummy data
                for key, value in card.items():
                    if isinstance(value, str):
                        issues = check_dummy_data(value, f"cards.json.{card.get('id', 'unknown')}.{key}")
                        if issues:
                            report["dummy_data"].append({
                                "file": "cards.json",
                                "card_id": card.get("id", "unknown"),
                                "field": key,
                                "value": value,
                                "issues": issues
                            })
                
                # Check file references
                src = card.get("src") or card.get("front_svg") or card.get("front_webp")
                if src:
                    file_path = pack_dir / src
                    if not file_path.exists():
                        report["file_issues"].append(f"Card {card.get('id')}: Missing file {src}")
                    else:
                        # Check filename
                        valid, issues = check_filename(src)
                        if not valid:
                            report["file_issues"].append(f"Card {card.get('id')}: {', '.join(issues)}")
        except json.JSONDecodeError as e:
            report["errors"].append(f"Invalid cards.json: {e}")
    
    # Check stickers.json
    stickers_json_path = pack_dir / "stickers.json"
    if stickers_json_path.exists():
        try:
            with open(stickers_json_path, "r", encoding="utf-8") as f:
                stickers_data = json.load(f)
            
            # Handle both array and object formats
            if isinstance(stickers_data, list):
                stickers = stickers_data
            else:
                stickers = stickers_data.get("stickers", [])
            report["structure"]["stickers_count"] = len(stickers)
            
            # Check each sticker
            for sticker in stickers:
                # Check for dummy data
                for key, value in sticker.items():
                    if isinstance(value, str):
                        issues = check_dummy_data(value, f"stickers.json.{sticker.get('id', 'unknown')}.{key}")
                        if issues:
                            report["dummy_data"].append({
                                "file": "stickers.json",
                                "sticker_id": sticker.get("id", "unknown"),
                                "field": key,
                                "value": value,
                                "issues": issues
                            })
                
                # Check file references
                src = sticker.get("src")
                if src:
                    if not src or src.strip() == "":
                        report["dummy_data"].append({
                            "file": "stickers.json",
                            "sticker_id": sticker.get("id", "unknown"),
                            "field": "src",
                            "value": src,
                            "issues": ["Empty src field"]
                        })
                    else:
                        file_path = pack_dir / src
                        if not file_path.exists():
                            report["file_issues"].append(f"Sticker {sticker.get('id')}: Missing file {src}")
                        else:
                            # Check filename
                            valid, issues = check_filename(src)
                            if not valid:
                                report["file_issues"].append(f"Sticker {sticker.get('id')}: {', '.join(issues)}")
        except json.JSONDecodeError as e:
            report["errors"].append(f"Invalid stickers.json: {e}")
    
    # Check tracks.json
    tracks_json_path = pack_dir / "tracks.json"
    if tracks_json_path.exists():
        try:
            with open(tracks_json_path, "r", encoding="utf-8") as f:
                tracks_data = json.load(f)
            
            # Handle both array and object formats
            if isinstance(tracks_data, list):
                tracks = tracks_data
            else:
                tracks = tracks_data.get("tracks", [])
            
            report["structure"]["tracks_count"] = len(tracks)
            
            # Check each track
            for track in tracks:
                # Check for dummy data
                for key, value in track.items():
                    if isinstance(value, str):
                        issues = check_dummy_data(value, f"tracks.json.{track.get('id', 'unknown')}.{key}")
                        if issues:
                            report["dummy_data"].append({
                                "file": "tracks.json",
                                "track_id": track.get("id", "unknown"),
                                "field": key,
                                "value": value,
                                "issues": issues
                            })
                
                # Check file references
                src = track.get("src")
                if src:
                    if not src or src.strip() == "":
                        report["dummy_data"].append({
                            "file": "tracks.json",
                            "track_id": track.get("id", "unknown"),
                            "field": "src",
                            "value": src,
                            "issues": ["Empty src field (fake/placeholder track)"]
                        })
                    else:
                        file_path = pack_dir / src
                        if not file_path.exists():
                            report["file_issues"].append(f"Track {track.get('id')}: Missing file {src}")
                        else:
                            # Check filename
                            valid, issues = check_filename(src)
                            if not valid:
                                report["file_issues"].append(f"Track {track.get('id')}: {', '.join(issues)}")
                else:
                    # Track without src is suspicious
                    report["warnings"].append(f"Track {track.get('id')}: No src field")
        except json.JSONDecodeError as e:
            report["errors"].append(f"Invalid tracks.json: {e}")
    
    # V2 Compliance checks
    # Check structure compliance
    if (report["structure"].get("has_assets_dir") and 
        report["structure"].get("has_cards_dir") and
        report["structure"].get("has_covers_dir")):
        report["compliance"]["v2_structure"] = True
    else:
        report["warnings"].append("Does not match v2 folder structure")
    
    # Check naming compliance (no long filenames)
    if len(report["file_issues"]) == 0:
        report["compliance"]["v2_naming"] = True
    
    return report

def main():
    """Run audit on all packs."""
    packs_dir = Path("packs")
    manifest_path = packs_dir / "manifest.json"
    
    if not manifest_path.exists():
        print("Error: packs/manifest.json not found")
        return 1
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    all_reports = []
    summary = {
        "total_packs": len(manifest["packs"]),
        "packs_with_errors": 0,
        "packs_with_warnings": 0,
        "packs_with_dummy_data": 0,
        "packs_v2_compliant": 0,
        "total_dummy_items": 0,
        "total_file_issues": 0,
    }
    
    print("=" * 80)
    print("PACK AUDIT REPORT")
    print("=" * 80)
    print()
    
    for pack_entry in manifest["packs"]:
        pack_id = pack_entry["id"]
        pack_dir = packs_dir / pack_id
        
        if not pack_dir.exists():
            print(f"ERROR: Pack directory not found: {pack_id}")
            continue
        
        print(f"Auditing: {pack_id}...")
        report = audit_pack(pack_dir)
        all_reports.append(report)
        
        # Update summary
        if report["errors"]:
            summary["packs_with_errors"] += 1
        if report["warnings"]:
            summary["packs_with_warnings"] += 1
        if report["dummy_data"]:
            summary["packs_with_dummy_data"] += 1
        if all(report["compliance"].values()):
            summary["packs_v2_compliant"] += 1
        
        summary["total_dummy_items"] += len(report["dummy_data"])
        summary["total_file_issues"] += len(report["file_issues"])
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total packs: {summary['total_packs']}")
    print(f"Packs with errors: {summary['packs_with_errors']}")
    print(f"Packs with warnings: {summary['packs_with_warnings']}")
    print(f"Packs with dummy data: {summary['packs_with_dummy_data']}")
    print(f"V2 compliant packs: {summary['packs_v2_compliant']}")
    print(f"Total dummy/placeholder items: {summary['total_dummy_items']}")
    print(f"Total file issues: {summary['total_file_issues']}")
    print()
    
    # Detailed reports
    print("=" * 80)
    print("DETAILED REPORTS")
    print("=" * 80)
    print()
    
    for report in all_reports:
        print(f"\n{'=' * 80}")
        print(f"PACK: {report['pack_id']}")
        print(f"{'=' * 80}")
        
        if report["errors"]:
            print("\n[ERRORS]")
            for error in report["errors"]:
                print(f"  - {error}")
        
        if report["warnings"]:
            print("\n[WARNINGS]")
            for warning in report["warnings"]:
                print(f"  - {warning}")
        
        if report["dummy_data"]:
            print("\n[DUMMY/PLACEHOLDER DATA]")
            for item in report["dummy_data"]:
                print(f"  - {item['file']} -> {item.get('card_id') or item.get('sticker_id') or item.get('track_id', 'unknown')}.{item['field']}")
                print(f"    Value: '{item['value']}'")
                print(f"    Issues: {', '.join(item['issues'])}")
        
        if report["file_issues"]:
            print("\n[FILE ISSUES]")
            for issue in report["file_issues"]:
                print(f"  - {issue}")
        
        print(f"\nStructure: {report['structure']}")
        print(f"V2 Compliance: {report['compliance']}")
    
    # Save report to file
    report_path = Path("pack_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary,
            "reports": all_reports
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nFull report saved to: {report_path}")
    
    return 0 if summary["packs_with_errors"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())

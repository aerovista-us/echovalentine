#!/usr/bin/env python3
"""Simple pack audit script that analyzes SVGs and pack configs."""
import json
import os
import re
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / 'audit-results'
RESULTS_DIR.mkdir(exist_ok=True)

def load_manifest():
    manifest_path = Path(__file__).parent.parent / 'packs' / 'manifest.json'
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_pack(pack_id):
    pack_path = Path(__file__).parent.parent / 'packs' / pack_id / 'pack.json'
    if not pack_path.exists():
        raise FileNotFoundError(f"Pack file not found: {pack_path}")
    with open(pack_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_pack_data(pack_id):
    pack = load_pack(pack_id)
    base_path = Path(__file__).parent.parent / 'packs' / pack_id
    
    # Try different possible paths for cards.json
    possible_paths = [
        base_path / (pack.get('data', {}).get('cards', 'cards.json')),
        base_path / 'cards.json',
        base_path / 'assets' / 'cards' / 'cards.json',
        base_path / 'cards' / 'cards.json'
    ]
    
    cards_path = None
    for p in possible_paths:
        if p.exists():
            cards_path = p
            break
    
    if not cards_path:
        return {'pack': pack, 'cards': [], 'error': 'cards.json not found'}
    
    with open(cards_path, 'r', encoding='utf-8') as f:
        cards_raw = json.load(f)
    
    cards = cards_raw if isinstance(cards_raw, list) else cards_raw.get('cards', [])
    
    # Get first non-sticker card
    launch_cards = [c for c in cards if c and not any(
        x in str(c.get('id', '')).lower() or x in str(c.get('front_svg', c.get('src', ''))).lower()
        for x in ['-st-', '_st_', 'sticker']
    )]
    
    return {
        'pack': pack,
        'first_card': launch_cards[0] if launch_cards else (cards[0] if cards else None),
        'sample_cards': launch_cards[:3]
    }

def check_placeholder_in_svg(svg_path):
    if not svg_path.exists():
        return {'has_placeholder': False, 'error': 'SVG file not found'}
    
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        placeholder_patterns = [
            re.compile(r'To:\s*_{3,}', re.IGNORECASE),
            re.compile(r'From:\s*_{3,}', re.IGNORECASE),
            re.compile(r'To:\s*_{2,}\s*From:', re.IGNORECASE),
            re.compile(r'To:\s*_{8,}', re.IGNORECASE),
            re.compile(r'From:\s*_{8,}', re.IGNORECASE),
        ]
        
        found = any(pattern.search(svg_content) for pattern in placeholder_patterns)
        match = None
        if found:
            match_obj = re.search(r'To:.*?From:', svg_content, re.IGNORECASE)
            match = match_obj.group(0)[:100] if match_obj else None
        
        return {
            'has_placeholder': found,
            'svg_path': str(svg_path),
            'sample': match
        }
    except Exception as err:
        return {'has_placeholder': False, 'error': str(err)}

def analyze_svg_layout(svg_path):
    if not svg_path.exists():
        return None
    
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Extract text elements and their y positions
        text_matches = re.findall(r'<text[^>]*y="(\d+)"', svg_content)
        text_positions = [int(y) for y in text_matches]
        
        has_top_text = any(y < 200 for y in text_positions)
        has_middle_text = any(200 <= y < 400 for y in text_positions)
        has_bottom_text = any(y >= 500 for y in text_positions)
        
        return {
            'has_top_text': has_top_text,
            'has_middle_text': has_middle_text,
            'has_bottom_text': has_bottom_text,
            'text_positions': sorted(text_positions)
        }
    except Exception:
        return None

def audit_pack(pack_id, pack_data):
    results = {
        'pack_id': pack_id,
        'pack_name': pack_data['pack'].get('name', pack_id),
        'timestamp': str(Path().cwd()),
        'cards': [],
        'issues': [],
        'overlay_config': pack_data['pack'].get('overlay'),
        'recommendations': []
    }
    
    if not pack_data.get('first_card'):
        results['issues'].append('No launch cards found')
        return results
    
    base_path = Path(__file__).parent.parent / 'packs' / pack_id
    
    # Test each sample card
    cards_to_test = pack_data.get('sample_cards') or [pack_data['first_card']]
    for card in cards_to_test:
        card_id = card.get('id')
        card_src = card.get('front_svg') or card.get('src', '')
        svg_path = base_path / card_src if card_src else None
        
        placeholder_check = check_placeholder_in_svg(svg_path) if svg_path else {'has_placeholder': False, 'error': 'No SVG path'}
        layout = analyze_svg_layout(svg_path) if svg_path else None
        
        card_info = {
            'card_id': card_id,
            'card_title': card.get('title', card_id),
            'svg_path': card_src,
            'placeholder': placeholder_check,
            'layout': layout
        }
        
        results['cards'].append(card_info)
        
        if placeholder_check.get('has_placeholder'):
            results['issues'].append(f'Card {card_id} has placeholder text in SVG')
        
        if layout:
            if layout.get('has_bottom_text') and 'bottom-content' not in results['recommendations']:
                results['recommendations'].append('Has bottom text - may need To/From positioned higher')
            if layout.get('has_middle_text') and 'middle-content' not in results['recommendations']:
                results['recommendations'].append('Has middle text - message box may need adjustment')
    
    return results

def main():
    print('Starting pack audit (SVG analysis)...\n')
    
    manifest = load_manifest()
    packs = manifest.get('packs', [])
    
    print(f'Found {len(packs)} packs to audit\n')
    
    all_results = []
    
    for pack_entry in packs:
        pack_id = pack_entry['id']
        print(f'Auditing pack: {pack_id}')
        
        try:
            pack_data = load_pack_data(pack_id)
            result = audit_pack(pack_id, pack_data)
            all_results.append(result)
            
            if result['issues']:
                print(f'  ⚠️  Issues found: {len(result["issues"])}')
                for issue in result['issues']:
                    print(f'    - {issue}')
            if result['recommendations']:
                print(f'  💡 Recommendations: {len(result["recommendations"])}')
                for rec in result['recommendations']:
                    print(f'    - {rec}')
            if not result['issues'] and not result['recommendations']:
                print('  ✓ No issues found')
            print()
        except Exception as err:
            print(f'  ❌ Failed to audit {pack_id}: {err}')
            all_results.append({
                'pack_id': pack_id,
                'error': str(err),
                'timestamp': str(Path().cwd())
            })
    
    # Write JSON report
    report_path = RESULTS_DIR / 'audit-report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f'\nAudit complete! Report saved to: {report_path}')
    
    # Generate markdown summary
    markdown_path = RESULTS_DIR / 'audit-report.md'
    markdown = ['# Pack Overlay Audit Report (SVG Analysis)\n']
    markdown.append(f'Generated: {Path().cwd()}\n\n')
    markdown.append(f'Total packs audited: {len(all_results)}\n\n')
    
    packs_with_issues = [r for r in all_results if r.get('issues')]
    markdown.append('## Summary\n\n')
    markdown.append(f'- Packs with issues: {len(packs_with_issues)}\n')
    markdown.append(f'- Total issues found: {sum(len(r.get("issues", [])) for r in packs_with_issues)}\n\n')
    
    for result in all_results:
        markdown.append(f'## {result.get("pack_name", result.get("pack_id"))}\n\n')
        markdown.append(f'- **Pack ID**: {result["pack_id"]}\n')
        if result.get('overlay_config'):
            markdown.append('- **Has overlay config**: Yes\n')
        else:
            markdown.append('- **Has overlay config**: No (using defaults)\n')
        markdown.append(f'- **Cards tested**: {len(result.get("cards", []))}\n')
        markdown.append(f'- **Issues**: {len(result.get("issues", []))}\n')
        
        if result.get('issues'):
            markdown.append('\n### Issues:\n')
            for issue in result['issues']:
                markdown.append(f'- ⚠️ {issue}\n')
        
        if result.get('recommendations'):
            markdown.append('\n### Recommendations:\n')
            for rec in result['recommendations']:
                markdown.append(f'- 💡 {rec}\n')
        
        if result.get('cards'):
            markdown.append('\n### Card Details:\n')
            for card in result['cards']:
                markdown.append(f'- **{card.get("card_title", card.get("card_id"))}** ({card.get("card_id")})\n')
                if card.get('placeholder', {}).get('has_placeholder'):
                    markdown.append('  - ⚠️ Placeholder text found in SVG\n')
                layout = card.get('layout')
                if layout:
                    markdown.append('  - Layout: ')
                    layout_parts = []
                    if layout.get('has_top_text'):
                        layout_parts.append('top text')
                    if layout.get('has_middle_text'):
                        layout_parts.append('middle text')
                    if layout.get('has_bottom_text'):
                        layout_parts.append('bottom text')
                    markdown.append(', '.join(layout_parts) if layout_parts else 'no text elements detected')
                    markdown.append('\n')
        
        markdown.append('\n')
    
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(''.join(markdown))
    print(f'Markdown report saved to: {markdown_path}')

if __name__ == '__main__':
    main()

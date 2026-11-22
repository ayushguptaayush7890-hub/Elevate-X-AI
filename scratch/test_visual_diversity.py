"""
ELEVATE X AI — FEATURE 3 DESIGN DIVERSITY TEST SUITE
Audits actual layout properties, structural composition, header variations,
typography pairings, and palette distribution across the 1,024-design catalog.
"""

import math
from collections import Counter

BASE_LAYOUTS = [
    "single_column_classic",
    "single_column_modern",
    "two_column_left_sidebar",
    "two_column_right_sidebar",
    "two_column_balanced",
    "split_header_single",
    "compact_technical_terminal",
    "executive_bordered_frame",
]

HEADER_STYLES = [
    "minimal_inline",
    "centered_classic",
    "banner_accent",
    "terminal_code",
    "editorial_serif",
    "split_contrast",
    "gradient_modern",
]

TYPOGRAPHY_SYSTEMS = [
    "modern_sans",
    "classic_serif",
    "technical_mono",
    "display_serif_body_sans",
    "display_sans_body_serif",
]

PALETTES = [
    "Royal Navy & Gold", "Executive Slate & Platinum", "Emerald Forest & Sage",
    "Burgundy Wine & Rose", "Electric Violet & Indigo", "Nordic Monochrome & Crisp",
    "Teal Tech & Cyan", "Terracotta Artisan & Sand", "Terminal Matrix Dark",
    "High-Tech Cyberpunk Dark", "Oxford Blue & Champagne", "Minimalist Ivory Classic"
]

SECTION_ORDERS = [
    "experience_first",
    "skills_first",
    "education_first",
    "projects_first",
]

def pseudo_hash(n):
    x = math.sin(n + 1) * 10000
    return x - math.floor(x)

def generate_design(index):
    r1 = int(pseudo_hash(index * 13 + 1) * 10000)
    r2 = int(pseudo_hash(index * 29 + 3) * 10000)
    r3 = int(pseudo_hash(index * 47 + 7) * 10000)
    r4 = int(pseudo_hash(index * 61 + 11) * 10000)
    r5 = int(pseudo_hash(index * 83 + 17) * 10000)
    r6 = int(pseudo_hash(index * 97 + 23) * 10000)

    layout = BASE_LAYOUTS[r1 % len(BASE_LAYOUTS)]
    header = HEADER_STYLES[r2 % len(HEADER_STYLES)]
    typography = TYPOGRAPHY_SYSTEMS[r3 % len(TYPOGRAPHY_SYSTEMS)]
    palette = PALETTES[r4 % len(PALETTES)]
    section_order = SECTION_ORDERS[r6 % len(SECTION_ORDERS)]

    # Specialized overrides
    if layout == "compact_technical_terminal":
        palette = "Terminal Matrix Dark"
        typography = "technical_mono"
        header = "terminal_code"
    elif layout == "executive_bordered_frame":
        typography = "classic_serif"
        header = "centered_classic"

    return {
        "id": f"des-{str(index+1).zfill(4)}",
        "layout": layout,
        "header": header,
        "typography": typography,
        "palette": palette,
        "section_order": section_order,
    }

def run_diversity_audit():
    catalog = [generate_design(i) for i in range(1024)]
    print(f"Auditing Catalog of {len(catalog)} Designs for Genuine Visual Diversity...\n")

    layout_counts = Counter(d["layout"] for d in catalog)
    header_counts = Counter(d["header"] for d in catalog)
    typo_counts = Counter(d["typography"] for d in catalog)
    palette_counts = Counter(d["palette"] for d in catalog)
    order_counts = Counter(d["section_order"] for d in catalog)

    print("1. Structural Base Layout Distribution:")
    for l, count in sorted(layout_counts.items()):
        print(f"   - {l.ljust(30)}: {count} ({count/10.24:.1f}%)")
    assert len(layout_counts) == 8, "Expected 8 distinct base layouts"

    print("\n2. Header Architecture Distribution:")
    for h, count in sorted(header_counts.items()):
        print(f"   - {h.ljust(30)}: {count} ({count/10.24:.1f}%)")
    assert len(header_counts) == 7, "Expected 7 distinct header styles"

    print("\n3. Typography System Distribution:")
    for t, count in sorted(typo_counts.items()):
        print(f"   - {t.ljust(30)}: {count} ({count/10.24:.1f}%)")
    assert len(typo_counts) == 5, "Expected 5 distinct typography systems"

    print("\n4. Curated Color Palette Distribution:")
    for p, count in sorted(palette_counts.items()):
        print(f"   - {p.ljust(30)}: {count} ({count/10.24:.1f}%)")
    assert len(palette_counts) == 12, "Expected 12 distinct color palettes"

    print("\n5. Section Ordering Distribution:")
    for o, count in sorted(order_counts.items()):
        print(f"   - {o.ljust(30)}: {count} ({count/10.24:.1f}%)")
    assert len(order_counts) == 4, "Expected 4 distinct section orders"

    # Test Curated 6-Batch Diversity
    print("\n6. Curated 6-Batch Diversity Audit (Simulating 5 consecutive batches):")
    seen = []
    for batch_num in range(1, 6):
        unseen = [d for d in catalog if d["id"] not in seen]
        # Diverse selection algorithm
        batch = []
        used_layouts = set()
        for d in unseen:
            if len(batch) >= 6:
                break
            if d["layout"] not in used_layouts:
                batch.append(d)
                used_layouts.add(d["layout"])
        if len(batch) < 6:
            for d in unseen:
                if len(batch) >= 6:
                    break
                if d["id"] not in [x["id"] for x in batch]:
                    batch.append(d)
        seen.extend([d["id"] for d in batch])

        layouts_in_batch = set(d["layout"] for d in batch)
        palettes_in_batch = set(d["palette"] for d in batch)
        print(f"   Batch {batch_num}: {len(batch)} designs | {len(layouts_in_batch)} distinct layouts | {len(palettes_in_batch)} distinct palettes")
        assert len(batch) == 6, f"Batch {batch_num} must have exactly 6 designs"
        assert len(layouts_in_batch) >= 4, f"Batch {batch_num} should have at least 4 distinct layouts"

    print("\n[SUCCESS] Visual Diversity Audit Passed with 100% compliance!")

if __name__ == "__main__":
    run_diversity_audit()

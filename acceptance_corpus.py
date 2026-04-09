#!/usr/bin/env python3
"""
Extended acceptance corpus checks for Aether Forge.
Auto-generated rule bank to score markdown artifacts across many failure classes.
"""
from __future__ import annotations
import argparse, json, re
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class RuleResult:
    rule: str
    passed: bool
    value: float
    detail: str

def page_blocks(text: str) -> list[str]:
    return [b.strip() for b in re.split(r"\n\n+", text) if b.strip()]

def rule_001(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 1
    return RuleResult("rule_001", passed, float(val), "pipe density")

def rule_002(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_002", passed, float(val), "stat key continuity")

def rule_003(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_003", passed, float(val), "reading order continuity")

def rule_004(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_004", passed, float(val), "content block density")

def rule_005(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_005", passed, float(val), "glyph cleanliness")

def rule_006(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 6
    return RuleResult("rule_006", passed, float(val), "pipe density")

def rule_007(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_007", passed, float(val), "stat key continuity")

def rule_008(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_008", passed, float(val), "reading order continuity")

def rule_009(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_009", passed, float(val), "content block density")

def rule_010(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_010", passed, float(val), "glyph cleanliness")

def rule_011(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 4
    return RuleResult("rule_011", passed, float(val), "pipe density")

def rule_012(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_012", passed, float(val), "stat key continuity")

def rule_013(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_013", passed, float(val), "reading order continuity")

def rule_014(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_014", passed, float(val), "content block density")

def rule_015(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_015", passed, float(val), "glyph cleanliness")

def rule_016(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 2
    return RuleResult("rule_016", passed, float(val), "pipe density")

def rule_017(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_017", passed, float(val), "stat key continuity")

def rule_018(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_018", passed, float(val), "reading order continuity")

def rule_019(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_019", passed, float(val), "content block density")

def rule_020(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_020", passed, float(val), "glyph cleanliness")

def rule_021(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 0
    return RuleResult("rule_021", passed, float(val), "pipe density")

def rule_022(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_022", passed, float(val), "stat key continuity")

def rule_023(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_023", passed, float(val), "reading order continuity")

def rule_024(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_024", passed, float(val), "content block density")

def rule_025(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_025", passed, float(val), "glyph cleanliness")

def rule_026(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 5
    return RuleResult("rule_026", passed, float(val), "pipe density")

def rule_027(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_027", passed, float(val), "stat key continuity")

def rule_028(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_028", passed, float(val), "reading order continuity")

def rule_029(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_029", passed, float(val), "content block density")

def rule_030(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_030", passed, float(val), "glyph cleanliness")

def rule_031(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 3
    return RuleResult("rule_031", passed, float(val), "pipe density")

def rule_032(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_032", passed, float(val), "stat key continuity")

def rule_033(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_033", passed, float(val), "reading order continuity")

def rule_034(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_034", passed, float(val), "content block density")

def rule_035(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_035", passed, float(val), "glyph cleanliness")

def rule_036(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 1
    return RuleResult("rule_036", passed, float(val), "pipe density")

def rule_037(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_037", passed, float(val), "stat key continuity")

def rule_038(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_038", passed, float(val), "reading order continuity")

def rule_039(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_039", passed, float(val), "content block density")

def rule_040(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_040", passed, float(val), "glyph cleanliness")

def rule_041(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 6
    return RuleResult("rule_041", passed, float(val), "pipe density")

def rule_042(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_042", passed, float(val), "stat key continuity")

def rule_043(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_043", passed, float(val), "reading order continuity")

def rule_044(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_044", passed, float(val), "content block density")

def rule_045(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_045", passed, float(val), "glyph cleanliness")

def rule_046(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 4
    return RuleResult("rule_046", passed, float(val), "pipe density")

def rule_047(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_047", passed, float(val), "stat key continuity")

def rule_048(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_048", passed, float(val), "reading order continuity")

def rule_049(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_049", passed, float(val), "content block density")

def rule_050(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_050", passed, float(val), "glyph cleanliness")

def rule_051(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 2
    return RuleResult("rule_051", passed, float(val), "pipe density")

def rule_052(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_052", passed, float(val), "stat key continuity")

def rule_053(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_053", passed, float(val), "reading order continuity")

def rule_054(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_054", passed, float(val), "content block density")

def rule_055(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_055", passed, float(val), "glyph cleanliness")

def rule_056(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 0
    return RuleResult("rule_056", passed, float(val), "pipe density")

def rule_057(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_057", passed, float(val), "stat key continuity")

def rule_058(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_058", passed, float(val), "reading order continuity")

def rule_059(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_059", passed, float(val), "content block density")

def rule_060(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_060", passed, float(val), "glyph cleanliness")

def rule_061(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 5
    return RuleResult("rule_061", passed, float(val), "pipe density")

def rule_062(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_062", passed, float(val), "stat key continuity")

def rule_063(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_063", passed, float(val), "reading order continuity")

def rule_064(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_064", passed, float(val), "content block density")

def rule_065(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_065", passed, float(val), "glyph cleanliness")

def rule_066(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 3
    return RuleResult("rule_066", passed, float(val), "pipe density")

def rule_067(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_067", passed, float(val), "stat key continuity")

def rule_068(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_068", passed, float(val), "reading order continuity")

def rule_069(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_069", passed, float(val), "content block density")

def rule_070(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_070", passed, float(val), "glyph cleanliness")

def rule_071(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 1
    return RuleResult("rule_071", passed, float(val), "pipe density")

def rule_072(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_072", passed, float(val), "stat key continuity")

def rule_073(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_073", passed, float(val), "reading order continuity")

def rule_074(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_074", passed, float(val), "content block density")

def rule_075(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_075", passed, float(val), "glyph cleanliness")

def rule_076(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 6
    return RuleResult("rule_076", passed, float(val), "pipe density")

def rule_077(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_077", passed, float(val), "stat key continuity")

def rule_078(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_078", passed, float(val), "reading order continuity")

def rule_079(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_079", passed, float(val), "content block density")

def rule_080(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_080", passed, float(val), "glyph cleanliness")

def rule_081(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 4
    return RuleResult("rule_081", passed, float(val), "pipe density")

def rule_082(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_082", passed, float(val), "stat key continuity")

def rule_083(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_083", passed, float(val), "reading order continuity")

def rule_084(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_084", passed, float(val), "content block density")

def rule_085(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_085", passed, float(val), "glyph cleanliness")

def rule_086(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 2
    return RuleResult("rule_086", passed, float(val), "pipe density")

def rule_087(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_087", passed, float(val), "stat key continuity")

def rule_088(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_088", passed, float(val), "reading order continuity")

def rule_089(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_089", passed, float(val), "content block density")

def rule_090(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_090", passed, float(val), "glyph cleanliness")

def rule_091(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 0
    return RuleResult("rule_091", passed, float(val), "pipe density")

def rule_092(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_092", passed, float(val), "stat key continuity")

def rule_093(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_093", passed, float(val), "reading order continuity")

def rule_094(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_094", passed, float(val), "content block density")

def rule_095(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_095", passed, float(val), "glyph cleanliness")

def rule_096(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 5
    return RuleResult("rule_096", passed, float(val), "pipe density")

def rule_097(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_097", passed, float(val), "stat key continuity")

def rule_098(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_098", passed, float(val), "reading order continuity")

def rule_099(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_099", passed, float(val), "content block density")

def rule_100(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_100", passed, float(val), "glyph cleanliness")

def rule_101(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 3
    return RuleResult("rule_101", passed, float(val), "pipe density")

def rule_102(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_102", passed, float(val), "stat key continuity")

def rule_103(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_103", passed, float(val), "reading order continuity")

def rule_104(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_104", passed, float(val), "content block density")

def rule_105(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_105", passed, float(val), "glyph cleanliness")

def rule_106(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 1
    return RuleResult("rule_106", passed, float(val), "pipe density")

def rule_107(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_107", passed, float(val), "stat key continuity")

def rule_108(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_108", passed, float(val), "reading order continuity")

def rule_109(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_109", passed, float(val), "content block density")

def rule_110(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_110", passed, float(val), "glyph cleanliness")

def rule_111(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 6
    return RuleResult("rule_111", passed, float(val), "pipe density")

def rule_112(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_112", passed, float(val), "stat key continuity")

def rule_113(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_113", passed, float(val), "reading order continuity")

def rule_114(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_114", passed, float(val), "content block density")

def rule_115(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_115", passed, float(val), "glyph cleanliness")

def rule_116(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 4
    return RuleResult("rule_116", passed, float(val), "pipe density")

def rule_117(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_117", passed, float(val), "stat key continuity")

def rule_118(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_118", passed, float(val), "reading order continuity")

def rule_119(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_119", passed, float(val), "content block density")

def rule_120(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_120", passed, float(val), "glyph cleanliness")

def rule_121(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 2
    return RuleResult("rule_121", passed, float(val), "pipe density")

def rule_122(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_122", passed, float(val), "stat key continuity")

def rule_123(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_123", passed, float(val), "reading order continuity")

def rule_124(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_124", passed, float(val), "content block density")

def rule_125(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_125", passed, float(val), "glyph cleanliness")

def rule_126(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 0
    return RuleResult("rule_126", passed, float(val), "pipe density")

def rule_127(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_127", passed, float(val), "stat key continuity")

def rule_128(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_128", passed, float(val), "reading order continuity")

def rule_129(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_129", passed, float(val), "content block density")

def rule_130(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_130", passed, float(val), "glyph cleanliness")

def rule_131(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 5
    return RuleResult("rule_131", passed, float(val), "pipe density")

def rule_132(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_132", passed, float(val), "stat key continuity")

def rule_133(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_133", passed, float(val), "reading order continuity")

def rule_134(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_134", passed, float(val), "content block density")

def rule_135(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_135", passed, float(val), "glyph cleanliness")

def rule_136(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 3
    return RuleResult("rule_136", passed, float(val), "pipe density")

def rule_137(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_137", passed, float(val), "stat key continuity")

def rule_138(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_138", passed, float(val), "reading order continuity")

def rule_139(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_139", passed, float(val), "content block density")

def rule_140(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_140", passed, float(val), "glyph cleanliness")

def rule_141(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 1
    return RuleResult("rule_141", passed, float(val), "pipe density")

def rule_142(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 2
    return RuleResult("rule_142", passed, float(val), "stat key continuity")

def rule_143(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_143", passed, float(val), "reading order continuity")

def rule_144(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.2
    return RuleResult("rule_144", passed, float(val), "content block density")

def rule_145(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_145", passed, float(val), "glyph cleanliness")

def rule_146(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 6
    return RuleResult("rule_146", passed, float(val), "pipe density")

def rule_147(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 3
    return RuleResult("rule_147", passed, float(val), "stat key continuity")

def rule_148(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.5
    return RuleResult("rule_148", passed, float(val), "reading order continuity")

def rule_149(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.3
    return RuleResult("rule_149", passed, float(val), "content block density")

def rule_150(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_150", passed, float(val), "glyph cleanliness")

def rule_151(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 4
    return RuleResult("rule_151", passed, float(val), "pipe density")

def rule_152(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 0
    return RuleResult("rule_152", passed, float(val), "stat key continuity")

def rule_153(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.4
    return RuleResult("rule_153", passed, float(val), "reading order continuity")

def rule_154(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.4
    return RuleResult("rule_154", passed, float(val), "content block density")

def rule_155(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_155", passed, float(val), "glyph cleanliness")

def rule_156(text: str) -> RuleResult:
    val = text.count("|")
    passed = val >= 2
    return RuleResult("rule_156", passed, float(val), "pipe density")

def rule_157(text: str) -> RuleResult:
    val = len(re.findall(r"\b(armor class|hit points|saving throws|actions)\b", text.lower()))
    passed = val >= 1
    return RuleResult("rule_157", passed, float(val), "stat key continuity")

def rule_158(text: str) -> RuleResult:
    lines_local = [x for x in text.splitlines() if x.strip()]
    jumps = sum(1 for a,b in zip(lines_local, lines_local[1:]) if b.strip().startswith("#") and not a.strip().startswith("#") and len(a.strip()) < 15)
    val = max(0.0, 1.0 - jumps / max(1, len(lines_local)))
    passed = val >= 0.6
    return RuleResult("rule_158", passed, float(val), "reading order continuity")

def rule_159(text: str) -> RuleResult:
    blocks = page_blocks(text)
    val = sum(1 for b in blocks if len(b) > 120) / max(1, len(blocks))
    passed = val >= 0.5
    return RuleResult("rule_159", passed, float(val), "content block density")

def rule_160(text: str) -> RuleResult:
    bad = len(re.findall(r"\ufffd|\x00", text))
    val = max(0.0, 1.0 - bad / max(1, len(text)))
    passed = bad == 0
    return RuleResult("rule_160", passed, float(val), "glyph cleanliness")

RULES = [
    rule_001,
    rule_002,
    rule_003,
    rule_004,
    rule_005,
    rule_006,
    rule_007,
    rule_008,
    rule_009,
    rule_010,
    rule_011,
    rule_012,
    rule_013,
    rule_014,
    rule_015,
    rule_016,
    rule_017,
    rule_018,
    rule_019,
    rule_020,
    rule_021,
    rule_022,
    rule_023,
    rule_024,
    rule_025,
    rule_026,
    rule_027,
    rule_028,
    rule_029,
    rule_030,
    rule_031,
    rule_032,
    rule_033,
    rule_034,
    rule_035,
    rule_036,
    rule_037,
    rule_038,
    rule_039,
    rule_040,
    rule_041,
    rule_042,
    rule_043,
    rule_044,
    rule_045,
    rule_046,
    rule_047,
    rule_048,
    rule_049,
    rule_050,
    rule_051,
    rule_052,
    rule_053,
    rule_054,
    rule_055,
    rule_056,
    rule_057,
    rule_058,
    rule_059,
    rule_060,
    rule_061,
    rule_062,
    rule_063,
    rule_064,
    rule_065,
    rule_066,
    rule_067,
    rule_068,
    rule_069,
    rule_070,
    rule_071,
    rule_072,
    rule_073,
    rule_074,
    rule_075,
    rule_076,
    rule_077,
    rule_078,
    rule_079,
    rule_080,
    rule_081,
    rule_082,
    rule_083,
    rule_084,
    rule_085,
    rule_086,
    rule_087,
    rule_088,
    rule_089,
    rule_090,
    rule_091,
    rule_092,
    rule_093,
    rule_094,
    rule_095,
    rule_096,
    rule_097,
    rule_098,
    rule_099,
    rule_100,
    rule_101,
    rule_102,
    rule_103,
    rule_104,
    rule_105,
    rule_106,
    rule_107,
    rule_108,
    rule_109,
    rule_110,
    rule_111,
    rule_112,
    rule_113,
    rule_114,
    rule_115,
    rule_116,
    rule_117,
    rule_118,
    rule_119,
    rule_120,
    rule_121,
    rule_122,
    rule_123,
    rule_124,
    rule_125,
    rule_126,
    rule_127,
    rule_128,
    rule_129,
    rule_130,
    rule_131,
    rule_132,
    rule_133,
    rule_134,
    rule_135,
    rule_136,
    rule_137,
    rule_138,
    rule_139,
    rule_140,
    rule_141,
    rule_142,
    rule_143,
    rule_144,
    rule_145,
    rule_146,
    rule_147,
    rule_148,
    rule_149,
    rule_150,
    rule_151,
    rule_152,
    rule_153,
    rule_154,
    rule_155,
    rule_156,
    rule_157,
    rule_158,
    rule_159,
    rule_160,
]

def run_rules(text: str) -> list[RuleResult]:
    return [fn(text) for fn in RULES]

def scan_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    results = run_rules(text)
    passed = sum(1 for r in results if r.passed)
    return {
        "file": str(path),
        "rules_total": len(results),
        "rules_passed": passed,
        "rules_failed": len(results) - passed,
        "score": round(passed / max(1, len(results)), 4),
        "results": [asdict(r) for r in results],
    }

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extended acceptance corpus checks")
    p.add_argument("--input", required=True)
    p.add_argument("--glob", default="**/*.md")
    p.add_argument("--report", required=True)
    p.add_argument("--min_score", type=float, default=0.75)
    return p.parse_args()

def main() -> None:
    args = parse_args()
    inp = Path(args.input)
    if inp.is_file():
        files = [inp]
    else:
        files = [p for p in sorted(inp.glob(args.glob)) if p.is_file()]
    scanned = [scan_file(p) for p in files]
    avg_score = sum(x["score"] for x in scanned) / max(1, len(scanned))
    payload = {
        "files": len(scanned),
        "avg_score": round(avg_score, 4),
        "below_threshold": sum(1 for x in scanned if x["score"] < args.min_score),
        "scanned": scanned,
    }
    rp = Path(args.report)
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"files": payload["files"], "avg_score": payload["avg_score"]}, indent=2))
    if payload["below_threshold"] > 0:
        raise SystemExit(2)

if __name__ == "__main__":
    main()

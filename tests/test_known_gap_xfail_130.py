from __future__ import annotations

import pytest

from lorebook_splitter import detect_rule_like_blocks, detect_table_blocks, normalize_whitespace


@pytest.mark.xfail(
    strict=True,
    reason="Known Lane A gap: multi-column gear-table/D66 pages lose structured rows in native block-sorted extraction.",
)
def test_lane_a_multicolumn_gear_d66_table_should_canonicalize_rows():
    # Known gap: Lane A often emits table-like text that still needs robust row recovery/canonicalization.
    lane_a_like_text = normalize_whitespace(
        """
        <!-- PAGE:12 -->
        Gear Table (d66)
        d66  Item              Cost
        11   Rusted Lockpick   5 sp
        12   Coil of Wire      1 gp
        13   Glowcap Vial      8 sp
        14   Wrist Compass     2 gp
        """
    )

    table_blocks = detect_table_blocks(lane_a_like_text)

    # Desired future behavior: extracted D66 rows are canonicalized into stable, pipe-delimited table rows.
    assert any("| 11 | Rusted Lockpick | 5 sp |" in block for block in table_blocks)


@pytest.mark.xfail(
    strict=True,
    reason="Known lorebook splitter gap: D&D/fantasy-biased mechanics grammar misses non-fantasy rules phrasing.",
)
def test_lorebook_splitter_should_detect_non_fantasy_rules_grammar():
    # Known gap: rule detection currently overfits fantasy/TTRPG vocabulary and misses broader mechanics phrasing.
    cyberpunk_rules_para = (
        "When you breach a secured host, spend 1 bandwidth and roll 2d6 plus Interface. "
        "On 10+, choose two outcomes: stay undetected, exfiltrate data, or plant a backdoor."
    )

    hits = detect_rule_like_blocks(cyberpunk_rules_para, ttrpg_mode=False)

    # Desired future behavior: grammar like 'when you ... on 10+, choose ... outcomes' is recognized as rules text.
    assert hits == [cyberpunk_rules_para]

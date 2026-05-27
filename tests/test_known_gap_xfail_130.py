from __future__ import annotations

import pytest

from lorebook_splitter import detect_rule_like_blocks


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

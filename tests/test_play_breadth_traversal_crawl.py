"""#493 first post-baseline executable traversal-method vertical.

Crawl uses original R4-C movement commits, AFQR-18 route evidence and
AFQR-19 current opportunity. A declared synthetic low clearance admits
crawling under the moved Waystone while walking remains obstructed. No
universal morphology, stealth, posture or speed mechanics are inferred.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import replace

import pytest

from astra_runtime.myravant_play_fixture import (
    ORCHARD_PATH_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
    FixtureMovementMethodRoute, MyravantPlayFixtureError,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import execute_vsm14_follow_request
from astra_runtime.myravant_play_fixture import GROUNDSKEEPER_ID


def _establish_obstruction(app):
    # Real acquisition, light and physical Waystone relocation. The same
    # object ID is retained; no fixture shortcuts insert a fake blocker.
    assert app.pickup("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    dragged=app.displace_object("waystone","west",method="drag")
    assert dragged.authoritative_changed, dragged
    assert dragged.receipt_id and dragged.state_delta_id
    assert app.move("west").authoritative_changed
    assert app.current_place_id()==YARD_ID
    assert app.entity_place_id(WAYSTONE_ID)==YARD_ID
    return dragged


@pytest.mark.parametrize("raw,action,direction",[
    ("crawl south","move_crawl","south"),
    ("I crawl south","move_crawl","south"),
    ("crawl to the south exit","move_crawl","south"),
    ("crawl east","move_crawl","east"),
    ("walk south","move","south"),
    ("sprint south","unsupported",None),
    ("sneak south","unsupported",None),
    ("crawl south then move north","unsupported",None),
])
def test_crawl_parser_selects_method_without_synonym_success(raw,action,direction):
    parsed=parse_terminal_command(raw)
    assert parsed.action==action
    if direction is not None:
        assert parsed.argument==direction


def test_crawl_and_walk_use_same_owner_but_distinct_command_fingerprints():
    walk=MyravantVSM14Application.new()
    crawl=MyravantVSM14Application.new()
    a=walk.move("south")
    b=crawl.move("south",method="crawl")
    assert a.authoritative_changed and b.authoritative_changed
    assert walk.current_place_id()==crawl.current_place_id()==YARD_ID
    assert a.receipt_id!=b.receipt_id
    assert a.command_fingerprint!=b.command_fingerprint
    assert a.spatial_evidence_id and b.spatial_evidence_id
    assert a.opportunity_evidence_id!=b.opportunity_evidence_id
    assert "crawl" in b.message
    assert crawl.state.committed_transitions[-1].receipt.command_fingerprint==b.command_fingerprint
    assert walk.state.committed_transitions[-1].receipt.command_fingerprint==a.command_fingerprint


def test_fixture_rejects_nonexistent_crawl_corridor_or_bypass():
    app=MyravantVSM14Application.new()
    with pytest.raises(MyravantPlayFixtureError):
        replace(app.fixture, movement_method_routes=(
            FixtureMovementMethodRoute(
                source_place_id=WORKSHOP_ID, direction="west",
                method="crawl", bypass_obstruction=True,
            ),
        ))
    with pytest.raises(MyravantPlayFixtureError):
        replace(app.fixture, movement_method_routes=(
            FixtureMovementMethodRoute(
                source_place_id=WORKSHOP_ID, direction="south",
                method="crawl", bypass_obstruction=True,
            ),
        ))


def test_subclass_movement_contract_preserves_walk_follow_and_crawl_nontransfer():
    app=MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.current_place_id()==YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    agreement=execute_vsm14_follow_request(
        app,"ask groundskeeper to follow me"
    )
    assert agreement.result.authoritative_changed
    assert agreement.result.receipt_id

    # Default walking still invokes the preexisting co-present actor follower.
    walked=app.move("north")
    assert walked.result_type=="movement_committed"
    assert walked.authoritative_changed
    assert walked.consequence_receipt_id
    assert app.current_place_id()==WORKSHOP_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID)==WORKSHOP_ID

    # Follow intent does not invent the Groundskeeper's ability to crawl.
    crawled=app.move("south",method="crawl")
    assert crawled.result_type=="movement_committed"
    assert crawled.receipt_id
    assert crawled.consequence_receipt_id is None
    assert "cannot follow that traversal method" in crawled.message
    assert app.current_place_id()==YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID)==WORKSHOP_ID
    # Actor consent/intent remains independent and persistent.
    assert len(app.follow_intent_state.committed_transitions)==1


def test_move_override_seam_preserves_old_positional_walk_behavior():
    app=MyravantVSM14Application.new()
    positional=app.move("south")
    explicit=MyravantVSM14Application.new().move("south",method="walk")
    assert positional.result_type==explicit.result_type=="movement_committed"
    assert positional.receipt_id==explicit.receipt_id
    assert positional.command_fingerprint==explicit.command_fingerprint
    assert positional.opportunity_evidence_id==explicit.opportunity_evidence_id


def test_unlicensed_crawl_refused_even_when_normal_walk_is_open():
    app=MyravantVSM14Application.new()
    assert app.move("south",method="crawl").authoritative_changed
    before=app.authoritative_digest()
    refused=app.move("south",method="crawl")
    assert refused.failure_class=="traversal_method_opportunity_unavailable"
    assert not refused.authoritative_changed
    assert refused.pre_state_digest==refused.post_state_digest==before
    assert app.authoritative_digest()==before
    ordinary=app.move("south")
    assert ordinary.authoritative_changed  # Yard -> Gatehouse is still open


def test_method_discrimination_at_same_obstructed_corridor_with_checkpoint(tmp_path):
    checkpoint=tmp_path/"crawl.json"
    app=MyravantVSM14Application.new(checkpoint_path=checkpoint)
    dragging=_establish_obstruction(app)
    before=app.authoritative_digest()
    blocked=app.move("east")
    assert blocked.failure_class=="movement_opportunity_obstructed"
    assert blocked.pre_state_digest==blocked.post_state_digest==before
    assert app.authoritative_digest()==before

    passed=app.move("east",method="crawl")
    assert passed.authoritative_changed
    assert passed.result_type=="movement_committed"
    assert passed.receipt_id and passed.state_delta_id
    assert app.current_place_id()==ORCHARD_PATH_ID
    assert app.entity_place_id(WAYSTONE_ID)==YARD_ID
    assert "crawl" in passed.message
    assert app.save().checkpoint_digest

    restored=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert restored.entity_place_id(WAYSTONE_ID)==YARD_ID
    assert restored.current_place_id()==ORCHARD_PATH_ID
    assert restored.state.committed_transitions[-1].receipt.command_fingerprint==passed.command_fingerprint
    assert dragging.receipt_id and passed.receipt_id
    assert dragging.receipt_id!=passed.receipt_id


def test_method_constraint_reacts_to_real_obstruction_removal():
    app=MyravantVSM14Application.new()
    _establish_obstruction(app)
    # The player clears the route via the original physical owner.
    removed=app.displace_object("waystone","north",method="push")
    assert removed.authoritative_changed
    assert app.entity_place_id(WAYSTONE_ID)==WORKSHOP_ID
    walked=app.move("east")
    assert walked.authoritative_changed
    assert app.current_place_id()==ORCHARD_PATH_ID


def test_refusal_does_not_alias_unqualified_speed_stealth_or_body_form():
    app=MyravantVSM14Application.new()
    before=app.authoritative_digest()
    for method in ("sprint","sneak","fly","crawl quickly"):
        rejected=app.move("south",method=method)
        assert rejected.failure_class=="traversal_method_unavailable"
        assert rejected.pre_state_digest==rejected.post_state_digest==before
        assert app.authoritative_digest()==before


def test_repeat_history_deterministic_and_no_unattested_consequences():
    outcomes=[]
    for _ in range(2):
        app=MyravantVSM14Application.new()
        _establish_obstruction(app)
        blocked=app.move("east")
        moved=app.move("east",method="crawl")
        outcomes.append((
            blocked.failure_class,moved.receipt_id,
            moved.command_fingerprint,moved.opportunity_evidence_id,
            app.authoritative_digest(),
        ))
    assert outcomes[0]==outcomes[1]


def test_two_session_installed_terminal_exercises_crawl_then_recovery(tmp_path):
    checkpoint=tmp_path/"crawl-terminal.json"
    def play(cmds,*args):
        return subprocess.run(
            [sys.executable,"-m","astra_runtime.myravant_terminal",*args],
            input="\n".join((*cmds,"exit","")),text=True,capture_output=True,
            timeout=120,
        )
    first=play(("crawl south",), "--checkpoint",str(checkpoint))
    assert first.returncode==0,(first.stdout,first.stderr)
    assert "crawl through to the Yard" in first.stdout
    assert checkpoint.is_file()
    loaded=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert loaded.current_place_id()==YARD_ID
    second=play(("crawl south","walk south","look"),"--load",str(checkpoint))
    assert second.returncode==0,(second.stdout,second.stderr)
    assert "no qualified clearance" in second.stdout
    final=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert final.current_place_id()!=YARD_ID


def test_baseline_real_installed_cases_distinguish_crawl_and_sneak(tmp_path):
    from scripts.report_myravant_action_coverage import CASES, run_baseline
    cases=tuple(c for c in CASES if c.case_id in {"M01","M02","M03","M04"})
    assert len(cases)==4
    summary=run_baseline(output=tmp_path/"movement-methods.json",cases=cases)
    lookup={x["case_id"]:x for x in summary["cases"]}
    assert lookup["M01"]["outcome"]=="executed"
    assert lookup["M04"]["outcome"]=="executed"
    assert lookup["M04"]["parsed_action"]=="move_crawl"
    assert lookup["M02"]["outcome"]=="unsupported_novelty"
    assert lookup["M03"]["outcome"]=="unsupported_novelty"

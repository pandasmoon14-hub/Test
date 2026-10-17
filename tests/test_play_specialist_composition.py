"""#536: existing specialist meaning survives two-step interpretation and restart."""
from __future__ import annotations

import io
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from astra_runtime.myravant_terminal import (
    _explicit_two_step_intent, _execute_composable_core_step,
    parse_terminal_command, run_terminal,
)
from astra_runtime.myravant_terminal_capabilities import (
    BOUNDED_TERMINAL_ROUTES, classify_bounded_terminal_request,
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application as App
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID, ORCHARD_PATH_ID,
)

COMMON = ('take lantern', 'light lantern', 'go south', 'wait', 'drop lantern')
OBSTRUCTION = (*COMMON, 'go east', 'drag waystone west', 'go west')
# One actual grammar representative per specialist family, not synonym counts.
FAMILIES = (
    ('chest_investigation_goal', 'investigate chest with groundskeeper by asking for a firsthand sighting', COMMON),
    ('chest_readiness_goal', 'prepare chest for transport by manual service', COMMON),
    ('orchard_supply_goal', 'supply orchard with lantern by carrying', (*COMMON, 'take lantern')),
    ('destination_goal_method', 'get lantern to orchard by pushing', COMMON),
    ('physical_placement_goal', 'get waystone to workshop by pushing', OBSTRUCTION),
    ('player_sensory_attempt', 'check my hands', COMMON),
    ('actor_service', 'ask groundskeeper to repair chest latch with lantern', COMMON),
    ('fixture_duty', 'ask groundskeeper to secure chest latch later', (*COMMON, 'service chest latch', 'service chest latch', 'close chest')),
    ('fixture_brace', 'loosen chest brace', COMMON),
    ('actor_situated_investigation', 'ask groundskeeper to inspect chest', COMMON),
    ('waystone_clearance', 'clear waystone route', OBSTRUCTION),
    ('fixture_service', 'service chest latch', COMMON),
    ('bounded_work', 'prepare lantern for yard', ()),
    ('cooperative_delivery_goal', 'ask groundskeeper to bring lantern to orchard', COMMON),
    ('institutional_petition', 'ask the town council for a charter', COMMON),
    ('situated_inquiry', 'ask groundskeeper what are you carrying', COMMON),
    ('large3_actor_mediated_ground_contact', 'ask groundskeeper to push chest east', COMMON),
    ('vsm14_persistent_follow_intent', 'ask groundskeeper to follow me', COMMON),
    ('vsm13_actor_mediated_displacement', 'ask groundskeeper to throw lantern east', (*COMMON, 'ask groundskeeper to pick up lantern')),
    ('vsm12_actor_mediated_custody', 'ask groundskeeper to pick up lantern', COMMON),
    ('vsm11_actor_mediated_storage', 'ask groundskeeper to put lantern in chest', (*COMMON, 'open chest', 'ask groundskeeper to pick up lantern')),
    ('vsm10_actor_mediated_movement', 'ask groundskeeper to go to gatehouse', COMMON),
    ('vsm9_actor_mediated', 'ask groundskeeper to extinguish lantern', COMMON),
)
CORE_ACTORS = (
    ('handoff', 'give lantern to groundskeeper', (*COMMON, 'take lantern')),
    ('request_handoff', 'ask groundskeeper for lantern', (*COMMON, 'ask groundskeeper to pick up lantern')),
    ('request_object_state', 'ask groundskeeper to open chest', COMMON),
)


def play(path, trace, commands, *, load=False):
    exe = shutil.which('myravant-play')
    assert exe, 'installed launcher required'
    args = [exe, '--checkpoint', str(path), '--trace', str(trace), '--repository-sha', 'a' * 40]
    if load:
        args += ['--load', str(path)]
    proc = subprocess.run(args, input='\n'.join((*commands, 'save', 'exit', '')),
                          capture_output=True, text=True, timeout=90)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    records = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
    assert records[-1]['record_type'] == 'session_end' and records[-1]['evidence_complete']
    rows = [r for r in records if r['record_type'] == 'interaction'][:-1]
    for a, b in zip(rows, rows[1:]):
        assert a['post_state_digest'] == b['pre_state_digest']
    app = App.restore(checkpoint_path=path)
    assert rows[-1]['post_state_digest'] == app.authoritative_digest()
    return proc, rows, app


def test_family_inventory_is_complete_for_current_installed_router():
    assert len(FAMILIES) == len(BOUNDED_TERMINAL_ROUTES) == 23
    assert {row[0] for row in FAMILIES} == BOUNDED_TERMINAL_ROUTES


@pytest.mark.parametrize('route,raw,setup', FAMILIES + CORE_ACTORS)
def test_preflight_is_pure_and_keeps_standalone_precedence(route, raw, setup, monkeypatch):
    import astra_runtime.myravant_terminal_capabilities as capabilities
    def forbidden(*args, **kwargs):
        pytest.fail('preflight called an executor')
    for name in vars(capabilities):
        if name.startswith('execute_'):
            monkeypatch.setattr(capabilities, name, forbidden)
    app = App.new()
    before = app.authoritative_digest()
    plan = _explicit_two_step_intent('inspect self then ' + raw, fixture=app.fixture)
    assert plan is not None
    assert plan[1].action == ('player_sense' if route == 'player_sensory_attempt' else route)
    assert plan[1].raw_text == raw
    assert app.authoritative_digest() == before
    assert classify_bounded_terminal_request(raw, fixture=app.fixture) == (
        route if route in BOUNDED_TERMINAL_ROUTES else None)


@pytest.mark.parametrize('route,raw,setup', FAMILIES + CORE_ACTORS)
def test_installed_family_receipts_refusals_and_restored_outcomes_match_standalone(tmp_path, route, raw, setup):
    _, a, direct = play(tmp_path / 'direct.json', tmp_path / 'direct.jsonl', (*setup, raw))
    _, b, sequence = play(tmp_path / 'sequence.json', tmp_path / 'sequence.jsonl', (*setup, 'inspect self then ' + raw))
    last_a, last_b = a[-1], b[-1]
    expected = 'player_sense' if route == 'player_sensory_attempt' else route
    assert last_a['parsed_action'] == route
    assert last_b['parsed_action'] == 'sequence_2_' + expected
    for key in ('result_type', 'failure_class', 'authoritative_changed', 'receipt_id',
                'command_fingerprint', 'pre_state_digest', 'post_state_digest'):
        assert last_a.get(key) == last_b.get(key), (route, key, last_a, last_b)
    assert last_b['raw_player_input'] == 'inspect self then ' + raw + '\n'
    assert direct.authoritative_digest() == sequence.authoritative_digest()
    # Only the existing institutional refusal is deliberately unexecutable.
    if route == 'institutional_petition':
        assert last_b['failure_class'] and not last_b['authoritative_changed']
    else:
        assert last_b['failure_class'] is None, (route, last_b)


def test_inspect_component_collision_uses_original_specialist_owner(tmp_path):
    out, rows, app = play(tmp_path / 'brace.json', tmp_path / 'brace.jsonl',
                          ('go south', 'crouch then inspect chest brace'))
    assert rows[-1]['parsed_action'] == 'sequence_2_fixture_brace'
    assert rows[-1]['result_type'] == 'fixture_brace_status' and rows[-1]['failure_class'] is None
    assert app.posture_state.configuration == 'crouching' and app.brace_state.condition == 'attached'
    assert 'Recorded posture is now crouching' in out.stdout or 'recorded posture is now crouching' in out.stdout


def test_first_step_changes_second_actor_opportunity_and_preserves_partial_commit(tmp_path):
    # Original VSM movement may accept departure. It grants no subsequent remote dialogue.
    out, rows, app = play(tmp_path / 'depart.json', tmp_path / 'depart.jsonl',
                          (*COMMON, 'ask groundskeeper to go to gatehouse then ask groundskeeper to inspect chest'))
    assert rows[-2]['authoritative_changed'] and rows[-2]['receipt_id']
    assert rows[-1]['failure_class'] == 'actor_knowledge_actor_not_local'
    assert not rows[-1]['authoritative_changed'] and 'Sequence halted' in out.stdout
    assert app.entity_place_id(GROUNDSKEEPER_ID) != app.current_place_id()
    assert not app.knowledge_state.events


def test_first_refusal_cancels_later_core_change(tmp_path):
    out, rows, app = play(tmp_path / 'remote.json', tmp_path / 'remote.jsonl',
                          ('ask groundskeeper to inspect chest then crouch',))
    assert len(rows) == 1 and rows[0]['failure_class'] == 'actor_knowledge_actor_not_local'
    assert not app.posture_state.events and 'Sequence halted' in out.stdout


@pytest.mark.parametrize('raw', [
    'crouch then invent wings', 'service chest latch then cast a spell',
    'ask groundskeeper to inspect chest then save',
    'service chest latch while inspecting chest',
    'service chest latch then inspect chest then wait',
    'ask groundskeeper to follow me and then go north',
])
def test_unknown_unsupported_or_extra_step_prevents_all_execution(raw):
    app = App.new()
    before = app.authoritative_digest()
    assert _explicit_two_step_intent(raw, fixture=app.fixture) is None
    assert app.authoritative_digest() == before


def test_legacy_handoff_now_composes_with_resource_use_and_restart(tmp_path):
    path = tmp_path / 'handoff.json'
    _, rows, app = play(path, tmp_path / 'handoff.jsonl',
                        (*COMMON, 'ask groundskeeper to pick up lantern',
                         'open chest then ask groundskeeper for lantern'))
    # This exact utterance was excluded by the earlier core-only batch.
    assert all(r['receipt_id'] and r['authoritative_changed'] for r in rows[-2:])
    assert [r['parsed_action'] for r in rows[-2:]] == ['sequence_1_open', 'sequence_2_request_handoff']
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id() == YARD_ID
    assert 'Brass Lantern' in app.inspect('self').view.description
    _, rows, app = play(path, tmp_path / 'handoff-restored.jsonl',
                        ('give lantern to groundskeeper then ask groundskeeper what are you carrying',), load=True)
    assert rows[-2]['authoritative_changed'] and not rows[-1]['authoritative_changed']
    assert 'Brass Lantern' in rows[-1]['player_visible_output']
    assert 'Carrying: nothing' in app.inspect('self').view.description


def test_service_then_duty_remains_a_voluntary_delayed_world_consequence(tmp_path):
    path = tmp_path / 'duty.json'
    _, rows, app = play(path, tmp_path / 'duty.jsonl',
                        ('go south', 'service chest latch then service chest latch',
                         'close chest then ask groundskeeper to secure chest latch later'))
    assert app.service_state.progress == 2 and app.duty_state.status == 'pending'
    _, rows, app = play(path, tmp_path / 'duty-restored.jsonl', ('go north then wait',), load=True)
    assert app.current_place_id() == WORKSHOP_ID
    assert app.duty_state.status == 'fulfilled' and app.service_state.secured
    assert app.duty_state.events[-1].service_receipt_id


def test_specialist_write_failure_closes_before_ack_or_second_action(tmp_path, monkeypatch):
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointWriteError
    app = App.new(checkpoint_path=tmp_path / 'fault.json')
    app.move('south')
    app.save()
    prior = app.checkpoint_path.read_bytes()
    def fail():
        raise PersistentWorldCheckpointWriteError('injected failure')
    monkeypatch.setattr(app, 'save', fail)
    out = io.StringIO()
    with pytest.raises(SystemExit) as failure:
        run_terminal(app, input_stream=io.StringIO('loosen chest brace then crouch\n'),
                     output_stream=out, specialized_router=execute_bounded_terminal_request)
    assert failure.value.code == 3 and 'durably acknowledged' in out.getvalue()
    assert 'loosened' not in out.getvalue() and not app.posture_state.events
    assert app.checkpoint_path.read_bytes() == prior
    restored = App.restore(checkpoint_path=app.checkpoint_path)
    assert restored.brace_state.condition == 'attached'

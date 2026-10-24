"""Four repeatable installed #561 journeys with actual restored state predicates."""
import argparse
from pathlib import Path
import shutil
import tempfile

from _myravant_evidence_runner import (
    assert_repeat_digest_equality, resolve_repository_sha, run_installed_session,
    trace_rows, write_json_report,
)
from astra_runtime.domain.persistent_world_material import active_effects
from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_tarrow_structures import create_structures_fixture, cover_subjects
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_actor_participation import selected

CASES = ("reconfigure", "cover", "actor", "alternate")


def run_case(folder, case, sha):
    launcher = shutil.which("myravant-play")
    assert launcher, "Installed myravant-play is required for retained journey evidence"
    folder.mkdir()
    save = folder / "campaign.json"
    variant = "cross-workshop" if case == "alternate" else "standard"
    fixture = create_structures_fixture(structures_case=variant)
    application = None
    stages = []
    initial_count = None

    def play(*commands):
        nonlocal application, initial_count
        trace = folder / f"{len(stages):02}.jsonl"
        result = run_installed_session(
            launcher, ("--locality", "tarrow-structures", "--structures-case", variant),
            save, trace, sha, commands, load=save.exists(), timeout=100,
        )
        assert result.returncode == 0, (case, commands, result.stdout, result.stderr)
        events = trace_rows(trace)
        assert events and events[-1].get("evidence_complete") is True
        restored = StructuresApplication.restore(fixture=fixture, checkpoint_path=save)
        if application is not None:
            assert restored.journal[:len(application.journal)] == application.journal
        count = (sum(v for _, v in restored.water_state.water) +
                 sum(v for _, v in restored.environment_state.evaporated),
                 sum(v for _, v in restored.water_state.adhered) +
                 sum(v for _, v in restored.water_state.suspended) +
                 sum(v for _, v in restored.environment_state.deposits))
        if initial_count is None:
            initial_count = count
        assert count == initial_count
        application = restored
        stages.append(dict(commands=commands, time=len(restored.intervals),
                           journal_length=len(restored.journal), digest=restored.authoritative_digest(),
                           tally=(count[0], str(count[1])), trace=str(trace),
                           output=result.stdout[-800:]))
    build = ("go south", "go west",
             "take work panel", "put work panel on yard work trestle",
             "take barrier crossbar", "put barrier crossbar on yard work trestle",
             "take work cord", "tie work panel to barrier crossbar using work cord")
    cover = ("go south", "go west",
             "take barrier crossbar", "put barrier crossbar on yard work trestle",
             "take cover cloth", "put cover cloth on yard work trestle",
             "take cover tie", "tie cover cloth to barrier crossbar using cover tie")
    goals = {}
    if case in {"reconfigure", "alternate"}:
        play(*build)
        route = "north" if case == "reconfigure" else "west"
        goals["live_passage_obstruction"] = any(
            e.kind == "movement" and e.source == identity("yard-tools") and e.direction == route
            for e in active_effects(application.state.representation, application.connections,
                                    application.material_profile))
        play("untie work cord", "lift work panel from yard work trestle",
             "go east", "go north", "go east", "go east",
             "put work panel on document box", "tie work panel to notice board using work cord",
             "go west", "look east")
        goals["sight_not_passage"] = any(
            e.kind == "sight" and e.source == identity("common-threshold")
            for e in active_effects(application.state.representation, application.connections,
                                    application.material_profile)) and not any(
            e.kind == "movement" for e in active_effects(
                application.state.representation, application.connections, application.material_profile))
        play("go east", "untie work cord")
        goals["whole_cord_recovered"] = (
            not application.connections and any(
                r.subject_entity_id == identity("work-cord") and
                r.relation_type == "carried_by" and
                r.object_entity_id == application.fixture.player_entity_id
                for r in application.state.representation.relations))
    elif case == "cover":
        play(*cover)
        goals["cover_is_physical"] = bool(application.connections)
        play("go west", "go west", "take packing felt", "take wash bucket",
             "go east", "go east", "soak packing felt from wash bucket",
             "put packing felt on yard work trestle")
        goals["actually_covered"] = identity("packing-felt") in cover_subjects(
            application.state.representation, application.connections, fixture.cover_profile)
        held = dict(application.water_state.water)[identity("packing-felt")]
        play("wait")
        goals["retained_wetness_after_exposure"] = (
            held > 0 and dict(application.water_state.water)[identity("packing-felt")] > 0)
        play("untie cover tie")
        goals["remove_cover_removes_qualification"] = not cover_subjects(
            application.state.representation, application.connections, fixture.cover_profile)
    else:
        play("go south", "go west", "ask tali ren to assemble work partition")
        goals["accepted_without_free_assembly"] = not application.connections
        play("wait 8 steps")
        task = selected(application.participation_state, identity("tali"))
        goals["actor_real_join"] = (task.status == "completed" and
            any(e.kind == "movement" and e.source == identity("yard-tools")
                for e in active_effects(application.state.representation, application.connections,
                                        application.material_profile)))
    assert all(goals.values()), (case, goals, stages)
    return {"case": case, "variant": variant, "goals": goals,
            "stages": stages, "final_digest": application.authoritative_digest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repository-sha")
    args = parser.parse_args()
    # The installed launcher and export identity must refer to the checkout
    # actually executed. Retained-command discovery requires --output only.
    sha = resolve_repository_sha(args.repository_sha)
    with tempfile.TemporaryDirectory(prefix="myravant-structures-") as root:
        data = [run_case(Path(root)/f"{case}-{iteration}", case, sha)
                for case in CASES for iteration in range(2)]
        assert_repeat_digest_equality(
            data, CASES, case_field="case", digest_field="final_digest"
        )
        result = {"schema": "myravant.structures-installed.v1",
                  "engineering_authored": True, "cases": data,
                  "campaigns": len(data), "source": sha}
    write_json_report(args.output, result)
    print(f"Structures: {len(data)} installed journeys, objectives and replay passed.")


if __name__ == "__main__":
    main()

"""Installed public #555 transformation campaigns, authored goals, not blind acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_transformation import create_transformation_fixture
from astra_runtime.myravant_transformation_application import TransformationApplication
from astra_runtime.domain.persistent_world_transformation import role
from astra_runtime.domain.persistent_world_material import placement, active_effects


SCENARIOS=("refit-barrier","replace-repurpose","actor-contention")


def journey(root,scenario,head):
    save=root/"campaign.json"
    fixture=create_transformation_fixture()
    launcher=shutil.which("myravant-play")
    assert launcher,"installed myravant-play launcher required"
    stages=[]
    app=None

    def stage(*commands):
        nonlocal app
        trace=root/(str(len(stages))+".jsonl")
        argv=[launcher,"--locality","tarrow-transformation","--checkpoint",str(save),
              "--trace",str(trace),"--repository-sha",head]
        if save.exists():argv+=["--load",str(save)]
        before=time.perf_counter()
        proc=subprocess.run(argv,input="\n".join((*commands,"save","exit","")),
            capture_output=True,text=True,timeout=90)
        assert proc.returncode==0,(argv,proc.stdout,proc.stderr)
        events=[json.loads(row) for row in trace.read_text().splitlines()]
        assert events[-1]["evidence_complete"] is True
        interactions=[row for row in events if row.get("record_type")=="interaction"]
        assert interactions and interactions[-1]["post_state_digest"]
        restored=TransformationApplication.restore(fixture=fixture,checkpoint_path=save)
        assert restored.authoritative_digest()==interactions[-1]["post_state_digest"]
        if app is not None:
            assert tuple(restored.journal[:len(app.journal)])==app.journal
        app=restored
        stages.append({"commands":commands,"stdout":proc.stdout,"trace":events,
                       "restored_digest":app.authoritative_digest(),
                       "duration_seconds":time.perf_counter()-before})
        return proc.stdout

    prefix=("go south","go west","take barrier crossbar",
            "put barrier crossbar on yard work trestle")
    if scenario=="refit-barrier":
        stage(*prefix,"take alignment tool",
              "start refitting barrier crossbar using alignment tool",
              "work transformation","inspect transformation")
        partial=(app.transform_state.work.stage==1 and
                 role(app.transform_state,identity("barrier-crossbar"))=="prepared")
        stage("work transformation","take barrier board",
              "put barrier board on yard work trestle","take barrier cord",
              "tie barrier board to barrier crossbar using barrier cord","go north")
        effects=active_effects(app.state.representation,app.connections,app.material_profile)
        blocked=any(r.get("failure_class")=="material_passage_obstructed"
                    for r in stages[-1]["trace"] if r.get("record_type")=="interaction")
        objectives={"committed_partial_and_restart":partial,
                    "original_identity_restored":role(app.transform_state,identity("barrier-crossbar"))=="fit",
                    "real_barrier_effect":blocked and any(e.kind=="movement" and
                      e.source==identity("yard-tools") for e in effects),
                    "two_lineage_receipts":len(app.transform_state.lineage)==2}
    elif scenario=="replace-repurpose":
        stage(*prefix,"take barrier spare",
              "start replacing barrier crossbar with barrier spare","work transformation")
        partial=(app.transform_state.work.stage==1 and
                 placement(app.state.representation,identity("barrier-crossbar")).relation_type=="carried_by")
        stage("work transformation")
        replacement=(placement(app.state.representation,identity("barrier-spare")).relation_type=="supported_by"
                     and placement(app.state.representation,identity("barrier-crossbar")).relation_type=="carried_by"
                     and app.transform_state.lineage[-1][3]==identity("barrier-spare"))
        stage("take alignment tool","go west","go west",
              "start repurposing barrier crossbar using alignment tool","work transformation",
              "take repair board","put repair board on workroom bench",
              "put barrier crossbar on workroom bench","take repair cord",
              "tie repair board to barrier crossbar using repair cord")
        joined=any(c.left==identity("repair-board") and c.right==identity("barrier-crossbar")
                   for c in app.connections)
        objectives={"removed_old_part_retained":partial,
                    "whole_spare_installed":replacement,
                    "old_part_repurposed_with_real_assembly":joined and
                       role(app.transform_state,identity("barrier-crossbar"))=="spacer",
                    "three_distinct_stage_receipts":len({x[5] for x in app.transform_state.lineage})==3}
    elif scenario=="actor-contention":
        stage(*prefix,"ask tali ren to refit barrier crossbar using alignment tool",
              "wait","wait")
        started=(app.transform_state.work.actor==identity("tali") and
                 app.transform_state.work.stage==1 and
                 placement(app.state.representation,identity("alignment-tool")).object_entity_id==identity("tali"))
        stage("lift barrier crossbar from yard work trestle")
        blocked=(app.transform_state.work.stage==1 and
                 app.transform_state.work.status=="blocked")
        stage("put barrier crossbar on yard work trestle","wait")
        objectives={"qualified_voluntary_actor_work":started,
                    "real_access_contention_blocks":blocked,
                    "restore_after_resource_return":app.transform_state.work.status=="completed",
                    "actor_attributed_lineage":all(r[1]==identity("tali")
                        for r in app.transform_state.lineage)}
    else:raise ValueError("invalid scenario")
    assert all(objectives.values()),(scenario,objectives,[s["stdout"][-1200:] for s in stages])
    return {"scenario":scenario,"objectives":objectives,
            "stages":stages,"final_digest":app.authoritative_digest(),
            "receipt_ids":tuple(r[5] for r in app.transform_state.lineage),
            "lineage":app.transform_state.lineage,
            "limits":["developer-authored installed journey; not blind/human",
                      "whole-component profile only, not universal physics"]}


def report(output):
    head=subprocess.run(["git","rev-parse","HEAD"],check=True,capture_output=True,text=True).stdout.strip()
    profiles=[]
    with tempfile.TemporaryDirectory(prefix="myravant-transform-") as temp:
        for scenario in SCENARIOS:
            repeats=[]
            for n in range(2):
                root=Path(temp)/(scenario+"-"+str(n))
                root.mkdir()
                repeats.append(journey(root,scenario,head))
            assert repeats[0]["final_digest"]==repeats[1]["final_digest"]
            assert repeats[0]["receipt_ids"]==repeats[1]["receipt_ids"]
            profiles.append({"scenario":scenario,"repeats":repeats})
    payload={"schema":"myravant.transformation-installed.v1","repository_sha":head,
             "engineering_authored":True,"blind":False,"human_acceptance":False,
             "profiles":profiles}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(payload,sort_keys=True,indent=2)+"\n")
    print("Transformation: three installed campaigns repeated twice; staged receipts and replay.")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    report(p.parse_args().output)

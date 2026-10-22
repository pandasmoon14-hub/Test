"""Source-bound independent-goal-table check for #555 engineering-authored journeys.

This is not a blind assessor: supplied journey records require separate replay CI.
"""
import argparse
import json
from pathlib import Path
import subprocess


GOALS = Path(__file__).resolve().parents[1] / "tests/fixtures/tarrow_transformation_assessor_goals.json"


def evaluate(journeys, spec, head):
    if (journeys.get("schema")!="myravant.transformation-installed.v1" or
            spec.get("schema")!="myravant.transformation-goals.v1" or
            spec.get("contract_issue")!=555 or journeys.get("repository_sha")!=head):
        raise ValueError("wrong evidence source or goal specification")
    profiles=journeys["profiles"]
    goals=spec["goals"]
    if len(profiles)!=3 or len(goals)!=3 or set(x["scenario"] for x in profiles)!=set(x["scenario"] for x in goals):
        raise ValueError("missing distinct scenario")
    rows=[]
    for goal in goals:
        matched=next(x for x in profiles if x["scenario"]==goal["scenario"])
        repeats=matched["repeats"]
        if len(repeats)!=spec["repeat_count"] or len({x["final_digest"] for x in repeats})!=1:
            raise ValueError("missing deterministic repetition")
        for n,rep in enumerate(repeats):
            if any(rep["objectives"].get(flag) is not True for flag in goal["required_objectives"]):
                raise ValueError("missing independently named functional objective")
            if not rep.get("lineage") or not rep.get("receipt_ids"):
                raise ValueError("no source-bound component history")
            stages=rep["stages"]
            if not stages or stages[-1].get("restored_digest")!=rep["final_digest"]:
                raise ValueError("missing replay agreement")
            if not all(s.get("trace") and s["trace"][-1].get("evidence_complete") for s in stages):
                raise ValueError("incomplete public evidence traces")
            commands=[x.casefold() for s in stages for x in s["commands"]]
            for prefix in goal["required_public_inputs"]:
                if not any(cmd.startswith(prefix) for cmd in commands):
                    raise ValueError("public action was not attempted: "+prefix)
            # Do not substitute a developer-authored boolean for a public action.
            interactions=[r for s in stages for r in s["trace"] if r.get("record_type")=="interaction"]
            if not interactions or len(interactions)<len(commands):
                raise ValueError("missing installed interactive evidence")
            if not all(r.get("pre_state_digest") and r.get("post_state_digest") for r in interactions):
                raise ValueError("source-incomplete interaction")
            if goal["scenario"]=="refit-barrier" and not any(
                    r.get("failure_class")=="material_passage_obstructed" and
                    r.get("raw_player_input","").casefold().strip()=="go north" for r in interactions):
                raise ValueError("no actual barrier-blocked movement")
            if goal["scenario"]=="replace-repurpose":
                if rep.get("resource_case")!="split-spare":
                    raise ValueError("required alternate physical resource profile missing")
                north=[r for r in interactions
                       if r.get("raw_player_input","").strip().casefold()=="go north"]
                if len(north)!=2 or north[0].get("failure_class")!="material_passage_obstructed" or north[1].get("failure_class"):
                    raise ValueError("replacement route did not block and later reopen")
                if not any(r.get("raw_player_input","").strip().casefold().startswith("start replacing") and
                           r.get("failure_class")=="transformation_acceptance_unavailable" for r in interactions):
                    raise ValueError("missing actual remote-resource refusal")
            if goal["scenario"]=="actor-contention" and not any(
                    row[1]==rep["lineage"][0][1] for row in rep["lineage"]):
                raise ValueError("actor attribution mismatch")
            rows.append({"scenario":goal["scenario"],"repeat":n,
                         "objective_count":len(goal["required_objectives"]),
                         "interaction_count":len(interactions),
                         "source":head})
    return {"schema":"myravant.transformation-assessment.v1","repository_sha":head,
            "passed":True,"assessed_repeats":len(rows),"rows":rows,"blind":False,
            "human_acceptance":False,"independent_from_implementation_author":False,
            "limits":["Engineering-authored journeys and separately declared developer goals.",
                      "Not independent blind/human play; replay and negative mutation checks are separate."]}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    head=subprocess.run(["git","rev-parse","HEAD"],check=True,text=True,
                         capture_output=True).stdout.strip()
    result=evaluate(json.loads(args.input.read_text()),json.loads(GOALS.read_text()),head)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("Separate developer transformation assessor: 3 goals x 2 repeats passed.")


if __name__=="__main__":
    main()

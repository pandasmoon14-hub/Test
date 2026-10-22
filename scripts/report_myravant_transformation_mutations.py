"""Five isolated source-copy #555 regressions; never modify the checked-out code."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS=(
    ("unqualified_tool_used_without_custody","myravant_transformation_application.py",
     '        if (r.relation_type,r.object_entity_id)!=("carried_by",actor):',
     "        if False:",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("replacement_output_identity_duplicated","domain/persistent_world_transformation.py",
     '    output = profile.spare if task.method == "replace" and stage == 2 else profile.old',
     '    output = profile.old',
     "test_replacement_preserves_removed_part_then_repurposes_it"),
    ("barrier_uses_unfitted_component","myravant_transformation_application.py",
     '                if left==p.barrier_board and right==p.old and role(self.transform_state,p.old)!="fit":',
     "                if False:",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("lost_acknowledged_partial_progress","domain/persistent_world_transformation.py",
     "    stage = task.stage + 1",
     "    stage = 1",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("stale_target_opportunity_ignored","myravant_transformation_application.py",
     '            if condition!=needed or placement(self.state.representation,p.old).relation_type!="supported_by" or placement(self.state.representation,p.old).object_entity_id!=p.trestle:',
     '            if condition!=needed:',
     "test_stale_refit_opportunity_refuses_without_free_interval"),
    ("resealed_replay_final_forgery_accepted","myravant_material_application.py",
     "if app.authoritative_digest()!=p['final'] or list(app.journal)!=p['journal']:",
     "if list(app.journal)!=p['journal']:",
     "test_resealed_final_digest_tamper_rejected_even_if_checksum_valid"),
)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    output=p.parse_args().output
    report=run_mutations(Path(__file__).resolve().parents[1],
        mutations=MUTATIONS,test_filename="test_play_transformation_1.py")
    assert len(report["mutations"])==6
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("Transformation mutations: 6/6 intended defects detected; all controls passed.")

if __name__=="__main__":
    main()

"""Eleven isolated source-copy #555 regressions; never edit checked-out runtime."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS=(
    ("unqualified_tool_used_without_custody","myravant_transformation_application.py",
     '        if (r.relation_type,r.object_entity_id)!=("carried_by",actor):',
     "        if False:",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("replacement_output_identity_duplicated","domain/persistent_world_material.py",
     '    output = profile.spare if task.method == "replace" and stage == 2 else profile.old',
     '    output = profile.old',
     "test_replacement_preserves_removed_part_then_repurposes_it"),
    ("barrier_uses_unfitted_component","myravant_transformation_application.py",
     '                if left==p.barrier_board and right==p.old and role(self.transform_state,p.old)!="fit":',
     "                if False:",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("lost_acknowledged_partial_progress","domain/persistent_world_material.py",
     "    stage = task.stage + 1",
     "    stage = 1",
     "test_refit_requires_actual_custody_and_restores_function_with_replay"),
    ("stale_target_opportunity_ignored","myravant_transformation_application.py",
     '            if condition!=needed or placement(self.state.representation,p.old).relation_type!="supported_by" or placement(self.state.representation,p.old).object_entity_id!=p.trestle:',
     '            if condition!=needed:',
     "test_stale_refit_work_interval_is_charged_and_previous_receipts_survive"),
    ("resealed_replay_final_forgery_accepted","myravant_material_application.py",
     "if app.authoritative_digest()!=p['final'] or list(app.journal)!=p['journal']:",
     "if list(app.journal)!=p['journal']:",
     "test_resealed_final_digest_tamper_rejected_even_if_checksum_valid"),
    ("premature_spare_fastening_accepted","myravant_transformation_application.py",
     '                if left==p.barrier_board and right==p.spare and not self._replacement_committed():',
     '                if False:',
     "test_spare_cannot_bypass_committed_replacement_barrier"),
    ("remote_npc_task_control_accepted","myravant_transformation_application.py",
     '                self._route(actor,"control")',
     '                pass  # mutated remote-control qualification',
     "test_npc_work_control_requires_named_local_consensual_request"),
    ("stale_work_avoids_world_clock","myravant_transformation_application.py",
     '        before=self.authoritative_digest()\n        clock=self._interval("wait")',
     '        before=self.authoritative_digest()\n        try:self._qualified(task)\n        except ValueError as exc:return self._result(str(exc),failure="transformation_opportunity_unavailable")\n        clock=self._interval("wait")',
     "test_stale_refit_work_interval_is_charged_and_previous_receipts_survive"),
    ("post_owner_failure_does_not_rollback","myravant_transformation_application.py",
     '            self._restore_transaction(after_clock)',
     '            pass  # mutated missing stage rollback',
     "test_fault_after_physical_lift_rolls_back_only_stage_and_preserves_time"),
    ("blocked_player_work_counter_overflows","myravant_transformation_application.py",
     '            blocked_due=min(32,current.blocked_due+1)',
     '            blocked_due=current.blocked_due+1',
     "test_player_may_retry_after_more_than_profile_maximum_blocked_intervals"),
)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    output=p.parse_args().output
    report=run_mutations(Path(__file__).resolve().parents[1],
        mutations=MUTATIONS,test_filename="test_play_transformation_1.py")
    assert len(report["mutations"])==11
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("Transformation mutations: 11/11 intended defects detected; all controls passed.")

if __name__=="__main__":
    main()

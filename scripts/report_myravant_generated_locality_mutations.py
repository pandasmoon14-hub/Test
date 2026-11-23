"""Isolated negative controls for generated worksite admission and replay."""
import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ("skip_finite_budget_rejection", "myravant_generated_locality.py",
     "if recipe.budget == 0:", "if False and recipe.budget == 0:",
     "test_generation_failures_are_bounded_and_distinct"),
    ("skip_existing_campaign_guard", "myravant_generated_locality.py",
     "if path is not None and path.exists():",
     "if False and path is not None and path.exists():",
     "test_existing_state_never_regenerates_and_wrong_binding_rejects"),
    ("drop_material_barrier", "myravant_investigation_neutral.py",
     "if generated_case == 'access' or coordinated:", "if coordinated:",
     "test_access_barrier_is_live_material_and_alternate_route_exists"),
)

SITUATED_MUTATIONS = (
    ("remote_method_discussion_exposes_local_opportunity", "myravant_investigation_application.py",
     '            self._route(actor, "status")', '            pass',
     "test_worksite_discussion_does_not_reach_an_absent_worker"),
    ("generated_shelter_loses_drying_difference", "myravant_investigation_neutral.py",
     "(Fraction(1, 4), 'sheltered') if reverse else rates['studio']",
     "rates['studio']",
     "test_installed_drying_difference_and_return"),
    ("additional_annexes_replace_admitted_identities", "myravant_investigation_neutral.py",
     "    entity_token = identity_token or generated_token", "    entity_token = generated_token",
     "test_adjoining_annex_admission_preserves_prefix_identities_and_edges"),
    ("new_explicit_agreement_ignores_unusable_resource", "myravant_actor_application.py",
     "if method is None or self.qualify_explicit_cleaning_request:", "if method is None:",
     "test_installed_stock_contrast_refusal_and_already_satisfied"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    results = run_mutations(Path(__file__).resolve().parents[1],
                            mutations=MUTATIONS,
                            test_filename="test_play_generated_locality.py")
    situated = run_mutations(Path(__file__).resolve().parents[1],
                             mutations=SITUATED_MUTATIONS,
                             test_filename="test_play_situated_worksite.py")
    assert len(results["mutations"]) == len(MUTATIONS)
    assert len(situated["mutations"]) == len(SITUATED_MUTATIONS)
    assert results["repository_sha"] == situated["repository_sha"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "source": "PLAY-TARROW-LOCALITY-GEN-1", "engineering_authored": True,
        "isolated_source_mutations": results,
        "situated_worksite_mutations": situated,
        "not_blind_acceptance": True}, indent=2, sort_keys=True) + "\n")
    count = len(MUTATIONS) + len(SITUATED_MUTATIONS)
    print(f"Generated worksite: {count} isolated mutations detected with controls.")


if __name__ == "__main__":
    main()

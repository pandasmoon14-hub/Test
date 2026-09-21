import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROGRAM_PATH = (
    ROOT / "docs" / "doctrine" / "control" / "post_r2a_transition_program.md"
)
MANIFEST_PATH = (
    ROOT / "docs" / "doctrine" / "control" / "post_r2a_transition_manifest.yaml"
)

EXPECTED_BASELINE = "b1e4c70435ddd94a8e8fe82a11d8d6cace82b5bd"
R2B_CORE_BASELINE = "0a52db603589168a14f3c50beefbbf28274d0836"
R2B_CORE_AUTHORIZATION = "owner_directive_2026-09-07_r2b_core_activation"
R2B_CORE_HEAD = "8a88068b802a9819328e09691e7c1def778a778d"
R2B_CORE_PR = 376

R2B_CROSS_PHASE_BASELINE = "307ab295a8590d60a310d4b8d872971620fa74eb"
R2B_CROSS_PHASE_AUTHORIZATION = "owner_directive_2026-09-08_r2b_cross_phase_activation"
R2B_CROSS_PHASE_HEAD = "eededa8e0b845fa14ba303f4d34369cefdd2f861"
R2B_CROSS_PHASE_PR = 377

R2B_CONTINUITY_BASELINE = "d70e9a5c1ab67c8e2bb6a2b8331c73269cc3b286"
R2B_CONTINUITY_AUTHORIZATION = "owner_directive_2026-09-08_r2b_continuity_activation"
R2B_CONTINUITY_HEAD = "d94f5e8f40b1b74d6bdb23e2e419e5cb5d6fb34f"
R2B_CONTINUITY_PR = 378
R2C_BASELINE = "5cae79bcdd86c93c6fe77b6492a8a087a83900b0"
R2C_AUTHORIZATION = "owner_directive_2026-09-08_r2c_activation"
R2C_VALIDATED_HEAD = "949575f42f8b4ba1e01963013b35376d49433faf"
R2C_PUBLICATION_HEAD = "ea47efef19e1552f40fee7b7658797b59bd35b7f"
R2C_PR = 379
R2C_MERGE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"
PR2_ID_AUTHORIZATION = "owner_directive_2026-09-08_pr2_id_activation"
PR2_ID_T2B_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2b_activation"
PR2_ID_T2B_STARTING_HEAD = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
PR2_ID_T2C_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"
PR2_ID_T2C_STARTING_HEAD = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
PR2_ID_T2D_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2d_activation"
PR2_ID_T2D_STARTING_HEAD = "89d101fb6cbf44d2120871dbc6723ba8842e431b"
PR2_ID_T2E_AUTHORIZATION = "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
PR2_ID_T2E_STARTING_HEAD = "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
PR2_ID_T2E_EFFECT = "identity_migration_completion_recording_only"
PR2_ID_PR = 380
PR2_ID_HEAD = "024236e0ce9af3b6622e0a5b7be3a1ec3d4c99a3"
PR2_ID_MERGE = "1d1b16004b4bee0c75ca42c82900755ec29022bd"
PR2_SRC_A_BASELINE = "4033f43b2a4ad7088955ca1a29daf47a33ef7a37"
PR2_SRC_A_AUTHORIZATION = "owner_directive_2026-09-10_pr2_src_a_activation"
PR2_SRC_A_EFFECT = "foundational_source_research_governance_only"
PR2_SRC_A_PR = 382
PR2_SRC_A_HEAD = "ac82cebeeb3b8eb63fc6b4a312e90554584a1d32"
PR2_SRC_A_MERGE = "818a79d03ac487722762a44c9a80b29391278a8f"
PR2_SRC_B_BASELINE = "818a79d03ac487722762a44c9a80b29391278a8f"
PR2_SRC_B_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_b_activation"
PR2_SRC_B_EFFECT = "heterogeneous_source_research_method_qualification_only"
PR2_SRC_B_PR = 383
PR2_SRC_B_HEAD = "cabd12d56e7e036b2b839f21486776b49ebff56b"
PR2_SRC_B_MERGE = "70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"
PR2_SRC_C_BASELINE = "70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"
PR2_SRC_C_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_c_activation"
PR2_SRC_C_EFFECT = "legacy_source_conversion_surface_disposition_only"
PR2_SRC_C_PR = 384
PR2_SRC_C_HEAD = "b71de0fb8b5565f63dbb0019faad2cd5cf390465"
PR2_SRC_C_MERGE = "21b4ba706bb3f68aeb51dc4195fe1aa60014a439"
PR2_SRC_D_BASELINE = "21b4ba706bb3f68aeb51dc4195fe1aa60014a439"
PR2_SRC_D_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_d_activation"
PR2_SRC_D_EFFECT = "independent_source_research_completion_review_only"
PR2_SRC_D_PR = 385
PR2_SRC_D_HEAD = "7fd2f1c202abd7107dc2918e168d7885fb9452ce"
PR2_SRC_D_MERGE = "376214e1b715de34160dfb03d328547f510b6586"
PR2_SRC_D_TREE = "bcf9dd80d9a39594e60a62218bff3ee64aa85abb"
PR2_SRC_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_post_merge_closure"
PR2_SRC_CLOSURE_EFFECT = "source_research_post_merge_lifecycle_reconciliation_only"
PR2_SRC_CLOSURE_MERGE = "c14da427bf5c5c21c7ef1655e83aea3519587cc6"
PR2_ORG_BASELINE = "c14da427bf5c5c21c7ef1655e83aea3519587cc6"
PR2_ORG_AUTHORIZATION = "owner_directive_2026-09-11_pr2_org_activation"
PR2_ORG_EFFECT = "content_eligibility_and_provenance_governance_only"
PR2_ORG_CONTRACT = "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
PR2_ORG_PR = 387
PR2_ORG_HEAD = "a7aed059e1b96872150c05203dfdb9c07affe831"
PR2_ORG_MERGE = "031053afd9ac581cfc421554ee3383a11a0dc2bd"
PR2_ORG_TREE = "ac770e1c69a448545b0a58eb7ed49a0b13f81614"
PR2_ORG_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-11_pr2_org_post_merge_closure"
PR2_ORG_CLOSURE_EFFECT = "originality_eligibility_post_merge_lifecycle_reconciliation_only"
PR2_IR_BASELINE = "8e2ba57ad61aac366e2d34c47811a3d17fd59220"
PR2_IR_AUTHORIZATION = "owner_directive_2026-09-11_pr2_ir_activation"
PR2_IR_EFFECT = "information_barrier_and_representation_contract_only"
PR2_IR_CONTRACT = "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
PR2_IR_PR = 389
PR2_IR_HEAD = "ac48a9896840e5b9b236de8f7b4cc0febd9fdf5a"
PR2_IR_MERGE = "2b9c21fae92dd210a12e5f7e3d6c8d8931db0201"
PR2_IR_TREE = "8e99389020a3626e32dc7cb17e62cec081d96e54"
PR2_IR_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-12_pr2_ir_post_merge_closure"
PR2_IR_CLOSURE_EFFECT = "information_barrier_post_merge_lifecycle_reconciliation_only"
PR2_CORPUS_BASELINE = "92a4b6e15d9df10dedf4cec8bd1267111975cba2"
PR2_CORPUS_AUTHORIZATION = "owner_directive_2026-09-12_pr2_corpus_activation"
PR2_CORPUS_EFFECT = "corpus_governance_only"
PR2_CORPUS_CONTRACT = "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
PR2_CORPUS_PR = 391
PR2_CORPUS_HEAD = "f9881379bbbd492674c938724349da41fcd55141"
PR2_CORPUS_MERGE = "e8e2c0cef0fb1d9b7fdf758fb221f9d9b9ad3bb1"
PR2_CORPUS_TREE = "ae9949d1d34cb3208f7036d8bee74f6ca8c7e87b"
PR2_CORPUS_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-12_pr2_corpus_post_merge_closure"
PR2_CORPUS_CLOSURE_EFFECT = "corpus_governance_post_merge_lifecycle_reconciliation_only"
PR2_FICT_BASELINE = "fb9d4596c80ad779f5f58dd4fce066fb7ba797c9"
PR2_FICT_AUTHORIZATION = "owner_directive_2026-09-12_pr2_fict_activation"
PR2_FICT_EFFECT = "research_pressure_governance_only"
PR2_FICT_CONTRACT = "docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md"
PR2_FICT_PR = 393
PR2_FICT_HEAD = "31e5c4f71eef200ee7ad43c0c9f76ec6995ed806"
PR2_FICT_MERGE = "6a768616166d35fcf51dd8345895847e0554ed28"
PR2_FICT_TREE = "105b51247673fc7941491bc743e4100d7d317701"
PR2_FICT_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-12_pr2_fict_post_merge_closure"
PR2_FICT_CLOSURE_EFFECT = "fiction_pressure_governance_post_merge_lifecycle_reconciliation_only"
PR2_SIMEX_BASELINE = "302732db03175726de2cdd7c24e78eb257520083"
PR2_SIMEX_AUTHORIZATION = "owner_directive_2026-09-13_pr2_simex_activation"
PR2_SIMEX_EFFECT = "architecture_pressure_governance_only"
PR2_SIMEX_CONTRACT = "docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md"
PR2_SIMEX_PR = 395
PR2_SIMEX_HEAD = "1c0fafaa862f01b623baa51d8e557dd0a3095414"
PR2_SIMEX_MERGE = "5c48a8e4393374dba3f9f2edc5541c1bb75906f4"
PR2_SIMEX_TREE = "99955d4b9fb54abc494c254fb2364bbfc75d4049"
PR2_SIMEX_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-13_pr2_simex_post_merge_closure"
PR2_SIMEX_CLOSURE_EFFECT = "simulation_infrastructure_exemplar_pressure_governance_post_merge_lifecycle_reconciliation_only"
PR2_SCALE_BASELINE = "5268f85135b9ad5d67719b37305b204554729bed"
PR2_SCALE_AUTHORIZATION = "owner_directive_2026-09-14_pr2_scale_activation"
PR2_SCALE_EFFECT = "runtime_architecture_contract_only"
PR2_SCALE_CONTRACT = "docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md"
PR2_SCALE_PR = 397
PR2_SCALE_HEAD = "01f82d331792e266e44b59ffc261e9b55f15decf"
PR2_SCALE_MERGE = "862ee41369ec8cba5768cb13aa59ecd853a7f8c4"
PR2_SCALE_TREE = "77717680ea254bb81043a7109b4842164834c925"
PR2_SCALE_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-14_pr2_scale_post_merge_closure"
PR2_SCALE_CLOSURE_EFFECT = "runtime_scalability_governance_post_merge_lifecycle_reconciliation_only"
PR2_PART_BASELINE = "26e0d5ea870ab8aac23fd0aeb0e200cd3a4bf965"
PR2_PART_AUTHORIZATION = "owner_directive_2026-09-14_pr2_part_activation"
PR2_PART_EFFECT = "runtime_partitioning_contract_only"
PR2_PART_CONTRACT = "docs/doctrine/control/myravant_authority_partitioning_migration_contract.md"
PR2_PART_PR = 399
PR2_PART_HEAD = "4b3c98328df32d02593f5632603d59c06ebbf879"
PR2_PART_MERGE = "ba992c51d781a37a85da4757c2c00af3e9da1f8e"
PR2_PART_TREE = "de108cccbe0d8018b90be5bfde8e317616e5fea4"
PR2_PART_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-14_pr2_part_post_merge_closure"
PR2_PART_CLOSURE_EFFECT = "runtime_partitioning_governance_post_merge_lifecycle_reconciliation_only"
PR2_CONC_BASELINE = "0c24b4dad5e2f8e35b93cfb38632c5d3fb92b96a"
PR2_CONC_AUTHORIZATION = "owner_directive_2026-09-14_pr2_conc_activation"
PR2_CONC_EFFECT = "runtime_concurrency_contract_only"
PR2_CONC_CONTRACT = "docs/doctrine/control/myravant_deterministic_concurrency_scheduling_contract.md"
PR2_CONC_PR = 401
PR2_CONC_HEAD = "684740e41ab3ae10759d6b999c23e8cc6ff9c470"
PR2_CONC_MERGE = "5752de38f432c59f9e603ffd1ef38384e621a407"
PR2_CONC_TREE = "f5cdf3282132537088088ee6aa0592a82354b063"
PR2_CONC_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-14_pr2_conc_post_merge_closure"
PR2_CONC_CLOSURE_EFFECT = "runtime_concurrency_governance_post_merge_lifecycle_reconciliation_only"
PR2_EVENT_BASELINE = "e765d00e57e3a444ecd16078a3390eb49958f5b2"
PR2_EVENT_AUTHORIZATION = "owner_directive_2026-09-15_pr2_event_activation"
PR2_EVENT_EFFECT = "runtime_message_contract_only"
PR2_EVENT_CONTRACT = "docs/doctrine/control/myravant_command_event_message_projection_contract.md"
PR2_EVENT_PR = 403
PR2_EVENT_HEAD = "a70cca1310e3a8a70fef40c325c850c69202c6b2"
PR2_EVENT_MERGE = "e9a41cc7b144ffab0ca8fa91c4a9b3a9a1a56214"
PR2_EVENT_TREE = "201998a6eb39814e75e0bd696886eabd6bd0e66e"
PR2_EVENT_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-15_pr2_event_post_merge_closure"
PR2_EVENT_CLOSURE_EFFECT = "runtime_message_projection_governance_post_merge_lifecycle_reconciliation_only"
PR2_EVENT_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_command_event_message_projection_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_event_message_projection_contract.py', 'tests/test_pr2_conc_post_merge_closure.py'}
PR2_PERSIST_BASELINE = "56a5cf065bc37588ee6b62b3a51f1576d0168d6e"
PR2_PERSIST_AUTHORIZATION = "owner_directive_2026-09-15_pr2_persist_activation"
PR2_PERSIST_EFFECT = "runtime_persistence_contract_only"
PR2_PERSIST_CONTRACT = "docs/doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md"
PR2_PERSIST_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_persist_persistence_recovery_contract.py', 'tests/test_pr2_event_post_merge_closure.py'}
PR2_PERSIST_PR = 405
PR2_PERSIST_HEAD = "814476c63d5ee65701f1abfff19db5b347c1dd05"
PR2_PERSIST_MERGE = "e53e64f92fe2639d68c96bfa70825c6f6ec39f03"
PR2_PERSIST_TREE = "9171db95438dfc75460ed7c340f3be5d84813825"
PR2_PERSIST_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-15_pr2_persist_post_merge_closure"
PR2_PERSIST_CLOSURE_EFFECT = "runtime_persistence_governance_post_merge_lifecycle_reconciliation_only"
PR2_FID_BASELINE = "bc79bc629f3cc6bff220c8e71c37d9df515b9f8c"
PR2_FID_AUTHORIZATION = "owner_directive_2026-09-15_pr2_fid_activation"
PR2_FID_EFFECT = "runtime_fidelity_contract_only"
PR2_FID_CONTRACT = "docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md"
PR2_FID_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_fid_relevance_fidelity_contract.py', 'tests/test_pr2_persist_post_merge_closure.py'}
PR2_FID_PR = 407
PR2_FID_HEAD = "6a3fd4de79fb421fc03352b311c1168faa71255a"
PR2_FID_MERGE = "c077abf5a90e896ef535d4956c49803cbf8163b6"
PR2_FID_TREE = "766d61cb47101f15eefb14db88607f3473c006e3"
PR2_FID_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-16_pr2_fid_post_merge_closure"
PR2_FID_CLOSURE_EFFECT = "runtime_fidelity_governance_post_merge_lifecycle_reconciliation_only"
PR2_BP_BASELINE = "59520af5f2a68a5979091c00bb632f0cb5d2600e"
PR2_BP_AUTHORIZATION = "owner_directive_2026-09-16_pr2_bp_activation"
PR2_BP_EFFECT = "runtime_performance_contract_only"
PR2_BP_CONTRACT = "docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md"
PR2_BP_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_bp_performance_overload_backpressure_contract.py', 'tests/test_pr2_fid_post_merge_closure.py'}
PR2_BP_PR = 409
PR2_BP_HEAD = "001a46a543fc83bd6032ea0605cc28d7627ca0d9"
PR2_BP_MERGE = "7ef7b6df93936f3dbedefe1dcc362f50fb4f482f"
PR2_BP_TREE = "b76f92c664fa51fe25a2fe5df8923cef7efc1611"
PR2_BP_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-16_pr2_bp_post_merge_closure"
PR2_BP_CLOSURE_EFFECT = "runtime_performance_governance_post_merge_lifecycle_reconciliation_only"
R3_AUTHORIZATION = "owner_directive_2026-09-16_r3_initial_conformance"
R3_EFFECT = "r3_conformance_review_only"
R3_BASELINE = "a92e47bb2e0d5ffd853da2c1bbf6425efc8c659c"
R3_REVIEW = "docs/doctrine/reviews/r3_initial_conformance_review.yaml"
PR2_AUDIT_A_BASELINE = "b8c00ed48f2859eeef4a9229b3aec0ea4cd1405c"
PR2_AUDIT_A_AUTHORIZATION = "owner_directive_2026-09-16_pr2_audit_a_r3_r4_entry_disposition"
PR2_AUDIT_A_EFFECT = "inventory_and_disposition_only"
PR2_AUDIT_A_REVIEW = (
    "docs/doctrine/reviews/"
    "pr2_audit_r3_promotion_blocker_r4_entry_disposition.yaml"
)

R4_0_BASELINE = "503cd04e69225398d32d3ad4848c05522b96e83c"
R4_0_AUTHORIZATION = "owner_directive_2026-09-16_r4_0_read_only_substrate_reconciliation"
R4_0_EFFECT = "read_only_substrate_reconciliation_only"
R4_0_REVIEW = (
    "docs/doctrine/reviews/"
    "r4_0_substrate_reconciliation.yaml"
)
AUDIT_A_PR = 412
AUDIT_A_HEAD = "0592a3701d6ecaf13f2bcec849ae6ac58d584232"
AUDIT_A_MERGE = "503cd04e69225398d32d3ad4848c05522b96e83c"
AUDIT_A_TREE = "0e593ea18290541d36af020bdde445df41371b6f"

R4_A_BASELINE = "fa4f1d795275eaaad4ee525aea7e3f3c2c2bd5e9"
R4_A_AUTHORIZATION = "owner_directive_2026-09-17_r4_a_myravant_native_substrate_design"
R4_A_EFFECT = "myravant_native_substrate_design_only"
R4_A_REVIEW = (
    "docs/doctrine/reviews/"
    "r4_a_myravant_native_substrate_design.yaml"
)
R4_0_PR = 413
R4_0_HEAD = "d7ab9a2eff47b0a11855ad46e8c3b03434e7b7ec"
R4_0_MERGE = "fa4f1d795275eaaad4ee525aea7e3f3c2c2bd5e9"
R4_0_TREE = "cf0217da37e38f546ee0185fbced11104c9dfb5d"

R4_A_PR = 414
R4_A_HEAD = "08a0cb05edc2d9ca99b71ec32ff12163c1e58c08"
R4_A_MERGE = "6455659b61bc0b56fa6c41f95e15f5b1b94d077a"
R4_A_TREE = "6e71bcc985fd10762cf51bfc95d413e9184e2f6a"
AUDIT_D_BASELINE = "6455659b61bc0b56fa6c41f95e15f5b1b94d077a"
AUDIT_D_AUTHORIZATION = "owner_directive_2026-09-17_pr2_audit_d_completion_synthesis"
AUDIT_D_EFFECT = "repository_wide_post_r2_audit_completion_synthesis_only"
AUDIT_D_REVIEW = (
    "docs/doctrine/reviews/"
    "pr2_audit_completion_synthesis.yaml"
)
AUDIT_D_PR = 415
AUDIT_D_HEAD = "21916c30eb96dbeb2b84c6b056709339ec31048d"
AUDIT_D_MERGE = "720ee27248aac46e8f4e39492d51fda331778209"
AUDIT_D_TREE = "04c094a41eda056b58f59bb5553ab718535d1f41"
PR2_AUDIT_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-18_pr2_audit_post_merge_closure"
PR2_AUDIT_CLOSURE_EFFECT = "repository_wide_post_r2_audit_post_merge_lifecycle_reconciliation_only"
PR2_MIG_A_BASELINE = "33e09250ef2d68946bd058044f15306c66bbefaf"
PR2_MIG_A_AUTHORIZATION = "owner_directive_2026-09-18_pr2_mig_rs_0028"
PR2_MIG_A_EFFECT = "bounded_rs_0028_commitment_qualification_migration_only"
PR2_MIG_A_CANDIDATE = "R2A-DISPOSITION-RS-0028"
PR2_MIG_A_TARGET = "src/astra_runtime/domain/object_lever_event_commit_state_delta_path.py"
PR2_MIG_A_PR = 417
PR2_MIG_A_HEAD = "f853830ff8b1f4a8f5fccba030fe66c796e03f21"
PR2_MIG_A_MERGE = "3d2125e91da1d6f687dd5d72805c39cafef9afb6"
PR2_MIG_A_TREE = "07c2c8f70d220f3b3e382bc2ad67e73d2c342eca"
PR2_MIG_A_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-18_pr2_mig_a_post_merge_closure"
PR2_MIG_A_CLOSURE_EFFECT = "bounded_rs_0028_post_merge_lifecycle_reconciliation_only"
PR2_MIG_B_BASELINE = "b4b52cab91916e050e20ad54ff3559153436a944"
PR2_MIG_B_AUTHORIZATION = "owner_directive_2026-09-18_pr2_mig_rs_0030"
PR2_MIG_B_EFFECT = "bounded_rs_0030_replay_audit_qualification_migration_only"
PR2_MIG_B_CANDIDATE = "R2A-DISPOSITION-RS-0030"
PR2_MIG_B_TARGET = "src/astra_runtime/domain/object_lever_replay_audit_check.py"
PR2_MIG_B_PR = 419
PR2_MIG_B_HEAD = "8e33ade1bc7f1346401131394b3de2327802d882"
PR2_MIG_B_MERGE = "2b9e1a690bb567dfa3fda8c1982179e86106860b"
PR2_MIG_B_TREE = "cef6740107d345a8ff97c6b06b0eb777aaf158a9"
PR2_MIG_B_CI_RUN = 238
PR2_MIG_B_CI_RUN_ID = 35405934205
PR2_MIG_B_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-18_pr2_mig_b_post_merge_closure"
PR2_MIG_B_CLOSURE_EFFECT = "bounded_rs_0030_post_merge_lifecycle_reconciliation_only"
PR2_TEST_BASELINE = "02d63b38e83000099e2654d74db0d0454bf97346"
PR2_TEST_AUTHORIZATION = "owner_directive_2026-09-18_pr2_test_activation"
PR2_TEST_EFFECT = "post_r2_acceptance_evaluation_only"
PR2_IMPL_AUTHORIZATION = "owner_directive_2026-09-19_pr2_impl_activation"
PR2_TEST_CONTRACT = "docs/doctrine/control/myravant_post_r2_acceptance_evaluation_contract.md"
PR2_CONC_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_deterministic_concurrency_scheduling_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_conc_deterministic_concurrency_contract.py', 'tests/test_pr2_part_post_merge_closure.py'}
PR2_PART_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_authority_partitioning_migration_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_part_authority_partitioning_contract.py', 'tests/test_pr2_scale_post_merge_closure.py'}
PR2_SCALE_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_scale_runtime_scalability_contract.py', 'tests/test_pr2_simex_post_merge_closure.py'}
PR2_SIMEX_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_simex_exemplar_pressure_contract.py', 'tests/test_pr2_fict_post_merge_closure.py'}
PR2_FICT_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_fict_experience_pressure_contract.py', 'tests/test_pr2_corpus_post_merge_closure.py'}
PR2_CORPUS_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_corpus_scale_coverage_governance.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_corpus_scale_coverage_governance.py', 'tests/test_pr2_ir_post_merge_closure.py'}
PR2_IR_OWNED_PATHS = {'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/myravant_source_design_information_barrier_contract.md', 'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_ir_information_barrier.py', 'tests/test_pr2_org_post_merge_closure.py'}
PR2_ORG_OWNED_PATHS = {'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'tests/test_pr2_src_completion_review.py', 'tests/test_pr2_src_post_merge_closure.py', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_org_originality_provenance_eligibility.py', 'docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md', 'docs/doctrine/control/post_r2a_transition_program.md', 'docs/decisions/current_decisions_log.md'}

EXPECTED_R2_GATES = {
    "R1": "complete",
    "R2": "complete",
    "R2-0": "complete",
    "R2A": "complete",
    "R2B": "complete",
    "R2C": "complete",
    "R3": "complete",
    "R4-R6": "blocked",
    "RT-002G": "unauthorized",
    "temporary_evidence_deletion": "unauthorized",
}

EXPECTED_R2B_PACKAGES = {
    "R2B-CORE": "merged",
    "R2B-AGENCY": "not_required",
    "R2B-WORLD": "not_required",
    "R2B-CONTINUITY": "merged",
    "R2B-CROSS-PHASE": "merged",
}

EXPECTED_R2B_SEQUENCE = [
    "R2B-CORE",
    "R2B-CROSS-PHASE",
    "R2B-CONTINUITY",
]

EXPECTED_WORKSTREAM_IDS = {
    "PR2-CTRL",
    "PR2-R2B-C",
    "PR2-R2B-X",
    "PR2-R2B-N",
    "PR2-R2C",
    "PR2-ID",
    "PR2-SRC",
    "PR2-ORG",
    "PR2-CORPUS",
    "PR2-IR",
    "PR2-FICT",
    "PR2-SIMEX",
    "PR2-SCALE",
    "PR2-PART",
    "PR2-CONC",
    "PR2-FID",
    "PR2-EVENT",
    "PR2-PERSIST",
    "PR2-BP",
    "PR2-AUDIT",
    "PR2-MIG",
    "PR2-TEST",
    "PR2-IMPL",
}

EXPECTED_STATUS_VOCABULARY = {
    "identified",
    "blocked",
    "ready_pending_authorization",
    "authorized",
    "active",
    "implemented",
    "validated",
    "merged",
    "superseded",
    "not_required",
}

TERMINAL_STATUSES = {
    "merged",
    "superseded",
    "not_required",
}

UNRESOLVED_IDENTITY_CLASSES = [
    "roadmap_currentness_setting_and_planning_authority",
    "astra_prefixed_governance_and_working_group_role_identity",
    "r1b_shared_vocabulary_identity_and_exact_parity",
    "software_namespace_future_alias_or_deprecation_policy",
]

POST_R2_READY = set()

POST_R2_ACTIVE = set()

POST_R2_BLOCKED = set()


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _by_id(manifest):
    return {
        workstream["workstream_id"]: workstream
        for workstream in manifest["workstreams"]
    }


def test_control_artifacts_exist():
    assert PROGRAM_PATH.is_file()
    assert MANIFEST_PATH.is_file()


def test_frozen_baseline_and_identity_are_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"
    assert manifest["frozen_starting_baseline"] == EXPECTED_BASELINE
    assert manifest["starting_event"]["pull_request"] == 374
    assert manifest["starting_event"]["merge_commit"] == EXPECTED_BASELINE

    invariants = manifest["program_invariants"]
    assert invariants["future_project_identity"] == "Myravant"
    assert invariants["historical_project_identity"] == "Astra Ascension"
    assert invariants["minimum_external_source_scale"] >= 1000


def test_core_program_invariants_are_preserved():
    manifest = _load_manifest()
    invariants = manifest["program_invariants"]

    assert invariants["books_are_atomic_evidence_units"] is True
    assert invariants["books_are_default_myravant_production_units"] is False
    assert invariants["corpus_frequency_is_doctrine_authority"] is False
    assert invariants["semantic_mapping_implies_distribution_eligibility"] is False
    assert invariants["rename_may_rewrite_immutable_history"] is False
    assert invariants["post_r2_program_work_held_until_r2c_complete"] is True
    assert (
        invariants["runtime_scalability_invariant"]
        == "logical_simulation_semantics_are_independent_of_physical_execution_topology"
    )


def test_r2c_gate_state_and_r2b_completion_are_exact():
    manifest = _load_manifest()

    assert manifest["r2_gate_state"] == EXPECTED_R2_GATES
    assert manifest["r2b_package_state"] == EXPECTED_R2B_PACKAGES
    assert manifest["recommended_r2b_sequence"] == EXPECTED_R2B_SEQUENCE


def test_r3_target_is_validated_complete_and_exact():
    manifest = _load_manifest()
    target = manifest["r3_conformance_target"]

    assert manifest["r2_gate_state"]["R3"] == "complete"
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert target["status"] == "validated"
    assert target["selector"] == "pressure_route == r3_conformance"
    assert target["candidate_count"] == 34
    assert target["assessed_candidate_count"] == 34
    assert target["execution_authorized"] is True
    assert target["authorization_reference"] == R3_AUTHORIZATION
    assert target["authority_effect"] == R3_EFFECT
    assert target["starting_baseline"] == R3_BASELINE
    assert target["review_artifact"] == R3_REVIEW
    assert target["review_state"] == "validated_complete"
    assert target["completion_state"] == (
        "validated_complete_with_nonconformances_routed"
    )

    assert target["source_index"] == (
        "docs/doctrine/reviews/r2a/"
        "dispositions_runtime_schema/index.yaml"
    )

    assert set(target["excluded_pressure_routes"]) == {
        "r4_substrate",
        "later_gate",
        "none",
    }

    assert target["current_blob_state_counts"] == {
        "unchanged_since_r2a": 34,
    }

    assert target["outcome_counts"] == {
        "conformant_as_nonauthoritative_surface": 15,
        "conformant_with_required_remediation_before_promotion": 17,
        "nonconformant_requires_remediation": 2,
    }

    assert target["direct_nonconformance_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]

    assert target["promotion_blocking_candidate_count"] == 19
    assert target["runtime_promotion_clear"] is False
    assert target["r4_activation_authorized"] is False
    assert target["downstream_remediation_authorized"] is False

    assert set(target["validation_evidence"]) == {
        "R3 focused conformance validation:39 passed",
        (
            "R3 full local repository suite:"
            "9211 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "R3 git diff --check:clean",
        "R3 exact eight-file review footprint:PASS",
        "R3 runtime/schema noninterference audit:PASS",
    }

    program = PROGRAM_PATH.read_text(encoding="utf-8")

    assert (
        "### 5.39 R3 initial conformance validation and completion"
        in program
    )
    assert "R3 gate state is now `complete`." in program
    assert "`runtime_promotion_clear=false`" in program

def test_status_vocabulary_is_bounded():
    manifest = _load_manifest()
    statuses = manifest["status_vocabulary"]

    assert len(statuses) == len(set(statuses))
    assert set(statuses) == EXPECTED_STATUS_VOCABULARY
    assert set(manifest["terminal_statuses"]) == TERMINAL_STATUSES


def test_workstream_registry_is_exact_and_unique():
    manifest = _load_manifest()
    workstreams = manifest["workstreams"]
    ids = [workstream["workstream_id"] for workstream in workstreams]

    assert len(ids) == 23
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_WORKSTREAM_IDS


def test_all_dependencies_resolve_and_statuses_are_legal():
    manifest = _load_manifest()
    workstreams = manifest["workstreams"]
    ids = {workstream["workstream_id"] for workstream in workstreams}
    allowed = set(manifest["status_vocabulary"])

    missing = []
    for workstream in workstreams:
        assert workstream["status"] in allowed
        for dependency in workstream["dependencies"]:
            if dependency not in ids:
                missing.append((workstream["workstream_id"], dependency))

    assert missing == []


def test_r2b_merge_chain_is_fully_recorded():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    core = by_id["PR2-R2B-C"]
    assert core["status"] == "merged"
    assert core["authorization_reference"] == R2B_CORE_AUTHORIZATION
    assert core["starting_baseline"] == R2B_CORE_BASELINE
    assert core["pull_request"] == R2B_CORE_PR
    assert core["branch_head"] == R2B_CORE_HEAD
    assert core["merge_commit"] == R2B_CROSS_PHASE_BASELINE
    assert core["residual_gaps"] == []

    cross = by_id["PR2-R2B-X"]
    assert cross["status"] == "merged"
    assert cross["authorization_reference"] == R2B_CROSS_PHASE_AUTHORIZATION
    assert cross["starting_baseline"] == R2B_CROSS_PHASE_BASELINE
    assert cross["pull_request"] == R2B_CROSS_PHASE_PR
    assert cross["branch_head"] == R2B_CROSS_PHASE_HEAD
    assert cross["merge_commit"] == R2B_CONTINUITY_BASELINE
    assert cross["residual_gaps"] == []

    continuity = by_id["PR2-R2B-N"]
    assert continuity["status"] == "merged"
    assert continuity["authorization_reference"] == R2B_CONTINUITY_AUTHORIZATION
    assert continuity["starting_baseline"] == R2B_CONTINUITY_BASELINE
    assert continuity["pull_request"] == R2B_CONTINUITY_PR
    assert continuity["branch_head"] == R2B_CONTINUITY_HEAD
    assert continuity["merge_commit"] == R2C_BASELINE
    assert continuity["residual_gaps"] == []


def test_r2c_through_pr2_mig_are_merged_and_no_migration_successor_remains():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    active = {
        workstream["workstream_id"]
        for workstream in manifest["workstreams"]
        if workstream["status"] == "active"
    }
    assert active == set()

    pr2_test = by_id["PR2-TEST"]
    assert pr2_test["status"] == "merged"
    assert (
        pr2_test["authorization_reference"]
        == PR2_TEST_AUTHORIZATION
    )
    assert pr2_test["authority_effect"] == PR2_TEST_EFFECT
    assert pr2_test["starting_baseline"] == PR2_TEST_BASELINE
    assert pr2_test["control_artifact"] == PR2_TEST_CONTRACT
    assert (
        pr2_test["completion_state"]
        == "merged_complete_with_future_implementation_handoffs"
    )

    pr2_impl = by_id["PR2-IMPL"]

    assert pr2_impl["status"] == "merged"

    assert (
        pr2_impl["completion_state"]
        == (
            "merged_complete_r4_b_ready_"
            "pending_authorization"
        )
    )

    assert pr2_impl["completion_condition_satisfied"] is True
    assert pr2_impl["completion_recommended"] is True
    assert pr2_impl["r4_b_package_definition_complete"] is True
    candidate = pr2_impl["first_playable_candidate"]
    assert candidate["ready_pending_authorization"] is False
    assert candidate["authorized"] is True
    assert candidate["authorization_reference"] == "owner_directive_2026-09-20_r4_b_implementation_authorization"
    assert candidate["runtime_path"] == (
        "src/astra_runtime/domain/"
        "persistent_world_entity_location_representation.py"
    )

    r4_target = manifest["r4_native_substrate_design_target"]
    assert r4_target["r4_b_ready_pending_authorization"] is False
    assert r4_target["r4_b_authorized"] is True
    assert r4_target["implementation_authorized"] is True
    assert r4_target["runtime_edits_authorized"] is True
    assert r4_target["schema_edits_authorized"] is False
    assert r4_target["r4_activation_authorized"] is False
    assert r4_target["runtime_promotion_clear"] is False

    assert pr2_impl["r4_b_authorized"] is True

    # PR2-IMPL remains terminal and does not itself become a generalized
    # runtime-implementation authority source.
    assert pr2_impl["runtime_implementation_authorized"] is False
    assert pr2_impl["production_schema_authorized"] is False
    assert pr2_impl["r4_activation_authorized"] is False
    assert pr2_impl["runtime_promotion_authorized"] is False

    r2c = by_id["PR2-R2C"]
    assert r2c["status"] == "merged"
    assert r2c["authorization_reference"] == R2C_AUTHORIZATION
    assert r2c["starting_baseline"] == R2C_BASELINE
    assert r2c["pull_request"] == R2C_PR
    assert r2c["branch_head"] == R2C_PUBLICATION_HEAD
    assert r2c["merge_commit"] == R2C_MERGE
    assert r2c["residual_gaps"] == []

    pr2id = by_id["PR2-ID"]
    assert pr2id["status"] == "merged"
    assert pr2id["authorization_reference"] == PR2_ID_AUTHORIZATION
    assert pr2id["starting_baseline"] == R2C_MERGE
    assert set(pr2id["dependencies"]) == {"PR2-CTRL", "PR2-R2C"}
    assert pr2id["pull_request"] == PR2_ID_PR
    assert pr2id["branch_head"] == PR2_ID_HEAD
    assert pr2id["merge_commit"] == PR2_ID_MERGE
    assert pr2id["residual_gaps"] == []
    assert [row["class_id"] for row in pr2id["carried_forward_obligations"]] == UNRESOLVED_IDENTITY_CLASSES
    assert pr2id["current_tranche"] == "PR2-ID-T2E"
    assert pr2id["tranche_authority_effect"] == PR2_ID_T2E_EFFECT
    assert pr2id["current_tranche_starting_head"] == PR2_ID_T2E_STARTING_HEAD
    assert (
        pr2id["current_tranche_authorization_reference"]
        == PR2_ID_T2E_AUTHORIZATION
    )
    assert pr2id["completion_audit_result"] == "PASS"
    assert pr2id["next_tranche_authorized"] is False

    src = by_id["PR2-SRC"]
    assert src["status"] == "merged"
    assert src["authorization_reference"] == PR2_SRC_A_AUTHORIZATION
    assert src["authority_effect"] == PR2_SRC_A_EFFECT
    assert src["starting_baseline"] == PR2_SRC_A_BASELINE
    assert src["current_tranche"] == "PR2-SRC-D"
    assert src["tranche_authority_effect"] == PR2_SRC_D_EFFECT
    assert src["tranche_control_artifact"] == (
        "docs/doctrine/reviews/pr2_src_source_research_completion_review.yaml"
    )
    assert src["current_tranche_starting_head"] == PR2_SRC_D_BASELINE
    assert src["current_tranche_authorization_reference"] == PR2_SRC_D_AUTHORIZATION
    assert src["completion_review_result"] == "PASS"
    assert src["completion_review_blocking_findings"] == []
    assert src["next_tranche_authorized"] is False
    assert src["pull_request"] == PR2_SRC_D_PR
    assert src["branch_head"] == PR2_SRC_D_HEAD
    assert src["merge_commit"] == PR2_SRC_D_MERGE
    assert src["completion_state"] == "merged"
    assert src["post_merge_closure_authorization_reference"] == PR2_SRC_CLOSURE_AUTHORIZATION
    assert src["post_merge_closure_authority_effect"] == PR2_SRC_CLOSURE_EFFECT
    assert src["post_merge_closure_recorded_from"] == PR2_SRC_D_MERGE
    assert src["post_merge_closure_tree"] == PR2_SRC_D_TREE
    assert [row["tranche_id"] for row in src["planned_tranches"]] == [
        "PR2-SRC-A",
        "PR2-SRC-B",
        "PR2-SRC-C",
        "PR2-SRC-D",
    ]
    tranches = {row["tranche_id"]: row for row in src["planned_tranches"]}
    assert tranches["PR2-SRC-A"]["state"] == "merged"
    assert tranches["PR2-SRC-A"]["pull_request"] == PR2_SRC_A_PR
    assert tranches["PR2-SRC-A"]["branch_head"] == PR2_SRC_A_HEAD
    assert tranches["PR2-SRC-A"]["merge_commit"] == PR2_SRC_A_MERGE
    assert tranches["PR2-SRC-B"]["state"] == "merged"
    assert tranches["PR2-SRC-B"]["pull_request"] == PR2_SRC_B_PR
    assert tranches["PR2-SRC-B"]["branch_head"] == PR2_SRC_B_HEAD
    assert tranches["PR2-SRC-B"]["merge_commit"] == PR2_SRC_B_MERGE
    assert tranches["PR2-SRC-C"]["state"] == "merged"
    assert tranches["PR2-SRC-C"]["pull_request"] == PR2_SRC_C_PR
    assert tranches["PR2-SRC-C"]["branch_head"] == PR2_SRC_C_HEAD
    assert tranches["PR2-SRC-C"]["merge_commit"] == PR2_SRC_C_MERGE
    assert tranches["PR2-SRC-D"]["state"] == "merged"
    assert tranches["PR2-SRC-D"]["authorization_reference"] == PR2_SRC_D_AUTHORIZATION
    assert tranches["PR2-SRC-D"]["authority_effect"] == PR2_SRC_D_EFFECT
    assert tranches["PR2-SRC-D"]["starting_baseline"] == PR2_SRC_D_BASELINE
    assert tranches["PR2-SRC-D"]["review_result"] == "PASS"
    assert tranches["PR2-SRC-D"]["source_processing_authorized"] is False
    assert tranches["PR2-SRC-D"]["pull_request"] == PR2_SRC_D_PR
    assert tranches["PR2-SRC-D"]["branch_head"] == PR2_SRC_D_HEAD
    assert tranches["PR2-SRC-D"]["merge_commit"] == PR2_SRC_D_MERGE
    assert tranches["PR2-SRC-D"]["merge_tree"] == PR2_SRC_D_TREE

    org = by_id["PR2-ORG"]
    assert org["status"] == "merged"
    assert org["authorization_reference"] == PR2_ORG_AUTHORIZATION
    assert org["authority_effect"] == PR2_ORG_EFFECT
    assert org["starting_baseline"] == PR2_ORG_BASELINE
    assert org["control_artifact"] == PR2_ORG_CONTRACT
    assert set(org["owned_paths"]) == PR2_ORG_OWNED_PATHS
    assert org["pull_request"] == PR2_ORG_PR
    assert org["branch_head"] == PR2_ORG_HEAD
    assert org["merge_commit"] == PR2_ORG_MERGE
    assert org["completion_state"] == "merged"
    assert org["post_merge_closure_authorization_reference"] == PR2_ORG_CLOSURE_AUTHORIZATION
    assert org["post_merge_closure_authority_effect"] == PR2_ORG_CLOSURE_EFFECT
    assert org["post_merge_closure_recorded_from"] == PR2_ORG_MERGE
    assert org["post_merge_closure_tree"] == PR2_ORG_TREE

    ir = by_id["PR2-IR"]
    assert ir["status"] == "merged"
    assert ir["authorization_reference"] == PR2_IR_AUTHORIZATION
    assert ir["authority_effect"] == PR2_IR_EFFECT
    assert ir["starting_baseline"] == PR2_IR_BASELINE
    assert ir["control_artifact"] == PR2_IR_CONTRACT
    assert set(ir["owned_paths"]) == PR2_IR_OWNED_PATHS
    assert ir["pull_request"] == PR2_IR_PR
    assert ir["branch_head"] == PR2_IR_HEAD
    assert ir["merge_commit"] == PR2_IR_MERGE
    assert ir["completion_state"] == "merged"
    assert ir["post_merge_closure_authorization_reference"] == PR2_IR_CLOSURE_AUTHORIZATION
    assert ir["post_merge_closure_authority_effect"] == PR2_IR_CLOSURE_EFFECT
    assert ir["post_merge_closure_recorded_from"] == PR2_IR_MERGE
    assert ir["post_merge_closure_tree"] == PR2_IR_TREE

    corpus = by_id["PR2-CORPUS"]
    assert corpus["status"] == "merged"
    assert corpus["authorization_reference"] == PR2_CORPUS_AUTHORIZATION
    assert corpus["authority_effect"] == PR2_CORPUS_EFFECT
    assert corpus["starting_baseline"] == PR2_CORPUS_BASELINE
    assert corpus["control_artifact"] == PR2_CORPUS_CONTRACT
    assert set(corpus["owned_paths"]) == PR2_CORPUS_OWNED_PATHS
    assert corpus["pull_request"] == PR2_CORPUS_PR
    assert corpus["branch_head"] == PR2_CORPUS_HEAD
    assert corpus["merge_commit"] == PR2_CORPUS_MERGE
    assert corpus["completion_state"] == "merged"
    assert corpus["post_merge_closure_authorization_reference"] == PR2_CORPUS_CLOSURE_AUTHORIZATION
    assert corpus["post_merge_closure_authority_effect"] == PR2_CORPUS_CLOSURE_EFFECT
    assert corpus["post_merge_closure_recorded_from"] == PR2_CORPUS_MERGE
    assert corpus["post_merge_closure_tree"] == PR2_CORPUS_TREE

    fict = by_id["PR2-FICT"]
    assert fict["status"] == "merged"
    assert fict["authorization_reference"] == PR2_FICT_AUTHORIZATION
    assert fict["authority_effect"] == PR2_FICT_EFFECT
    assert fict["starting_baseline"] == PR2_FICT_BASELINE
    assert fict["control_artifact"] == PR2_FICT_CONTRACT
    assert set(fict["owned_paths"]) == PR2_FICT_OWNED_PATHS
    assert fict["pull_request"] == PR2_FICT_PR
    assert fict["branch_head"] == PR2_FICT_HEAD
    assert fict["merge_commit"] == PR2_FICT_MERGE
    assert fict["completion_state"] == "merged"
    assert fict["post_merge_closure_authorization_reference"] == PR2_FICT_CLOSURE_AUTHORIZATION
    assert fict["post_merge_closure_authority_effect"] == PR2_FICT_CLOSURE_EFFECT
    assert fict["post_merge_closure_recorded_from"] == PR2_FICT_MERGE
    assert fict["post_merge_closure_tree"] == PR2_FICT_TREE

    simex = by_id["PR2-SIMEX"]
    assert simex["status"] == "merged"
    assert simex["authorization_reference"] == PR2_SIMEX_AUTHORIZATION
    assert simex["authority_effect"] == PR2_SIMEX_EFFECT
    assert simex["starting_baseline"] == PR2_SIMEX_BASELINE
    assert simex["control_artifact"] == PR2_SIMEX_CONTRACT
    assert set(simex["owned_paths"]) == PR2_SIMEX_OWNED_PATHS
    assert simex["pull_request"] == PR2_SIMEX_PR
    assert simex["branch_head"] == PR2_SIMEX_HEAD
    assert simex["merge_commit"] == PR2_SIMEX_MERGE
    assert simex["completion_state"] == "merged"
    assert simex["post_merge_closure_authorization_reference"] == PR2_SIMEX_CLOSURE_AUTHORIZATION
    assert simex["post_merge_closure_authority_effect"] == PR2_SIMEX_CLOSURE_EFFECT
    assert simex["post_merge_closure_recorded_from"] == PR2_SIMEX_MERGE
    assert simex["post_merge_closure_tree"] == PR2_SIMEX_TREE

    scale = by_id["PR2-SCALE"]
    assert scale["status"] == "merged"
    assert scale["authorization_reference"] == PR2_SCALE_AUTHORIZATION
    assert scale["authority_effect"] == PR2_SCALE_EFFECT
    assert scale["starting_baseline"] == PR2_SCALE_BASELINE
    assert scale["control_artifact"] == PR2_SCALE_CONTRACT
    assert set(scale["owned_paths"]) == PR2_SCALE_OWNED_PATHS
    assert scale["pull_request"] == PR2_SCALE_PR
    assert scale["branch_head"] == PR2_SCALE_HEAD
    assert scale["merge_commit"] == PR2_SCALE_MERGE
    assert scale["completion_state"] == "merged"
    assert scale["post_merge_closure_authorization_reference"] == PR2_SCALE_CLOSURE_AUTHORIZATION
    assert scale["post_merge_closure_authority_effect"] == PR2_SCALE_CLOSURE_EFFECT
    assert scale["post_merge_closure_recorded_from"] == PR2_SCALE_MERGE
    assert scale["post_merge_closure_tree"] == PR2_SCALE_TREE

    part = by_id["PR2-PART"]
    assert part["status"] == "merged"
    assert part["authorization_reference"] == PR2_PART_AUTHORIZATION
    assert part["authority_effect"] == PR2_PART_EFFECT
    assert part["starting_baseline"] == PR2_PART_BASELINE
    assert part["control_artifact"] == PR2_PART_CONTRACT
    assert set(part["owned_paths"]) == PR2_PART_OWNED_PATHS
    assert part["pull_request"] == PR2_PART_PR
    assert part["branch_head"] == PR2_PART_HEAD
    assert part["merge_commit"] == PR2_PART_MERGE
    assert part["completion_state"] == "merged"
    assert part["post_merge_closure_authorization_reference"] == PR2_PART_CLOSURE_AUTHORIZATION
    assert part["post_merge_closure_authority_effect"] == PR2_PART_CLOSURE_EFFECT
    assert part["post_merge_closure_recorded_from"] == PR2_PART_MERGE
    assert part["post_merge_closure_tree"] == PR2_PART_TREE

    conc = by_id["PR2-CONC"]
    assert conc["status"] == "merged"
    assert conc["authorization_reference"] == PR2_CONC_AUTHORIZATION
    assert conc["authority_effect"] == PR2_CONC_EFFECT
    assert conc["starting_baseline"] == PR2_CONC_BASELINE
    assert conc["control_artifact"] == PR2_CONC_CONTRACT
    assert set(conc["owned_paths"]) == PR2_CONC_OWNED_PATHS
    assert conc["downstream_handoff"] == ["PR2-EVENT"]
    assert conc["pull_request"] == PR2_CONC_PR
    assert conc["branch_head"] == PR2_CONC_HEAD
    assert conc["merge_commit"] == PR2_CONC_MERGE
    assert conc["completion_state"] == "merged"
    assert conc["post_merge_closure_authorization_reference"] == PR2_CONC_CLOSURE_AUTHORIZATION
    assert conc["post_merge_closure_authority_effect"] == PR2_CONC_CLOSURE_EFFECT
    assert conc["post_merge_closure_recorded_from"] == PR2_CONC_MERGE
    assert conc["post_merge_closure_tree"] == PR2_CONC_TREE

    event = by_id["PR2-EVENT"]
    assert event["status"] == "merged"
    assert event["authorization_reference"] == PR2_EVENT_AUTHORIZATION
    assert event["authority_effect"] == PR2_EVENT_EFFECT
    assert event["starting_baseline"] == PR2_EVENT_BASELINE
    assert event["control_artifact"] == PR2_EVENT_CONTRACT
    assert set(event["owned_paths"]) == PR2_EVENT_OWNED_PATHS
    assert event["downstream_handoff"] == ["PR2-PERSIST", "PR2-TEST"]
    assert event["pull_request"] == PR2_EVENT_PR
    assert event["branch_head"] == PR2_EVENT_HEAD
    assert event["merge_commit"] == PR2_EVENT_MERGE
    assert event["completion_state"] == "merged"
    assert event["post_merge_closure_authorization_reference"] == PR2_EVENT_CLOSURE_AUTHORIZATION
    assert event["post_merge_closure_authority_effect"] == PR2_EVENT_CLOSURE_EFFECT
    assert event["post_merge_closure_recorded_from"] == PR2_EVENT_MERGE
    assert event["post_merge_closure_tree"] == PR2_EVENT_TREE

    persist = by_id["PR2-PERSIST"]
    assert persist["status"] == "merged"
    assert persist["authorization_reference"] == PR2_PERSIST_AUTHORIZATION
    assert persist["authority_effect"] == PR2_PERSIST_EFFECT
    assert persist["starting_baseline"] == PR2_PERSIST_BASELINE
    assert persist["control_artifact"] == PR2_PERSIST_CONTRACT
    assert set(persist["owned_paths"]) == PR2_PERSIST_OWNED_PATHS
    assert persist["downstream_handoff"] == ["PR2-FID", "PR2-TEST"]
    assert persist["pull_request"] == PR2_PERSIST_PR
    assert persist["branch_head"] == PR2_PERSIST_HEAD
    assert persist["merge_commit"] == PR2_PERSIST_MERGE
    assert persist["completion_state"] == "merged"
    assert persist["post_merge_closure_authorization_reference"] == PR2_PERSIST_CLOSURE_AUTHORIZATION
    assert persist["post_merge_closure_authority_effect"] == PR2_PERSIST_CLOSURE_EFFECT
    assert persist["post_merge_closure_recorded_from"] == PR2_PERSIST_MERGE
    assert persist["post_merge_closure_tree"] == PR2_PERSIST_TREE

    fid = by_id["PR2-FID"]
    assert fid["status"] == "merged"
    assert fid["authorization_reference"] == PR2_FID_AUTHORIZATION
    assert fid["authority_effect"] == PR2_FID_EFFECT
    assert fid["starting_baseline"] == PR2_FID_BASELINE
    assert fid["control_artifact"] == PR2_FID_CONTRACT
    assert set(fid["owned_paths"]) == PR2_FID_OWNED_PATHS
    assert fid["downstream_handoff"] == ["PR2-BP", "PR2-TEST"]
    assert fid["pull_request"] == PR2_FID_PR
    assert fid["branch_head"] == PR2_FID_HEAD
    assert fid["merge_commit"] == PR2_FID_MERGE
    assert fid["completion_state"] == "merged"
    assert fid["post_merge_closure_authorization_reference"] == PR2_FID_CLOSURE_AUTHORIZATION
    assert fid["post_merge_closure_authority_effect"] == PR2_FID_CLOSURE_EFFECT
    assert fid["post_merge_closure_recorded_from"] == PR2_FID_MERGE
    assert fid["post_merge_closure_tree"] == PR2_FID_TREE

    bp = by_id["PR2-BP"]
    assert bp["status"] == "merged"
    assert bp["authorization_reference"] == PR2_BP_AUTHORIZATION
    assert bp["authority_effect"] == PR2_BP_EFFECT
    assert bp["starting_baseline"] == PR2_BP_BASELINE
    assert bp["control_artifact"] == PR2_BP_CONTRACT
    assert set(bp["owned_paths"]) == PR2_BP_OWNED_PATHS
    assert bp["downstream_handoff"] == ["PR2-TEST"]
    assert bp["pull_request"] == PR2_BP_PR
    assert bp["branch_head"] == PR2_BP_HEAD
    assert bp["merge_commit"] == PR2_BP_MERGE
    assert bp["completion_state"] == "merged"
    assert (
        bp["post_merge_closure_authorization_reference"]
        == PR2_BP_CLOSURE_AUTHORIZATION
    )
    assert (
        bp["post_merge_closure_authority_effect"]
        == PR2_BP_CLOSURE_EFFECT
    )
    assert (
        bp["post_merge_closure_recorded_from"]
        == PR2_BP_MERGE
    )
    assert bp["post_merge_closure_tree"] == PR2_BP_TREE

    mig = by_id["PR2-MIG"]

    assert mig["status"] == "merged"

    # Overall workstream provenance remains anchored to the
    # original PR2-MIG activation.
    assert (
        mig["authorization_reference"]
        == PR2_MIG_A_AUTHORIZATION
    )
    assert mig["starting_baseline"] == PR2_MIG_A_BASELINE

    assert mig["current_tranche"] == "PR2-MIG-B"
    assert (
        mig["current_tranche_candidate_id"]
        == PR2_MIG_B_CANDIDATE
    )
    assert mig["current_tranche_state"] == "merged"

    assert (
        mig["current_tranche_authorization_reference"]
        == PR2_MIG_B_AUTHORIZATION
    )
    assert (
        mig["current_tranche_authority_effect"]
        == PR2_MIG_B_EFFECT
    )
    assert (
        mig["current_tranche_starting_baseline"]
        == PR2_MIG_B_BASELINE
    )
    assert (
        mig["current_tranche_target_path"]
        == PR2_MIG_B_TARGET
    )

    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []

    assert mig["remaining_candidate_ids"] == []
    assert mig["next_candidate_id"] is None
    assert mig["next_candidate_authorized"] is False
    assert mig["next_tranche_id"] is None
    assert mig["next_tranche_authorized"] is False
    assert mig["next_tranche_state"] is None
    assert mig["next_tranche_candidate_id"] is None

    assert (
        mig["current_tranche_completion_state"]
        == "merged"
    )
    assert mig["current_tranche_validation_state"] == "validated"
    assert mig["current_tranche_candidate_validated"] is True

    assert (
        mig["current_tranche_runtime_promotion_authorized"]
        is False
    )

    assert mig["pull_request"] == PR2_MIG_B_PR
    assert mig["branch_head"] == PR2_MIG_B_HEAD
    assert mig["merge_commit"] == PR2_MIG_B_MERGE

    assert (
        mig["current_tranche_pull_request"]
        == PR2_MIG_B_PR
    )
    assert (
        mig["current_tranche_branch_head"]
        == PR2_MIG_B_HEAD
    )
    assert (
        mig["current_tranche_merge_commit"]
        == PR2_MIG_B_MERGE
    )
    assert (
        mig["current_tranche_merge_tree"]
        == PR2_MIG_B_TREE
    )

    assert (
        mig["post_merge_closure_authorization_reference"]
        == PR2_MIG_B_CLOSURE_AUTHORIZATION
    )
    assert (
        mig["post_merge_closure_authority_effect"]
        == PR2_MIG_B_CLOSURE_EFFECT
    )
    assert (
        mig["post_merge_closure_recorded_from"]
        == PR2_MIG_B_MERGE
    )
    assert (
        mig["post_merge_closure_tree"]
        == PR2_MIG_B_TREE
    )

    assert mig["completed_tranches"] == [
        {
            "tranche_id": "PR2-MIG-A",
            "candidate_id": "R2A-DISPOSITION-RS-0028",
            "state": "merged",
            "authorization_reference":
                PR2_MIG_A_AUTHORIZATION,
            "authority_effect": PR2_MIG_A_EFFECT,
            "starting_baseline": PR2_MIG_A_BASELINE,
            "target_path": PR2_MIG_A_TARGET,
            "pull_request": PR2_MIG_A_PR,
            "branch_head": PR2_MIG_A_HEAD,
            "merge_commit": PR2_MIG_A_MERGE,
            "merge_tree": PR2_MIG_A_TREE,
            "validation_state": "validated",
            "ci_run": 234,
            "ci_run_id": 35396966183,
            "ci_result": "success",
        },
        {
            "tranche_id": "PR2-MIG-B",
            "candidate_id": PR2_MIG_B_CANDIDATE,
            "state": "merged",
            "authorization_reference":
                PR2_MIG_B_AUTHORIZATION,
            "authority_effect": PR2_MIG_B_EFFECT,
            "starting_baseline": PR2_MIG_B_BASELINE,
            "target_path": PR2_MIG_B_TARGET,
            "pull_request": PR2_MIG_B_PR,
            "branch_head": PR2_MIG_B_HEAD,
            "merge_commit": PR2_MIG_B_MERGE,
            "merge_tree": PR2_MIG_B_TREE,
            "validation_state": "validated",
            "ci_run": PR2_MIG_B_CI_RUN,
            "ci_run_id": PR2_MIG_B_CI_RUN_ID,
            "ci_result": "success",
        },
    ]

    audit_target = manifest["pr2_audit_completion_target"]

    assert audit_target["current_migration_required_count"] == 0
    assert audit_target["migration_required_candidate_ids"] == []
    assert (
        audit_target["pr2_mig_last_completed_tranche"]
        == "PR2-MIG-B"
    )
    assert (
        audit_target["pr2_mig_last_completed_candidate_id"]
        == PR2_MIG_B_CANDIDATE
    )
    assert audit_target["pr2_mig_next_tranche"] is None
    assert audit_target["pr2_mig_next_candidate_id"] is None
    assert (
        audit_target["pr2_mig_next_ready_pending_authorization"]
        is False
    )



def test_pr2_mig_terminal_closure_validation_evidence_is_exact():
    manifest = _load_manifest()
    mig = _by_id(manifest)["PR2-MIG"]

    assert mig["validation_evidence"][-5:] == ['PR2-MIG-B post-merge closure bounded regression:442 passed, 3 skipped', 'PR2-MIG-B post-merge closure full local repository suite:9273 passed, 10 skipped, 2 xfailed, 1 warning', 'PR2-MIG-B post-merge closure focused post-suite certification:80 passed, 1 skipped', 'PR2-MIG-B post-merge closure exact five-file footprint:PASS', 'PR2-MIG-B post-merge closure runtime/schema noninterference:PASS']

    assert mig["status"] == "merged"
    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []

    target = manifest["pr2_audit_completion_target"]

    assert target["current_migration_required_count"] == 0
    assert target["migration_required_candidate_ids"] == []


def test_post_r2_successor_readiness_does_not_imply_authorization():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    org = by_id["PR2-ORG"]
    assert org["status"] == "merged"
    assert org["authorization_reference"] == PR2_ORG_AUTHORIZATION
    assert org["post_merge_closure_authorization_reference"] == PR2_ORG_CLOSURE_AUTHORIZATION

    ir = by_id["PR2-IR"]
    assert ir["status"] == "merged"
    assert ir["authorization_reference"] == PR2_IR_AUTHORIZATION
    assert ir["starting_baseline"] == PR2_IR_BASELINE
    assert ir["post_merge_closure_authorization_reference"] == PR2_IR_CLOSURE_AUTHORIZATION

    corpus = by_id["PR2-CORPUS"]
    assert corpus["status"] == "merged"
    assert corpus["authorization_reference"] == PR2_CORPUS_AUTHORIZATION
    assert corpus["starting_baseline"] == PR2_CORPUS_BASELINE
    assert corpus["post_merge_closure_authorization_reference"] == PR2_CORPUS_CLOSURE_AUTHORIZATION

    fict = by_id["PR2-FICT"]
    assert fict["status"] == "merged"
    assert fict["authorization_reference"] == PR2_FICT_AUTHORIZATION
    assert fict["starting_baseline"] == PR2_FICT_BASELINE
    assert fict["post_merge_closure_authorization_reference"] == PR2_FICT_CLOSURE_AUTHORIZATION

    simex = by_id["PR2-SIMEX"]
    assert simex["status"] == "merged"
    assert simex["authorization_reference"] == PR2_SIMEX_AUTHORIZATION
    assert simex["starting_baseline"] == PR2_SIMEX_BASELINE
    assert simex["post_merge_closure_authorization_reference"] == PR2_SIMEX_CLOSURE_AUTHORIZATION

    scale = by_id["PR2-SCALE"]
    assert scale["status"] == "merged"
    assert scale["authorization_reference"] == PR2_SCALE_AUTHORIZATION
    assert scale["starting_baseline"] == PR2_SCALE_BASELINE
    assert scale["post_merge_closure_authorization_reference"] == PR2_SCALE_CLOSURE_AUTHORIZATION

    part = by_id["PR2-PART"]
    assert part["status"] == "merged"
    assert part["authorization_reference"] == PR2_PART_AUTHORIZATION
    assert part["starting_baseline"] == PR2_PART_BASELINE
    assert part["post_merge_closure_authorization_reference"] == PR2_PART_CLOSURE_AUTHORIZATION

    conc = by_id["PR2-CONC"]
    assert conc["status"] == "merged"
    assert conc["authorization_reference"] == PR2_CONC_AUTHORIZATION
    assert conc["starting_baseline"] == PR2_CONC_BASELINE
    assert conc["post_merge_closure_authorization_reference"] == PR2_CONC_CLOSURE_AUTHORIZATION

    event = by_id["PR2-EVENT"]
    assert event["status"] == "merged"
    assert event["authorization_reference"] == PR2_EVENT_AUTHORIZATION
    assert event["starting_baseline"] == PR2_EVENT_BASELINE
    assert event["control_artifact"] == PR2_EVENT_CONTRACT
    assert event["post_merge_closure_authorization_reference"] == PR2_EVENT_CLOSURE_AUTHORIZATION

    persist = by_id["PR2-PERSIST"]
    assert persist["status"] == "merged"
    assert persist["authorization_reference"] == PR2_PERSIST_AUTHORIZATION
    assert persist["starting_baseline"] == PR2_PERSIST_BASELINE
    assert persist["control_artifact"] == PR2_PERSIST_CONTRACT
    assert persist["post_merge_closure_authorization_reference"] == PR2_PERSIST_CLOSURE_AUTHORIZATION

    fid = by_id["PR2-FID"]
    assert fid["status"] == "merged"
    assert fid["authorization_reference"] == PR2_FID_AUTHORIZATION
    assert fid["starting_baseline"] == PR2_FID_BASELINE
    assert fid["control_artifact"] == PR2_FID_CONTRACT
    assert fid["post_merge_closure_authorization_reference"] == PR2_FID_CLOSURE_AUTHORIZATION

    bp = by_id["PR2-BP"]
    assert bp["status"] == "merged"
    assert bp["authorization_reference"] == PR2_BP_AUTHORIZATION
    assert bp["starting_baseline"] == PR2_BP_BASELINE
    assert bp["control_artifact"] == PR2_BP_CONTRACT
    assert (
        bp["post_merge_closure_authorization_reference"]
        == PR2_BP_CLOSURE_AUTHORIZATION
    )

    audit = by_id["PR2-AUDIT"]

    assert audit["status"] == "merged"
    assert audit["authorization_reference"] == PR2_AUDIT_A_AUTHORIZATION
    assert audit["authority_effect"] == PR2_AUDIT_A_EFFECT
    assert audit["starting_baseline"] == PR2_AUDIT_A_BASELINE

    assert audit["completed_tranches"] == [
        {
            "tranche_id": "PR2-AUDIT-A",
            "state": "merged",
            "authorization_reference": PR2_AUDIT_A_AUTHORIZATION,
            "pull_request": AUDIT_A_PR,
            "branch_head": AUDIT_A_HEAD,
            "merge_commit": AUDIT_A_MERGE,
            "merge_tree": AUDIT_A_TREE,
            "review_artifact": PR2_AUDIT_A_REVIEW,
            "validation_state": "validated",
        },
        {
            "tranche_id": "PR2-AUDIT-B",
            "alias": "R4-0",
            "state": "merged",
            "authorization_reference": R4_0_AUTHORIZATION,
            "pull_request": R4_0_PR,
            "branch_head": R4_0_HEAD,
            "merge_commit": R4_0_MERGE,
            "merge_tree": R4_0_TREE,
            "review_artifact": R4_0_REVIEW,
            "validation_state": "validated",
        },
        {
            "tranche_id": "PR2-AUDIT-C",
            "alias": "R4-A",
            "state": "merged",
            "authorization_reference": R4_A_AUTHORIZATION,
            "pull_request": R4_A_PR,
            "branch_head": R4_A_HEAD,
            "merge_commit": R4_A_MERGE,
            "merge_tree": R4_A_TREE,
            "review_artifact": R4_A_REVIEW,
            "validation_state": "validated",
        },
        {
            "tranche_id": "PR2-AUDIT-D",
            "alias": "AUDIT-CLOSE",
            "state": "merged",
            "authorization_reference": AUDIT_D_AUTHORIZATION,
            "pull_request": AUDIT_D_PR,
            "branch_head": AUDIT_D_HEAD,
            "merge_commit": AUDIT_D_MERGE,
            "merge_tree": AUDIT_D_TREE,
            "review_artifact": AUDIT_D_REVIEW,
            "validation_state": "validated",
        },
    ]

    assert audit["current_tranche"] == "PR2-AUDIT-D"
    assert audit["current_tranche_alias"] == "AUDIT-CLOSE"
    assert audit["current_tranche_state"] == "merged"
    assert (
        audit["current_tranche_repository_wide_audit_complete"]
        is True
    )
    assert audit["current_tranche_completion_state"] == (
        "merged_repository_wide_audit_complete"
    )

    assert audit["pull_request"] == AUDIT_D_PR
    assert audit["branch_head"] == AUDIT_D_HEAD
    assert audit["merge_commit"] == AUDIT_D_MERGE

    assert (
        audit["post_merge_closure_authorization_reference"]
        == PR2_AUDIT_CLOSURE_AUTHORIZATION
    )
    assert (
        audit["post_merge_closure_authority_effect"]
        == PR2_AUDIT_CLOSURE_EFFECT
    )
    assert (
        audit["post_merge_closure_recorded_from"]
        == AUDIT_D_MERGE
    )
    assert audit["post_merge_closure_tree"] == AUDIT_D_TREE

    for workstream_id in POST_R2_READY:
        assert by_id[workstream_id]["status"] == "ready_pending_authorization"
        assert by_id[workstream_id]["authorization_reference"] is None

    for workstream_id in POST_R2_ACTIVE:
        assert by_id[workstream_id]["status"] == "active"
        assert (
            by_id[workstream_id]["authorization_reference"]
            == PR2_IMPL_AUTHORIZATION
        )

    for workstream_id in POST_R2_BLOCKED:
        assert by_id[workstream_id]["status"] == "blocked"
        assert by_id[workstream_id]["authorization_reference"] is None


def test_critical_dependency_chain_is_preserved():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    assert by_id["PR2-R2B-C"]["dependencies"] == ["PR2-CTRL"]
    assert by_id["PR2-R2B-X"]["dependencies"] == ["PR2-R2B-C"]
    assert by_id["PR2-R2B-N"]["dependencies"] == ["PR2-R2B-X"]
    assert set(by_id["PR2-R2C"]["dependencies"]) == {
        "PR2-R2B-C",
        "PR2-R2B-X",
        "PR2-R2B-N",
    }
    assert by_id["PR2-SRC"]["dependencies"] == ["PR2-CTRL"]
    assert set(by_id["PR2-AUDIT"]["dependencies"]) == {
        "PR2-ID",
        "PR2-SRC",
        "PR2-ORG",
        "PR2-CORPUS",
        "PR2-IR",
        "PR2-SCALE",
    }
    assert set(by_id["PR2-PERSIST"]["dependencies"]) == {
        "PR2-SCALE",
        "PR2-R2B-C",
        "PR2-R2B-X",
        "PR2-R2B-N",
    }
    assert set(by_id["PR2-IMPL"]["dependencies"]) == {
        "PR2-R2C",
        "PR2-MIG",
        "PR2-TEST",
    }


def test_program_and_manifest_retain_required_current_cross_references():
    program = PROGRAM_PATH.read_text(encoding="utf-8")
    manifest = _load_manifest()

    assert "**Artifact version:** `0.4.82`" in program
    assert EXPECTED_BASELINE in program
    assert R2B_CORE_BASELINE in program
    assert R2B_CROSS_PHASE_BASELINE in program
    assert R2B_CONTINUITY_BASELINE in program
    assert R2C_BASELINE in program
    assert R2C_AUTHORIZATION in program
    assert "Myravant" in program
    assert "1,000+" in program
    assert "Review result:\n\n`PASS`" in program
    assert "`R3=ready_pending_authorization`" in program
    assert "exactly `34` such records" in program

    for package in EXPECTED_R2B_SEQUENCE:
        assert package in program

    for workstream_id in EXPECTED_WORKSTREAM_IDS:
        assert workstream_id in program

    assert (
        "Logical simulation semantics must remain independent of physical execution topology."
        in program
    )
    assert (
        manifest["program_document"]
        == "docs/doctrine/control/post_r2a_transition_program.md"
    )


def test_program_explicitly_preserves_successor_authorization_boundaries():
    program = PROGRAM_PATH.read_text(encoding="utf-8")

    # R2C itself did not activate a successor. PR2-ID was authorized later
    # through its own explicit owner directive.
    assert "R2C completion did not automatically activate a successor." in program
    assert "`PR2-ID` is `merged` through PR `#380`" in program
    assert "`R3` remains `ready_pending_authorization`" in program
    assert "### 5.9 PR2-SRC-A foundational source research governance" in program
    assert "### 5.10 PR2-SRC-B heterogeneous research-method qualification" in program
    assert "### 5.11 PR2-SRC-C legacy source/conversion surface disposition" in program
    assert "### 5.12 PR2-SRC-D independent completion review" in program
    assert "### 5.13 PR2-SRC post-merge closure recording" in program
    assert "`PR2-SRC` is terminal `merged`" in program
    assert "### 5.14 PR2-ORG originality, provenance, and content-eligibility activation" in program
    assert "### 5.15 PR2-ORG post-merge closure recording" in program
    assert "PR2-ORG is\nterminal `merged`" in program
    assert "### 5.16 PR2-IR source-analysis / Myravant-design information-barrier activation" in program
    assert "### 5.17 PR2-IR post-merge closure recording" in program
    assert "PR2-IR is terminal `merged`" in program
    assert PR2_IR_AUTHORIZATION in program
    assert PR2_IR_BASELINE in program
    assert PR2_IR_CONTRACT in program
    assert PR2_IR_CLOSURE_AUTHORIZATION in program
    assert PR2_IR_MERGE in program
    assert "### 5.18 PR2-CORPUS corpus-scale coverage-governance activation" in program
    assert PR2_CORPUS_AUTHORIZATION in program
    assert PR2_CORPUS_BASELINE in program
    assert PR2_CORPUS_CONTRACT in program
    assert "### 5.19 PR2-CORPUS post-merge closure recording" in program
    assert "PR2-CORPUS is terminal `merged`" in program
    assert PR2_CORPUS_CLOSURE_AUTHORIZATION in program
    assert PR2_CORPUS_MERGE in program
    assert "### 5.20 PR2-FICT fiction/LitRPG experience-pressure activation" in program
    assert PR2_FICT_AUTHORIZATION in program
    assert PR2_FICT_BASELINE in program
    assert PR2_FICT_CONTRACT in program
    assert "### 5.21 PR2-FICT post-merge closure recording" in program
    assert "PR2-FICT is terminal `merged`" in program
    assert PR2_FICT_CLOSURE_AUTHORIZATION in program
    assert PR2_FICT_MERGE in program
    assert "### 5.22 PR2-SIMEX simulation/infrastructure exemplar-pressure activation" in program
    assert PR2_SIMEX_AUTHORIZATION in program
    assert PR2_SIMEX_BASELINE in program
    assert PR2_SIMEX_CONTRACT in program
    assert "PR2-SIMEX is the only active successor workstream." in program
    assert "PR2-SCALE remains `blocked`" in program
    assert "### 5.23 PR2-SIMEX post-merge closure recording" in program
    assert "PR2-SIMEX is terminal `merged`" in program
    assert PR2_SIMEX_CLOSURE_AUTHORIZATION in program
    assert PR2_SIMEX_MERGE in program
    assert "No successor is active." in program
    assert "### 5.24 PR2-SCALE runtime scalability and execution-topology activation" in program
    assert PR2_SCALE_AUTHORIZATION in program
    assert PR2_SCALE_BASELINE in program
    assert PR2_SCALE_CONTRACT in program
    assert "PR2-SCALE is the only active successor workstream." in program
    assert "No downstream runtime workstream is activated by this decision." in program
    assert "### 5.25 PR2-SCALE post-merge closure recording" in program
    assert "PR2-SCALE is terminal `merged`." in program
    assert PR2_SCALE_CLOSURE_AUTHORIZATION in program
    assert PR2_SCALE_MERGE in program
    assert "No successor is active after PR2-SCALE closure." in program
    assert "### 5.26 PR2-PART authority partitioning and migration activation" in program
    assert PR2_PART_AUTHORIZATION in program
    assert PR2_PART_BASELINE in program
    assert PR2_PART_CONTRACT in program
    assert "PR2-PART is the only active successor workstream." in program
    assert "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3" in program
    assert "### 5.27 PR2-PART post-merge closure recording" in program
    assert PR2_PART_CLOSURE_AUTHORIZATION in program
    assert PR2_PART_MERGE in program
    assert PR2_PART_TREE in program
    assert "No successor is active after PR2-PART closure." in program
    assert "PR2-CONC remains `blocked` and unauthorized." in program
    assert "### 5.28 PR2-CONC deterministic concurrency and scheduling activation" in program
    assert PR2_CONC_AUTHORIZATION in program
    assert PR2_CONC_BASELINE in program
    assert PR2_CONC_CONTRACT in program
    assert "PR2-CONC is the only active successor workstream." in program
    assert "PR2-EVENT remains `blocked` and unauthorized." in program
    assert "### 5.29 PR2-CONC post-merge closure recording" in program
    assert PR2_CONC_CLOSURE_AUTHORIZATION in program
    assert PR2_CONC_MERGE in program
    assert PR2_CONC_TREE in program
    assert "No successor is active after PR2-CONC closure." in program
    assert "### 5.30 PR2-EVENT command/event/message/projection activation" in program
    assert PR2_EVENT_AUTHORIZATION in program
    assert PR2_EVENT_BASELINE in program
    assert PR2_EVENT_CONTRACT in program
    assert "PR2-EVENT is the only active successor workstream." in program
    assert "PR2-PERSIST remains `blocked` and unauthorized." in program
    assert "### 5.31 PR2-EVENT post-merge closure recording" in program
    assert PR2_EVENT_CLOSURE_AUTHORIZATION in program
    assert PR2_EVENT_HEAD in program
    assert PR2_EVENT_MERGE in program
    assert PR2_EVENT_TREE in program
    assert "PR2-EVENT is terminal `merged`." in program
    assert "No successor is active after PR2-EVENT closure." in program
    assert "### 5.32 PR2-PERSIST persistence/recovery activation" in program
    assert PR2_PERSIST_AUTHORIZATION in program
    assert PR2_PERSIST_BASELINE in program
    assert PR2_PERSIST_CONTRACT in program
    assert "PR2-PERSIST is the only active runtime successor workstream." in program
    assert "PR2-FID remains `blocked` and unauthorized." in program
    assert "PR2-BP remains `blocked` and unauthorized." in program
    assert "### 5.33 PR2-PERSIST post-merge closure recording" in program
    assert PR2_PERSIST_CLOSURE_AUTHORIZATION in program
    assert PR2_PERSIST_HEAD in program
    assert PR2_PERSIST_MERGE in program
    assert PR2_PERSIST_TREE in program
    assert "PR2-PERSIST is terminal `merged`." in program
    assert "No successor is active after PR2-PERSIST closure." in program
    assert "### 5.34 PR2-FID relevance/fidelity/aggregation/reconstitution activation" in program
    assert PR2_FID_AUTHORIZATION in program
    assert PR2_FID_BASELINE in program
    assert PR2_FID_CONTRACT in program
    assert "PR2-FID is the only active runtime successor workstream." in program
    assert "PR2-BP remains `blocked` and unauthorized." in program
    assert "### 5.35 PR2-FID post-merge closure recording" in program
    assert PR2_FID_CLOSURE_AUTHORIZATION in program
    assert PR2_FID_HEAD in program
    assert PR2_FID_MERGE in program
    assert PR2_FID_TREE in program
    assert "PR2-FID is terminal `merged`." in program
    assert "No successor is active after PR2-FID closure." in program
    assert "### 5.36 PR2-BP performance budgets, overload, and backpressure activation" in program
    assert PR2_BP_AUTHORIZATION in program
    assert PR2_BP_BASELINE in program
    assert PR2_BP_CONTRACT in program
    assert "PR2-BP is the only active runtime successor workstream." in program
    assert "PR2-TEST remains blocked and unauthorized." in program
    assert "### 5.37 PR2-BP post-merge closure recording" in program
    assert PR2_BP_CLOSURE_AUTHORIZATION in program
    assert PR2_BP_HEAD in program
    assert PR2_BP_MERGE in program
    assert PR2_BP_TREE in program
    assert "PR2-BP is terminal `merged`." in program
    assert "No successor is active after PR2-BP closure." in program
    assert PR2_ORG_AUTHORIZATION in program
    assert PR2_ORG_BASELINE in program
    assert PR2_ORG_CONTRACT in program
    assert PR2_ORG_HEAD in program
    assert PR2_ORG_MERGE in program
    assert PR2_ORG_TREE in program
    assert PR2_SRC_A_AUTHORIZATION in program
    assert PR2_SRC_A_BASELINE in program
    assert PR2_SRC_A_HEAD in program
    assert PR2_SRC_A_MERGE in program
    assert PR2_SRC_B_AUTHORIZATION in program
    assert PR2_SRC_B_BASELINE in program
    assert PR2_SRC_B_HEAD in program
    assert PR2_SRC_B_MERGE in program
    assert PR2_SRC_C_AUTHORIZATION in program
    assert PR2_SRC_C_BASELINE in program
    assert PR2_SRC_C_HEAD in program
    assert PR2_SRC_C_MERGE in program
    assert PR2_SRC_D_AUTHORIZATION in program
    assert PR2_SRC_D_BASELINE in program
    assert PR2_SRC_D_HEAD in program
    assert PR2_SRC_D_MERGE in program
    assert "PR2-ID identity authority does not transfer authority" in program
    assert "RT-002G=unauthorized" in program
    assert "### 5.4 PR2-ID-T2B audited current-doctrine identity migration" in program
    assert PR2_ID_T2B_AUTHORIZATION in program
    assert PR2_ID_T2B_STARTING_HEAD in program
    assert "### 5.5 PR2-ID-T2C noncurrent identity-surface retention recording" in program
    assert PR2_ID_T2C_AUTHORIZATION in program
    assert PR2_ID_T2C_STARTING_HEAD in program
    assert "### 5.6 PR2-ID-T2D roadmap and registry occurrence adjudication" in program
    assert PR2_ID_T2D_AUTHORIZATION in program
    assert PR2_ID_T2D_STARTING_HEAD in program
    assert "### 5.7 PR2-ID-T2E completion audit recording" in program
    assert PR2_ID_T2E_AUTHORIZATION in program
    assert PR2_ID_T2E_STARTING_HEAD in program

def test_program_completion_rule_forbids_untracked_disappearance():
    manifest = _load_manifest()
    rule = manifest["program_completion_rule"]

    assert rule["untracked_disappearance_allowed"] is False
    assert "terminal state" in rule["required"]
    assert "successor handoff" in rule["required"]



def test_r4_b_current_regression_certified_lifecycle():
    manifest = _load_manifest()

    pr2_impl = next(
        row
        for row in manifest["workstreams"]
        if row["workstream_id"] == "PR2-IMPL"
    )

    candidate = pr2_impl["first_playable_candidate"]
    target = manifest["r4_native_substrate_design_target"]

    state = "merged_complete"

    # PR2-IMPL remains terminal.
    assert pr2_impl["status"] == "merged"

    # R4-B is separately authorized and regression-certified.
    assert candidate["authorized"] is True
    assert candidate["implementation_state"] == state
    assert candidate["regression_certified"] is True

    assert pr2_impl["r4_b_authorized"] is True

    assert target["r4_b_authorized"] is True
    assert target["r4_b_implementation_state"] == state
    assert target["r4_b_regression_certified"] is True

    certification = target["r4_b_regression_certification"]

    assert certification[
        "focused_pre_regression"
    ]["passed"] == 241

    assert certification[
        "broader_pr2_regression"
    ]["passed"] == 415

    assert certification[
        "full_repository_regression"
    ]["passed"] == 9378

    assert certification[
        "focused_post_suite_regression"
    ]["passed"] == 316

    recovery = target["r4_b_failure_recovery_evidence"]

    assert recovery[
        "failed_full_repository_regression"
    ]["failed"] == 40

    assert (
        recovery["classification"]
        == "stale_runtime_domain_authorization_guardrails"
    )

    assert recovery["r4_b_behavioral_defect_detected"] is False

    # R4-B certification does not activate downstream authority.
    assert target["schema_edits_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_clear"] is False

    assert pr2_impl["r4_activation_authorized"] is False
    assert pr2_impl["runtime_promotion_authorized"] is False



def test_r4_b_post_merge_closure_is_terminal_and_bounded():
    manifest = _load_manifest()

    impl = next(
        row
        for row in manifest["workstreams"]
        if row["workstream_id"] == "PR2-IMPL"
    )

    candidate = impl["first_playable_candidate"]
    target = manifest["r4_native_substrate_design_target"]

    state = "merged_complete"

    assert manifest["artifact_version"] == "0.4.82"

    assert candidate["implementation_state"] == state
    assert candidate["post_merge_closure_complete"] is True

    assert target["r4_b_implementation_state"] == state
    assert target["r4_b_post_merge_closure_complete"] is True

    assert (
        target[
            "r4_b_post_merge_closure_authorization_reference"
        ]
        == "owner_directive_2026-09-20_r4_b_post_merge_closure"
    )

    assert (
        target[
            "r4_b_post_merge_closure_authority_effect"
        ]
        == "bounded_r4_b_post_merge_lifecycle_reconciliation_only"
    )

    assert target["r4_b_pull_request"] == 429

    assert (
        target["r4_b_branch_head"]
        == "67837933eaab8cd8089e3f37100c6abfdc21115f"
    )

    assert (
        target["r4_b_merge_commit"]
        == "e49b2997d4c965065975f77b885b1db2a2ebf4db"
    )

    assert (
        target["r4_b_merge_tree"]
        == "51fae436b0dbc9f56c656697a9ba2e4dadcbaf95"
    )

    assert target["r4_b_ci_run"] == 258
    assert target["r4_b_ci_run_id"] == 35531310888

    # PR2-IMPL itself remains terminal.
    assert impl["status"] == "merged"
    assert impl["r4_b_authorized"] is True

    # Closure does not activate downstream authority.
    assert impl["r4_activation_authorized"] is False
    assert impl["runtime_promotion_authorized"] is False

    assert target["schema_edits_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_clear"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_b_post_merge_closure_regression_certification_is_exact():
    manifest = _load_manifest()

    impl = next(
        row
        for row in manifest["workstreams"]
        if row["workstream_id"] == "PR2-IMPL"
    )

    candidate = impl["first_playable_candidate"]
    target = manifest["r4_native_substrate_design_target"]

    assert manifest["artifact_version"] == "0.4.82"

    # R4-B stays terminal; evidence recording is separate.
    assert candidate["implementation_state"] == "merged_complete"
    assert target["r4_b_implementation_state"] == "merged_complete"

    assert (
        candidate["post_merge_closure_regression_certified"]
        is True
    )

    assert (
        candidate["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    assert (
        target["r4_b_post_merge_closure_regression_certified"]
        is True
    )

    assert (
        target["r4_b_post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    cert = target[
        "r4_b_post_merge_closure_regression_certification"
    ]

    assert cert["focused_pre_certification"]["passed"] == 84
    assert cert["broader_pr2_regression"]["passed"] == 417

    assert cert["full_repository_suite"] == {
        "passed": 9382,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert (
        cert["focused_post_suite_regression"]["passed"]
        == 84
    )

    assert cert["changed_path_count"] == 6
    assert cert["runtime_implementation_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    assert (
        impl["r4_b_post_merge_closure_regression_certified"]
        is True
    )

    assert (
        impl["r4_b_post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    # No downstream authority.
    assert impl["r4_activation_authorized"] is False
    assert impl["runtime_promotion_authorized"] is False

    assert target["schema_edits_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_clear"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"
def test_r4_c_current_state_is_implementation_authorized_and_bounded():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["status"] == "merged_complete"
    assert target["package_id"] == "R4-C"

    assert (
        target["package_name"]
        == "persistent_world_playable_movement_integration"
    )

    assert target["package_defined"] is True
    assert target["implementation_authorized"] is True
    assert target["implementation_state"] == "merged_complete"
    assert target["implementation_regression_certified"] is True

    assert (
        target["implementation_authorization_reference"]
        == "owner_directive_2026-09-20_r4_c_implementation_authorization"
    )

    assert (
        target["implementation_starting_baseline"]
        == "9118ec2af6d4afcbf6d597186200f3fb11243776"
    )

    assert (
        target["implementation_starting_tree"]
        == "2d380f53245192a95049c607f6a66d3b634df348"
    )

    assert target["definition_recording_state"] == "merged_complete"
    assert target["definition_pull_request"] == 431

    assert target["post_merge_closure_complete"] is True

    assert (
        target["post_merge_closure_recorded_from"]
        == "8cb6da94894d2b8142d72c4a61fb5335135fe97e"
    )

    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert (
        target[
            "durable_persistence_required_for_initial_slice"
        ]
        is False
    )

    impl = next(
        row
        for row in manifest["workstreams"]
        if row["workstream_id"] == "PR2-IMPL"
    )

    assert impl["status"] == "merged"

    assert (
        impl["completion_state"]
        == "merged_complete_r4_b_ready_pending_authorization"
    )

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

def test_r4_c_definition_certification_evidence_is_preserved():
    manifest = _load_manifest()

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["definition_regression_certified"] is True
    assert target["definition_recording_state"] == "merged_complete"

    cert = target["definition_regression_certification"]

    assert cert["focused_pre_certification"] == {
        "passed": 63,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 468,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9393,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_certification"] == {
        "passed": 63,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 6
    assert cert["production_runtime_path_count"] == 0
    assert cert["production_schema_path_count"] == 0


def test_r4_c_implementation_authorization_does_not_activate_general_r4():
    manifest = _load_manifest()
    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_c_implementation_regression_certification_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["implementation_authorized"] is True
    assert target["implementation_regression_certified"] is True
    assert target["implementation_state"] == "merged_complete"

    cert = target[
        "implementation_regression_certification"
    ]

    assert cert["repaired_rt001e_root_guardrail"] == {
        "passed": 68,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 506,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9428,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_certification"] == {
        "passed": 445,
        "result": "pass",
    }

    assert cert["changed_path_count"] == 10
    assert cert["production_runtime_path_count"] == 1
    assert cert["production_schema_path_count"] == 0

    assert target["post_merge_closure_complete"] is True

    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_c_post_merge_closure_is_recorded_without_downstream_activation():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["status"] == "merged_complete"
    assert target["implementation_state"] == "merged_complete"

    assert target["post_merge_closure_complete"] is True

    assert (
        target["post_merge_closure_authorization_reference"]
        == "owner_directive_2026-09-20_r4_c_post_merge_closure"
    )

    assert (
        target["post_merge_closure_authority_effect"]
        == "bounded_r4_c_post_merge_lifecycle_reconciliation_only"
    )

    assert (
        target["post_merge_closure_recorded_from"]
        == "8cb6da94894d2b8142d72c4a61fb5335135fe97e"
    )

    assert (
        target["post_merge_closure_tree"]
        == "91b486771ba2e0c85a847fe0f71e37b3c551bd32"
    )

    assert target["post_merge_closure_pull_request"] == 432

    assert (
        target["post_merge_closure_branch_head"]
        == "92e4a198b160101a188dee67f85e284ba9bd85c9"
    )

    assert target["post_merge_closure_ci_run"] == 264
    assert target["post_merge_closure_ci_run_id"] == 35553516783

    assert (
        target["post_merge_closure_regression_certified"]
        is True
    )

    assert (
        target["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"


def test_r4_c_post_merge_closure_certification_evidence_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["status"] == "merged_complete"
    assert target["implementation_state"] == "merged_complete"

    assert target["post_merge_closure_complete"] is True

    assert (
        target["post_merge_closure_regression_certified"]
        is True
    )

    assert (
        target["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    cert = target[
        "post_merge_closure_regression_certification"
    ]

    assert cert["focused_pre_certification"] == {
        "passed": 446,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 507,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9432,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_regression"] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["changed_path_count"] == 6
    assert cert["runtime_implementation_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    recovery = target[
        "post_merge_closure_failure_recovery_evidence"
    ]

    assert recovery[
        "failed_focused_closure_certification"
    ] == {
        "failed": 4,
        "passed": 445,
        "result": "fail",
    }

    assert recovery["r4_c_behavioral_defect_detected"] is False

    second = recovery["post_recording_validation_recovery"]

    assert second[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 4,
        "passed": 65,
        "result": "fail",
    }

    assert second["r4_c_behavioral_defect_detected"] is False
    assert second["runtime_scope_expanded"] is False
    assert second["production_schema_scope_expanded"] is False
    assert second["semantic_authority_expanded"] is False
    assert second["full_repository_rerun_required"] is False

    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_d_local_checkpoint_restore_definition_is_bounded():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["package_id"] == "R4-D"
    assert (
        target["package_name"]
        == "persistent_world_local_checkpoint_restore"
    )

    assert target["status"] == "implementation_authorized"
    assert target["package_defined"] is True

    assert target["implementation_authorized"] is True
    assert target["implementation_state"] == "ci_repair_regression_certified_pending_ci"

    assert target["predecessor_package"] == "R4-C"
    assert target["persistence_contract"] == "PR2-PERSIST"

    assert (
        target["persistence_handoff"]
        == "PR2-TEST-HANDOFF-PERSIST-001"
    )

    assert target["proposed_production_schema_edit_allowlist"] == []

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

def test_r4_d_definition_certification_evidence_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["status"] == "implementation_authorized"
    assert target["definition_regression_certified"] is True
    assert target["definition_recording_state"] == "merged_complete"

    evidence = target[
        "definition_regression_certification"
    ]

    assert evidence["focused_pre_certification"] == {
        "passed": 123,
        "result": "pass",
    }

    assert evidence["broader_pr2_r4_regression"] == {
        "passed": 519,
        "result": "pass",
    }

    assert evidence["full_repository_suite"] == {
        "passed": 9444,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert evidence["focused_post_suite_certification"] == {
        "passed": 49,
        "result": "pass",
    }

    assert evidence["changed_path_count"] == 7
    assert evidence["production_runtime_path_count"] == 0
    assert evidence["production_schema_path_count"] == 0

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

def test_r4_d_manifest_definition_recording_recovery_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    recovery = target[
        "definition_recording_failure_recovery_evidence"
    ]

    assert recovery[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 1,
        "passed": 50,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "stale_r4_d_next_gate_expectation_"
            "after_certification_recording"
        )
    )

    assert recovery["r4_d_behavioral_defect_detected"] is False
    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

def test_r4_d_definition_post_merge_closure_control_state_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["status"] == "implementation_authorized"
    assert target["definition_recording_state"] == "merged_complete"

    assert target["definition_post_merge_closure_complete"] is True

    assert (
        target[
            "definition_post_merge_closure_authorization_reference"
        ]
        == (
            "owner_directive_2026-09-21_"
            "r4_d_definition_post_merge_closure"
        )
    )

    assert (
        target[
            "definition_post_merge_closure_authority_effect"
        ]
        == (
            "bounded_r4_d_definition_post_merge_"
            "lifecycle_reconciliation_only"
        )
    )

    assert (
        target["definition_post_merge_closure_recorded_from"]
        == "3cf57fb816e51610c98258399ae11267abd2c1f5"
    )

    assert (
        target["definition_post_merge_closure_tree"]
        == "5674c05bd8d216373925ac5151a965acec6e72ec"
    )

    assert target["definition_post_merge_closure_pull_request"] == 434

    assert (
        target["definition_post_merge_closure_branch_head"]
        == "f453dde3ae2046a88048291f2f9b79c6b3406f52"
    )

    assert target["definition_post_merge_closure_ci_run"] == 268

    assert (
        target["definition_post_merge_closure_ci_run_id"]
        == 35608929257
    )

    assert (
        target[
            "definition_post_merge_closure_regression_certified"
        ]
        is True
    )

    assert (
        target[
            "definition_post_merge_closure_recording_state"
        ]
        == "merged_complete"
    )

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False

    assert target["implementation_authorized"] is True
    assert target["implementation_state"] == "ci_repair_regression_certified_pending_ci"
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

def test_r4_d_definition_closure_manifest_key_recovery_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["package_defined"] is True

    assert (
        target["status"]
        == "implementation_authorized"
    )

    assert "definition_merged_complete" not in target

    recovery = target[
        "definition_post_merge_closure_failure_recovery_evidence"
    ]

    assert (
        recovery["classification"]
        == (
            "accidental_test_key_rewrite_during_"
            "definition_closure_lifecycle_alignment"
        )
    )

    assert recovery[
        "r4_d_behavioral_defect_detected"
    ] is False

    assert recovery["runtime_scope_expanded"] is False

    assert (
        recovery[
            "production_schema_scope_expanded"
        ]
        is False
    )

    assert (
        recovery["semantic_authority_expanded"]
        is False
    )

    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False



def test_r4_d_definition_post_merge_closure_certification_control_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert (
        target[
            "definition_post_merge_closure_regression_certified"
        ]
        is True
    )

    assert (
        target[
            "definition_post_merge_closure_recording_state"
        ]
        == "merged_complete"
    )

    cert = target[
        "definition_post_merge_closure_regression_certification"
    ]

    assert cert["focused_pre_certification"] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 528,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9453,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": (
            "existing_nonblocking_deprecation"
        ),
        "result": "pass",
    }

    assert cert["focused_post_suite_regression"] == {
        "passed": 58,
        "result": "pass",
    }

    assert cert["changed_path_count"] == 7
    assert cert["runtime_implementation_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_d_closure_post_recording_recovery_control_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    recovery = target[
        "definition_post_merge_closure_failure_recovery_evidence"
    ]["post_recording_validation_recovery"]

    assert recovery[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 6,
        "passed": 54,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "stale_closure_certification_state_expectations_"
            "after_evidence_recording"
        )
    )

    assert (
        recovery["authoritative_next_gate"]
        == "r4_d_definition_post_merge_closure_commit_push"
    )

    assert recovery[
        "authoritative_closure_regression_certified"
    ] is True

    assert recovery[
        "r4_d_behavioral_defect_detected"
    ] is False

    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False

    assert target["implementation_authorized"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False



def test_r4_d_implementation_authorization_control_state_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["status"] == "implementation_authorized"
    assert target["implementation_authorized"] is True

    assert (
        target["implementation_state"]
        == "ci_repair_regression_certified_pending_ci"
    )

    assert (
        target[
            "implementation_authorization_regression_certified"
        ]
        is True
    )

    assert (
        target[
            "implementation_authorization_recording_state"
        ]
        == "merged_complete"
    )

    assert target["implementation_regression_certified"] is False

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert (
        target["production_schema_implementation_authorized"]
        is False
    )

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

def test_r4_d_implementation_authorization_certification_control_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert (
        target[
            "implementation_authorization_regression_certified"
        ]
        is True
    )

    assert (
        target[
            "implementation_authorization_recording_state"
        ]
        == "merged_complete"
    )

    cert = target[
        "implementation_authorization_regression_certification"
    ]

    assert cert[
        "focused_authorization_certification"
    ] == {
        "passed": 76,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 537,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9462,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": (
            "existing_nonblocking_deprecation"
        ),
        "result": "pass",
    }

    assert cert[
        "focused_post_suite_confirmation"
    ] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["changed_path_count"] == 7
    assert cert["production_runtime_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False

    assert target["implementation_authorized"] is True
    assert target["implementation_regression_certified"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"



def test_r4_d_partial_authorization_recording_recovery_control_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    recovery = target[
        "implementation_authorization_recording_failure_recovery_evidence"
    ]

    assert (
        recovery["classification"]
        == (
            "partial_implementation_authorization_"
            "certification_recording_before_late_assertion"
        )
    )

    assert recovery["certification_state_already_written"] is True
    assert recovery["r4_d_behavioral_defect_detected"] is False
    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False


def test_r4_d_implementation_regression_certification_control_state_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["status"] == "implementation_authorized"
    assert target["implementation_authorized"] is True

    assert (
        target["implementation_authorization_recording_state"]
        == "merged_complete"
    )

    assert target["implementation_authorization_pull_request"] == 436

    assert (
        target["implementation_authorization_merge_commit"]
        == "df7ce01e53ad69cf19a2b993764e8c38029eee58"
    )

    assert (
        target["implementation_execution_starting_baseline"]
        == "df7ce01e53ad69cf19a2b993764e8c38029eee58"
    )

    assert (
        target["implementation_state"]
        == "ci_repair_regression_certified_pending_ci"
    )

    assert target["implementation_regression_certified"] is False

    cert = target["implementation_regression_certification"]

    assert cert["focused_behavioral_implementation"] == {
        "passed": 34,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 575,
        "result": "pass",
    }

    assert cert["full_repository_suite"]["passed"] == 9500
    assert cert["full_repository_suite"]["skipped"] == 10
    assert cert["full_repository_suite"]["xfailed"] == 2
    assert cert["full_repository_suite"]["warnings"] == 1

    assert cert["production_runtime_path_count"] == 1
    assert cert["production_schema_path_count"] == 0
    assert cert["final_working_tree_changed_path_count"] == 11

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert (
        target["production_schema_implementation_authorized"]
        is False
    )

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"


def test_r4_d_implementation_recovery_control_evidence_is_exact():
    manifest = _load_manifest()

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    recovery = target[
        "implementation_failure_recovery_evidence"
    ]

    assert len(recovery) == 4

    assert (
        recovery["generated_test_import_syntax_error"][
            "r4_d_behavioral_defect_detected"
        ]
        is False
    )

    assert (
        recovery["representation_tuple_order_assertion"][
            "runtime_semantic_defect_detected"
        ]
        is False
    )

    assert (
        recovery["historical_rt001e_exact_module_guardrail"][
            "semantic_authority_expanded"
        ]
        is False
    )

    assert (
        recovery["termux_guardrail_log_path"][
            "production_scope_expanded"
        ]
        is False
    )


def test_r4_d_windows_ci_failure_and_repair_control_state_is_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.82"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert (
        target["implementation_state"]
        == "ci_repair_regression_certified_pending_ci"
    )

    assert target["implementation_regression_certified"] is False

    assert (
        target["implementation_local_repair_regression_certified"]
        is True
    )

    assert (
        target["implementation_cross_platform_ci_certified"]
        is False
    )

    failure = target["implementation_ci_failure_evidence"]

    assert failure["workflow_run_id"] == 35650004765

    assert (
        failure["classification"]
        == "r4_d_windows_posix_directory_fsync_portability_defect"
    )

    repair = target["windows_durability_portability_repair"]

    header_recovery = repair[
        "post_recording_program_header_recovery"
    ]

    assert (
        header_recovery["authoritative_program_version"]
        == "0.4.82"
    )

    assert (
        header_recovery["stale_expected_program_version"]
        == "0.4.81"
    )

    assert header_recovery["runtime_defect_detected"] is False

    assert repair["focused_behavioral"]["passed"] == 35
    assert repair["r4_d_package_implementation"]["passed"] == 96
    assert repair["broader_pr2_r4"]["passed"] == 580
    assert repair["full_repository_suite"]["passed"] == 9505

    completion = target["implementation_completion_proof"]

    assert "directory_fsync" not in completion
    assert completion["posix_parent_directory_fsync"] is True
    assert completion["windows_write_through_replace"] is True

    assert (
        target["next_gate"]
        == "r4_d_windows_ci_verification"
    )

    assert target["next_gate_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

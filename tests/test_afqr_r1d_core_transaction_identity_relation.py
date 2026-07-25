"""Semantic contract tests for AFQR R1D-CORE (doctrine only)."""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "179bfdda605f45d26ffb018da12805780710bdb3"
DOC = ROOT / "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
R1B = ROOT / "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"
R1C = ROOT / "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"
AUTH = ROOT / "docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml"
ESCALATIONS = ROOT / "docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml"
CORE = {f"AFQR-{n:02}" for n in range(1, 10)}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contract():
    match = re.search(r"## 11\. Machine-reviewable R1D-CORE contract\n\n```json\n(.*?)\n```", DOC.read_text(encoding="utf-8"), re.S)
    assert match, "normative JSON contract missing"
    return json.loads(match.group(1))


def test_required_structure_and_exact_responsibility_set():
    text = DOC.read_text(encoding="utf-8")
    assert all(f"## {n}." in text for n in range(1, 13))
    records = contract()["responsibility_records"]
    assert len(records) == 9
    assert {r["afqr_id"] for r in records} == CORE
    assert len({r["record_id"] for r in records}) == 9


def test_sources_exist_in_authority_index_and_on_disk():
    c, authority = contract(), load_json(AUTH)
    valid_ids = {i for r in authority["afqr_records"] for i in r["source_evidence_records"]}
    for record in c["responsibility_records"]:
        assert set(record["source_evidence_identifiers"]) <= valid_ids
        assert all((ROOT / p).is_file() for p in record["source_paths"])
    for group in (c["internal_edge_dispositions"], c["boundary_dispositions"]):
        for record in group:
            assert set(record["source_evidence"]["identifiers"]) <= valid_ids
            assert all((ROOT / p).is_file() for p in record["source_evidence"]["paths"])


def test_r1b_forms_and_owners_are_exact():
    c, vocabulary = contract(), load_json(R1B)
    allowed = set()
    roots = {}
    for term in vocabulary["term_records"]:
        roots[term["term_id"]] = term
        owner = term["type_owner"]
        if owner["owner_kind"] == "afqr":
            allowed.add((term["term_id"], term["canonical_form"], owner["owner_id"]))
        allowed.update((term["term_id"], q["qualified_form"], q["owner_id"]) for q in term.get("qualified_forms", []) if q["owner_kind"] == "afqr")
    cited = [x for r in c["responsibility_records"] for x in r["r1b_terms_or_qualified_forms"]]
    assert cited
    assert all(x["term_id"] in roots for x in cited)
    assert {(x["term_id"], x["form"], x["owner"]) for x in cited} <= allowed
    # Qualified/reserved roots cannot acquire a made-up unqualified core owner.
    for x in cited:
        term = roots[x["term_id"]]
        if term["unqualified_usage"] == "qualified_only":
            assert x["form"] in {q["qualified_form"] for q in term["qualified_forms"]}


def test_exact_r1c_internal_and_boundary_coverage_without_duplicates():
    c, r1c = contract(), load_json(R1C)
    edges = r1c["dependency_edge_dispositions"]
    expected_internal = {e["edge_id"] for e in edges if e["producer_afqr"] in CORE and e["consumer_afqr"] in CORE}
    expected_boundary = {e["edge_id"] for e in edges if (e["producer_afqr"] in CORE) ^ (e["consumer_afqr"] in CORE)}
    actual_internal = [e["edge_id"] for e in c["internal_edge_dispositions"]]
    actual_boundary = [i for e in c["boundary_dispositions"] for i in e["r1c_edge_ids_covered"]]
    assert len(actual_internal) == len(set(actual_internal)) == 33
    assert len(actual_boundary) == len(set(actual_boundary)) == 38
    assert set(actual_internal) == expected_internal
    assert set(actual_boundary) == expected_boundary
    assert set(actual_internal).isdisjoint(actual_boundary)


def test_dispositions_preserve_r1c_semantics_not_just_ids():
    c, r1c = contract(), load_json(R1C)
    vocabulary = {term["term_id"]: term for term in load_json(R1B)["term_records"]}
    source = {e["edge_id"]: e for e in r1c["dependency_edge_dispositions"]}
    for d in c["internal_edge_dispositions"]:
        e = source[d["edge_id"]]
        assert (d["producer"], d["consumer"], d["handoff_kind"]) == (e["producer_afqr"], e["consumer_afqr"], e["relation_or_handoff_kind"])
        assert d["semantic_owner"] == e["semantic_type_owner"]
        assert d["r1b_semantic_binding"] == e["semantic_type_owner"]
        for binding in d["r1b_semantic_binding"]["r1b_term_bindings"]:
            term = vocabulary[binding["term_id"]]
            if "qualified_form" in binding:
                owners = {(q["qualified_form"], q["owner_kind"], q["owner_id"]) for q in term["qualified_forms"]}
                assert (binding["qualified_form"], binding["owner_kind"], binding["owner_id"]) in owners
            else:
                assert binding["owner_kind"] == term["type_owner"]["owner_kind"]
                assert binding["owner_id"] == term["type_owner"]["owner_id"]
        assert d["producer_output"] == e["producer_supplies"]
        assert d["permitted_consumer_use"] == e["consumer_may_use"]
        assert d["ownership_nontransfer"] == e["ownership_does_not_transfer"]
        assert d["ordering_or_phase_constraint"] == e["preconditions"]
        assert d["failure_or_unavailable_input_behavior"] == e["unavailable_input_behavior"]
        assert d["source_evidence"] == {"identifiers": e["source_evidence_records"], "paths": e["source_evidence_paths"]}
        assert d["cycle_or_dependency_risk_treatment"] == e["cycle_participation"]
    for d in c["boundary_dispositions"]:
        assert len(d["r1c_edge_ids_covered"]) == 1
        e = source[d["r1c_edge_ids_covered"][0]]
        core = e["producer_afqr"] if e["producer_afqr"] in CORE else e["consumer_afqr"]
        external = e["consumer_afqr"] if core == e["producer_afqr"] else e["producer_afqr"]
        expected_family = "R1D-AGENCY" if 10 <= int(external[-2:]) <= 15 else "R1D-WORLD"
        assert d["core_family_endpoint"] == core
        assert d["external_endpoint"] == external
        assert (d["producer"], d["consumer"]) == (e["producer_afqr"], e["consumer_afqr"])
        assert d["direction"] == ("export" if e["producer_afqr"] in CORE else "import")
        assert d["handoff_kind"] == e["relation_or_handoff_kind"]
        assert d["typed_handoff"] == d["typed_producer_output"] == e["producer_supplies"]
        assert d["semantic_owner"] == e["semantic_type_owner"]
        assert d["ownership_nontransfer"] == e["ownership_does_not_transfer"]
        assert d["failure_behavior"] == e["unavailable_input_behavior"]
        assert d["source_evidence"] == {"identifiers": e["source_evidence_records"], "paths": e["source_evidence_paths"]}
        assert d["external_family"] == expected_family


def test_exact_cycle_and_dependency_risk_treatments():
    c, r1c = contract(), load_json(R1C)
    expected_cycles = [x for x in r1c["cycle_risk_resolutions"] if set(x["afqrs"]) <= CORE]
    assert c["cycle_resolutions"] == expected_cycles
    assert {tuple(x["edge_ids"]) for x in c["cycle_resolutions"]} == {("DEP-008", "DEP-061"), ("DEP-021", "DEP-024"), ("DEP-048", "DEP-052")}
    assert c["dependency_risk_reclassifications"] == r1c["cycle_risk_reclassifications"]
    assert {tuple(x["edge_ids"]) for x in c["dependency_risk_reclassifications"]} == {("DEP-022", "DEP-062"), ("DEP-028", "DEP-063"), ("DEP-049", "DEP-064"), ("DEP-054", "DEP-066")}
    assert all("not_recorded_cycle_group" in x["classification"] for x in c["dependency_risk_reclassifications"])


def test_nonownership_invariants_and_escalations():
    text = DOC.read_text(encoding="utf-8").lower()
    required = ["commitment never owns the committed domain", "scheduling creates neither command identity nor truth", "admission proves neither truth nor identity", "reservation and settlement", "replay idempotent", "recovery identity-preserving", "compatibility never absorbs endpoint meaning"]
    assert all(x in text for x in required)
    records = {r["afqr_id"]: r for r in contract()["responsibility_records"]}
    assert all(x in records["AFQR-02"]["explicit_nonowned_concerns"] for x in ("action representation", "opportunity", "target", "resolution"))
    assert all(x in records["AFQR-08"]["explicit_nonowned_concerns"] for x in ("ownership", "agency", "authority", "responsibility"))
    assert all(x in records["AFQR-09"]["explicit_nonowned_concerns"] for x in ("obligation", "jurisdiction", "legal effect", "social standing"))
    actual = {x["collision_identifier"]: x for x in contract()["escalations"]}
    ledger = {x["collision_ids"][0]: x for x in load_json(ESCALATIONS)["escalations"]}
    assert set(actual) == set(ledger) == {"COLL-03", "COLL-08", "COLL-10"}
    expected_external = {"COLL-03": {"AFQR-11", "AFQR-15"}, "COLL-08": {"AFQR-13", "AFQR-15"}, "COLL-10": {"AFQR-11", "AFQR-12", "AFQR-13"}}
    for collision, record in actual.items():
        source = ledger[collision]
        assert set(record["exact_collision_terms"]) == set(source["terms"])
        assert set(record["affected_afqrs"]) == set(source["affected_afqrs"])
        assert set(record["source_evidence_identifiers"]) == set(source["source_evidence_records"])
        assert record["safe_interim_usage"] == source["lawful_interim_usage"]
        assert record["prohibited_inference"] == source["prohibited_interim_usage"]
        assert set(record["external_family_afqrs"]) == expected_external[collision]
        assert record["downstream_family"] == "R1D-AGENCY"
        assert all((ROOT / path).is_file() for path in record["source_paths"])


def test_responsibility_collision_references_match_ledger_taxonomy():
    records = {x["afqr_id"]: x for x in contract()["responsibility_records"]}
    ledger = load_json(ESCALATIONS)["escalations"]
    affected = {collision: set(e["affected_afqrs"]) for e in ledger for collision in e["collision_ids"]}
    for afqr, record in records.items():
        collisions = set(re.findall(r"COLL-\d+", " ".join(record["unresolved_seams"])))
        assert all(afqr in affected[collision] for collision in collisions)
    assert "COLL-03" not in " ".join(records["AFQR-03"]["unresolved_seams"])
    assert "capability readiness" not in " ".join(records["AFQR-08"]["unresolved_seams"]).lower()
    assert "COLL-03" in " ".join(records["AFQR-08"]["unresolved_seams"])
    assert "COLL-08" in " ".join(records["AFQR-09"]["unresolved_seams"])
    coll10 = next(x for x in contract()["escalations"] if x["collision_identifier"] == "COLL-10")
    assert not ({"signal", "observation", "evidence", "interpretation", "knowledge"} & set(coll10["exact_collision_terms"]))


def test_substrate_dispositions_have_bounded_core_and_external_scopes():
    records = {x["substrate_id"]: x for x in contract()["missing_substrates"]}
    assert set(records) == {"SUB-001", "SUB-002", "SUB-003", "SUB-004"}
    required = {"core_family_scope", "external_family_scope", "r1d_core_may_consolidate", "r1d_core_must_not_implement", "later_owner_or_gate", "collapse_risk"}
    assert all(required <= set(record) for record in records.values())
    assert "AFQR-09" in records["SUB-001"]["core_family_scope"] and all(x in records["SUB-001"]["external_family_scope"] for x in ("AFQR-13", "AFQR-15"))
    assert all(x in records["SUB-002"]["core_family_scope"] for x in ("AFQR-04", "AFQR-06"))
    assert all(x in records["SUB-002"]["external_family_scope"] for x in ("AFQR-10", "AFQR-20"))
    assert all(x in records["SUB-003"]["core_family_scope"] for x in ("AFQR-01", "AFQR-02", "AFQR-04", "AFQR-09"))
    assert "AFQR-05" in records["SUB-004"]["core_family_scope"]
    assert all(any(word in record["r1d_core_must_not_implement"] for word in ("schema", "registry", "journal")) for record in records.values())


def test_no_external_domain_ownership_or_forbidden_authority():
    c = contract()
    assert c["excluded_afqrs"] == [f"AFQR-{n:02}" for n in range(10, 21)]
    assert all(r["afqr_id"] in CORE for r in c["responsibility_records"])
    boundary = json.dumps(c["boundary_dispositions"])
    assert "does not define them" in boundary
    authority = c["authority_boundary"]
    assert all(x in authority for x in ("no runtime", "persistence", "conversion execution", "canon/sourcebook", "model-facing", "narration", "live-play", "RT-002G", "evidence-deletion"))


def test_gate_and_temporary_evidence_posture():
    c = contract()
    gates = c["downstream_gates"]
    assert gates == {"R1D-CORE":"complete", "overall_R1D":"incomplete", "R1D-AGENCY":"ready_not_started", "R1D-WORLD":"ready_not_started", "R1E":"blocked", "R2-R6":"blocked", "RT-002G":"unauthorized"}
    assert "present" in c["temporary_evidence_status"] and "non-authoritative" in c["temporary_evidence_status"] and "deletion unauthorized" in c["temporary_evidence_status"]
    assert (ROOT / "working/afqr_consolidation_inputs/manifest.yaml").is_file()


def test_all_corpus_pressures_have_bounded_dispositions():
    records = contract()["corpus_pressure_records"]
    assert len(records) == 16 == len({r["record_id"] for r in records})
    expected = ["class and archetype actions", "point-buy action construction", "narrative moves and aspects", "cultivation techniques and advancement transactions", "spells, powers, maneuvers, and procedures", "cyberware and biotech transformations", "psionic identity and proxy constructs", "horror evidence and hidden-information systems", "vehicles, mechs, ships, and operator separation", "companions, summons, copies, and proxies", "crafting, salvage, requisition, and settlement", "currencies, charges, fuel, ammunition, heat, stress, and abstract reserves", "clocks, turns, rounds, phases, real time, downtime, and asynchronous processes", "social or legal obligations attached to relations", "identity copying, body replacement, fusion, fission, possession, and reinstantiation", "mission and adventure structures that contain source-local procedures"]
    assert [r["pressure_class"] for r in records] == expected
    assert all(r["disposition"] and r["universalization"] == "prohibited" for r in records)


def test_committed_diff_is_bounded_and_preserves_evidence():
    changed = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}...HEAD"], cwd=ROOT, text=True).splitlines()
    numstat = subprocess.check_output(["git", "diff", "--numstat", f"{BASE}...HEAD"], cwd=ROOT, text=True).splitlines()
    deleted = subprocess.check_output(["git", "diff", "--name-status", "--diff-filter=D", f"{BASE}...HEAD"], cwd=ROOT, text=True).splitlines()
    # This test intentionally evaluates committed diff, never working-tree diff.
    assert not any(p.startswith("src/") for p in changed)
    assert not any(p.lower().endswith(".zip") for p in changed)
    assert not any(row.startswith("-\t-\t") for row in numstat)
    assert not any("working/afqr_consolidation_inputs/" in row for row in deleted)
    forbidden = ("afqr_epistemic_agency_social_communication", "afqr_world_action_sensing", "afqr_01_20_formal_completion_review")
    assert not any(any(x in p for x in forbidden) for p in changed)


def test_production_does_not_import_temporary_or_review_artifacts():
    for path in (ROOT / "src").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "working.afqr_consolidation_inputs" not in text
        assert "afqr_r1d_core_consolidation_report" not in text

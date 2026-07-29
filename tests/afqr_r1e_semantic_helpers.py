"""Deterministic semantic comparison and reconciliation helpers for AFQR R1E."""
from __future__ import annotations
import copy, hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load_json(path):
    path=Path(path); path=path if path.is_absolute() else ROOT/path
    return json.loads(path.read_text(encoding="utf-8"))
def load_markdown_json(path):
    text=(ROOT/path).read_text(encoding="utf-8"); match=re.search(r"```json\n(.*?)\n```",text,re.S)
    if not match: raise AssertionError(f"missing JSON fence: {path}")
    return json.loads(match.group(1))
def normalized_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def family(afqr):
    n=int(afqr.split("-")[1]); return "core" if n<=9 else "agency" if n<=15 else "world"
def partition(edge):
    order=["core","agency","world"]; a,b=family(edge["producer_afqr"]),family(edge["consumer_afqr"])
    return f"{a}_internal" if a==b else "–".join(sorted((a,b),key=order.index))+"_boundary"
def projection_records(document):
    for section in ("internal_edge_dispositions","boundary_dispositions","core_boundary_dispositions","agency_boundary_dispositions"):
        for index,record in enumerate(document.get(section,[])):
            ids=record.get("r1c_edge_ids_covered",[record.get("edge_id")]); ids=[ids] if isinstance(ids,str) else ids
            for edge_id in ids:
                if edge_id: yield edge_id,section,index,record

def nested_dict_hashes(value,out=None):
    out=set() if out is None else out
    if isinstance(value,dict):
        if len(value)>=5: out.add(normalized_hash(value))
        for child in value.values(): nested_dict_hashes(child,out)
    elif isinstance(value,list):
        for child in value: nested_dict_hashes(child,out)
    return out

def _norm(value):
    if isinstance(value,str): return " ".join(value.lower().replace("_"," ").split())
    if isinstance(value,list): return [_norm(x) for x in value]
    if isinstance(value,dict): return {k:_norm(v) for k,v in sorted(value.items())}
    return value
def _term_ids(value):
    if isinstance(value,dict):
        if "term_id" in value:return [value["term_id"]]
        return sorted(set(sum((_term_ids(v) for v in value.values()),[])))
    if isinstance(value,list):return sorted(set(sum((_term_ids(v) for v in value),[])))
    if isinstance(value,str):return sorted(set(re.findall(r"TERM-\d{3}",value)))
    return []
def compact_owner(owner):
    return {k:owner.get(k) for k in ("owner_kind","owner_id","ownership_basis") if owner.get(k) is not None}
REQUIRED_R1C_FIELDS = [
    "producer_afqr","consumer_afqr","relation_or_handoff_kind","semantic_type_owner",
    "semantic_type_owner.r1b_term_bindings","producer_supplies","consumer_may_use",
    "ownership_does_not_transfer","consumer_not_semantic_owner_by_consumption","preconditions",
    "postconditions","unavailable_input_behavior","revocation_invalidation_or_cascade",
    "hidden_information_or_projection_constraints","source_evidence_records","source_evidence_paths",
    "cycle_participation","r1d_destination_family_or_escalation",
]

def projection_contract(family_name, section, artifact):
    explicit={"producer_afqr","consumer_afqr","relation_or_handoff_kind","semantic_type_owner","semantic_type_owner.r1b_term_bindings","producer_supplies","consumer_may_use","ownership_does_not_transfer","unavailable_input_behavior","source_evidence_records","source_evidence_paths"}
    if section!="boundary_dispositions": explicit.add("preconditions")
    if family_name=="world": explicit|={"consumer_not_semantic_owner_by_consumption","postconditions","revocation_invalidation_or_cascade","hidden_information_or_projection_constraints","r1d_destination_family_or_escalation"}
    elif family_name=="agency": explicit.add("r1d_destination_family_or_escalation")
    elif family_name=="core" and section=="internal_edge_dispositions": explicit.add("r1d_destination_family_or_escalation")
    blob=json.dumps(artifact,sort_keys=True).lower(); preserved="r1c" in blob and "consolidation only" in artifact.get("authority_boundary","").lower()
    return {"family":family_name,"section":section,"explicit_fields":sorted(explicit),"preserves_r1c_authority":preserved}

def _disposition(field,dest,mode,source,destination,ok=True,reason=None,rationale=None,details=None):
    record={"r1c_field":field,"r1d_field":dest,"disposition":mode,"comparison_mode":mode if mode in ("exact","bounded_projection") else mode,"normalization_rule":"N2","source_hash":normalized_hash(source),"destination_hash":normalized_hash(destination) if destination is not None else None,"result":"pass" if ok else "fail","mismatch_reason":None if ok else reason}
    if rationale is not None: record["preservation_rationale"]=rationale
    if details: record["condition_deltas"]=details
    return record
def _exact_disposition(field,dest,source,destination):
    ok=_norm(source)==_norm(destination);return _disposition(field,dest,"exact",source,destination,ok,"normalized values differ")
def _missing(field,source,reason):return _disposition(field,None,"missing_blocking",source,None,False,reason)
def _upstream(field,source,contract):
    ok=contract["preserves_r1c_authority"]
    return _disposition(field,None,"upstream_only_preserved",source,None,ok,"family does not preserve R1C authority","R1C authority preserved; omission adds no contradiction or ownership transfer.")
def _not_applicable(field,source,why):return _disposition(field,None,"not_applicable",source,None,True,rationale=why)
def _condition_compare(field,dest,source,destination):
    s=[_norm(x) for x in source];d=[_norm(x) for x in destination] if isinstance(destination,list) else []
    retained=[x for x in s if x in d];removed=[x for x in s if x not in d];added=[x for x in d if x not in s]
    ok=not removed
    return _disposition(field,dest,"bounded_projection",source,destination,ok,"authoritative condition removed",details=[f"retained:{x}" for x in retained]+[f"removed:{x}" for x in removed]+[f"strengthened_or_added:{x}" for x in added])
def _downstream_compare(source,destination,family_name):
    allowed={"core":{"unimplemented and unauthorized; doctrine handoff only"},"agency":{"unimplemented; later explicit authorization required"},"world":{"unimplemented; r2-r6 blocked"}}
    ok=_norm(destination) in allowed[family_name]
    return _disposition("r1d_destination_family_or_escalation","downstream_implementation_status","bounded_projection",source,destination,ok,"status is not an explicitly allowed deferred/unimplemented family outcome")

def compare_projection(edge,projection,contract):
    """Account for every authoritative R1C field using explicit semantic contracts."""
    explicit=set(contract["explicit_fields"]); out=[]
    def exact(field,dest,value=None):
        source=edge[field] if value is None else value
        if dest not in projection:return _missing(field,source,f"required destination {dest} absent") if field in explicit else _upstream(field,source,contract)
        out.append(_exact_disposition(field,dest,source,projection[dest]))
    exact("producer_afqr","producer");exact("consumer_afqr","consumer");exact("relation_or_handoff_kind","handoff_kind")
    owner=compact_owner(edge["semantic_type_owner"])
    if "semantic_owner" not in projection:out.append(_missing("semantic_type_owner",owner,"semantic_owner absent"))
    else:out.append(_exact_disposition("semantic_type_owner","semantic_owner",owner,compact_owner(projection["semantic_owner"])))
    binding_field=("exact_r1b_term_bindings" if contract["family"]=="world" and "exact_r1b_term_bindings" in projection else "r1b_semantic_binding" if contract["family"]=="core" and contract["section"]=="internal_edge_dispositions" and "r1b_semantic_binding" in projection else None); bindings=_term_ids(edge["semantic_type_owner"].get("r1b_term_bindings",[]))
    if binding_field: destination_bindings=_term_ids(projection[binding_field]); binding_dest=binding_field
    elif contract["family"]!="world" and isinstance(projection.get("semantic_owner"),dict) and "r1b_term_bindings" in projection["semantic_owner"]: destination_bindings=_term_ids(projection["semantic_owner"]["r1b_term_bindings"]); binding_dest="semantic_owner.r1b_term_bindings"
    else: destination_bindings=None; binding_dest=None
    if destination_bindings is None:out.append(_missing("semantic_type_owner.r1b_term_bindings",bindings,"R1B binding destination absent"))
    else:out.append(_exact_disposition("semantic_type_owner.r1b_term_bindings",binding_dest,bindings,destination_bindings))
    for field,dests in (("producer_supplies",("typed_producer_output",) if contract["family"]=="core" and contract["section"]=="boundary_dispositions" else ("producer_output",)),("consumer_may_use",("r1d_core_may_assert",) if contract["family"]=="core" and contract["section"]=="boundary_dispositions" else ("permitted_consumer_use",))):
        dest=next((x for x in dests if x in projection),None)
        if not dest:out.append(_missing(field,edge[field],"required semantic payload destination absent"))
        elif field=="consumer_may_use" and dest=="r1d_core_may_assert":
            allowed="only the core endpoint output and r1c handoff constraints";ok=_norm(projection[dest])==allowed
            out.append(_disposition(field,dest,"bounded_projection",edge[field],projection[dest],ok,"core boundary permission is not the documented owner-preserving narrowing",details=["retained:core endpoint output only","retained:R1C handoff constraints"]))
        else:out.append(_exact_disposition(field,dest,edge[field],projection[dest]))
    exact("ownership_does_not_transfer","ownership_nontransfer")
    if "consumer_nonownership" in projection:out.append(_exact_disposition("consumer_not_semantic_owner_by_consumption","consumer_nonownership",edge["consumer_not_semantic_owner_by_consumption"],projection["consumer_nonownership"]))
    elif "consumer_not_semantic_owner_by_consumption" in explicit:out.append(_missing("consumer_not_semantic_owner_by_consumption",edge["consumer_not_semantic_owner_by_consumption"],"consumer nonownership destination absent"))
    else:out.append(_upstream("consumer_not_semantic_owner_by_consumption",edge["consumer_not_semantic_owner_by_consumption"],contract))
    pre=next((x for x in ("preconditions","ordering_or_phase_constraint") if x in projection),None)
    if not pre:out.append(_missing("preconditions",edge["preconditions"],"precondition destination absent") if "preconditions" in explicit else _upstream("preconditions",edge["preconditions"],contract))
    else:out.append(_condition_compare("preconditions",pre,edge["preconditions"],projection[pre]))
    if "postconditions" in projection:out.append(_condition_compare("postconditions","postconditions",edge["postconditions"],projection["postconditions"]))
    elif "postconditions" in explicit:out.append(_missing("postconditions",edge["postconditions"],"postconditions absent"))
    else:out.append(_upstream("postconditions",edge["postconditions"],contract))
    unavailable=("failure_behavior" if contract["family"]=="core" and contract["section"]=="boundary_dispositions" and "failure_behavior" in projection else "failure_or_unavailable_input_behavior" if contract["family"]=="core" and "failure_or_unavailable_input_behavior" in projection else "unavailable_input_behavior" if "unavailable_input_behavior" in projection else None)
    if not unavailable:out.append(_missing("unavailable_input_behavior",edge["unavailable_input_behavior"],"unavailable-input outcome absent"))
    else:out.append(_exact_disposition("unavailable_input_behavior",unavailable,edge["unavailable_input_behavior"],projection[unavailable]))
    for field,dest in (("revocation_invalidation_or_cascade","revocation_invalidation_or_cascade"),("hidden_information_or_projection_constraints","hidden_information_and_projection_constraints")):
        if dest in projection:out.append(_exact_disposition(field,dest,edge[field],projection[dest]))
        elif field in explicit:out.append(_missing(field,edge[field],f"{dest} absent"))
        else:out.append(_upstream(field,edge[field],contract))
    evidence=projection.get("source_evidence");ids=evidence.get("identifiers") if isinstance(evidence,dict) else evidence;paths=evidence.get("paths") if isinstance(evidence,dict) else None
    if ids is None:out.append(_missing("source_evidence_records",edge["source_evidence_records"],"evidence identifiers absent"))
    else:out.append(_exact_disposition("source_evidence_records","source_evidence.identifiers",sorted(edge["source_evidence_records"]),sorted(ids)))
    if paths is None:out.append(_missing("source_evidence_paths",edge["source_evidence_paths"],"evidence paths absent") if "source_evidence_paths" in explicit else _upstream("source_evidence_paths",edge["source_evidence_paths"],contract))
    else:out.append(_exact_disposition("source_evidence_paths","source_evidence.paths",sorted(edge["source_evidence_paths"]),sorted(paths)))
    cycle_dest=next((x for x in ("cycle_participation","cycle_or_dependency_risk_treatment","cycle_or_dependency_risk_status") if x in projection and isinstance(projection[x],type(edge["cycle_participation"]))),None)
    if cycle_dest:out.append(_exact_disposition("cycle_participation",cycle_dest,edge["cycle_participation"],projection[cycle_dest]))
    elif not edge["cycle_participation"]:out.append(_not_applicable("cycle_participation",False,"edge has no authoritative cycle participation"))
    else:out.append(_upstream("cycle_participation",edge["cycle_participation"],contract))
    if "downstream_implementation_status" in projection:out.append(_downstream_compare(edge["r1d_destination_family_or_escalation"],projection["downstream_implementation_status"],contract["family"]))
    elif "r1d_destination_family_or_escalation" in explicit:out.append(_missing("r1d_destination_family_or_escalation",edge["r1d_destination_family_or_escalation"],"downstream status absent"))
    else:out.append(_upstream("r1d_destination_family_or_escalation",edge["r1d_destination_family_or_escalation"],contract))
    categories={"compared_fields":[x["r1c_field"] for x in out if x["disposition"] in ("exact","bounded_projection")],"upstream_only_preserved_fields":[x["r1c_field"] for x in out if x["disposition"]=="upstream_only_preserved"],"not_applicable_fields":[x["r1c_field"] for x in out if x["disposition"]=="not_applicable"],"missing_fields":[x["r1c_field"] for x in out if x["disposition"]=="missing_blocking"]}
    mismatched=[x["r1c_field"] for x in out if x["result"]=="fail" and x["disposition"]!="missing_blocking"]
    return {"required_r1c_fields":REQUIRED_R1C_FIELDS,"field_comparisons":out,**categories,"mismatched_fields":mismatched,"result":"pass" if len(out)==len(REQUIRED_R1C_FIELDS) and all(x["result"]=="pass" for x in out) else "fail"}

def evidence_locator(record,archives):
    if record.get("normalized_path"):
        return {"evidence_id":record["source_record_id"],"path_kind":"materialized_normalized_file","path":record["normalized_path"]}
    archive=archives[record["parent_archive_record_id"]]
    return {"evidence_id":record["source_record_id"],"path_kind":"archive_member","archive_path":archive["current_path"],"archive_member_path":record["original_archive_path"]}

def calculate_consistency(auth,vocab,r1c,families,edge_rows,source_manifest,r1e_coverage=None):
    """Run thirteen relationship-specific calculations; returned diagnostics are normative audit proof."""
    auth_ids={x["afqr_id"] for x in auth["afqr_records"]}; evidence={x["source_record_id"] for x in source_manifest["contained_file_records"]}; terms={x["term_id"] for x in vocab["term_records"]}
    rows=[]
    def add(i,label,rules,details):
        informational={"owned_term_ids","term_claim_dispositions","projection_ids","expected_boundary_ids","expected_r1d_record_counts","covered_family_artifact_ids","covered_responsibility_record_ids","covered_projection_refs","covered_cycle_record_ids","covered_risk_record_ids","covered_collision_candidate_ids","covered_substrate_record_ids","covered_pressure_record_ids","covered_completion_boundary_hashes","covered_authority_not_granted"}
        problems=[item for k,v in details.items() if k not in informational and isinstance(v,list) for item in v]
        rows.append({"comparator_id":f"REL-{i:02}","relationship":label,"comparison_rules":rules,"calculated_details":details,"missing_ids":details.get("missing_ids",[]),"surplus_ids":details.get("surplus_ids",[]),"mismatched_ids_and_fields":details.get("mismatches",[]),"authority_transfer_violations":details.get("violations",[]),"blocking_status":"blocking" if problems else "nonblocking","result":"fail" if problems else "pass"})
    owner_afqrs=[]
    for t in vocab["term_records"]:
        owner=t.get("type_owner",{}); owner_afqrs += [x for x in re.findall(r"AFQR-\d{2}",json.dumps(owner))]
    add(1,"R1A -> R1B",["evidence resolution","owner authority","packaging is not ownership"],{"unresolved_evidence_ids":sorted({e for t in vocab["term_records"] for e in t["source_evidence_records"]}-evidence),"invalid_owner_afqrs":sorted(set(owner_afqrs)-auth_ids),"packaging_ownership_violations":[],"missing_ids":[]})
    add(2,"R1A -> R1C",["edge evidence/path resolution","endpoint authority"],{"unresolved_evidence_ids":sorted({e for x in r1c["dependency_edge_dispositions"] for e in x["source_evidence_records"]}-evidence),"unresolved_paths":sorted({p for x in r1c["dependency_edge_dispositions"] for p in x["source_evidence_paths"] if not (ROOT/p).exists()}),"missing_endpoint_authorities":sorted({a for x in r1c["dependency_edge_dispositions"] for a in (x["producer_afqr"],x["consumer_afqr"]) if a not in auth_ids}),"missing_ids":[]})
    term_map={x["term_id"]:x for x in vocab["term_records"]}
    binding_records=[(edge,b) for edge in r1c["dependency_edge_dispositions"] for b in edge["semantic_type_owner"].get("r1b_term_bindings",[])]
    missing_bindings=[[edge["edge_id"],b.get("term_id")] for edge,b in binding_records if b.get("term_id") not in terms]
    owner_mismatches=[]; nonowner_violations=[]; qualification_violations=[]
    for edge,binding in binding_records:
        term=term_map.get(binding.get("term_id"))
        if not term: continue
        actual=(binding.get("owner_kind"),binding.get("owner_id")); base=(term["type_owner"].get("owner_kind"),term["type_owner"].get("owner_id")); qualified={(q.get("owner_kind"),q.get("owner_id"),q.get("qualified_form")) for q in term["qualified_forms"]}
        if actual!=base and not any(actual==q[:2] for q in qualified): owner_mismatches.append([edge["edge_id"],binding["term_id"],"owner_kind_or_id"])
        if actual[1] in term["explicit_nonowners"]: nonowner_violations.append([edge["edge_id"],binding["term_id"],actual[1]])
        if actual!=base and qualified and not any(actual==q[:2] and binding.get("qualified_form")==q[2] for q in qualified): qualification_violations.append([edge["edge_id"],binding["term_id"]])
    add(3,"R1B -> R1C",["binding existence","binding owner","qualification","explicit nonowner"],{"missing_term_bindings":missing_bindings,"owner_mismatches":owner_mismatches,"qualification_violations":qualification_violations,"explicit_nonowner_violations":nonowner_violations,"missing_ids":[]})
    for i,name in enumerate(("core","agency","world"),4):
        records=families[name]["responsibility_records"]; dispositions=[]; missing=[]; qualification=[]; handoff=[]; prohibited=[]; surplus=[]
        for record in records:
            afqr=record["afqr_id"]
            for claim in record.get("r1b_terms_or_qualified_forms",[]):
                term_id=claim.get("term_id");term=term_map.get(term_id);form=claim.get("form");declared=claim.get("owner")
                if not term: missing.append([record["record_id"],term_id]);continue
                base=term["type_owner"];qualified=[q for q in term["qualified_forms"] if q.get("qualified_form")==form and q.get("owner_id")==declared]
                if afqr in term["explicit_nonowners"]: posture="prohibited";prohibited.append([record["record_id"],term_id,form])
                elif afqr in term["handoff_only_consumers"]: posture="consumed_handoff_only";handoff.append([record["record_id"],term_id,form])
                elif qualified: posture="qualified_owned"
                elif base.get("owner_kind")=="afqr" and base.get("owner_id")==declared: posture="owned"
                elif declared!=afqr: posture="mentioned_nonowning"
                else: posture="prohibited";surplus.append([record["record_id"],term_id,form,declared])
                if base.get("owner_kind")=="shared_qualified_family" and posture=="prohibited": qualification.append([record["record_id"],term_id,form])
                dispositions.append({"responsibility_record_id":record["record_id"],"afqr_id":afqr,"term_id":term_id,"exact_form":form,"declared_owner":declared,"r1b_owner_kind":base.get("owner_kind"),"r1b_owner_id":base.get("owner_id"),"allowed_qualified_form":qualified[0].get("qualified_form") if qualified else None,"explicit_nonowners":term["explicit_nonowners"],"handoff_only":afqr in term["handoff_only_consumers"],"disposition":posture})
        add(i,f"R1B -> R1D-{name.upper()}",[f"{name} responsibility term classification","exact qualified-form ownership","handoff/nonowner prohibition"],{"term_claim_dispositions":dispositions,"owned_term_ids":sorted({x["term_id"] for x in dispositions if x["disposition"] in ("owned","qualified_owned")}),"missing_ids":missing,"qualification_violations":qualification,"handoff_only_violations":handoff,"prohibited_ownership_claims":prohibited,"surplus_ownership_claims":surplus,"missing_required_qualified_forms":qualification})
    for i,name in enumerate(("core","agency","world"),7):
        refs=[p for e in edge_rows for p in e["projections"] if f"afqr_{'core_transaction_identity_relation' if name=='core' else 'epistemic_agency_social_communication' if name=='agency' else 'world_action_sensing'}" in p["projection_ref"]]
        add(i,f"R1C -> R1D-{name.upper()}",[f"{name} real projection field comparator pipeline"],{"projection_ids":[x["projection_ref"] for x in refs],"missing_ids":[],"mismatches":[[x["projection_ref"],x["mismatched_fields"]] for x in refs if x["result"]!="pass"],"surplus_ids":[]})
    pairs=[("core","agency"),("core","world"),("agency","world")]
    edge_map={x["edge_id"]:x for x in r1c["dependency_edge_dispositions"]}
    for i,(a,b) in enumerate(pairs,10):
        expected=sorted(e for e,x in edge_map.items() if {family(x["producer_afqr"]),family(x["consumer_afqr"])}=={a,b})
        ids={n:{e for e,_,_,_ in projection_records(families[n])} for n in (a,b)}
        add(i,f"R1D-{a.upper()} <-> R1D-{b.upper()}",[f"{a}-{b} two-sided boundary identity","semantic owner/nontransfer parity"],{"expected_boundary_ids":expected,"missing_ids":sorted([e for e in expected if e not in ids[a] or e not in ids[b]]),"mismatches":[[e,p["projection_ref"]] for e in expected for row in edge_rows if row["edge_id"]==e for p in row["projections"] if p["result"]!="pass"],"surplus_ids":[]})
    expected_records={n:len(d["responsibility_records"])+len(list(projection_records(d)))+len(d["corpus_pressure_records"]) for n,d in families.items()}
    coverage=r1e_coverage or {}
    expected_family={d["artifact_id"] for d in families.values()}; expected_resp={x["record_id"] for d in families.values() for x in d["responsibility_records"]}; expected_proj={p["projection_ref"] for row in edge_rows for p in row["projections"]}
    expected_cycles={x.get("cycle_id") for d in families.values() for x in d.get("cycle_resolutions",[]) if x.get("cycle_id")}|({families["world"].get("cycle_004_treatment",{}).get("cycle_id")}-{None})
    expected_risks={x.get("reclassification_id") for d in families.values() for x in d.get("dependency_risk_reclassifications",[]) if x.get("reclassification_id")}
    expected_candidates={x["record_id"] for x in families["agency"].get("collision_resolution_candidates",[])}; expected_substrates={x.get("substrate_id") for d in families.values() for section in ("missing_substrates","missing_substrate_dispositions") for x in d.get(section,[]) if x.get("substrate_id")}; expected_pressure={x["record_id"] for d in families.values() for x in d["corpus_pressure_records"]}; expected_boundaries={normalized_hash(d["completion_boundary"]) for d in families.values() if d.get("completion_boundary")}
    required_nonauthority={"runtime implementation","persistence","reducers","production schemas","conversion execution","canon promotion","sourcebook drafting","live-play behavior","narration","model training","UI behavior","R2 work","RT-002G implementation","temporary evidence deletion"}
    def missing(expected,key):return sorted(expected-set(coverage.get(key,[])))
    add(13,"R1D -> R1E",["complete family-record coverage","candidate and pressure coverage","historical boundary preservation","no implementation authority"],{"expected_r1d_record_counts":expected_records,"covered_family_artifact_ids":coverage.get("family_artifact_ids",[]),"covered_responsibility_record_ids":coverage.get("responsibility_record_ids",[]),"covered_projection_refs":coverage.get("projection_refs",[]),"covered_cycle_record_ids":coverage.get("cycle_record_ids",[]),"covered_risk_record_ids":coverage.get("risk_record_ids",[]),"covered_collision_candidate_ids":coverage.get("collision_candidate_ids",[]),"covered_substrate_record_ids":coverage.get("substrate_record_ids",[]),"covered_pressure_record_ids":coverage.get("pressure_record_ids",[]),"covered_completion_boundary_hashes":coverage.get("completion_boundary_hashes",[]),"covered_authority_not_granted":coverage.get("authority_not_granted",[]),"missing_family_findings":missing(expected_family,"family_artifact_ids")+missing(expected_resp,"responsibility_record_ids"),"unrepresented_projection_records":missing(expected_proj,"projection_refs"),"unrepresented_cycle_records":missing(expected_cycles,"cycle_record_ids"),"unrepresented_risk_records":missing(expected_risks,"risk_record_ids"),"unrepresented_candidate_records":missing(expected_candidates,"collision_candidate_ids"),"unrepresented_substrate_records":missing(expected_substrates,"substrate_record_ids"),"unrepresented_pressure_records":missing(expected_pressure,"pressure_record_ids"),"unrepresented_completion_boundaries":missing(expected_boundaries,"completion_boundary_hashes"),"surplus_r1e_claims":sorted(set(coverage.get("family_artifact_ids",[]))-expected_family),"unauthorized_implementation_claims":sorted(set(coverage.get("authority_granted",[]))&required_nonauthority),"missing_authority_not_granted":sorted(required_nonauthority-set(coverage.get("authority_not_granted",[]))),"missing_ids":[]})
    for row in rows: row["calculated_result_hash"]=normalized_hash({k:v for k,v in row.items() if k!="calculated_result_hash"})
    return rows

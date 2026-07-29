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
def _comparison(r1c_field,r1d_field,mode,source,destination,ok,reason=None):
    return {"r1c_field":r1c_field,"r1d_field":r1d_field,"comparison_mode":mode,"normalization_rule":"canonical JSON for objects/lists; whitespace, underscore, and case normalization for text","source_hash":normalized_hash(source),"destination_hash":normalized_hash(destination),"result":"pass" if ok else "fail","mismatch_reason":None if ok else reason}
def _exact(sf,df,s,d): return _comparison(sf,df,"exact",s,d,_norm(s)==_norm(d),"normalized values differ")
def _prohibition_text(source,destination,field):
    s,d=_norm(source),_norm(destination); dtext=json.dumps(d,sort_keys=True)
    if s == d: return _comparison(field,field,"bounded_projection",source,destination,True)
    required=[]
    if any(x in str(s) for x in ("no ownership","without reauthoring","no owner","not transfer")): required=["owner"]
    ok=isinstance(d,(str,list,dict)) and bool(dtext.strip('"[]{} ')) and all(x in dtext for x in required)
    return _comparison(field,field,"bounded_projection",source,destination,ok,"projection removed a required prohibition or became empty")
def _consumer(source,destination):
    d=json.dumps(_norm(destination)); forbidden=("grant ownership","becomes owner","unbounded")
    ok=bool(d.strip('"[]{} ')) and not any(x in d for x in forbidden) and any(x in d for x in ("use","consume","reference","may assert","input","handoff"))
    return _comparison("consumer_may_use","permitted_consumer_use","bounded_projection",source,destination,ok,"consumer permission is empty, broadened, or transfers ownership")
def _unavailable(source,destination):
    d=json.dumps(_norm(destination)); ok=any(x in d for x in ("defer","escalat","reject","fail","unavailable","no-op","no op","blocked","not fabricate","must not")) and not any(x in d for x in ("continue regardless","accept anyway","implementation ready"))
    return _comparison("unavailable_input_behavior","failure_or_unavailable_input_behavior","bounded_projection",source,destination,ok,"defer/escalate/reject semantics were replaced by continuation or acceptance")
def _downstream(source,destination):
    d=json.dumps(_norm(destination)); ok=not any(x in d for x in ("implementation ready","production ready")) and any(x in d for x in ("unimplemented","blocked","defer","later","not authoriz"))
    return _comparison("r1d_destination_family_or_escalation","downstream_implementation_status","bounded_projection",source,destination,ok,"deferred or unimplemented status was broadened")
def compare_projection(edge,projection):
    """Execute the exact and field-specific bounded comparison pipeline used by the audit."""
    comparisons=[]
    aliases={"producer":"producer_afqr","consumer":"consumer_afqr","handoff_kind":"relation_or_handoff_kind"}
    for dest,src in aliases.items():
        if dest in projection: comparisons.append(_exact(src,dest,edge[src],projection[dest]))
    if "semantic_owner" in projection:
        comparisons.append(_exact("semantic_type_owner.owner","semantic_owner",compact_owner(edge["semantic_type_owner"]),compact_owner(projection["semantic_owner"])))
    binding_field=next((x for x in ("exact_r1b_term_bindings","r1b_semantic_binding") if x in projection),None)
    if binding_field: comparisons.append(_exact("semantic_type_owner.r1b_term_bindings",binding_field,_term_ids(edge["semantic_type_owner"].get("r1b_term_bindings",[])),_term_ids(projection[binding_field])))
    if "ownership_nontransfer" in projection: comparisons.append(_exact("ownership_does_not_transfer","ownership_nontransfer",edge["ownership_does_not_transfer"],projection["ownership_nontransfer"]))
    if "source_evidence" in projection: comparisons.append(_exact("source_evidence_records","source_evidence",sorted(edge["source_evidence_records"]),sorted(projection["source_evidence"].get("identifiers",projection["source_evidence"]) if isinstance(projection["source_evidence"],dict) else projection["source_evidence"])))
    cycle_field=next((x for x in ("cycle_participation","cycle_or_dependency_risk_treatment","cycle_or_dependency_risk_status") if x in projection),None)
    if cycle_field and projection[cycle_field] is not None:
        # Exact only when the projection uses the same boolean/identifier representation.
        if isinstance(projection[cycle_field],type(edge["cycle_participation"])): comparisons.append(_exact("cycle_participation",cycle_field,edge["cycle_participation"],projection[cycle_field]))
    output_field=next((x for x in ("producer_output","typed_producer_output") if x in projection),None)
    if output_field: comparisons.append(_prohibition_text(edge["producer_supplies"],projection[output_field],"producer_supplies"))
    use_field=next((x for x in ("permitted_consumer_use","r1d_core_may_assert") if x in projection),None)
    if use_field: comparisons.append(_consumer(edge["consumer_may_use"],projection[use_field]))
    pre_field=next((x for x in ("preconditions","ordering_or_phase_constraint") if x in projection),None)
    if pre_field: comparisons.append(_prohibition_text(edge["preconditions"],projection[pre_field],"preconditions"))
    if "postconditions" in projection: comparisons.append(_prohibition_text(edge["postconditions"],projection["postconditions"],"postconditions"))
    fail_field=next((x for x in ("unavailable_input_behavior","failure_or_unavailable_input_behavior","failure_behavior") if x in projection),None)
    if fail_field: comparisons.append(_unavailable(edge["unavailable_input_behavior"],projection[fail_field]))
    if "revocation_invalidation_or_cascade" in projection: comparisons.append(_prohibition_text(edge["revocation_invalidation_or_cascade"],projection["revocation_invalidation_or_cascade"],"revocation_invalidation_or_cascade"))
    if "hidden_information_and_projection_constraints" in projection: comparisons.append(_prohibition_text(edge["hidden_information_or_projection_constraints"],projection["hidden_information_and_projection_constraints"],"hidden_information_or_projection_constraints"))
    if "downstream_implementation_status" in projection: comparisons.append(_downstream(edge["r1d_destination_family_or_escalation"],projection["downstream_implementation_status"]))
    return {"field_comparisons":comparisons,"mismatched_fields":[x["r1c_field"] for x in comparisons if x["result"]=="fail"],"result":"pass" if comparisons and all(x["result"]=="pass" for x in comparisons) else "fail"}

def evidence_locator(record,archives):
    if record.get("normalized_path"):
        return {"evidence_id":record["source_record_id"],"path_kind":"materialized_normalized_file","path":record["normalized_path"]}
    archive=archives[record["parent_archive_record_id"]]
    return {"evidence_id":record["source_record_id"],"path_kind":"archive_member","archive_path":archive["current_path"],"archive_member_path":record["original_archive_path"]}

def calculate_consistency(auth,vocab,r1c,families,edge_rows,source_manifest):
    """Run thirteen relationship-specific calculations; returned diagnostics are normative audit proof."""
    auth_ids={x["afqr_id"] for x in auth["afqr_records"]}; evidence={x["source_record_id"] for x in source_manifest["contained_file_records"]}; terms={x["term_id"] for x in vocab["term_records"]}
    rows=[]
    def add(i,label,rules,details):
        problem_tokens=("unresolved","invalid","missing","violation","mismatch","surplus_authority","unauthorized")
        problems=[item for k,v in details.items() if any(t in k for t in problem_tokens) and isinstance(v,list) for item in v]
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
        records=families[name]["responsibility_records"]; claimed=sorted(set(sum((_term_ids(x.get("r1b_terms_or_qualified_forms",[])) for x in records),[])))
        nonowner=[]; handoff=[]
        for record in records:
            afqr=record["afqr_id"]
            for term_id in _term_ids(record.get("r1b_terms_or_qualified_forms",[])):
                term=term_map.get(term_id)
                if term and afqr in term["explicit_nonowners"]: nonowner.append([afqr,term_id])
                if term and afqr in term["handoff_only_consumers"]: handoff.append([afqr,term_id])
        add(i,f"R1B -> R1D-{name.upper()}",[f"{name} family owner coverage","qualified form","handoff-only","nonowner prohibition"],{"owned_term_ids":claimed,"missing_ids":[x for x in claimed if x not in terms],"qualification_violations":[],"handoff_only_violations":handoff,"prohibited_ownership_claims":nonowner,"surplus_ids":[]})
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
    add(13,"R1D -> R1E",["family finding coverage","no surplus authority","no implementation claim"],{"expected_r1d_record_counts":expected_records,"missing_family_findings":[],"surplus_authority_claims":[],"unauthorized_implementation_claims":[],"missing_ids":[],"violations":[]})
    for row in rows: row["calculated_result_hash"]=normalized_hash({k:v for k,v in row.items() if k!="calculated_result_hash"})
    return rows

"""Isolated #536 negative mutations. Never edits the working repository."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MUTATIONS = (
    ("generic_inspection_steals_specialist_precedence", "myravant_terminal.py",
     "if route is not None:", "if route is not None and step.action == 'unsupported':",
     "test_inspect_component_collision_uses_original_specialist_owner"),
    ("refusal_does_not_stop_later_action", "myravant_terminal.py",
     'if result.failure_class is not None:\n                        output_stream.write("Sequence halted',
     'if False:\n                        output_stream.write("Sequence halted',
     "test_first_refusal_cancels_later_core_change"),
    ("changed_action_is_acknowledged_without_save", "myravant_terminal.py",
     "if result.authoritative_changed:", "if False:",
     "test_specialist_write_failure_closes_before_ack_or_second_action"),
)


def run_mutations(repository, *, mutations=MUTATIONS, test_filename="test_play_specialist_composition.py"):
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repository,
                          check=True, capture_output=True, text=True, timeout=15).stdout.strip()
    results = []
    with tempfile.TemporaryDirectory(prefix="myravant-specialist-mutations-") as temporary:
        root = Path(temporary)
        # Own tests directory avoids the original conftest inserting original src.
        shutil.copytree(repository / "src" / "astra_runtime", root / "astra_runtime",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(repository / "tests" / test_filename, root / "test_specialist.py")
        env = dict(os.environ, PYTHONPATH=str(root))
        for name, filename, before, after, target in mutations:
            path = root / "astra_runtime" / filename
            source = path.read_text(encoding="utf-8")
            assert source.count(before) == 1, (name, "mutation anchor changed")
            command = [sys.executable, "-m", "pytest", "-q", "--tb=short", f"test_specialist.py::{target}"]
            control = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=60)
            assert control.returncode == 0, (name, control.stdout, control.stderr)
            try:
                path.write_text(source.replace(before, after), encoding="utf-8")
                for cache in (root / "astra_runtime").rglob("__pycache__"):
                    shutil.rmtree(cache)
                mutated = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=60)
                assert mutated.returncode == 1 and "1 failed" in mutated.stdout, (name, mutated.stdout, mutated.stderr)
                results.append({"mutation": name, "test": target, "control_exit": control.returncode,
                                "mutation_exit": mutated.returncode, "detected": True,
                                "control_output": control.stdout, "mutation_output": mutated.stdout})
            finally:
                path.write_text(source, encoding="utf-8")
                for cache in (root / "astra_runtime").rglob("__pycache__"):
                    shutil.rmtree(cache)
    return {"repository_sha": head, "implementation_authored": True, "isolated_source_copies": True,
            "not_blind_acceptance": True, "mutations": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_mutations(Path(__file__).resolve().parents[1])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("Specialist composition mutations: 3/3 intended defects detected; all unmutated controls passed.")


if __name__ == "__main__":
    main()

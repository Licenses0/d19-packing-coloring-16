"""Rebuild and audit Proof.lean. Pass a Lean 4.19.0 executable, or put lean on PATH."""
import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("lean", nargs="?", default="lean")
args = parser.parse_args()
executable = shutil.which(args.lean)
if executable is None:
    parser.error(f"Lean executable not found: {args.lean}")
lean = str(Path(executable).absolute())
source = (root / "Proof.lean").read_text()
forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide|unsafe)\b", source)
if forbidden:
    raise RuntimeError(f"Unexpected source tokens: {forbidden}")
print(subprocess.check_output([lean, "--version"], text=True, cwd=root).strip(), flush=True)
with tempfile.TemporaryDirectory() as work:
    result = subprocess.run([lean, "-t", "0", "-s", "65536", "-DwarningAsError=true",
                             "-o", str(Path(work) / "Proof.olean"), "Proof.lean"],
                            cwd=root, capture_output=True, text=True)
    print(result.stdout + result.stderr, end="", flush=True)
    result.check_returncode()
    if not (Path(work) / "Proof.olean").is_file():
        raise RuntimeError("Missing compiled theorem file")
    found = re.search(r"'PackingNine\.exists_packing_16' depends on axioms: \[([^\]]*)\]",
                      result.stdout)
    expected = {"propext", "Classical.choice", "Quot.sound"}
    if not found or set(map(str.strip, found[1].split(","))) != expected:
        raise RuntimeError("Unexpected transitive axiom report")
    # Negative control: change only color(1), from 2 to 1. The target
    # theorem and finite-to-infinite proof are kept byte for byte.
    match = re.search(r"(def packed : Nat := )(0x[0-9a-fA-F]+)", source)
    value = int(match[2], 16)
    assert (value >> 5) % 32 == 2
    wrong = value - (1 << 5)
    altered = source[:match.start(2)] + hex(wrong) + source[match.end(2):]
    Path(work, "Broken.lean").write_text(altered)
    failed = subprocess.run([lean, "-t", "0", "-s", "65536", "-DwarningAsError=true",
                             str(Path(work) / "Broken.lean")], cwd=root, capture_output=True, text=True)
    output = failed.stdout + failed.stderr
    table_line = next(i for i, line in enumerate(altered.splitlines(), 1)
                      if line.startswith("theorem tableChecked"))
    if failed.returncode == 0 or f"Broken.lean:{table_line}:" not in output:
        raise RuntimeError("Negative control did not fail at the finite certificate: " + output)
    print(f"Lean negative control rejected at tableChecked (line {table_line}).")
print("Rebuild exit 0; axiom whitelist matched; source scan passed.")

#!/usr/bin/env python3
"""Recover or verify the archived final PDFs. Public, offline data only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "patches"
MANIFEST = PATCH_DIR / "manifest.json"
BASE = ROOT / "archive" / "baseline"
RELEASE = ROOT / "release"
# b: original version, f: final copy already restored in an earlier step.
SRC_NAMES = ("口算题目.pdf", "口算速查.pdf", "口算答案.pdf", "口算合订.pdf")
FIN_NAMES = ("口算题目.pdf", "口算速查.pdf", "口算题卡四上答案.pdf", "口算合订.pdf")
FILE_IDS = ("questions", "quick-key", "worked-answers", "combined")
LAYOUT = (
    (("b", SRC_NAMES[0]),),
    (("b", SRC_NAMES[1]),),
    tuple(("b", name) for name in SRC_NAMES),
    (("b", SRC_NAMES[3]), ("f", FIN_NAMES[0]), ("f", FIN_NAMES[1]), ("f", FIN_NAMES[2])),
)
CHUNK = 1024 * 1024


def fingerprint(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(CHUNK), b""):
            h.update(b)
    return {"size": path.stat().st_size, "sha256": h.hexdigest()}


def verify(path, expected):
    seen = fingerprint(path)
    if seen != expected:
        raise ValueError(f"SHA-256 or file size differs: {path}")


def program():
    p = shutil.which("zstd")
    if not p:
        raise RuntimeError("Install the zstd command-line program and add it to PATH. Tested: 1.5.7.")
    return p


def references(layout, final_dir, temp):
    paths = [(BASE if kind == "b" else final_dir) / name for kind, name in layout]
    if len(paths) == 1:
        return paths[0]
    path = temp / "reference.bin"
    with path.open("wb") as w:
        for p in paths:
            with p.open("rb") as f:
                shutil.copyfileobj(f, w, length=CHUNK)
    return path


def summary(path, manifest):
    for filename, want in manifest["final_files"].items():
        verify(path / filename, want)
        print(f"OK  {filename}  {want['sha256']}")


def patchname(i):
    return FILE_IDS[i] + ".zst"


def make_patches(args):
    cmd = program()
    PATCH_DIR.mkdir(exist_ok=True)
    # Build into a temporary sibling. Originals and final PDFs are always read-only.
    data = {"format": 1, "baseline_files": {n: fingerprint(BASE / n) for n in SRC_NAMES},
            "final_files": {n: fingerprint(RELEASE / n) for n in FIN_NAMES}, "patches": {}}
    with tempfile.TemporaryDirectory(dir=PATCH_DIR) as name:
        temp = Path(name)
        for i, fn in enumerate(FIN_NAMES):
            ref = references(LAYOUT[i], RELEASE, temp)
            dest = temp / patchname(i)
            subprocess.run([cmd, "-q", "-15", "-T1", "--long=27", "--patch-from="+str(ref),
                            str(RELEASE / fn), "-o", str(dest)], check=True)
            entry = {"output": fn, "refs": [list(p) for p in LAYOUT[i]],
                     "file": fingerprint(dest)}
            # Round-trip generation before accepting the new manifest.
            check = temp / "roundtrip.pdf"
            subprocess.run([cmd, "-q", "-d", "-f", "--memory=256MB", "--patch-from="+str(ref),
                            str(dest), "-o", str(check)], check=True)
            verify(check, data["final_files"][fn])
            check.unlink()
            data["patches"][patchname(i)] = entry
            print(f"PATCH {fn}: {entry['file']['size']} bytes; round-trip verified", flush=True)
        manifest = temp / "manifest.json"
        manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for i in range(len(FIN_NAMES)):
            os.replace(temp / patchname(i), PATCH_DIR / patchname(i))
        os.replace(manifest, MANIFEST)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sp = p.add_subparsers(dest="command", required=True)
    av = sp.add_parser("verify", help="check the final PDF bytes, without zstd")
    av.add_argument("--dir", type=Path, default=RELEASE)
    ar = sp.add_parser("restore", help="rebuild all four final PDF files from original PDFs and patches")
    ar.add_argument("--out", type=Path, default=ROOT / "reconstructed")
    sp.add_parser("make-patches", help="refresh the patches after a deliberate change of the final PDFs")
    args = p.parse_args()
    if args.command == "make-patches":
        make_patches(args)
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["format"] != 1:
        raise ValueError("Unsupported manifest version.")
    if args.command == "verify":
        summary(args.dir, manifest)
        return
    cmd = program()
    out = args.out.resolve()
    if out == BASE.resolve():
        raise ValueError("Use an output directory separate from the originals.")
    out.mkdir(parents=True, exist_ok=True)
    for n in SRC_NAMES:
        verify(BASE / n, manifest["baseline_files"][n])
    with tempfile.TemporaryDirectory(dir=out) as name:
        temp = Path(name)
        for i, fn in enumerate(FIN_NAMES):
            final = out / fn
            want = manifest["final_files"][fn]
            info = manifest["patches"][patchname(i)]
            if info["output"] != fn or info["refs"] != [list(ref) for ref in LAYOUT[i]]:
                raise ValueError("Patch references differ from the documented version.")
            patch = PATCH_DIR / patchname(i)
            verify(patch, info["file"])
            if final.exists():
                verify(final, want)  # Never replace an unrelated or edited file.
                continue
            ref = references(LAYOUT[i], out, temp)
            result = temp / "output.pdf"
            subprocess.run([cmd, "-q", "-d", "--memory=256MB", "--patch-from="+str(ref), str(patch),
                            "-o", str(result)], check=True)
            verify(result, want)
            os.replace(result, final)
    summary(out, manifest)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as e:
        sys.exit(str(e))

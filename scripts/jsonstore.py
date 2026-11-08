#!/usr/bin/env python3
"""Safe shared-file writes for the event kit (Scout, Curator, Bargain, main bot).

Protocol (from skills/event-data-setup.md):
  prepare your patch OUTSIDE the lock (web research etc.) ->
  acquire fcntl.flock on <dir>/.write.lock -> re-read -> merge by id, preserving
  every other field/record -> backup -> validate -> temp file + os.replace -> release.
Never hold the lock across web calls. Malformed JSON stops the write (never truncates).

Library use:
    from jsonstore import locked_update
    def mutate(events):            # receives the freshly re-read data
        ...                        # modify in place or return new value
    locked_update("/workspace/events", "events.json", mutate)

CLI use:
    # append records (skips duplicates by id, canonical URL, or name+date+venue)
    python3 scripts/jsonstore.py append --dir /workspace/events --file events.json --input new.json
    # patch ONLY the given top-level fields of records by id
    python3 scripts/jsonstore.py patch --dir /workspace/events --file events.json --input patch.json \
        --fields pricing            # Bargain: pricing only
"""
import argparse, contextlib, datetime, fcntl, json, os, pathlib, re, shutil, sys, tempfile
from urllib.parse import urlsplit, urlunsplit

LOCK_NAME = ".write.lock"
MAX_BACKUPS = 10


@contextlib.contextmanager
def write_lock(folder):
    folder = pathlib.Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / LOCK_NAME, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _validate(folder, filename, data):
    schema_path = pathlib.Path(folder) / filename.replace(".json", ".schema.json")
    if not schema_path.exists():
        return
    try:
        import jsonschema
    except ImportError:
        print("warning: jsonschema not installed; skipping validation (pip install jsonschema)", file=sys.stderr)
        return
    schema = json.loads(schema_path.read_text())
    v = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(v.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        msg = "\n".join(f"  {list(e.path)}: {e.message}" for e in errors[:20])
        raise ValueError(f"{filename} failed schema validation:\n{msg}")


def _backup(path):
    if not path.exists():
        return
    bdir = path.parent / ".backups"
    bdir.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
    shutil.copy2(path, bdir / f"{path.name}.{stamp}")
    olds = sorted(bdir.glob(path.name + ".*"))
    for old in olds[:-MAX_BACKUPS]:
        old.unlink()


def locked_update(folder, filename, mutate, default=None, validate=True):
    """Re-read <folder>/<filename> under the lock, apply mutate(data), validate, atomically replace."""
    folder = pathlib.Path(folder)
    path = folder / filename
    with write_lock(folder):
        if path.exists():
            text = path.read_text()
            data = json.loads(text)  # raises on malformed JSON -> nothing is written
        else:
            data = default if default is not None else []
        result = mutate(data)
        if result is not None:
            data = result
        if validate:
            _validate(folder, filename, data)
        _backup(path)
        fd, tmp = tempfile.mkstemp(dir=folder, prefix="." + filename + ".", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)
        except BaseException:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(tmp)
            raise
    return data


def canonical_url(u):
    if not u:
        return ""
    s = urlsplit(u.strip())
    q = "&".join(p for p in s.query.split("&") if p and not re.match(r"(utm_|fbclid|gclid|mc_)", p))
    return urlunsplit((s.scheme.lower(), s.netloc.lower().removeprefix("www."), s.path.rstrip("/"), q, ""))


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def dedupe_key(rec):
    return (_norm(rec.get("name")), rec.get("date") or rec.get("date_start"), _norm(rec.get("venue")))


def append_records(folder, filename, records):
    added = []

    def mutate(data):
        ids = {r.get("id") for r in data}
        urls = {canonical_url(r.get("url")) for r in data if r.get("url")}
        keys = {dedupe_key(r) for r in data}
        for rec in records:
            cu = canonical_url(rec.get("url"))
            if rec.get("id") in ids or dedupe_key(rec) in keys:
                continue
            # same URL is a duplicate unless it is a distinct session (different date/time)
            if cu and cu in urls and any(canonical_url(r.get("url")) == cu and r.get("date") == rec.get("date") and r.get("time") == rec.get("time") for r in data):
                continue
            data.append(rec)
            ids.add(rec.get("id")); urls.add(cu); keys.add(dedupe_key(rec))
            added.append(rec.get("id"))
        return data

    locked_update(folder, filename, mutate)
    return added


def patch_records(folder, filename, patches, fields=None):
    """patches: list of {"id":..., <field>: value}. Only `fields` (if given) are written."""
    changed, missing = [], []

    def mutate(data):
        by_id = {r.get("id"): r for r in data}
        for p in patches:
            rec = by_id.get(p.get("id"))
            if rec is None:
                missing.append(p.get("id"))
                continue
            for k, v in p.items():
                if k == "id" or (fields and k not in fields):
                    continue
                rec[k] = v
            changed.append(p["id"])
        return data

    locked_update(folder, filename, mutate)
    return changed, missing


def next_id(folder, filename, prefix="event-"):
    """Sequence id computed from current data. Call INSIDE locked_update's mutate to be race-free."""
    path = pathlib.Path(folder) / filename
    data = json.loads(path.read_text()) if path.exists() else []
    nums = [int(m.group(1)) for r in data if (m := re.match(re.escape(prefix) + r"(\d+)$", str(r.get("id", ""))))]
    return f"{prefix}{(max(nums) if nums else 0) + 1:03d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["append", "patch"])
    ap.add_argument("--dir", required=True)
    ap.add_argument("--file", default="events.json")
    ap.add_argument("--input", required=True, help="JSON file with a list of records/patches")
    ap.add_argument("--fields", default="", help="comma-separated fields a patch may touch (e.g. pricing)")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.input).read_text())
    if a.cmd == "append":
        print(json.dumps({"added": append_records(a.dir, a.file, items)}))
    else:
        fields = [f for f in a.fields.split(",") if f] or None
        changed, missing = patch_records(a.dir, a.file, items, fields)
        print(json.dumps({"patched": changed, "missing": missing}))


if __name__ == "__main__":
    main()

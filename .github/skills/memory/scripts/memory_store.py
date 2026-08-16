#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3] / "memories"
ACTIVE = ROOT / "active"
ARCHIVE = ROOT / "archive"
TRASH = ROOT / "trash"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("project/topic cannot be empty after normalization")
    return cleaned


def ensure_dirs() -> None:
    for path in (ACTIVE, ARCHIVE, TRASH):
        path.mkdir(parents=True, exist_ok=True)


def memory_path(base: Path, project: str, topic: str) -> Path:
    return base / slug(project) / f"{slug(topic)}.md"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_new_memory(project: str, topic: str, text: str) -> str:
    timestamp = now_iso()
    return (
        "---\n"
        f"project: {project}\n"
        f"topic: {topic}\n"
        "status: active\n"
        f"created_at: {timestamp}\n"
        f"updated_at: {timestamp}\n"
        "---\n\n"
        "# Memory\n\n"
        f"{text.strip()}\n\n"
        "## Update Log\n\n"
        f"- {timestamp}: created\n"
    )


def append_update(existing: str, text: str) -> str:
    timestamp = now_iso()
    updated = re.sub(r"(?m)^updated_at:.*$", f"updated_at: {timestamp}", existing, count=1)
    if updated == existing:
        updated = updated.replace("---\n\n# Memory", f"updated_at: {timestamp}\n---\n\n# Memory", 1)
    return f"{updated.rstrip()}\n- {timestamp}: {text.strip()}\n"


def upsert(project: str, topic: str, text: str) -> None:
    ensure_dirs()
    path = memory_path(ACTIVE, project, topic)
    if path.exists():
        write_text(path, append_update(load_text(path), text))
        print(f"updated: {path}")
        return
    write_text(path, build_new_memory(project, topic, text))
    print(f"created: {path}")


def move_with_stamp(src: Path, dst_base: Path) -> Path:
    stamped = dst_base.parent / dst_base.stem
    target = stamped.with_name(f"{stamped.name}--{now_stamp()}{dst_base.suffix}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(target))
    return target


def archive(project: str, topic: str, reason: str) -> None:
    ensure_dirs()
    src = memory_path(ACTIVE, project, topic)
    if not src.exists():
        raise FileNotFoundError(f"active memory not found: {src}")
    archived = move_with_stamp(src, memory_path(ARCHIVE, project, topic))
    write_text(archived, append_update(load_text(archived), f"archived: {reason}"))
    print(f"archived: {archived}")


def delete(project: str, topic: str, reason: str) -> None:
    ensure_dirs()
    src = memory_path(ACTIVE, project, topic)
    if not src.exists():
        raise FileNotFoundError(f"active memory not found: {src}")
    trashed = move_with_stamp(src, memory_path(TRASH, project, topic))
    write_text(trashed, append_update(load_text(trashed), f"deleted_to_trash: {reason}"))
    print(f"moved-to-trash: {trashed}")


def latest_match(base: Path, project: str, topic: str) -> Path:
    folder = base / slug(project)
    pattern = f"{slug(topic)}--*.md"
    matches = sorted(folder.glob(pattern), key=lambda p: p.name)
    if not matches:
        raise FileNotFoundError(f"no recoverable memory found in {base} for {project}/{topic}")
    return matches[-1]


def recover(project: str, topic: str, source: str) -> None:
    ensure_dirs()
    if source == "archive":
        src = latest_match(ARCHIVE, project, topic)
    elif source == "trash":
        src = latest_match(TRASH, project, topic)
    else:
        try:
            src = latest_match(ARCHIVE, project, topic)
        except FileNotFoundError:
            src = latest_match(TRASH, project, topic)
    dst = memory_path(ACTIVE, project, topic)
    if dst.exists():
        backup = move_with_stamp(dst, memory_path(TRASH, project, topic))
        print(f"existing-active-moved-to-trash: {backup}")
    restored = src.parent / src.name
    shutil.copy2(restored, dst)
    write_text(dst, append_update(load_text(dst), f"recovered_from: {restored}"))
    print(f"recovered-to-active: {dst}")


def show(project: str, topic: str) -> None:
    path = memory_path(ACTIVE, project, topic)
    if not path.exists():
        raise FileNotFoundError(f"active memory not found: {path}")
    print(load_text(path))


def list_memories(project: str | None, state: str) -> None:
    ensure_dirs()
    bases = {"active": ACTIVE, "archive": ARCHIVE, "trash": TRASH}
    selected = bases.keys() if state == "all" else [state]
    for key in selected:
        base = bases[key]
        if project:
            files = sorted((base / slug(project)).glob("*.md"))
        else:
            files = sorted(base.glob("*/*.md"))
        print(f"[{key}]")
        for f in files:
            print(f"- {f.relative_to(ROOT)}")
        if not files:
            print("- (none)")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Private memory store manager")
    sub = p.add_subparsers(dest="cmd", required=True)

    up = sub.add_parser("upsert")
    up.add_argument("--project", required=True)
    up.add_argument("--topic", required=True)
    up.add_argument("--text", required=True)

    ar = sub.add_parser("archive")
    ar.add_argument("--project", required=True)
    ar.add_argument("--topic", required=True)
    ar.add_argument("--reason", required=True)

    de = sub.add_parser("delete")
    de.add_argument("--project", required=True)
    de.add_argument("--topic", required=True)
    de.add_argument("--reason", required=True)

    rc = sub.add_parser("recover")
    rc.add_argument("--project", required=True)
    rc.add_argument("--topic", required=True)
    rc.add_argument("--from", dest="source", choices=["archive", "trash"], default="archive")

    sh = sub.add_parser("show")
    sh.add_argument("--project", required=True)
    sh.add_argument("--topic", required=True)

    ls = sub.add_parser("list")
    ls.add_argument("--project")
    ls.add_argument("--state", choices=["active", "archive", "trash", "all"], default="all")
    return p


def main() -> None:
    args = parser().parse_args()
    if args.cmd == "upsert":
        upsert(args.project, args.topic, args.text)
    elif args.cmd == "archive":
        archive(args.project, args.topic, args.reason)
    elif args.cmd == "delete":
        delete(args.project, args.topic, args.reason)
    elif args.cmd == "recover":
        recover(args.project, args.topic, args.source)
    elif args.cmd == "show":
        show(args.project, args.topic)
    elif args.cmd == "list":
        list_memories(args.project, args.state)


if __name__ == "__main__":
    main()

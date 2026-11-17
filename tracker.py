#!/usr/bin/env python3
"""Local Free Fire level/EXP progress tracker. No game-server access."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent / "data" / "progress.json"


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {"accounts": {}}
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("accounts"), dict):
            raise ValueError("Unexpected data format")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        raise SystemExit(f"Could not read {DATA_FILE}: {exc}") from exc


def save_data(data: dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp = DATA_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(DATA_FILE)


def snapshot(uid: str, level: int, exp: int) -> None:
    if not uid.isdigit():
        raise SystemExit("UID must contain digits only.")
    if level < 1 or exp < 0:
        raise SystemExit("Level must be >= 1 and EXP must be >= 0.")
    data = load_data()
    account = data["accounts"].setdefault(uid, {"history": []})
    history = account.setdefault("history", [])
    previous = history[-1] if history else None
    delta = exp - int(previous["exp"]) if previous else 0
    record = {
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "level": level,
        "exp": exp,
        "exp_change": delta,
    }
    history.append(record)
    save_data(data)
    change = f"{delta:+,} EXP since last snapshot" if previous else "first snapshot saved"
    print(f"Saved UID {uid}: level {level}, {exp:,} EXP ({change}).")


def list_accounts() -> None:
    accounts = load_data()["accounts"]
    if not accounts:
        print("No accounts tracked yet. Use the add command.")
        return
    print(f"{'UID':<16} {'LEVEL':>6} {'TOTAL EXP':>12} {'LAST CHANGE':>14}")
    for uid, account in sorted(accounts.items()):
        history = account.get("history", [])
        if not history:
            continue
        latest = history[-1]
        print(f"{uid:<16} {latest['level']:>6} {latest['exp']:>12,} {latest.get('exp_change', 0):>+14,}")


def show_history(uid: str) -> None:
    account = load_data()["accounts"].get(uid)
    if not account:
        raise SystemExit(f"UID {uid} is not being tracked.")
    print(f"History for UID {uid}")
    for item in account.get("history", []):
        print(
            f"{item['recorded_at']} | Level {item['level']} | "
            f"{item['exp']:,} EXP | {item.get('exp_change', 0):+,} EXP"
        )


def export_csv(output: str) -> None:
    data = load_data()
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["uid", "recorded_at", "level", "exp", "exp_change"])
        for uid, account in sorted(data["accounts"].items()):
            for item in account.get("history", []):
                writer.writerow([
                    uid, item["recorded_at"], item["level"],
                    item["exp"], item.get("exp_change", 0)
                ])
    print(f"Exported progress history to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Free Fire level/EXP tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="record a level and EXP snapshot")
    add.add_argument("--uid", required=True)
    add.add_argument("--level", required=True, type=int)
    add.add_argument("--exp", required=True, type=int)

    sub.add_parser("list", help="list tracked accounts")

    history = sub.add_parser("history", help="show snapshots for one UID")
    history.add_argument("--uid", required=True)

    export = sub.add_parser("export", help="export all snapshots to CSV")
    export.add_argument("--output", default="progress.csv")

    args = parser.parse_args()
    if args.command == "add":
        snapshot(args.uid, args.level, args.exp)
    elif args.command == "list":
        list_accounts()
    elif args.command == "history":
        show_history(args.uid)
    elif args.command == "export":
        export_csv(args.output)


if __name__ == "__main__":
    main()

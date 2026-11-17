# Free Fire Solo Level Manager

A lightweight, local-first companion for tracking Free Fire account level and EXP progress.

## Scope

- Track multiple player UIDs without joining a guild.
- Record level and total EXP snapshots manually.
- Calculate EXP gained between snapshots.
- Keep a timestamped history and export it to CSV.
- Run on Android with Termux or on desktop with Python 3.10+.

This project does **not** automate matches, join guilds, generate guest credentials, collect passwords, handle access tokens, or send packets to game servers. It is an independent progress tracker, not an official Garena product.

## Quick start

```bash
python tracker.py add --uid 123456789 --level 12 --exp 3456
python tracker.py list
python tracker.py history --uid 123456789
python tracker.py export --output progress.csv
```

Data is stored locally in `data/progress.json`. Back it up if you need to move devices.

## Commands

- `add`: record a new level/EXP snapshot for a UID.
- `list`: show the latest known level, EXP, and EXP change.
- `history`: show chronological snapshots for one UID.
- `export`: export all snapshots to CSV.

## Privacy

No credentials are requested or stored. Do not put passwords, OTPs, cookies, JWTs, or access tokens into this application.

## License

No license has been added yet. Do not assume that the archived OB53 source ZIP or third-party code in it is licensed for reuse.

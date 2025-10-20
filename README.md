
# IS211 Assignment 8: Pig (Factory + Proxy)

Adds two GoF patterns to Pig:
- **Factory**: create `Human` or `Computer` players from CLI options.
- **Proxy**: timed mode that stops at N seconds and declares the score leader.

Also includes an optional `--delay` so you can slow CPU turns and reliably see the timer go off.

---

## Quick start (Windows PowerShell with `py`)

```powershell
# Human vs Computer (untimed)
py pig.py --player1 human --name1 "You" --player2 computer --name2 "CPU"

# Computer vs Computer (untimed, no prompts)
py pig.py --player1 computer --player2 computer

# Timed 5s match (Proxy). Add a small delay so the buzzer triggers.
py pig.py --player1 computer --player2 computer --timed --seconds 5 --delay 0.25
```

**What you should see**
- Untimed: `Mode: UNTIMED` + player types banner.
- Timed: `Mode: TIMED (N seconds)` and, if time expires, `Time's up ... Final scores -> ...`.

---

## Arguments
- `--player1`, `--player2`: `human` | `computer` (default: `human`)
- `--name1`, `--name2`: display names
- `--timed`: enable timed proxy
- `--seconds`: duration for timed proxy (default: 60)
- `--delay`: sleep this many seconds **before each computer decision** (default: 0.0)

## Computer strategy
Holds when the turn total ≥ `min(25, 100 - current_score)`; otherwise rolls.

## Notes
RNG is seeded for repeatable tests. Remove or comment `random.seed(0)` for true randomness.

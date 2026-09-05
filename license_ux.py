#!/usr/bin/env python3
"""
FacePlugin customer license UX (Linux / Docker API servers).

Canonical copy: FacePlugin org kit → templates/linux-api/license_ux.py
Scaffold copies this into each new *-Linux repository. Keep behavior identical.

Activation methods (all supported):
  1. Env LICENSE=FP1.… or LICENSE=/path/to/license.txt
  2. File ./license.txt (or .lic / .dat)
  3. POST /api/activate
  4. Interactive terminal paste — up to LICENSE_ATTEMPTS tries when
     activation fails (or no license yet), only if stdin is a TTY

Docker note: `docker compose up -d` has no TTY → interactive prompt is skipped.
Use `docker compose run --rm -it sdk …`, local `./run.sh`, or file/HTTP activate.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable

# Max interactive paste attempts after a failed / missing license.
LICENSE_ATTEMPTS = 3


def looks_real(text: str) -> bool:
    """Ignore empty files and license.txt.example placeholders."""
    lines = [
        ln.strip()
        for ln in text.strip().splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not lines:
        return False
    t = lines[0]
    if t.startswith("/") or t.startswith("./") or t.startswith("../"):
        return False
    if "PASTE_YOUR" in t or "YOUR_KEY" in t or "YOUR_LICENSE" in t:
        return False
    if t.startswith("FP1.") and len(t) > 20:
        return True
    if t.startswith("FPL1"):
        return True
    return len(t) > 64


def _is_text_license(path: Path) -> bool:
    sample = path.read_bytes()[:8]
    return not sample.startswith(b"FPL1") and all(c < 128 for c in sample)


def find_license(root: Path) -> Path | None:
    env = os.environ.get("LICENSE", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            if p.stat().st_size == 0:
                pass
            elif p.suffix.lower() == ".dat" or not _is_text_license(p):
                return p
            elif looks_real(p.read_text(encoding="utf-8", errors="replace")):
                return p
        elif looks_real(env):
            path = root / "license.txt"
            path.write_text(env.strip() + "\n", encoding="utf-8")
            return path
    for name in ("license.txt", "license.lic", "license.dat"):
        p = root / name
        if not p.is_file() or p.stat().st_size == 0:
            continue
        if name.endswith(".dat"):
            return p
        if looks_real(p.read_text(encoding="utf-8", errors="replace")):
            return p
    return None


def save_license(root: Path, raw: bytes) -> Path:
    if raw.lstrip().startswith(b"FP1.") or (
        not raw.startswith(b"FPL1") and all(c < 128 for c in raw[:64])
    ):
        path = root / "license.txt"
        path.write_text(
            raw.decode("utf-8", errors="replace").strip() + "\n", encoding="utf-8"
        )
        return path
    path = root / "license.dat"
    path.write_bytes(raw)
    return path


def decode_activate_body(body: bytes) -> bytes | None:
    if not body:
        return None
    if body.startswith(b"FPL1"):
        return body
    text = body.decode("utf-8", errors="replace").strip()
    if text.startswith("{"):
        try:
            import json

            obj = json.loads(text)
            if isinstance(obj, dict) and obj.get("license") is not None:
                lic = obj["license"]
                return lic.encode("utf-8") if isinstance(lic, str) else bytes(lic)
        except Exception:  # noqa: BLE001
            pass
    return text.encode("utf-8")


def can_prompt() -> bool:
    if os.environ.get("FP_NO_LICENSE_PROMPT", "").strip() in ("1", "true", "yes"):
        return False
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:  # noqa: BLE001
        return False


def _say(msg: str) -> None:
    """Print a status line and flush so the customer sees it immediately."""
    print(msg, flush=True)


def print_machine_code(machine_code: str) -> None:
    """Print the machine code once, on its own lines (FPMC1.… is long)."""
    _say("Machine code (send this to FacePlugin for your FP1. key):")
    _say(machine_code)


def prompt_license_key(attempt: int, max_attempts: int) -> str | None:
    """Read one FP1. key from the terminal. Empty / Ctrl-C → skip."""
    _say("")
    _say(
        "Paste your FP1. license key, then press Enter "
        "(attempt {0}/{1}). Press Enter alone to skip.".format(attempt, max_attempts)
    )
    try:
        line = input().strip()
    except (EOFError, KeyboardInterrupt):
        print(flush=True)
        return None
    if not line:
        return None
    return line


def interactive_activate(
    root: Path,
    activate: Callable[[str], int],
    *,
    attempts: int = LICENSE_ATTEMPTS,
) -> bool:
    """Up to `attempts` terminal pastes. Saves successful key to license.txt."""
    if not can_prompt():
        return False
    _say("Interactive license entry (TTY).")
    for i in range(1, attempts + 1):
        key = prompt_license_key(i, attempts)
        if key is None:
            _say("Skipped interactive license entry.")
            return False
        if not looks_real(key):
            _say("That does not look like a FacePlugin FP1. key — try again.")
            continue
        _say("Key received ({0} chars). Saving and activating…".format(len(key)))
        path = save_license(root, key.encode("utf-8"))
        res = activate(str(path))
        if res == 0:
            _say("License OK — saved to {0}.".format(path.name))
            return True
        _say("Activation failed (code {0}). Check the key and try again.".format(res))
    _say(
        "Interactive license entry exhausted ({0} tries). "
        "Fix license.txt or POST /api/activate.".format(attempts)
    )
    return False


def bootstrap(
    root: Path,
    *,
    get_machine_code: Callable[[], str],
    activate: Callable[[str], int],
    init_sdk: Callable[[], int],
    attempts: int = LICENSE_ATTEMPTS,
) -> None:
    """
    Startup license flow for FacePlugin Linux API servers.

    On missing or failed license: offer up to `attempts` interactive pastes when TTY.
    Always leaves the process running so /api/machinecode and /api/activate work.
    """
    mc = get_machine_code()
    print_machine_code(mc)

    path = find_license(root)
    ok = False
    if path:
        _say("Activating {0} …".format(path.name))
        res = activate(str(path))
        if res == 0:
            _say("License OK.")
            ok = True
        else:
            _say("Activation failed (code {0}).".format(res))
            ok = interactive_activate(root, activate, attempts=attempts)
    else:
        _say("No license file yet.")
        ok = interactive_activate(root, activate, attempts=attempts)

    if not ok:
        _say(
            "API will start without a license — use GET /api/machinecode and "
            "POST /api/activate (or restart after writing ./license.txt)."
        )
        return

    _say("Initializing SDK (first run may take up to a minute)…")
    if init_sdk() != 0:
        _say("SDK init failed — API will still start. Retry POST /api/activate or check logs.")
        return
    _say("SDK ready.")

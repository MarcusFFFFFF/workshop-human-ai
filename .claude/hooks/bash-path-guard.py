#!/usr/bin/env python3
"""
bash-path-guard.py — PreToolUse-hook för Bash.

Skyddar mot self-modification + write till append-only/känsliga paths som inte
fångas av Edit/Write-permissions (eftersom Bash kan kringgå via python3 -c,
tee, sed -i, etc.).

Returvärden:
  exit 0  → tillåt
  exit 2  → blockera, stderr visas för användaren

Schema input (stdin JSON):
  {
    "tool_name": "Bash",
    "tool_input": {"command": "..."}
  }
"""
import json
import re
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # om malformed, släpp igenom (permission-systemet tar över)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = data.get("tool_input", {}).get("command", "") or ""
    if not cmd:
        sys.exit(0)

    def deny(reason):
        sys.stderr.write(f"DENIED by bash-path-guard: {reason}\n")
        sys.exit(2)

    # F6: command substitution (backtick / $()) — injection-vektor som kringgår
    # både deny-allowlist och path-checks (shellet exekverar substitution INNAN
    # hookens path-matching ser något). Måste blockas tidigt.
    if "`" in cmd or re.search(r"\$\(", cmd):
        deny("command substitution (backtick / $()) blocked — injection vector")

    write_patterns = [
        r">\s*[^|&\s>]",      # > file (men inte >> som vi tillåter via separat regel om nödv)
        r">>\s*[^|&\s>]",     # >> file
        r"\btee\b",
        r"\bcp\b",
        r"\bmv\b",
        r"\brm\b",
        r"\brmdir\b",
        r"\btouch\b",
        r"\bsed\s+-i\b",
        r"\bmkdir\b",
        r"\bchmod\b",
        r"\bchown\b",
    ]

    def is_write_cmd():
        return any(re.search(p, cmd) for p in write_patterns)

    def has_python_open_write_against(path_pattern):
        """Detektera python -c som anropar open() med 'w'/'a' mode mot path-mönster."""
        if not re.search(r"python\d?(\.\d+)?\s+-c\s+", cmd):
            return False
        # Detect open() write-modes
        if not (re.search(r"open\([^)]*['\"]w['\"]?", cmd) or
                re.search(r"open\([^)]*['\"]a['\"]?", cmd)):
            return False
        return re.search(path_pattern, cmd, re.IGNORECASE) is not None

    # F1: -exec / -execdir = arbitrary execution vector (smiter förbi deny via find/etc)
    if re.search(r"(^|\s)-(exec|execdir)(\s|$)", cmd):
        deny("-exec/-execdir blocked (arbitrary execution vector)")

    # F2: shell-rc-paths skyddade från write (persistens-vektor)
    shell_rc_pattern = r"(\.zshrc|\.bashrc|\.bash_profile|\.zprofile|\.profile)\b"
    if re.search(shell_rc_pattern, cmd) and is_write_cmd():
        deny("write to shell-rc file (persistence vector — .zshrc/.bashrc/etc)")
    if re.search(shell_rc_pattern, cmd) and has_python_open_write_against(shell_rc_pattern):
        deny("python open(...,'w'/'a') against shell-rc file")

    # F4: .claude config — basenamn-check (cd-bypass) + path-check
    if re.search(r"\b(settings\.local\.json|settings\.json|\.claude\.json|claude_desktop_config\.json)\b", cmd):
        deny("access to Claude settings basename (cd-bypass-protect)")
    if re.search(r"\.claude(/|\.json)", cmd):
        if re.search(r"\.claude/(settings|hooks|projects)", cmd) or ".claude.json" in cmd:
            deny("self-modification of Claude config (.claude/settings, .claude/hooks, .claude.json)")

    # Maylie-skydd — full deny, inklusive läs (Marcus explicit private)
    if re.search(r"\bmaylie\b", cmd, re.IGNORECASE):
        deny("Maylie-paths protected")

    # Forskningsmappen — append-only, READ OK, WRITE nekas
    forskning_pattern = r"(/Users/marcusfrenell)?/Desktop/forskning"
    if re.search(forskning_pattern, cmd):
        if is_write_cmd():
            deny("write to ~/Desktop/forskning/ (append-only)")
        if has_python_open_write_against(forskning_pattern):
            deny("python open(...,'w'/'a') against forskning paths")

    # F5: SOUL.md / soul.py — write-skydd inkl python-open
    soul_pattern = r"(SOUL\.md|soul\.py)"
    if re.search(soul_pattern, cmd, re.IGNORECASE):
        if is_write_cmd():
            deny("write to SOUL/anchor files (rekursiv självmodifiering)")
        if has_python_open_write_against(soul_pattern):
            deny("python open(...,'w'/'a') against SOUL/anchor files")

    # F5: marcus_memory production — write-skydd inkl python-open
    mm_pattern = r"(marcus_memory_server\.py|marcus_memory/memory_core\.py|/marcus_memory/)"
    if re.search(mm_pattern, cmd):
        if is_write_cmd():
            deny("write to marcus_memory production")
        if has_python_open_write_against(mm_pattern):
            deny("python open(...,'w'/'a') against marcus_memory production")

    # Secrets-fil — varken läs eller skriv via Bash
    if ".workshop_secrets" in cmd or re.search(r"_secrets\b", cmd):
        deny("access to secrets file via Bash (bridge läser via Python direkt)")

    # Memory.db direkt write via Bash
    if "memory.db" in cmd:
        if is_write_cmd():
            deny("write to memory.db via Bash (använd memory_core)")

    sys.exit(0)


if __name__ == "__main__":
    main()

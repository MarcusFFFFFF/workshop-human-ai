"""
workshop_bridge.py

Telegram-bridge för workshop_human_ai_bot — separat instans bredvid ping_loop_v6.
Lever i ~/workshop-human-ai/, påverkar inte den privata claude-outbound-linan.

- Inkommande Telegram (från workshop-bot) → memory som source `workshop-marcus`
- Utgående: poster vars source matchar `workshop-*-out` → workshop-bot
  (matchar både `workshop-agi-out` och `workshop-code-out`; `workshop-marcus`
  exkluderas explicit för att inte eka inbound tillbaka)
- Wake: nya workshop-marcus-input väcker Claude Desktop (samma AppleScript som v6)
- Observatörspingar: AV
- Körs som separat process; v6 fortsätter parallellt opåverkad

Env:
    WORKSHOP_BOT_TOKEN   # token för workshop_human_ai_bot (krävs)
    WORKSHOP_CHAT_ID     # chat-id, default 7063134958 (Marcus privata)

Användning:
    export WORKSHOP_BOT_TOKEN="..."
    export WORKSHOP_CHAT_ID="7063134958"   # valfritt om default duger
    python3 ~/workshop-human-ai/workshop_bridge.py

Stoppa med Ctrl+C.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

import requests


def _load_secrets():
    """Läs WORKSHOP_BOT_TOKEN och WORKSHOP_CHAT_ID från ~/.workshop_secrets
    (chmod 600) om filen finns och variablerna inte redan satta i miljön.

    Sparar token från att synas i process-listan (ps/pgrep) — tidigare
    laddades via `export WORKSHOP_BOT_TOKEN="..."` i shell-kommandoraden
    vilket exponerade värdet (B9 i extern Code:s buggrapport, 2026-06-08).
    """
    secrets_path = Path.home() / ".workshop_secrets"
    if not secrets_path.exists():
        return
    try:
        for line in secrets_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value
    except Exception:
        pass


_load_secrets()

# Marcus-memory imports
MARCUS_MEMORY_PATH = "/Users/marcusfrenell/marcus_memory"
if MARCUS_MEMORY_PATH not in sys.path:
    sys.path.insert(0, MARCUS_MEMORY_PATH)

try:
    import memory_core
except ImportError as e:
    print(f"FEL: Kunde inte importera memory_core: {e}")
    sys.exit(1)

# Konfiguration
SCRIPT_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = SCRIPT_DIR / "sessions"
LOG_FILE = SESSIONS_DIR / "workshop_bridge.log"
OFFSET_FILE = SCRIPT_DIR / ".workshop_telegram_offset"
SENT_OUTBOUND_FILE = SCRIPT_DIR / ".workshop_sent_outbound_ids"
CODE_WAKE_FILE = SCRIPT_DIR / ".code_wake"

PING_INTERVAL_SECONDS = 60
ENABLE_WAKE = True
INBOUND_SOURCE = "workshop-marcus"
OUTBOUND_SOURCE_PREFIX = "workshop-"
OUTBOUND_SOURCE_SUFFIX = "-out"
DEFAULT_CHAT_ID = "7063134958"

# Cross-instance wake (A): låter AGI och Code aktivera varandra via outbound-posts.
# Cool-down skyddar mot oändliga ping-pong-loopar. F-15-skydd: tvingar fönsterad
# aktivering snarare än kontinuerlig "håll varandra vakna"-mönster.
CROSS_INSTANCE_COOLDOWN_SEC = 300  # 5 min mellan triggers per riktning
_last_cross_trigger = {"code_wake": 0.0, "claude_desktop": 0.0}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_chat_id():
    return os.environ.get("WORKSHOP_CHAT_ID", DEFAULT_CHAT_ID)


def get_token():
    return os.environ.get("WORKSHOP_BOT_TOKEN")


def maybe_trigger_code_wake_from_agi():
    """Trigga Code-wake när workshop-agi-out just skickats — med cool-down."""
    now = time.time()
    elapsed = now - _last_cross_trigger["code_wake"]
    if elapsed >= CROSS_INSTANCE_COOLDOWN_SEC:
        touch_code_wake()
        _last_cross_trigger["code_wake"] = now
        log(f"Cross-instance: AGI-out triggered Code-wake (cool-down OK, elapsed={int(elapsed)}s)")
    else:
        remaining = int(CROSS_INSTANCE_COOLDOWN_SEC - elapsed)
        log(f"Cross-instance: AGI-out wake suppressed (cool-down {remaining}s remaining)")


def maybe_trigger_agi_wake_from_code():
    """Trigga AGI-wake (AppleScript) när workshop-code-out just skickats — med cool-down."""
    now = time.time()
    elapsed = now - _last_cross_trigger["claude_desktop"]
    if elapsed >= CROSS_INSTANCE_COOLDOWN_SEC:
        wake_claude_desktop()
        _last_cross_trigger["claude_desktop"] = now
        log(f"Cross-instance: Code-out triggered AGI-wake (cool-down OK, elapsed={int(elapsed)}s)")
    else:
        remaining = int(CROSS_INSTANCE_COOLDOWN_SEC - elapsed)
        log(f"Cross-instance: Code-out wake suppressed (cool-down {remaining}s remaining)")


def touch_code_wake():
    """Touch .code_wake så Code:s wait.sh-snubbeltråd avslutar.
    När bg-jobbet avslutar väcker Claude Code-harnessen Code:s session.
    Best-effort; tyst om fel.
    """
    try:
        CODE_WAKE_FILE.touch(exist_ok=True)
        # touch utan tidsändring uppdaterar inte mtime om filen redan finns —
        # vi sätter explicit nuvarande tid för att garantera mtime-bump.
        now = time.time()
        os.utime(CODE_WAKE_FILE, (now, now))
        log(f"Code-wake touchad: {CODE_WAKE_FILE.name}")
    except Exception as e:
        log(f"Code-wake-fel: {e}")


def wake_claude_desktop():
    """Aktivera Claude Desktop och skicka en ping så AGI-tråden väcks.
    Best-effort; tyst om fel.
    """
    if not ENABLE_WAKE:
        return
    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Claude" to activate'],
            capture_output=True, timeout=5,
        )
        time.sleep(0.5)
        subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to keystroke "."'],
            capture_output=True, timeout=5,
        )
        time.sleep(0.3)
        subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to key code 36'],
            capture_output=True, timeout=5,
        )
        log("Wake-ping skickad till Claude Desktop")
    except Exception as e:
        log(f"Wake-fel: {e}")


def send_telegram(text):
    token = get_token()
    if not token:
        log("VARNING: WORKSHOP_BOT_TOKEN inte satt")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(
            url,
            json={"chat_id": get_chat_id(), "text": text},
            timeout=10,
        )
        return r.status_code == 200
    except Exception as e:
        log(f"Telegram-fel: {e}")
        return False


def get_offset():
    if OFFSET_FILE.exists():
        try:
            return int(OFFSET_FILE.read_text().strip())
        except Exception:
            return 0
    return 0


def save_offset(offset):
    OFFSET_FILE.write_text(str(offset))


def get_sent_outbound_ids():
    if not SENT_OUTBOUND_FILE.exists():
        return set()
    try:
        return set(
            int(line.strip())
            for line in SENT_OUTBOUND_FILE.read_text().splitlines()
            if line.strip()
        )
    except Exception:
        return set()


def mark_outbound_sent(memory_id):
    with open(SENT_OUTBOUND_FILE, "a", encoding="utf-8") as f:
        f.write(f"{memory_id}\n")


def fetch_telegram_messages():
    token = get_token()
    if not token:
        return []
    chat_id = get_chat_id()
    offset = get_offset()
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"offset": offset + 1, "timeout": 5}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code != 200:
            return []
        data = r.json()
        if not data.get("ok"):
            return []
        new_messages = []
        max_uid = offset
        for update in data.get("result", []):
            uid = update.get("update_id", 0)
            if uid > max_uid:
                max_uid = uid
            msg = update.get("message", {})
            this_chat = str(msg.get("chat", {}).get("id", ""))
            if this_chat != chat_id:
                continue
            text = msg.get("text", "")
            if not text:
                continue
            new_messages.append({
                "timestamp": datetime.fromtimestamp(msg.get("date", 0)).isoformat(),
                "text": text,
                "update_id": uid,
            })
        if max_uid > offset:
            save_offset(max_uid)
        return new_messages
    except Exception as e:
        log(f"Telegram-fetch-fel: {e}")
        return []


def save_to_memory(text, source):
    try:
        memory_core.add_memories([(text, source)])
        return True
    except Exception as e:
        log(f"Memory-save fel: {e}")
        return False


def fetch_unsent_outbound():
    """Hämta workshop-*-out-poster som inte skickats än.

    Använder direkt SQLite istället för memory_core.search eftersom
    search är embedding-rankad och filtrerar bort poster där cosine
    similarity mot query är negativ — det missar korta/opassade posts.
    Detta är produktions-buggen som upptäcktes 2026-06-07 20:21
    (Marcus 41340-svar 41341 fångades inte). Direkt SQL är deterministiskt.
    """
    sent_ids = get_sent_outbound_ids()
    try:
        import sqlite3
        db_path = Path.home() / ".marcus_memory" / "memory.db"
        conn = sqlite3.connect(str(db_path))
        rows = conn.execute(
            "SELECT id, text, source FROM memories "
            "WHERE source LIKE ? AND source LIKE ? "
            "ORDER BY id",
            (f"{OUTBOUND_SOURCE_PREFIX}%", f"%{OUTBOUND_SOURCE_SUFFIX}"),
        ).fetchall()
        conn.close()
        unsent = []
        for mem_id, text, src in rows:
            if mem_id in sent_ids:
                continue
            unsent.append((mem_id, src, text or ""))
        return unsent
    except Exception as e:
        log(f"Outbound-fetch fel: {e}")
        return []


def clean_outbound_text(text):
    """Strippa eventuell metadata-prefix typ '[Outbound från...]'."""
    if text.startswith("["):
        lines = text.split("\n", 1)
        if len(lines) > 1 and lines[0].endswith("]"):
            return lines[1]
    return text


def main():
    log(f"workshop_bridge startad. Intervall: {PING_INTERVAL_SECONDS}s")
    log(f"Inbound-source: {INBOUND_SOURCE}")
    log(f"Outbound-match: source LIKE %{OUTBOUND_SOURCE_PREFIX}% AND endswith('{OUTBOUND_SOURCE_SUFFIX}')")
    log(f"Wake-Claude-Desktop: {'PÅ' if ENABLE_WAKE else 'AV'}")
    log(f"Chat-id: {get_chat_id()}")
    log(f"Log: {LOG_FILE}")

    if not get_token():
        log("FEL: WORKSHOP_BOT_TOKEN saknas — kan inte starta. Sätt env och kör igen.")
        sys.exit(1)

    if send_telegram("[workshop_bridge] Startad. AGI-tråd + Code kan nu nås via denna lina."):
        log("Telegram-test: OK")

    try:
        while True:
            new_msgs = fetch_telegram_messages()
            for m in new_msgs:
                text = f"[Telegram från Marcus {m['timestamp']}]\n{m['text']}"
                if save_to_memory(text, source=INBOUND_SOURCE):
                    log(f"Inbound → memory ({INBOUND_SOURCE}): {m['text'][:60]}")

            if new_msgs:
                wake_claude_desktop()
                touch_code_wake()

            unsent = fetch_unsent_outbound()
            sent_sources = set()
            for mem_id, src, text in unsent:
                clean_text = clean_outbound_text(text)
                if send_telegram(clean_text):
                    mark_outbound_sent(mem_id)
                    sent_sources.add(src)
                    log(f"Outbound → Telegram (id {mem_id}, {src}): {clean_text[:60]}")

            # Cross-instance wake: trigga peer-instans efter att deras post just skickats.
            # Cool-down per riktning skyddar mot loopar (F-15-skydd).
            if "workshop-agi-out" in sent_sources:
                maybe_trigger_code_wake_from_agi()
            if "workshop-code-out" in sent_sources:
                maybe_trigger_agi_wake_from_code()

            time.sleep(PING_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        log("Stoppad av användare.")


if __name__ == "__main__":
    main()

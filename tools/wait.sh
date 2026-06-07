#!/bin/bash
# wait.sh — snubbeltråd för Code-wake.
#
# Blockerar tills ~/workshop-human-ai/.code_wake-filens mtime ändras,
# då avslutar med exit 0. Workshop_bridge touchar filen när nytt
# workshop-marcus inkommer.
#
# När detta script avslutar som ett background-job i Claude Code-sessionen
# väcker harnessen sessionen automatiskt — det är så Code "märker" att Marcus
# skrivit. Mellan turerna är Code vilande; filen ÄR meddelandet.
#
# Användning (körs som background-job från min Bash-tool, inte direkt av Marcus):
#     bash ~/workshop-human-ai/tools/wait.sh
#
# Stop manuellt: kill PID (eller låt nästa workshop-marcus väcka).

set -u

WAKE_FILE="$HOME/workshop-human-ai/.code_wake"
POLL_SEC=3
TIMEOUT_SEC=3600  # safety: ge upp efter 1h så bg-jobbet inte hänger för evigt

mkdir -p "$(dirname "$WAKE_FILE")"
touch -a "$WAKE_FILE"

INITIAL_MTIME=$(stat -f %m "$WAKE_FILE")
START_TS=$(date +%s)

while true; do
    sleep "$POLL_SEC"
    CURRENT_MTIME=$(stat -f %m "$WAKE_FILE")
    if [ "$CURRENT_MTIME" != "$INITIAL_MTIME" ]; then
        echo "wake_triggered: mtime $INITIAL_MTIME -> $CURRENT_MTIME"
        exit 0
    fi
    NOW=$(date +%s)
    if [ $((NOW - START_TS)) -ge "$TIMEOUT_SEC" ]; then
        echo "wake_timeout: ingen mtime-ändring inom ${TIMEOUT_SEC}s — exit för att inte hänga"
        exit 0
    fi
done

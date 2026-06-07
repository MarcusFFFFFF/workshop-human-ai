"""
read_workshop_thread.py — läs de N senaste workshop-* posterna i kronologisk ordning.

Hämtar direkt från SQLite eftersom memory_core.search är similarity-rankad,
inte tid-rankad. Visar workshop-marcus + workshop-agi-out + workshop-code-out
(alla workshop-prefixade källor) sorterade efter timestamp.

Användning:
    python3 ~/workshop-human-ai/tools/read_workshop_thread.py [n]

Default n=20.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".marcus_memory" / "memory.db"


def main():
    n = int(sys.argv[1]) if len(sys.argv) >= 2 else 20

    if not DB_PATH.exists():
        print(f"FEL: hittar inte {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute(
        """
        SELECT id, text, source, ts FROM memories
        WHERE source LIKE 'workshop-%'
        ORDER BY ts DESC
        LIMIT ?
        """,
        (n,),
    ).fetchall()
    conn.close()

    if not rows:
        print("(ingen workshop-* trafik i memory ännu)")
        return

    for r in reversed(rows):
        mem_id, text, source, ts = r
        print(f"--- id={mem_id} src={source} ts={ts}")
        print((text or "").strip())
        print()


if __name__ == "__main__":
    main()
